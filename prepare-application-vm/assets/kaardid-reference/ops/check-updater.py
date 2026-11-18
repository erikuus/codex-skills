#!/usr/bin/env python3
"""Restore a rehearsal snapshot into a temporary VM cluster; never use a live DB."""
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess
import sys
import time


def main():
    os.umask(0o077)
    if (pwd.getpwuid(os.geteuid()).pw_name != 'erik'
            or subprocess.check_output(['hostname','-f'],text=True).strip() != 'kaardid.arhiiv.ee'):
        raise SystemExit('Run as erik on the Kaardid VM only.')
    root = Path(__file__).resolve().parent.parent
    if root.parent != Path.home()/'.kaardid-setup' or not root.name.startswith('updater-check.'):
        raise SystemExit('Run from the private updater-check staging directory.')
    pg = Path('/usr/lib/postgresql/17/bin')
    app = (Path('/srv/kaardid/rehearsal')/'apps/kaardid').resolve()
    sandbox = root/'sandbox'
    runtime = sandbox/'shared/runtime';runtime.mkdir(parents=True)
    socket = root/'socket';socket.mkdir()
    data = root/'pgdata'
    report = {'checkedAt':datetime.now(timezone.utc).isoformat(),
              'source':'rehearsal dump; not a production snapshot',
              'checkpointSource':'synthetic one-hour interval in the disposable runtime',
              'sourceRelease':app.parents[1].name}
    report['updaterSha256'] = hashlib.sha256((root/'protected/commands/UpdateCommand.php').read_bytes()).hexdigest()
    report['deploymentSha256'] = hashlib.sha256((root/'ops/deploy-rehearsal.py').read_bytes()).hexdigest()
    env = {k:v for k,v in os.environ.items() if not k.startswith('PG')}
    env['PATH'] = str(pg)+os.pathsep+env['PATH']
    started = False
    diagnostics = (root/'probe-diagnostics.log').open('w')

    def run(arguments, timeout=600):
        result = subprocess.run(arguments,env=env,stdin=subprocess.DEVNULL,
            stdout=diagnostics,stderr=diagnostics,timeout=timeout)
        if result.returncode:raise RuntimeError('Isolated probe subprocess failed: '+Path(arguments[0]).name)

    def sql(statement):
        run([str(pg/'psql'),'-X','-h',str(socket),'-p','55439','-U','updater_probe_admin',
             '-d','kaart_updater_probe','-v','ON_ERROR_STOP=1','-c',statement])

    def arguments(mode):
        return ['php8.5',str(root/'ops/check-updater.php'),mode,str(app),str(runtime),
                str(socket),str(root/'protected/commands/UpdateCommand.php')]

    def probe(mode):
        result = subprocess.run(arguments(mode),env=env,capture_output=True,text=True,timeout=600)
        diagnostics.write(result.stderr);diagnostics.write(result.stdout);diagnostics.flush()
        try:out=json.loads(result.stdout)
        except ValueError:raise RuntimeError('Isolated PHP probe returned invalid output: '+mode+
                                            '; exit='+str(result.returncode)+'; bytes='+str(len(result.stdout)))
        report[mode] = out
        print(json.dumps({mode:out}),flush=True)
        if result.returncode or not out.get('ok'):raise RuntimeError('Isolated PHP check failed: '+mode)
        return out['result']

    try:
        # The deployment lock prevents retention from removing the selected source dump.
        with (Path.home()/'.kaardid-setup/rehearsal-deploy.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            backups = Path.home()/'.kaardid-setup/rehearsal-backups'
            backup = sorted(backups.glob('*/kaart.dump'))[-1]
            metadata = json.loads((backup.parent/'backup.json').read_text())
            if metadata.get('database') != 'kaart':raise RuntimeError('Unexpected source database.')
            with backup.open('rb') as source:
                if hashlib.file_digest(source,'sha256').hexdigest()!=metadata['sha256']:
                    raise RuntimeError('Source backup checksum mismatch.')
            report['snapshot'] = backup.parent.name
            run([str(pg/'initdb'),'-D',str(data),'-A','trust','-U','updater_probe_admin',
                 '--no-locale','--encoding=UTF8'])
            run([str(pg/'pg_ctl'),'-D',str(data),'-l',str(root/'postgres.log'),
                 '-o',"-h '' -k "+str(socket)+' -p 55439','-w','start'])
            started = True
            run([str(pg/'createdb'),'-h',str(socket),'-p','55439','-U','updater_probe_admin','kaart_updater_probe'])
            run([str(pg/'pg_restore'),'-h',str(socket),'-p','55439','-U','updater_probe_admin',
                 '-d','kaart_updater_probe','--no-owner','--no-privileges','--exit-on-error',str(backup)])
        sql('CREATE ROLE updater_probe_app LOGIN; GRANT CONNECT ON DATABASE kaart_updater_probe TO updater_probe_app; '
            'GRANT USAGE ON SCHEMA public TO updater_probe_app; '
            'GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO updater_probe_app; '
            'GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO updater_probe_app')
        probe('fixture')
        probe('thumbnail-queue')
        checkpoint = runtime/'update.log'
        spec = importlib.util.spec_from_file_location('deployment',root/'ops/deploy-rehearsal.py')
        deployment = importlib.util.module_from_spec(spec);spec.loader.exec_module(deployment)
        with deployment.operation_lock(runtime):
            probe('blocked')
        holder = subprocess.Popen(arguments('hold'),env=env,stdout=subprocess.PIPE,stderr=diagnostics,text=True)
        try:
            deadline = time.monotonic()+15
            while not (runtime/'held').exists() and holder.poll() is None and time.monotonic()<deadline:
                time.sleep(0.05)
            if not (runtime/'held').exists():raise RuntimeError('Updater lock holder did not start.')
            probe('blocked')  # Another updater also cannot enter.
            try:
                deployment.deploy_with_maintenance(root/'unused',sandbox/'rehearsal',root/'unused',root/'unused',root/'unused')
            except RuntimeError as error:
                if 'no deployment work was started' not in str(error):raise
            else:raise RuntimeError('Deployment entered while updater held its lock.')
            if (sandbox/'shared/config/.maintenance').exists():raise RuntimeError('Blocked deployment touched maintenance.')
            report['overlap'] = {'deploymentBlocksUpdater':True,'updaterBlocksDeployment':True,'updaterBlocksUpdater':True}
        finally:
            (runtime/'release').touch()
            holder.communicate(timeout=25)
            if holder.returncode:raise RuntimeError('Lock holder did not exit successfully.')
        with deployment.operation_lock(runtime):pass
        external = probe('external')
        if external['dgs'] and external['soap']:
            checkpoint.write_text(str(int(time.time())-3600))
            probe('live')
            report['liveStatus'] = 'passed'
        else:report['liveStatus'] = 'blocked by external service checks'
        run(['python3',str(root/'ops/test_updater_status.py')])
        report['updaterStatusChecks'] = 'passed'
        report['isolatedChecks'] = 'passed'
    except BaseException as error:
        report['failure'] = str(error)
        raise
    finally:
        if started or (data/'postmaster.pid').exists():
            run([str(pg/'pg_ctl'),'-D',str(data),'-m','immediate','-w','stop'],timeout=30)
        diagnostics.close()
        for path in (data,socket,sandbox):
            if path.exists():shutil.rmtree(path)
        report['temporaryClusterRemoved'] = not data.exists()
        (root/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print('Private summary: '+str(root/'report.json'),flush=True)


if __name__ == '__main__':
    main()
