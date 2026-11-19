#!/usr/bin/env python3
"""Restore the agreed private snapshot into the prepared, otherwise empty kaart DB."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

os.umask(0o077)
if len(sys.argv) != 2:
    raise SystemExit('Usage: restore-rehearsal.py <private snapshot directory>')
bundle = Path(sys.argv[1]).resolve()
manifest = json.loads((bundle / 'manifest.json').read_text())
if manifest.get('purpose') != 'private-rehearsal' or manifest['source']['database'] != 'kaart_dev':
    raise SystemExit('Unexpected snapshot identity; refusing import.')
if manifest.get('custom_spatial_reference_rows') != 0:
    raise SystemExit('Custom spatial reference data requires a separately reviewed import; refusing to omit it.')
dump = bundle / 'kaart_dev.dump'
with dump.open('rb') as stream:
    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
if digest != manifest['dump_sha256']:
    raise SystemExit('Snapshot checksum mismatch; refusing import.')

credentials = json.loads((Path.home() / '.config/kaardid/migration-db.json').read_text())
if (credentials.get('host'), credentials.get('port'), credentials.get('database'), credentials.get('user'), credentials.get('role')) != ('127.0.0.1', 5432, 'kaart', 'kaart_migrate', 'kaart_owner'):
    raise SystemExit('Unexpected migration target; refusing import.')
descriptor, pass_path = tempfile.mkstemp(prefix='kaardid-restore-pgpass-')
def escape(value):
    return str(value).replace('\\', '\\\\').replace(':', '\\:')
with os.fdopen(descriptor, 'w') as stream:
    stream.write(':'.join(map(escape, ['127.0.0.1', 5432, 'kaart', 'kaart_migrate', credentials['password']])) + '\n')
environment = {key: value for key, value in os.environ.items() if not key.startswith('PG')}
environment.update(PGPASSFILE=pass_path, PGCONNECT_TIMEOUT='10', PGAPPNAME='kaardid-private-rehearsal', LC_ALL='C.UTF-8')
connection = ['--host=127.0.0.1', '--port=5432', '--username=kaart_migrate', '--dbname=kaart', '--no-password']
psql = ['/usr/lib/postgresql/17/bin/psql', '-X', '-Atq', '--set=ON_ERROR_STOP=1'] + connection
state_file = bundle / 'restore-state.json'

def sql(statement):
    result = subprocess.run(psql, input='SET ROLE kaart_owner;\n' + statement, env=environment, text=True, capture_output=True)
    if result.returncode:
        raise SystemExit('Database verification/setup failed. No credential values are printed.')
    return result.stdout.strip()

try:
    if sql('SELECT current_database();') != 'kaart':
        raise SystemExit('Wrong target database.')
    table_count = int(sql("SELECT count(*) FROM pg_tables WHERE schemaname IN ('public','au') AND tablename <> 'spatial_ref_sys';"))
    state = json.loads(state_file.read_text()) if state_file.exists() else {}
    if state and state.get('dump_sha256') != digest:
        raise SystemExit('A different snapshot has already been restored; refusing replacement.')
    if not state:
        if table_count:
            raise SystemExit('Target contains application tables; refusing to overwrite them.')
        backup = bundle / 'kaart-empty-before-rehearsal.dump'
        with (bundle / 'target-backup.log').open('w') as log:
            result = subprocess.run(['/usr/lib/postgresql/17/bin/pg_dump', '--format=custom', '--no-owner', '--no-acl',
                '--exclude-table-data=public.spatial_ref_sys', '--file=' + str(backup)] + connection,
                env=environment, stdout=log, stderr=log)
        if result.returncode:
            raise SystemExit('Empty-target backup failed; no restore attempted.')

        inventory = subprocess.run(['/usr/lib/postgresql/17/bin/pg_restore', '--list', str(dump)],
                                   capture_output=True, text=True, check=True).stdout
        # public already exists and belongs to kaart_owner. The source PostGIS
        # configuration table has zero custom rows; keep target extension defaults.
        excluded = [r'\bSCHEMA - public\b', r'\bTABLE DATA public spatial_ref_sys\b']
        if {'schema': 'public', 'name': 'histogram2d'} in manifest.get('unused_legacy_shell_types', []):
            # A pre-PostGIS-upgrade shell with typisdefined=false and no dependents,
            # verified at the source; it cannot hold data or implement app behavior.
            excluded.append(r'\bTYPE public histogram2d\b')
        if {'schema': 'public', 'name': 'gist_geometry_ops'} in manifest.get('unused_legacy_gist_aliases', []):
            # No indexes, external catalog dependents or stored function-text
            # references use this obsolete alias. Current PostGIS's default
            # gist_geometry_ops_2d continues to build the application's GiST index.
            excluded.append(r'\bOPERATOR (?:FAMILY|CLASS) public gist_geometry_ops\b')
        selected = []
        skipped = []
        for line in inventory.splitlines():
            if not line.startswith(';') and any(re.search(pattern, line) for pattern in excluded):
                skipped.append(line)
                selected.append('; skipped for prepared target: ' + line)
            else:
                selected.append(line)
        selection = bundle / 'restore-selected.list'
        selection.write_text('\n'.join(selected) + '\n')
        with (bundle / 'pg_restore.log').open('w') as log:
            result = subprocess.run(['/usr/lib/postgresql/17/bin/pg_restore', '--single-transaction', '--exit-on-error',
                '--no-owner', '--no-acl', '--no-tablespaces', '--role=kaart_owner', '--use-list=' + str(selection)]
                + connection + [str(dump)], env=environment, stdout=log, stderr=log)
        if result.returncode:
            raise SystemExit('Transactional restore failed and rolled back. Inspect the private pg_restore.log.')
        state = {'dump_sha256': digest, 'phase': 'restored', 'skipped_toc_entries': skipped}
        state_file.write_text(json.dumps(state, indent=2) + '\n')

    # The owner grants permissions only on its own imported tables. PostGIS
    # extension tables stay read-only to the app and the personal inspection role.
    sql(r'''
BEGIN;
GRANT USAGE ON SCHEMA public, au TO kaart_app, kaart_readonly;
SELECT format('GRANT SELECT ON TABLE %I.%I TO kaart_readonly, kaart_app', n.nspname, c.relname)
FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname IN ('public','au') AND c.relkind IN ('r','p','v','m','f') AND c.relowner=current_user::regrole
\gexec
SELECT format('GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE %I.%I TO kaart_app', n.nspname, c.relname)
FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname IN ('public','au') AND c.relkind IN ('r','p','v') AND c.relowner=current_user::regrole
\gexec
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public, au TO kaart_app;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_owner IN SCHEMA au GRANT SELECT ON TABLES TO kaart_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_owner IN SCHEMA au GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO kaart_app;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_owner IN SCHEMA au GRANT USAGE, SELECT ON SEQUENCES TO kaart_app;
COMMIT;
''')
    verified = []
    for table in manifest['tables']:
        if not re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', table['schema']) or not re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', table['name']):
            raise SystemExit('Unexpected manifest identifier.')
        rows = int(sql('SELECT count(*) FROM "' + table['schema'] + '"."' + table['name'] + '";'))
        if rows != table['rows']:
            raise SystemExit('Row count mismatch for ' + table['schema'] + '.' + table['name'])
        verified.append(dict(table, restored_rows=rows))
    state.update(phase='verified', verified_tables=verified)
    state_file.write_text(json.dumps(state, indent=2) + '\n')
    print(json.dumps({'status': 'verified', 'target': 'kaart', 'source': 'local kaart_dev private rehearsal',
        'verified_tables': len(verified), 'kaart_rows': next(t['rows'] for t in verified if t['schema']=='public' and t['name']=='kaart'),
        'session_rows': 0, 'dump_sha256': digest}, indent=2))
finally:
    os.unlink(pass_path)
