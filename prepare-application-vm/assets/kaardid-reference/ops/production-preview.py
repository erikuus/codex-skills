#!/usr/bin/env python3
"""Seed an empty production database from rehearsal and publish a VPN-only preview.

Run through bin/production-preview in the operator's Terminal. This never sets
the production current pointer, copies an updater checkpoint or runs migrations.
"""
from contextlib import ExitStack, contextmanager
from datetime import datetime, timezone
import fcntl
import grp
import hashlib
import http.client
import json
import os
from pathlib import Path
import pwd
import re
import stat
import subprocess
import sys
import tempfile


class Database:
    def __init__(self, bindir, prefix, connection):
        self.bindir, self.prefix, self.connection = Path(bindir), prefix, connection

    def command(self, tool, database, *arguments):
        return [*self.prefix, str(self.bindir/tool), *self.connection,
                '--dbname='+database, *arguments]

    def sql(self, database, statement):
        result = subprocess.run(self.command('psql', database, '-XAtq', '-v', 'ON_ERROR_STOP=1'),
                                input=statement, text=True, capture_output=True, timeout=120)
        if result.returncode:
            raise RuntimeError('Database check failed; database diagnostics omitted.')
        return result.stdout.strip()

    def run(self, tool, database, arguments, log, *, source=None, output=None):
        result = subprocess.run(self.command(tool, database, *arguments), stdout=output or log, stderr=log,
                                stdin=source or subprocess.DEVNULL, timeout=1800)
        if result.returncode:
            raise RuntimeError(tool+' failed; inspect the private setup diagnostics.')


def identifier(value):
    if not re.fullmatch('[A-Za-z_][A-Za-z0-9_]*',value):
        raise ValueError('Unexpected schema/table identifier; review the source before copying.')
    return '"'+value.replace('"', '""')+'"'


def application_tables(db, database):
    return json.loads(db.sql(database, """SELECT coalesce(json_agg(json_build_array(n.nspname,c.relname)
        ORDER BY n.nspname,c.relname),'[]') FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
        WHERE n.nspname IN ('public','au') AND c.relkind IN ('r','p') AND NOT EXISTS
        (SELECT 1 FROM pg_depend d WHERE d.classid='pg_class'::regclass AND d.objid=c.oid AND d.deptype='e');"""))


def seed_database(db, directory):
    """Only an empty target is eligible. Export/count/dump share one snapshot."""
    if application_tables(db, 'kaart_prod'):
        raise ValueError('Production has application tables; refusing to replace data.')
    if db.sql('kaart_prod', 'SELECT pg_get_userbyid(datdba) FROM pg_database WHERE datname=current_database();') != 'kaart_prod_owner':
        raise ValueError('Unexpected target database owner.')
    directory.mkdir(mode=0o700)
    with (directory/'database.log').open('x') as log:
        with (directory/'empty-target.dump').open('xb') as output:
            db.run('pg_dump', 'kaart_prod', ['--format=custom', '--no-owner', '--no-acl'],log,output=output)
        process = subprocess.Popen(db.command('psql', 'kaart', '-XAtq', '-v', 'ON_ERROR_STOP=1'),
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log, text=True)
        def query(statement):
            process.stdin.write(statement+'\n'); process.stdin.flush()
            line = process.stdout.readline()
            if not line:
                raise RuntimeError('Source snapshot query failed; no import attempted.')
            return line.strip()
        try:
            snapshot = query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY; SELECT pg_export_snapshot();')
            condition = query("SELECT coalesce(replace(replace(extcondition[1],chr(10),' '),chr(13),' '),'') FROM pg_extension WHERE extname='postgis';")
            if not condition or int(query('SELECT count(*) FROM public.spatial_ref_sys '+condition+';')):
                raise ValueError('Custom spatial reference data needs a reviewed restore.')
            tables = application_tables(db, 'kaart')
            counts = []
            for schema, name in tables:
                count = 0 if (schema,name)==('public','tbl_session') else int(query(
                    'SELECT count(*) FROM '+identifier(schema)+'.'+identifier(name)+';'))
                counts.append([schema,name,count])
            with (directory/'rehearsal.dump').open('xb') as output:
                db.run('pg_dump', 'kaart', ['--format=custom', '--no-owner', '--no-acl',
                       '--schema=public', '--schema=au', '--exclude-table-data=public.tbl_session',
                       '--exclude-table-data=public.spatial_ref_sys', '--snapshot='+snapshot],log,output=output)
        finally:
            if process.poll() is None:
                try: process.stdin.write('ROLLBACK;\n'); process.stdin.flush()
                except BrokenPipeError: pass
            try: process.communicate(timeout=10)
            except subprocess.TimeoutExpired: process.kill(); process.communicate()
        dump = directory/'rehearsal.dump'
        inventory = subprocess.run([str(db.bindir/'pg_restore'), '--list', str(dump)],
                                   text=True, capture_output=True, check=True).stdout
        selected = directory/'restore.list'
        selected.write_text('\n'.join(line for line in inventory.splitlines()
            if not re.search(r'\bSCHEMA - public\b|\bTABLE DATA public spatial_ref_sys\b|\b(?:COMMENT - )?EXTENSION\b',line))+'\n')
        # The entire schema, data and grants commit together. Failure rolls back.
        grants = r'''
GRANT USAGE ON SCHEMA public, au TO kaart_prod_app, kaart_prod_readonly;
SELECT format('GRANT SELECT ON TABLE %I.%I TO kaart_prod_readonly',n.nspname,c.relname)
FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname IN ('public','au') AND c.relkind IN ('r','p','v','m','f') AND c.relowner=current_user::regrole
\gexec
SELECT format('GRANT SELECT,INSERT,UPDATE,DELETE ON TABLE %I.%I TO kaart_prod_app',n.nspname,c.relname)
FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname IN ('public','au') AND c.relkind IN ('r','p','v') AND c.relowner=current_user::regrole
\gexec
GRANT USAGE,SELECT ON ALL SEQUENCES IN SCHEMA public, au TO kaart_prod_app;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_prod_owner IN SCHEMA au GRANT SELECT ON TABLES TO kaart_prod_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_prod_owner IN SCHEMA au GRANT SELECT,INSERT,UPDATE,DELETE ON TABLES TO kaart_prod_app;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_prod_owner IN SCHEMA au GRANT USAGE,SELECT ON SEQUENCES TO kaart_prod_app;
'''
        checks = []
        for schema,name,count in counts:
            table=identifier(schema)+'.'+identifier(name)
            checks.append("DO $check$ BEGIN IF (SELECT count(*) FROM "+table+") <> "+str(count)+
                          " THEN RAISE EXCEPTION 'Restored row count mismatch'; END IF; END $check$;")
        # psql's SQL stream is private on disk; never emit dump data in reports.
        sql_file=directory/'restore.sql'
        with sql_file.open('x') as output:
            output.write('BEGIN;\nSET LOCAL ROLE kaart_prod_owner;\n');output.flush()
            subprocess.run([str(db.bindir/'pg_restore'),'--no-owner','--no-acl','--no-tablespaces',
                            '--use-list='+str(selected),'--file=-',str(dump)],stdout=output,stderr=log,check=True)
            output.write('\n'+grants+'\n'+'\n'.join(checks)+'\nCOMMIT;\n')
        with sql_file.open() as source:
            db.run('psql','kaart_prod',['-Xq','-v','ON_ERROR_STOP=1'],log,source=source)
        sql_file.unlink()
        with dump.open('rb') as source:
            checksum=hashlib.file_digest(source,'sha256').hexdigest()
        return {'source':'kaart (rehearsal test data)', 'target':'kaart_prod', 'tables':len(counts),
                'sessionRowsCopied':0, 'dumpSha256':checksum}


@contextmanager
def operations_lock(root, account):
    path=root/'shared/runtime/operations.lock'
    descriptor=os.open(path,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o660)
    try:
        info=os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o007:
            raise ValueError('Unsafe operations lock.')
        if info.st_uid==0:
            os.fchown(descriptor,pwd.getpwnam('erik').pw_uid,grp.getgrnam(account).gr_gid)
            os.fchmod(descriptor,0o660)
        fcntl.flock(descriptor,fcntl.LOCK_EX|fcntl.LOCK_NB)
        yield
    finally: os.close(descriptor)


def prepare_locked_release(tooling, rehearsal, production, stages, sha, code_group, prefix):
    """Prepare as the code owner while the parent holds both operations locks.

    The standalone promotion CLI takes its own rehearsal lock. Calling its
    unlocked preparation function here preserves the parent's continuous locks
    through preparation, source snapshot and preview install without relocking
    the same file in a child process.
    """
    code = '''import importlib.util,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('promotion',sys.argv[1])
promotion=importlib.util.module_from_spec(spec);spec.loader.exec_module(promotion)
promotion.prepare(Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
'''
    subprocess.run([*prefix,sys.executable,'-B','-c',code,str(tooling/'promote-production.py'),
                    str(rehearsal),str(production),str(stages),sha,str(code_group)],check=True)


def health():
    def request(path):
        connection=http.client.HTTPConnection('127.0.0.1',18082,timeout=30)
        try:
            connection.request('GET',path,headers={'Host':'kaardid.arhiiv.ee'})
            response=connection.getresponse();body=response.read()
            if response.getheader('X-Kaardid-Data')!='rehearsal-copy':
                raise RuntimeError('Wrong preview backend.')
            return response.status,body
        finally: connection.close()
    status,body=request('/')
    if status!=200 or b'VPN preview' not in body:
        raise RuntimeError('Preview home/banner check failed.')
    assets=set(re.findall(rb'/assets/[a-zA-Z0-9_./-]+\.(?:css|js)',body))
    if not assets: raise RuntimeError('No published assets.')
    for path in [asset.decode() for asset in assets]+['/index.php/map/search']:
        if request(path)[0]!=200: raise RuntimeError('Preview route/asset check failed: '+path)
    for path in ['/protected/config/production.php','/index-dev.php','/index.php/test/login','/cron.php']:
        if request(path)[0]!=404: raise RuntimeError('Preview restriction failed: '+path)


def install_site(template, release):
    site=Path('/etc/nginx/sites-available/kaardid-production-preview')
    enabled=Path('/etc/nginx/sites-enabled/kaardid-production-preview')
    link=Path('/srv/kaardid-production/preview')
    for path in (site,enabled,link):
        if path.exists() or path.is_symlink():
            raise ValueError('Preview already exists; inspect it instead of replacing it: '+str(path))
    try:
        link.symlink_to(release)
        site.write_bytes(template.read_bytes());site.chmod(0o644)
        enabled.symlink_to(site)
        subprocess.run(['nginx','-t'],check=True)
        subprocess.run(['systemctl','reload','nginx'],check=True)
        health()
    except BaseException:
        enabled.unlink(missing_ok=True);site.unlink(missing_ok=True);link.unlink(missing_ok=True)
        subprocess.run(['nginx','-t'],check=True)
        subprocess.run(['systemctl','reload','nginx'],check=True)
        raise


def main():
    os.umask(0o077)
    if (os.geteuid()!=0 or os.environ.get('SUDO_USER')!='erik' or len(sys.argv)!=2
            or not re.fullmatch('[a-f0-9]{40}',sys.argv[1])
            or subprocess.check_output(['hostname','-f'],text=True).strip()!='kaardid.arhiiv.ee'):
        raise ValueError('Use bin/production-preview in your own Terminal on the Kaardid VM.')
    sha=sys.argv[1];root=Path('/srv/kaardid-production');tooling=Path(__file__).resolve().parent
    if (root/'current').exists() or (root/'current').is_symlink():
        raise ValueError('Production is activated; refusing preview setup.')
    for unit in ('kaardid-update.timer','kaardid-update.service'):
        state=subprocess.check_output(['systemctl','show',unit,'--property=LoadState','--value'],text=True).strip()
        if state!='not-found': raise ValueError('Updater unit exists; review before preview setup.')
    if not Path('/run/php/php8.5-fpm-kaardid-production.sock').is_socket():
        raise ValueError('Production FPM socket is missing.')
    with ExitStack() as stack:
        stack.enter_context(operations_lock(Path('/srv/kaardid'),'kaardid'))
        stack.enter_context(operations_lock(root,'kaardid-production'))
        prepare_locked_release(tooling,Path('/srv/kaardid'),root,Path('/home/erik/.kaardid-setup'),sha,
                               grp.getgrnam('kaardid-production-code').gr_gid,['runuser','-u','erik','--'])
        release=root/'releases'/sha
        check=(tooling/'check-production-config.php').read_text().removeprefix('<?php')
        subprocess.run(['runuser','-u','kaardid-production','--','php8.5','-r',check,
                        str(release/'apps/kaardid'),'web'],check=True)
        receipt=Path('/var/backups/kaardid-production/vpn-preview-seed.json')
        if receipt.exists():
            data=json.loads(receipt.read_text())
            if data.get('release')!=sha: raise ValueError('A different preview seed already exists.')
        else:
            directory=Path('/var/backups/kaardid-production')/('vpn-preview-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
            db=Database('/usr/lib/postgresql/17/bin',['runuser','-u','postgres','--'],
                        ['--host=/var/run/postgresql','--port=5432','--username=postgres','--no-password'])
            data=seed_database(db,directory)
            data.update(release=sha,seededAt=datetime.now(timezone.utc).isoformat())
            receipt.write_text(json.dumps(data,indent=2)+'\n')
        source=Path('/srv/kaardid/shared/upload');target=root/'shared/upload'
        if any(p.is_symlink() for p in source.rglob('*')):
            raise ValueError('Unexpected source upload symlink; refusing media copy.')
        subprocess.run(['rsync','-rt','--ignore-existing','--chown=kaardid-production:kaardid-production-code',
                        '--chmod=D2750,F0640',str(source)+'/',str(target)+'/'],check=True)
        install_site(tooling/'kaardid-production-preview.conf',release)
    print('KAARDID_PRODUCTION_VPN_PREVIEW_COMPLETE')
    print('http://kaardid.arhiiv.ee — rehearsal test data, separate kaart_prod database.')
    print('Production current, live-server jobs, updater checkpoint and readiness confirmations unchanged.')


if __name__=='__main__':
    try: main()
    except (ValueError,RuntimeError,OSError,subprocess.SubprocessError) as error:
        print('VPN preview setup stopped: '+str(error),file=sys.stderr);sys.exit(1)
