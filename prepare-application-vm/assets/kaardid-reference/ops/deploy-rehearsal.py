#!/usr/bin/env python3
"""Shared deployment lifecycle and the configured private rehearsal CLI."""
import fcntl
from contextlib import contextmanager
from datetime import datetime, timezone
import grp
import hashlib
import http.client
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import secrets
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile
import time

TARGETS = {
    'rehearsal': {'database':'kaart', 'user':'kaart_migrate', 'role':'kaart_owner',
                  'port':18080, 'backups':'rehearsal-backups'},
    'production': {'database':'kaart_prod', 'user':'kaart_prod_migrate', 'role':'kaart_prod_owner',
                   'port':18081, 'backups':'production-backups'},
}


def backup_and_migrate(app, stage, backups, credentials, *, target='rehearsal'):
    """Save a private pre-deploy dump, then apply and verify Yii migrations."""
    if (credentials.is_symlink() or credentials.stat().st_uid != os.geteuid()
            or credentials.stat().st_mode & 0o077):
        raise ValueError('Migration credentials must be private and owned by the deployment user.')
    db = json.loads(credentials.read_text())
    settings = TARGETS[target]
    expected = dict(host='127.0.0.1', **{key:settings[key] for key in ('database','user','role')})
    if (any(db.get(key) != value for key, value in expected.items())
            or type(db.get('port')) is not int or not 1 <= db['port'] <= 65535
            or not isinstance(db.get('password'), str) or not db['password']
            or '\n' in db['password'] or '\r' in db['password']):
        raise ValueError('Unexpected '+target+' backup database configuration.')
    backups.mkdir(mode=0o700, exist_ok=True)
    if (backups.is_symlink() or backups.stat().st_uid != os.geteuid()
            or backups.stat().st_mode & 0o077):
        raise ValueError('Backup directory must be private and owned by the deployment user.')
    commit = app.parent.parent.name
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    snapshot = Path(tempfile.mkdtemp(prefix=stamp+'-'+commit[:12]+'-', dir=backups))
    # Avoid inherited libpq settings or passwords redirecting the backup.
    env = {key:value for key,value in os.environ.items() if not key.startswith('PG')}
    env['PGCONNECT_TIMEOUT'] = '10'
    passfile = snapshot/'.pgpass'
    partial = snapshot/(settings['database']+'.dump.partial')
    backup = snapshot/(settings['database']+'.dump')
    escape = lambda value: str(value).replace('\\', '\\\\').replace(':', '\\:')
    try:
        with passfile.open('x') as output:
            passfile.chmod(0o600)
            output.write(':'.join(escape(db[key]) for key in ('host','port','database','user','password'))+'\n')
        env['PGPASSFILE'] = str(passfile)
        with partial.open('xb') as output, (snapshot/'backup.log').open('x') as log:
            partial.chmod(0o600)
            result = subprocess.run(['pg_dump','--format=custom','--no-password',
                '--host='+db['host'],'--port='+str(db['port']),'--username='+db['user'],
                '--role='+db['role'],'--dbname='+db['database'],'--lock-wait-timeout=30s'],
                stdout=output, stderr=log, stdin=subprocess.DEVNULL, env=env, timeout=900)
            if result.returncode or not partial.stat().st_size:
                raise RuntimeError('Database backup failed; release not switched. See '+str(snapshot))
            # Read every archive payload without executing SQL or connecting to a database.
            result = subprocess.run(['pg_restore','--file=/dev/null',str(partial)],
                stdout=log, stderr=log, stdin=subprocess.DEVNULL, env=env, timeout=900)
            if result.returncode:
                raise RuntimeError('Database archive check failed; release not switched. See '+str(snapshot))
        partial.rename(backup)
        with backup.open('rb') as source:
            checksum = hashlib.file_digest(source,'sha256').hexdigest()
        metadata = {'database':db['database'], 'target_commit':commit,
                    'created_at':datetime.now(timezone.utc).isoformat(),
                    'sha256':checksum, 'deployment_status':'pending'}
        (snapshot/'backup.json').write_text(json.dumps(metadata, indent=2)+'\n')
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError('Database backup could not complete; release not switched. See '+str(snapshot)) from error
    finally:
        passfile.unlink(missing_ok=True)
        env.pop('PGPASSFILE', None)
    print('Pre-deployment database backup: '+str(backup), flush=True)

    def migrate(arguments, name):
        with (snapshot/name).open('x') as log:
            try:
                result = subprocess.run(['php','protected/yiic.php','migrate',*arguments],
                    cwd=app, text=True, stdout=log, stderr=log, stdin=subprocess.DEVNULL,
                    env=env, timeout=900)
            except (OSError, subprocess.TimeoutExpired) as error:
                raise RuntimeError('Migration command could not complete; release not switched. '
                    'Database changes may remain. Backup and diagnostics: '+str(snapshot)) from error
        if result.returncode:
            raise RuntimeError('Migration command failed; release not switched. '
                'Database changes may remain. Backup and diagnostics: '+str(snapshot))
        return (snapshot/name).read_text()

    preview = migrate(['new'], 'migration-preview.txt')
    (stage/'migration-preview.txt').write_text(preview)
    migrate(['up','--interactive=0'], 'migration-apply.txt')
    remaining = migrate(['new'], 'migration-after.txt')
    if 'No new migrations found.' not in remaining:
        raise RuntimeError('Pending migrations remain; release not switched. '
            'Database changes may remain. Backup and diagnostics: '+str(snapshot))
    print('No pending migrations.' if 'No new migrations found.' in preview
          else 'Pending migrations applied successfully.', flush=True)
    return backup


def prune_backups(backups, completed_backup=None, *, target='rehearsal'):
    """Keep three verified successful/resolved snapshots, protecting other attempts."""
    if not shutil.rmtree.avoids_symlink_attacks:
        raise ValueError('Safe directory deletion is unavailable; retaining backups.')
    uid = os.geteuid()
    settings = TARGETS[target]
    dump_name = settings['database']+'.dump'
    snapshot_name = re.compile(r'\d{8}T\d{6}Z-[a-f0-9]{12}-[a-z0-9_]{8}')

    def private(path, directory=False):
        info = path.lstat()
        expected = stat.S_ISDIR if directory else stat.S_ISREG
        if not expected(info.st_mode) or info.st_uid != uid or info.st_mode & 0o077:
            raise ValueError('Unsafe backup path: '+str(path))

    def record(snapshot):
        private(snapshot, directory=True)
        private(snapshot/'backup.json')
        private(snapshot/dump_name)
        data = json.loads((snapshot/'backup.json').read_text())
        if (not isinstance(data, dict) or data.get('database') != settings['database']
                or not isinstance(data.get('target_commit'), str)
                or not re.fullmatch(r'[a-f0-9]{40}', data['target_commit'])
                or snapshot.name.split('-')[1] != data['target_commit'][:12]
                or not isinstance(data.get('sha256'), str)
                or not re.fullmatch(r'[a-f0-9]{64}', data['sha256'])
                or not (snapshot/dump_name).stat().st_size):
            raise ValueError('Unexpected backup identity: '+str(snapshot))
        return data

    private(backups, directory=True)
    if backups.name != settings['backups']:
        raise ValueError('Unexpected backup directory for '+target+'.')
    if completed_backup is not None:
        if (completed_backup.parent.parent != backups or completed_backup.name != dump_name
                or not snapshot_name.fullmatch(completed_backup.parent.name)):
            raise ValueError('Unexpected completed backup path.')
        data = record(completed_backup.parent)
        data['deployment_status'] = 'succeeded'
        # A crash before this atomic save leaves the snapshot protected as pending.
        descriptor, temporary = tempfile.mkstemp(prefix='.backup-', dir=completed_backup.parent)
        try:
            with os.fdopen(descriptor, 'w') as output:
                json.dump(data, output, indent=2)
                output.write('\n')
            os.replace(temporary, completed_backup.parent/'backup.json')
        finally:
            Path(temporary).unlink(missing_ok=True)

    eligible = []
    protected = 0
    for snapshot in sorted(backups.iterdir()):
        if not snapshot_name.fullmatch(snapshot.name):
            protected += 1
            continue
        private(snapshot, directory=True)
        if not (snapshot/'backup.json').exists():
            protected += 1  # Incomplete dump or an interrupted verification.
            continue
        data = record(snapshot)
        if data.get('deployment_status') not in ('succeeded', 'resolved'):
            protected += 1  # Includes backups from before outcome tracking existed.
            continue
        eligible.append((snapshot, data))
    # Names begin with the UTC creation timestamp; never use mutable filesystem mtime.
    retained = {snapshot for snapshot, _ in eligible[-3:]}
    if completed_backup is not None and completed_backup.parent not in retained:
        raise ValueError('Completed backup is not among the newest three; retaining all backups.')
    obsolete = eligible[:-3]
    # Before deleting anything, verify both the deletion candidates and the
    # copies that will remain. Archive readability was checked at creation.
    if obsolete:
        for snapshot, data in eligible:
            with (snapshot/dump_name).open('rb') as source:
                if hashlib.file_digest(source, 'sha256').hexdigest() != data['sha256']:
                    raise ValueError('Backup checksum mismatch; retaining backups: '+str(snapshot))
    for snapshot, _ in obsolete:
        shutil.rmtree(snapshot)
    return len(obsolete), protected


def rollback_for_deploy(incoming, current, pointer, report_path):
    """A repeat deployment must preserve the earlier rollback release."""
    if pointer.exists() and not pointer.is_symlink():
        raise ValueError('Unexpected previous-release pointer.')
    if incoming != current:
        return current
    if pointer.is_symlink():
        previous = Path(os.readlink(pointer))
    else:
        report = report_path.read_text() if report_path.is_file() else ''
        match = re.search(r'^Previous release retained: (.+)$', report, re.M)
        if not match:
            raise ValueError('Cannot identify the previous release for a repeat deployment.')
        previous = Path(match.group(1))
    if (previous.parent != incoming.parent or not re.fullmatch(r'[a-f0-9]{40}', previous.name)
            or previous == incoming or previous.is_symlink() or not previous.is_dir()):
        raise ValueError('Invalid previous release; refusing retention cleanup.')
    return previous


def prune_releases(releases, archived, stages, keep, *, bundle_prefix='release-'):
    """Remove only identified, owned releases; never follow shared-data links."""
    if not shutil.rmtree.avoids_symlink_attacks:
        raise ValueError('Safe directory deletion is unavailable; retaining old releases.')
    uid = os.geteuid()
    directories = []
    bundles = []

    def identity(directory):
        if (directory.is_symlink() or not directory.is_dir() or directory.stat().st_uid != uid
                or directory.stat().st_mode & 0o022):
            raise ValueError('Unsafe release directory: '+str(directory))
        manifest = directory/'release.json'
        if manifest.is_symlink() or manifest.stat().st_uid != uid or manifest.stat().st_mode & 0o022:
            raise ValueError('Unsafe release manifest: '+str(manifest))
        data = json.loads(manifest.read_text())
        if not isinstance(data, dict) or data.get('commit') != directory.name or data.get('purpose') != 'private-rehearsal':
            raise ValueError('Unexpected release identity: '+str(directory))

    for sha in keep:
        if not re.fullmatch(r'[a-f0-9]{40}', sha):
            raise ValueError('Invalid retained release identity.')
        identity(releases/sha)
    for root in (releases, archived):
        if not root.exists():
            continue
        if root.is_symlink() or not root.is_dir() or root.stat().st_uid != uid:
            raise ValueError('Unsafe release root: '+str(root))
        for directory in sorted(root.iterdir()):
            if not re.fullmatch(r'[a-f0-9]{40}', directory.name):
                raise ValueError('Unrecognized release entry: '+str(directory))
            identity(directory)
            if root == archived or directory.name not in keep:
                directories.append(directory)
    for pointer in releases.parent.iterdir():
        if pointer.is_symlink() and pointer.resolve() in directories:
            raise ValueError('Another pointer still references an old release: '+str(pointer))
    if stages.is_symlink() or stages.stat().st_uid != uid:
        raise ValueError('Unsafe artifact staging root.')
    for directory in sorted(stages.glob(bundle_prefix+'*')):
        manifest = directory/'release-manifest.json'
        if not manifest.exists():
            continue
        if (directory.is_symlink() or directory.stat().st_uid != uid or manifest.is_symlink()
                or manifest.stat().st_uid != uid):
            raise ValueError('Unsafe artifact directory: '+str(directory))
        data = json.loads(manifest.read_text())
        if not isinstance(data, dict):
            raise ValueError('Unexpected artifact identity: '+str(directory))
        sha = data.get('commit', '')
        if not isinstance(sha, str) or data.get('purpose') != 'private-rehearsal' or not re.fullmatch(r'[a-f0-9]{40}', sha):
            raise ValueError('Unexpected artifact identity: '+str(directory))
        bundle = directory/(sha+'.tar.gz')
        if sha not in keep and (bundle.exists() or bundle.is_symlink()):
            if bundle.is_symlink() or not bundle.is_file() or bundle.stat().st_uid != uid:
                raise ValueError('Unsafe artifact bundle: '+str(bundle))
            bundles.append(bundle)
    # Complete every safety check before deleting anything. rmtree unlinks the
    # app's runtime/upload/asset symlinks without traversing their targets.
    for directory in directories:
        shutil.rmtree(directory)
    for bundle in bundles:
        bundle.unlink()
    if archived.is_dir() and not any(archived.iterdir()):
        archived.rmdir()
    return len(directories), len(bundles)


def activate_release(release, link, rollback, health_check, stages):
    def switch(target, destination):
        temporary = destination.with_name(destination.name+'.next-'+str(os.getpid()))
        temporary.symlink_to(target, target_is_directory=True)
        os.replace(temporary, destination)

    original = os.readlink(link) if link.is_symlink() else None
    switch(str(release), link)
    try:
        report = health_check()
    except BaseException:
        if original is None:
            link.unlink()
        else:
            switch(original, link)
        print('Health check failed; previous '+('rehearsal' if link.name=='rehearsal' else 'production')+' link restored.'
              if original else 'Health check failed; first production release unlinked.', file=sys.stderr)
        raise
    if rollback is not None:
        switch(str(rollback), link.with_name('previous'))
    report.extend(['Active release: '+release.name, 'Previous release retained: '+str(rollback),
                   'KAARDID_'+('REHEARSAL' if link.name=='rehearsal' else 'PRODUCTION')+'_SWITCH_COMPLETE'])
    try:
        removed, bundles = prune_releases(release.parent, release.parent.parent/'archived-releases',
                                         stages, {p.name for p in (release, rollback) if p is not None},
                                         **({'bundle_prefix':'production-'} if link.name=='current' else {}))
        report.append('Retention cleanup: removed '+str(removed)+' old release directories and '+str(bundles)+' old bundles; active and previous retained.')
    except (OSError, ValueError) as error:
        warning = 'Retention cleanup warning: '+str(error)+'; the healthy release remains active.'
        report.append(warning)
        print(warning, file=sys.stderr)
    return report


def fetch(path, token=None, *, target='rehearsal'):
    # No redirects: the capability must never be forwarded to another origin.
    connection = http.client.HTTPConnection('127.0.0.1', TARGETS[target]['port'], timeout=30)
    try:
        headers = {'Authorization':'Bearer '+token} if token else {}
        if target == 'production':
            headers['Host'] = 'kaardid.ra.ee'
        connection.request('GET', path, headers=headers)
        response = connection.getresponse()
        if target=='production' and response.getheader('X-Kaardid-Environment')!='production':
            raise RuntimeError('Production probe reached an unexpected nginx backend.')
        return response.status, response.read(), response.getheader('Content-Type', '')
    finally:
        connection.close()


def health_check(token=None, *, target='rehearsal'):
    request = fetch if target=='rehearsal' else lambda path, token: fetch(path, token, target=target)
    report=[]
    status,body,_=request('/',token)
    if status!=200:raise RuntimeError('Home returned HTTP '+str(status))
    if target=='rehearsal' and b'analytics.ra.ee/js/script.js' in body:raise RuntimeError('Rehearsal analytics must be disabled.')
    assets=sorted(set(re.findall(rb'/assets/[a-zA-Z0-9_./-]+\.(?:css|js)',body)))
    if not assets:raise RuntimeError('No published CSS/JavaScript found.')
    for asset in assets:
        path=asset.decode();status,_,mime=request(path,token)
        if status!=200 or not ('javascript' in mime or 'text/css' in mime):
            raise RuntimeError('Asset check failed: '+path+' HTTP '+str(status))
    report.append('Home and '+str(len(assets))+' published CSS/JavaScript files passed.'+
                  (' Rehearsal analytics disabled.' if target=='rehearsal' else ''))
    for path,expected in [('/index.php/map/search',200),('/index.php/map/searchAdvanced',200),
        ('/protected/config/production.php',404),('/index-dev.php',404),('/index.php/test/login',404),('/cron.php',404)]:
        status,_,_=request(path,token)
        if status!=expected:raise RuntimeError('Route check failed: '+path+' HTTP '+str(status))
        report.append(path+' HTTP '+str(status))
    return report


@contextmanager
def operation_lock(runtime):
    """Share the updater's lock before maintenance, backup or migration work."""
    descriptor = os.open(runtime/'operations.lock', os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW, 0o660)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o007:
            raise ValueError('Unsafe updater/deployment lock permissions.')
        if info.st_uid == os.geteuid():
            os.fchmod(descriptor, 0o660)  # The VM runtime directory supplies its setgid group.
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Updater or deployment is running; no deployment work was started.')
        yield
    finally:
        os.close(descriptor)


def deploy_with_maintenance(release, link, rollback, stage, credentials, *, target='rehearsal'):
    with operation_lock(link.parent/'shared/runtime'):
        return deploy_locked(release, link, rollback, stage, credentials, target=target)


def deploy_locked(release, link, rollback, stage, credentials, *, target='rehearsal', reopen_after_cutover=False):
    """Close web traffic before database work; only reopen after readiness checks."""
    config = link.parent/'shared/config'
    marker = config/'.maintenance'
    probe = config/'.deployment-probe.json'
    # Both environments use this lifecycle, but never each other's DB/HTTP port.
    request = fetch if target=='rehearsal' else lambda path: fetch(path, target=target)
    check = health_check if target=='rehearsal' else lambda token=None: health_check(token, target=target)
    backups = stage.parent/TARGETS[target]['backups']

    def private_file(path):
        info = path.lstat()
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_mode & 0o027):
            raise ValueError('Unsafe deployment maintenance file: '+str(path))
        return info

    def create_marker():
        with marker.open('x') as output:
            os.fchown(output.fileno(), -1, config.stat().st_gid)
            os.fchmod(output.fileno(), 0o640)
        return marker.stat().st_ino

    # The caller holds the deployment lock. A stale capability from an interrupted
    # deploy is revoked before any database work; unsafe files are never replaced.
    if probe.exists() or probe.is_symlink():
        private_file(probe)
        probe.unlink()
    if reopen_after_cutover:
        if (target != 'production' or link.exists() or link.is_symlink()
                or not marker.exists() or private_file(marker).st_size):
            raise ValueError('Expected the empty cutover maintenance marker before first production activation.')
        created_inode = marker.lstat().st_ino
    elif marker.exists() or marker.is_symlink():
        private_file(marker)
        created_inode = None
    else:
        created_inode = create_marker()
    print('Maintenance enabled; visitors receive HTTP 503.', flush=True)
    try:
        if request('/')[0] != 503:
            raise RuntimeError('Maintenance did not close the site; no database work was started.')
        backup = backup_and_migrate(release/'apps/kaardid', stage, backups, credentials,
                                    **({'target':target} if target!='rehearsal' else {}))
        token = secrets.token_hex(32)
        with probe.open('x') as output:
            os.fchown(output.fileno(), -1, config.stat().st_gid)
            os.fchmod(output.fileno(), 0o640)
            json.dump({'token':token, 'expiresAt':int(time.time())+600,
                       'appPath':str((release/'apps/kaardid').resolve())}, output)

        def ready():
            report = check(token)
            if request('/')[0] != 503:
                raise RuntimeError('Visitors escaped maintenance during deployment checks.')
            probe.unlink()  # Revoke before allowing visitors back in.
            # Preserve a pre-existing manual switch, or one replaced by an operator.
            if created_inode is not None and marker.lstat().st_ino == created_inode:
                marker.unlink()
                try:
                    check()
                except BaseException:
                    # Close visitors before activate_release restores the old code.
                    if not marker.exists() and not marker.is_symlink():
                        create_marker()
                    raise
                report.append('Maintenance disabled; normal visitor checks passed.')
            else:
                report.append('Existing manual maintenance preserved; visitors still receive HTTP 503.')
            return report

        report = activate_release(release, link, rollback, ready, stage.parent)
        report.insert(0, 'Pre-deployment database backup: '+str(backup))
        try:
            removed, protected = prune_backups(backups, backup, target=target)
            report.append('Backup cleanup: removed '+str(removed)+' old snapshots; latest three verified '
                          'successful/resolved backups retained; '+str(protected)+' unresolved or unclassified entries protected.')
        except (OSError, ValueError) as error:
            warning = 'Backup cleanup warning: '+str(error)+'; the healthy release remains active.'
            report.append(warning)
            print(warning, file=sys.stderr)
        return report
    except BaseException:
        # Database changes may already exist, even after automatic code rollback.
        if not marker.exists() and not marker.is_symlink():
            create_marker()
        print('Deployment failed; maintenance remains ON. Inspect diagnostics before reopening. '
              'Database changes are not automatically reversed.', file=sys.stderr)
        raise
    finally:
        if probe.exists() or probe.is_symlink():
            private_file(probe)
            probe.unlink()


def interrupted(signum, frame):
    raise SystemExit('Deployment interrupted by signal '+str(signum))


def main():
    os.umask(0o077)
    if pwd.getpwuid(os.geteuid()).pw_name!='erik' or subprocess.check_output(['hostname','-f'],text=True).strip()!='kaardid.arhiiv.ee':
        raise SystemExit('Run as erik on the Kaardid VM only.')
    if len(sys.argv)!=2:
        raise SystemExit('Usage: deploy-rehearsal.py <private artifact directory>')
    lock=(Path.home()/'.kaardid-setup/rehearsal-deploy.lock').open('a')
    try:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit('Another rehearsal deployment is running.')
    stage=Path(sys.argv[1]).resolve()
    manifest=json.loads((stage/'release-manifest.json').read_text())
    commit=manifest.get('commit','')
    if not re.fullmatch(r'[a-f0-9]{40}',commit) or manifest.get('purpose')!='private-rehearsal':
        raise SystemExit('Unexpected release identity.')
    archive=stage/(commit+'.tar.gz')
    if hashlib.file_digest(archive.open('rb'),'sha256').hexdigest()!=manifest['artifact_sha256']:
        raise SystemExit('Artifact checksum mismatch.')
    link=Path('/srv/kaardid/rehearsal')
    if not link.is_symlink():
        raise SystemExit('Initial privileged setup is required: bin/rehearsal-activate.')
    previous=os.readlink(link)
    if not re.fullmatch(r'/srv/kaardid/releases/[a-f0-9]{40}',previous):
        raise SystemExit('Unexpected existing rehearsal target.')
    site_path=Path('/etc/nginx/sites-available/kaardid-rehearsal')
    site=site_path.read_text()
    if (site_path.stat().st_uid!=0 or site_path.stat().st_mode&0o022 or
        not site.startswith('# Managed by Kaardid activate-rehearsal\n') or
        re.findall(r'^\s*listen\s+([^;]+);',site,re.M)!=['127.0.0.1:18080'] or
        'root /srv/kaardid/rehearsal/apps/kaardid;' not in site):
        raise SystemExit('Expected managed loopback-only nginx configuration is missing.')
    release=Path('/srv/kaardid/releases')/commit
    previous_link=link.with_name('previous')
    switch_report=Path.home()/'.kaardid-setup/rehearsal-switch.txt'
    rollback=rollback_for_deploy(release,Path(previous),previous_link,switch_report)
    created=not release.exists()
    if created:
        with tarfile.open(archive) as bundle:
            # Reject unrelated top-level paths before extracting as the deployment user.
            if any(p.name!=commit and not p.name.startswith(commit+'/') for p in bundle):
                raise SystemExit('Unexpected archive root.')
            bundle.extractall(release.parent,filter='data')
        group=grp.getgrnam('kaardid-code').gr_gid
        for path in [release,*release.rglob('*')]:
            if path.is_symlink():continue
            os.chown(path,-1,group)
            path.chmod(0o2750 if path.is_dir() else (0o750 if path.stat().st_mode&0o111 else 0o640))
    app=release/'apps/kaardid'
    for name,target in {'assets':'assets','upload':'upload','protected/runtime':'runtime',
                        'protected/config/private':'config'}.items():
        path=app/name
        expected='/srv/kaardid/shared/'+target
        if path.is_symlink():
            if os.readlink(path)!=expected:raise SystemExit('Unexpected shared-data link: '+name)
        else:
            path.rmdir()
            path.symlink_to(expected,target_is_directory=True)
    with tarfile.open(archive) as bundle:
        for entry in bundle:
            if not entry.isfile():continue
            path=release.parent/entry.name
            if (path.is_symlink() or not path.is_file() or
                hashlib.file_digest(bundle.extractfile(entry),'sha256').digest()!=hashlib.file_digest(path.open('rb'),'sha256').digest()):
                raise SystemExit('Staged file differs from artifact: '+entry.name)
    group=grp.getgrnam('kaardid-code').gr_gid
    for path in [release,*release.rglob('*')]:
        if path.is_symlink():continue
        st=path.stat()
        if st.st_uid!=os.geteuid() or st.st_gid!=group or st.st_mode&0o022:
            raise SystemExit('Unsafe release ownership/permissions: '+str(path))
    identity=json.loads((release/'release.json').read_text())
    if identity.get('commit')!=commit or identity.get('purpose')!='private-rehearsal':
        raise SystemExit('Staged release identity mismatch.')
    print('Artifact contents and restricted release permissions verified.',flush=True)
    report=deploy_with_maintenance(release,link,rollback,stage,
        Path.home()/'.config/kaardid/migration-db.json')
    output='\n'.join(report)+'\n'
    (stage/'deployment-report.txt').write_text(output)
    switch_report.write_text(output)
    print(output,end='')


if __name__ == '__main__':
    for signum in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(signum, interrupted)
    main()
