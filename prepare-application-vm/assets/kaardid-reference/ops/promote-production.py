#!/usr/bin/env python3
"""Promote a verified rehearsal artifact; preparation never activates anything."""
from contextlib import contextmanager
from datetime import datetime, timezone
import argparse
import fcntl
import grp
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import pwd
import re
import secrets
import shutil
import signal
import stat
import subprocess
import tempfile
import time

spec = importlib.util.spec_from_file_location('deployment', Path(__file__).with_name('deploy-rehearsal.py'))
deployment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deployment)

SHARED = {'assets':'assets', 'upload':'upload', 'protected/runtime':'runtime',
          'protected/config/private':'config'}
READINESS = ('offVmBackupRestoreVerified', 'proxyDnsVauVerified', 'dgsUpdaterCopyVerified',
             'freshSnapshotCheckpointVerified', 'legacyUpdaterStopped')
RESTRICTED_READINESS = ('edgeAccessRestricted', 'dgsUpdaterCopyVerified',
                        'freshSnapshotCheckpointVerified', 'legacyUpdaterStopped')


class ReadinessError(ValueError):
    """A production activation prerequisite needs operator confirmation."""


def owned(path, directory=False):
    info = path.lstat()
    kind = stat.S_ISDIR if directory else stat.S_ISREG
    if not kind(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o022:
        raise ValueError('Unsafe deployment path: '+str(path))


def digest(path):
    owned(path)
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def save_private(path, text):
    if path.exists() or path.is_symlink():
        owned(path)
    descriptor, temporary=tempfile.mkstemp(prefix='.promotion-',dir=path.parent)
    try:
        with os.fdopen(descriptor,'w') as output:
            output.write(text)
        os.replace(temporary,path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def current_release(root, pointer):
    link = root/pointer
    if not link.is_symlink():
        if link.exists():
            raise ValueError('Release pointer is occupied by a regular file/directory.')
        return None
    release = Path(os.readlink(link))
    if (release.parent != root/'releases' or not re.fullmatch('[a-f0-9]{40}', release.name)):
        raise ValueError('Unexpected release pointer.')
    owned(release, directory=True)
    return release


def archive_entries(bundle, sha):
    entries = bundle.getmembers()
    names = set()
    for entry in entries:
        path = PurePosixPath(entry.name)
        # The builder produces only ordinary files/directories. Never extract
        # archive links, special files, duplicate names or ambiguous paths.
        if (path.is_absolute() or '..' in path.parts or str(path) != entry.name
                or path.parts[0] != sha or entry.name in names
                or not (entry.isdir() or entry.isfile())):
            raise ValueError('Unsafe or duplicate release archive entry.')
        names.add(entry.name)
    if not entries:
        raise ValueError('Empty release archive.')
    return entries


def verify_contents(archive, release, shared_root):
    """Compare every shipped byte, and reject extra code or unexpected symlinks."""
    owned(release, directory=True)
    with deployment.tarfile.open(archive) as bundle:
        entries = archive_entries(bundle, release.name)
        expected = set()
        for entry in entries:
            relative = PurePosixPath(entry.name).relative_to(release.name)
            if str(relative)=='.':
                continue
            expected.add(str(relative))
            path = release/str(relative)
            shared = str(relative).removeprefix('apps/kaardid/')
            if str(relative).startswith('apps/kaardid/') and shared in SHARED:
                if (not entry.isdir() or not path.is_symlink()
                        or os.readlink(path) != str(shared_root/SHARED[shared])):
                    raise ValueError('Unexpected shared-data link: '+str(relative))
                continue
            owned(path, directory=entry.isdir())
            if entry.isfile():
                with bundle.extractfile(entry) as source:
                    if hashlib.file_digest(source,'sha256').hexdigest() != digest(path):
                        raise ValueError('Release bytes differ from tested artifact: '+str(relative))
        # Path.rglob does not recurse through directory symlinks. Shared targets
        # (secrets, uploads and runtime) are deliberately never read or copied.
        actual = {str(p.relative_to(release)) for p in release.rglob('*')}
        if actual != expected:
            raise ValueError('Release contains missing or additional files.')


def tested_artifact(rehearsal, stages, sha):
    release = current_release(rehearsal, 'rehearsal')
    if release is None or release.name != sha:
        raise ValueError('Requested SHA is not the active tested rehearsal release.')
    marker=rehearsal/'shared/config/.maintenance'
    if marker.exists() or marker.is_symlink():
        raise ValueError('Rehearsal is in maintenance; promotion is not ready.')
    source = stages/('release-'+sha)
    owned(source, directory=True)
    owned(source/'release-manifest.json')
    manifest = json.loads((source/'release-manifest.json').read_text())
    if manifest.get('commit') != sha or manifest.get('purpose') != 'private-rehearsal':
        raise ValueError('Unexpected rehearsal artifact identity.')
    report = source/'deployment-report.txt'
    owned(report)
    lines = report.read_text().splitlines()
    if ('KAARDID_REHEARSAL_SWITCH_COMPLETE' not in lines or 'Active release: '+sha not in lines):
        raise ValueError('Successful rehearsal deployment evidence is missing.')
    archive = source/(sha+'.tar.gz')
    if digest(archive) != manifest.get('artifact_sha256'):
        raise ValueError('Rehearsal archive checksum mismatch.')
    verify_contents(archive, release, rehearsal/'shared')
    deployment.health_check()  # Fresh checks, never cached evidence alone.
    return archive, manifest, digest(report)


def prepare(rehearsal, production, stages, sha, code_group):
    for root in (rehearsal,rehearsal/'releases',production,production/'releases',stages):
        owned(root,directory=True)
    archive, manifest, report_hash = tested_artifact(rehearsal, stages, sha)
    current = current_release(production, 'current')
    stage = stages/('production-'+sha)
    stage.mkdir(mode=0o700, exist_ok=True)
    owned(stage, directory=True)
    saved_archive = stage/archive.name
    if saved_archive.exists() or saved_archive.is_symlink():
        if digest(saved_archive) != manifest['artifact_sha256']:
            raise ValueError('Existing production archive differs; refusing overwrite.')
    else:
        with archive.open('rb') as source, saved_archive.open('xb') as destination:
            shutil.copyfileobj(source, destination)
        saved_archive.chmod(0o600)
    if digest(saved_archive) != manifest['artifact_sha256']:
        raise ValueError('Copied artifact checksum mismatch.')
    release = production/'releases'/sha
    if not release.exists() and not release.is_symlink():
        # Extraction is disposable; publish a complete candidate only after it
        # has the production links and a byte-for-byte verification.
        with tempfile.TemporaryDirectory(prefix='.promotion-', dir=production/'releases') as temporary:
            with deployment.tarfile.open(saved_archive) as bundle:
                archive_entries(bundle, sha)
                bundle.extractall(temporary, filter='data')
            candidate = Path(temporary)/sha
            for name, target in SHARED.items():
                path = candidate/'apps/kaardid'/name
                path.rmdir()  # Only an empty packaged shared directory is allowed.
                path.symlink_to(production/'shared'/target, target_is_directory=True)
            for path in [candidate,*candidate.rglob('*')]:
                if path.is_symlink():
                    continue
                os.chown(path, -1, code_group)
                path.chmod(0o2750 if path.is_dir() else (0o750 if path.stat().st_mode&0o111 else 0o640))
            verify_contents(saved_archive, candidate, production/'shared')
            candidate.rename(release)
    verify_contents(saved_archive, release, production/'shared')
    for path in [release,*release.rglob('*')]:
        if not path.is_symlink() and path.stat().st_gid != code_group:
            raise ValueError('Unexpected production code group: '+str(path))
    identity = json.loads((release/'release.json').read_text())
    if identity != {key:value for key,value in manifest.items() if key!='artifact_sha256'}:
        raise ValueError('Production release manifest differs from tested archive.')
    plan = {'release':sha, 'artifact_sha256':manifest['artifact_sha256'],
            'rehearsal_report_sha256':report_hash,
            'expected_current':current.name if current else None,
            'prepared_at':datetime.now(timezone.utc).isoformat(),
            'activated':False}
    # Same artifact identity is kept; production secrets/data are separate links.
    save_private(stage/'release-manifest.json',json.dumps(manifest,indent=2)+'\n')
    save_private(stage/'promotion-plan.json',json.dumps(plan,indent=2)+'\n')
    return release, stage, plan


def cutover_confirmation(readiness, sha, required):
    try:
        owned(readiness)
    except FileNotFoundError:
        raise ReadinessError(f'Production readiness confirmation is missing: {readiness}.') from None
    if readiness.stat().st_mode & 0o077:
        raise ReadinessError(f'Production readiness confirmation must be private (0600): {readiness}.')
    try:
        confirmation = json.loads(readiness.read_text())
    except json.JSONDecodeError:
        raise ReadinessError(f'Production readiness confirmation is invalid JSON: {readiness}.') from None
    if not isinstance(confirmation, dict):
        raise ReadinessError(f'Production readiness confirmation must be a JSON object: {readiness}.')
    if confirmation.get('release') != sha:
        raise ReadinessError(f'Production readiness confirmation in {readiness} must name release {sha}.')
    missing = [key for key in required if confirmation.get(key) is not True]
    if missing:
        raise ReadinessError('Production readiness is incomplete. Confirm '+', '.join(missing)+f' in {readiness}.')
    return confirmation


def activation_preflight(release, production, stage, readiness, site, *, restricted=False):
    if (production/'preview').exists() or (production/'preview').is_symlink():
        raise ValueError('Remove the VPN test-data preview and its nginx site before production cutover.')
    current = current_release(production, 'current')
    if restricted and current is not None:
        raise ValueError('Restricted activation is only available before the first production release.')
    if (production/'previous').exists() and not (production/'previous').is_symlink():
        raise ValueError('Unexpected previous production pointer.')
    if current is None and (production/'previous').is_symlink():
        raise ValueError('Previous production pointer exists without an active release.')
    plan = json.loads((stage/'promotion-plan.json').read_text())
    if plan.get('expected_current') != (current.name if current else None):
        raise ValueError('Production changed since preparation; prepare and review again.')
    confirmation = {}
    if current is None:
        required = RESTRICTED_READINESS if restricted else READINESS
        confirmation = cutover_confirmation(readiness, release.name, required)
    info = site.lstat()
    text = site.read_text()
    enabled=site.parent.parent/'sites-enabled'/site.name
    if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022
            or not enabled.is_symlink() or enabled.resolve()!=site
            or not text.startswith('# Managed by Kaardid production deployment\n')
            or 'listen 127.0.0.1:18081;' not in text
            or 'root /srv/kaardid-production/current/apps/kaardid;' not in text
            or 'add_header X-Kaardid-Environment production always;' not in text
            or 'fastcgi_pass unix:/run/php/php8.5-fpm-kaardid-production.sock;' not in text
            or 'SCRIPT_FILENAME $realpath_root$fastcgi_script_name;' not in text):
        raise ValueError('Reviewed production nginx backend is not installed.')
    if restricted:
        if hashlib.sha256(text.encode()).hexdigest() != confirmation.get('backendConfigSha256'):
            raise ValueError('The installed restricted backend differs from the reviewed nginx configuration.')
        for unit in ('kaardid-update.service', 'kaardid-update.timer'):
            if subprocess.check_output(['systemctl','show','-p','LoadState','--value',unit],text=True).strip() != 'not-found':
                raise ValueError('Keep the updater service and timer uninstalled during restricted activation.')
    # Loading profiles internally is permitted; never emit secrets/config values.
    # Require both migration and app selectors to point to this production only.
    php = r'''require $argv[1].'/protected/config/Environment.php';
    $s=KaardidEnvironment::settings();
    $expected=array('environment'=>'production','databaseFile'=>'/etc/kaardid-production/app-db.json',
      'migrationDatabaseFile'=>'/home/erik/.config/kaardid/production-migration-db.json',
      'runtimePath'=>'/srv/kaardid-production/shared/runtime',
      'consoleRuntimePath'=>'/srv/kaardid-production/shared/runtime-console',
      'assetsPath'=>'/srv/kaardid-production/shared/assets','externalCallbackBaseUrl'=>'https://kaardid.ra.ee');
    foreach($expected as $k=>$v) if(($s[$k]??null)!==$v) exit(1);
    foreach(array('production'=>'kaart_prod_app','console'=>'kaart_prod_migrate','cron'=>'kaart_prod_app') as $p=>$u) {
      $d=KaardidEnvironment::database($p);
      if($d['connectionString']!=='pgsql:host=127.0.0.1;port=5432;dbname=kaart_prod' || $d['username']!==$u) exit(1);
      if($p==='console' && ($d['initSQLs']??array())!==array('SET ROLE kaart_prod_owner')) exit(1);
    }
    KaardidEnvironment::integrations();'''
    result = subprocess.run(['php','-d','display_errors=0','-r',php,str(release/'apps/kaardid')],
                            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=30)
    if result.returncode:
        raise ValueError('Production private configuration preflight failed; no database work started.')
    # An installed nginx with a missing current link must return 503, not serve
    # the test site. Reopening is verified only after the new pointer exists.
    if current is None and deployment.fetch('/',target='production')[0] != 503:
        raise ValueError('First-deployment backend is not closed with HTTP 503.')
    return current


def activate(release, production, stage, readiness, site, credentials, *, restricted=False):
    # Hold the *same* runtime lock as cron.php update before any preflight that
    # depends on current, and throughout migrations/checks/rollback/cleanup.
    with deployment.operation_lock(production/'shared/runtime'):
        current = activation_preflight(release,production,stage,readiness,site,restricted=restricted)
        previous = production/'previous'
        report_path=stage/'deployment-report.txt'
        if current==release and not previous.is_symlink():
            # Repeating the first successful deployment has no older code yet.
            lines=report_path.read_text().splitlines() if report_path.is_file() else []
            if ('Previous release retained: None' not in lines
                    or 'KAARDID_PRODUCTION_SWITCH_COMPLETE' not in lines):
                raise ValueError('Cannot establish rollback history for repeat production deployment.')
            rollback=None
        else:
            rollback=(deployment.rollback_for_deploy(release,current,previous,report_path) if current else None)
        attempt={'release':release.name,'started_at':datetime.now(timezone.utc).isoformat(),'status':'pending'}
        attempt_path=stage/'activation-attempt.json'
        save_private(attempt_path,json.dumps(attempt,indent=2)+'\n')
        try:
            report = deployment.deploy_locked(release,production/'current',rollback,stage,credentials,
                                              target='production',reopen_after_cutover=restricted)
        except BaseException:
            attempt.update(status='failed',finished_at=datetime.now(timezone.utc).isoformat())
            save_private(attempt_path,json.dumps(attempt,indent=2)+'\n')
            raise
        attempt.update(status='succeeded',finished_at=datetime.now(timezone.utc).isoformat())
        save_private(attempt_path,json.dumps(attempt,indent=2)+'\n')
        if restricted:
            report.append('First release activated under the restricted frontend. Public release checks remain pending.')
        save_private(stage/'deployment-report.txt','\n'.join(report)+'\n')
        return report


def rollback_code(release, production, stage):
    """Manual, explicit return to previous code; never run migrations or restore DB."""
    with deployment.operation_lock(production/'shared/runtime'):
        if (production/'preview').exists() or (production/'preview').is_symlink():
            raise ValueError('VPN preview is not an activated production release.')
        current=current_release(production,'current')
        previous=current_release(production,'previous')
        if current is None or previous!=release or release==current:
            raise ValueError('Rollback SHA must identify the retained previous production release.')
        config=production/'shared/config'
        marker=config/'.maintenance';probe=config/'.deployment-probe.json'
        def checked_file(path):
            owned(path)
            if path.stat().st_mode & 0o027:
                raise ValueError('Unsafe rollback maintenance/probe permissions.')
        def close():
            if marker.exists() or marker.is_symlink():
                checked_file(marker)
            else:
                with marker.open('x') as output:
                    os.fchown(output.fileno(),-1,config.stat().st_gid)
                    os.fchmod(output.fileno(),0o640)
        manual=marker.exists() or marker.is_symlink()
        close();marker_inode=marker.stat().st_ino
        try:
            if probe.exists() or probe.is_symlink():
                checked_file(probe);probe.unlink()
            if deployment.fetch('/',target='production')[0]!=503:
                raise RuntimeError('Maintenance did not close production; no code changed.')
            token=secrets.token_hex(32)
            with probe.open('x') as output:
                os.fchown(output.fileno(),-1,config.stat().st_gid)
                os.fchmod(output.fileno(),0o640)
                json.dump({'token':token,'expiresAt':int(time.time())+600,
                           'appPath':str((release/'apps/kaardid').resolve())},output)
            def ready():
                report=deployment.health_check(token,target='production')
                if deployment.fetch('/',target='production')[0]!=503:
                    raise RuntimeError('Visitors escaped rollback maintenance.')
                probe.unlink()
                if not manual and marker.stat().st_ino==marker_inode:
                    marker.unlink()
                    try: report+=deployment.health_check(target='production')
                    except BaseException: close();raise
                else:
                    report.append('Existing manual maintenance preserved; inspect before reopening.')
                return report
            report=deployment.activate_release(release,production/'current',current,ready,stage.parent)
            report.append('Manual code rollback complete; database and migrations unchanged.')
            save_private(stage/'rollback-report.txt','\n'.join(report)+'\n')
            return report
        except BaseException:
            close()
            raise
        finally:
            if probe.exists() or probe.is_symlink():
                checked_file(probe);probe.unlink()


@contextmanager
def promotion_lock(stages):
    descriptor = os.open(stages/'production-deploy.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    try:
        info=os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
            raise ValueError('Unexpected promotion lock owner/type/permissions.')
        try:
            fcntl.flock(descriptor,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Another production preparation/deployment is running.')
        yield
    finally:
        os.close(descriptor)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare',action='store_true',help='stage the exact tested archive only')
    mode.add_argument('--activate',action='store_true',help='activate a prepared release; confirm readiness for initial cutover')
    mode.add_argument('--activate-restricted',action='store_true',help='first activation under the verified restricted frontend')
    mode.add_argument('--rollback',action='store_true',help='explicit code-only rollback to retained previous release')
    parser.add_argument('sha')
    args = parser.parse_args()
    if not re.fullmatch('[a-f0-9]{40}',args.sha):
        parser.error('Supply the full tested rehearsal SHA.')
    os.umask(0o077)
    if (pwd.getpwuid(os.geteuid()).pw_name!='erik'
            or subprocess.check_output(['hostname','-f'],text=True).strip()!='kaardid.arhiiv.ee'):
        raise SystemExit('Run as erik on the Kaardid VM only.')
    rehearsal, production = Path('/srv/kaardid'),Path('/srv/kaardid-production')
    stages = Path.home()/'.kaardid-setup'
    with promotion_lock(stages), deployment.operation_lock(rehearsal/'shared/runtime'):
        if args.prepare:
            release, stage, plan = prepare(rehearsal,production,stages,args.sha,
                                           grp.getgrnam('kaardid-production-code').gr_gid)
            print('Exact tested archive prepared: '+plan['release']+'\nSHA256: '+plan['artifact_sha256'])
            print('No maintenance, backup, migration, pointer, nginx, traffic or timer changes made.')
            print('Plan: '+str(stage/'promotion-plan.json')+'\nKAARDID_PRODUCTION_PROMOTION_PREPARED')
        elif args.rollback:
            stage=stages/('production-'+args.sha)
            owned(stage,directory=True)
            owned(stage/'release-manifest.json')
            manifest=json.loads((stage/'release-manifest.json').read_text())
            archive=stage/(args.sha+'.tar.gz')
            if (manifest.get('commit')!=args.sha or manifest.get('purpose')!='private-rehearsal'
                    or digest(archive)!=manifest.get('artifact_sha256')):
                raise ValueError('Retained rollback artifact identity/checksum is invalid.')
            release=production/'releases'/args.sha
            verify_contents(archive,release,production/'shared')
            print('\n'.join(rollback_code(release,production,stage)))
        else:
            # Do not regenerate the plan on activation: preserve its current-
            # release guard and the operator's prepared artifact review.
            archive, manifest, report_hash = tested_artifact(rehearsal,stages,args.sha)
            stage=stages/('production-'+args.sha)
            owned(stage,directory=True)
            owned(stage/'promotion-plan.json')
            plan=json.loads((stage/'promotion-plan.json').read_text())
            if (plan.get('release')!=args.sha or plan.get('artifact_sha256')!=manifest['artifact_sha256']
                    or plan.get('rehearsal_report_sha256')!=report_hash
                    or digest(stage/archive.name)!=manifest['artifact_sha256']):
                raise ValueError('Prepared promotion evidence changed; prepare and review again.')
            release=production/'releases'/args.sha
            verify_contents(stage/archive.name,release,production/'shared')
            filename = 'production-restricted-readiness.json' if args.activate_restricted else 'production-readiness.json'
            try:
                report=activate(release,production,stage,Path.home()/'.config/kaardid'/filename,
                    Path('/etc/nginx/sites-available/kaardid-production'),
                    Path.home()/'.config/kaardid/production-migration-db.json', restricted=args.activate_restricted)
            except ReadinessError as error:
                flag = '--activate-restricted' if args.activate_restricted else '--activate'
                raise SystemExit(
                    f'{error}\nActivation stopped before maintenance, backup or migration. '
                    'Review the first activation checks in docs/deployment.md.\n'
                    f'After confirming readiness, resume: bin/production-deploy {flag} {args.sha}'
                ) from None
            print('\n'.join(report))


if __name__=='__main__':
    for signum in (signal.SIGTERM,signal.SIGHUP):
        signal.signal(signum,deployment.interrupted)
    main()
