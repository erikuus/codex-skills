#!/usr/bin/env bash
# Initial private-VM foundation. Does not deploy code, import data or switch nginx.
set -euo pipefail
umask 077

if [[ $EUID -ne 0 || $(hostname -f) != kaardid.arhiiv.ee ]]; then
    echo 'Run with sudo on kaardid.arhiiv.ee only.' >&2
    exit 1
fi
if [[ ${SUDO_USER:-} != erik ]]; then
    echo 'Expected sudo invoked by the verified deployment account erik.' >&2
    exit 1
fi

echo 'Installing missing PHP image/SOAP and PostgreSQL PostGIS support.'
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=l
apt-get update
apt-get install -y --no-install-recommends php8.5-soap php8.5-gd \
    postgresql-17-postgis-3 postgresql-17-postgis-3-scripts

if ! getent passwd kaardid >/dev/null; then
    useradd --system --user-group --home-dir /srv/kaardid --no-create-home \
        --shell /usr/sbin/nologin kaardid
fi
if [[ $(getent passwd kaardid | cut -d: -f7) != /usr/sbin/nologin ]]; then
    echo 'Existing kaardid system account differs from the expected service account.' >&2
    exit 1
fi
usermod -a -G kaardid erik
if ! getent group kaardid-code >/dev/null; then
    groupadd --system kaardid-code
fi
usermod -a -G kaardid-code erik
usermod -a -G kaardid-code kaardid
usermod -a -G kaardid-code www-data
install -d -o erik -g kaardid-code -m 2750 /srv/kaardid /srv/kaardid/releases /srv/kaardid/shared
install -d -o erik -g kaardid -m 2750 /srv/kaardid/shared/config
install -d -o kaardid -g kaardid -m 2770 /srv/kaardid/shared/runtime
install -d -o kaardid -g kaardid-code -m 2750 /srv/kaardid/shared/assets /srv/kaardid/shared/upload
install -d -o kaardid -g kaardid -m 0700 /srv/kaardid/shared/runtime/tmp \
    /srv/kaardid/shared/runtime/sessions
install -d -o root -g root -m 0700 /var/backups/kaardid
install -d -o root -g kaardid -m 0750 /etc/kaardid
install -d -o erik -g erik -m 0700 /home/erik/.config /home/erik/.config/kaardid

echo 'Preparing an empty kaart database and separate owner, migration, app and read-only roles.'
# All generated secrets stay in protected server files. SQL receives SCRAM verifiers,
# never raw passwords. Errors are summarized rather than printing secret-bearing SQL.
python3 - <<'PY'
import base64
import grp
import hashlib
import hmac
import json
import os
from pathlib import Path
import pwd
import secrets
import subprocess

PSQL = ['runuser', '-u', 'postgres', '--', '/usr/lib/postgresql/17/bin/psql',
        '-X', '--no-password', '-h', '/var/run/postgresql', '-p', '5432',
        '-U', 'postgres', '--set=ON_ERROR_STOP=1', '-Atq']

def sql(statement, database='postgres'):
    result = subprocess.run(PSQL + ['--dbname=' + database], input=statement,
                            text=True, capture_output=True)
    if result.returncode:
        raise SystemExit('Database preparation failed; inspect PostgreSQL logs privately. No passwords are printed.')
    return result.stdout.strip()

def write_json(path, value, owner, group, mode):
    path = Path(path)
    temp = path.with_name(path.name + '.new')
    descriptor = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as output:
        json.dump(value, output, indent=2)
        output.write('\n')
    os.chown(temp, pwd.getpwnam(owner).pw_uid, grp.getgrnam(group).gr_gid)
    os.chmod(temp, mode)
    os.replace(temp, path)

def verifier(password):
    salt = secrets.token_bytes(16)
    salted = hashlib.pbkdf2_hmac('sha256', password.encode('ascii'), salt, 4096)
    client_key = hmac.new(salted, b'Client Key', hashlib.sha256).digest()
    stored_key = hashlib.sha256(client_key).digest()
    server_key = hmac.new(salted, b'Server Key', hashlib.sha256).digest()
    encoded = lambda value: base64.b64encode(value).decode('ascii')
    return 'SCRAM-SHA-256$4096:' + encoded(salt) + '$' + encoded(stored_key) + ':' + encoded(server_key)

names = ['kaart_owner', 'kaart_migrate', 'kaart_app', 'kaart_readonly', 'erik']
existing = set(sql("SELECT rolname FROM pg_roles WHERE rolname IN ('kaart_owner', 'kaart_migrate', 'kaart_app', 'kaart_readonly', 'erik');").splitlines())
database_exists = sql("SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname='kaart');") == 't'
state_path = Path('/etc/kaardid/bootstrap-secrets.json')
if state_path.exists():
    state = json.loads(state_path.read_text())
    if state.get('managed_roles') != names:
        raise SystemExit('Unexpected existing bootstrap state; no database changes made.')
else:
    if existing or database_exists:
        raise SystemExit('Kaardid database/roles already exist without bootstrap state; refusing to take them over.')
    state = {'managed_roles': names, 'app_password': secrets.token_urlsafe(36),
             'migration_password': secrets.token_urlsafe(36)}
    write_json(state_path, state, 'root', 'root', 0o600)

statements = ['BEGIN;']
for name in names:
    if name not in existing:
        statements.append('CREATE ROLE ' + name + ';')
    login = 'LOGIN' if name in ('kaart_app', 'kaart_migrate', 'erik') else 'NOLOGIN'
    statements.append('ALTER ROLE ' + name + ' ' + login + ' INHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;')
for name, field in [('kaart_app', 'app_password'), ('kaart_migrate', 'migration_password')]:
    statements.append("ALTER ROLE " + name + " PASSWORD '" + verifier(state[field]) + "';")
statements += ['GRANT kaart_owner TO kaart_migrate;', 'GRANT kaart_readonly TO erik;', 'COMMIT;']
sql('\n'.join(statements))
if not database_exists:
    sql("CREATE DATABASE kaart OWNER kaart_owner TEMPLATE template0 ENCODING 'UTF8';")
if sql("SELECT pg_get_userbyid(datdba) FROM pg_database WHERE datname='kaart';") != 'kaart_owner':
    raise SystemExit('Unexpected kaart database owner; no schema changes made.')

sql('''
BEGIN;
REVOKE ALL ON DATABASE kaart FROM PUBLIC;
GRANT CONNECT ON DATABASE kaart TO kaart_migrate, kaart_app, kaart_readonly;
ALTER SCHEMA public OWNER TO kaart_owner;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO kaart_app, kaart_readonly;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS tablefunc;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO kaart_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO kaart_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO kaart_app;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_owner IN SCHEMA public GRANT SELECT ON TABLES TO kaart_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_owner IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO kaart_app;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_owner IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO kaart_app;
COMMIT;
''', 'kaart')

# Real role/permission checks; every probe object and row is rolled back.
sql('''
BEGIN;
SET ROLE kaart_owner;
CREATE TABLE public.__kaardid_privilege_probe (id serial PRIMARY KEY, value text);
RESET ROLE;
SET ROLE kaart_app;
INSERT INTO public.__kaardid_privilege_probe (value) VALUES ('probe');
UPDATE public.__kaardid_privilege_probe SET value='updated';
DO $$ BEGIN
  IF has_schema_privilege(current_user, 'public', 'CREATE') THEN
    RAISE EXCEPTION 'Application role unexpectedly has schema CREATE';
  END IF;
END $$;
RESET ROLE;
SET ROLE erik;
SELECT count(*) FROM public.__kaardid_privilege_probe;
DO $$ BEGIN
  IF has_table_privilege(current_user, 'public.__kaardid_privilege_probe', 'INSERT') OR
     has_schema_privilege(current_user, 'public', 'CREATE') THEN
    RAISE EXCEPTION 'Read-only role has unexpected write privileges';
  END IF;
END $$;
RESET ROLE;
ROLLBACK;
''', 'kaart')

base = {'host': '127.0.0.1', 'port': 5432, 'database': 'kaart'}
write_json('/etc/kaardid/app-db.json', dict(base, user='kaart_app', password=state['app_password']),
           'root', 'kaardid', 0o640)
write_json('/home/erik/.config/kaardid/migration-db.json',
           dict(base, user='kaart_migrate', password=state['migration_password'], role='kaart_owner'),
           'erik', 'erik', 0o600)
print('Database roles and transactional privilege checks passed. Credentials saved privately on the VM.')
PY

fpm_config=/etc/php/8.5/fpm/pool.d/kaardid.conf
if [[ -e "$fpm_config" ]] && ! head -1 "$fpm_config" | grep -qx '; Managed by Kaardid server-prepare'; then
    echo 'An unmanaged Kaardid PHP-FPM pool exists; refusing to overwrite it.' >&2
    exit 1
fi
fpm_backup=$(mktemp /etc/php/8.5/fpm/pool.d/.kaardid-backup.XXXXXX)
fpm_existed=false
if [[ -e "$fpm_config" ]]; then
    cp -p "$fpm_config" "$fpm_backup"
    fpm_existed=true
fi
restore_pool() {
    if "$fpm_existed"; then
        cp -p "$fpm_backup" "$fpm_config"
    else
        rm -f "$fpm_config"
    fi
    rm -f "$fpm_backup"
}
cat > "$fpm_config" <<'FPM'
; Managed by Kaardid server-prepare
[kaardid]
user = kaardid
group = kaardid
listen = /run/php/php8.5-fpm-kaardid.sock
listen.owner = www-data
listen.group = www-data
listen.mode = 0660
pm = ondemand
pm.max_children = 8
pm.process_idle_timeout = 10s
pm.max_requests = 500
clear_env = yes
catch_workers_output = yes
security.limit_extensions = .php
env[SENTRY_ENVIRONMENT] = staging
php_admin_flag[display_errors] = off
php_admin_flag[log_errors] = on
php_admin_value[upload_tmp_dir] = /srv/kaardid/shared/runtime/tmp
php_admin_value[session.save_path] = /srv/kaardid/shared/runtime/sessions
FPM
chmod 0644 "$fpm_config"
if ! /usr/sbin/php-fpm8.5 --test; then
    restore_pool
    echo 'PHP-FPM validation failed; previous pool configuration restored.' >&2
    exit 1
fi
if ! systemctl reload php8.5-fpm; then
    restore_pool
    systemctl reload php8.5-fpm || true
    echo 'PHP-FPM reload failed; previous pool configuration restored.' >&2
    exit 1
fi
rm -f "$fpm_backup"

psql_postgres=(runuser -u postgres -- /usr/lib/postgresql/17/bin/psql -X --no-password
    -h /var/run/postgresql -p 5432 -U postgres --dbname=postgres --set=ON_ERROR_STOP=1)
if [[ $("${psql_postgres[@]}" -Atqc "SELECT rolpassword IS NOT NULL FROM pg_authid WHERE rolname='erik';") != t ]]; then
    echo 'Choose a separate PostgreSQL password for erik and save it in your password manager.'
    echo 'The following password prompts are for desktop/managed pgAdmin, not sudo.'
    "${psql_postgres[@]}" -c '\password erik'
    if [[ $("${psql_postgres[@]}" -Atqc "SELECT rolpassword IS NOT NULL FROM pg_authid WHERE rolname='erik';") != t ]]; then
        echo 'No database password was set. Rerun this preparation to finish.' >&2
        exit 1
    fi
fi

# The personal CLI uses Unix peer authentication over the existing SSH connection.
runuser -u erik -- /usr/lib/postgresql/17/bin/psql -X --no-password --dbname=kaart \
    --set=ON_ERROR_STOP=1 -c 'SELECT current_user, current_database();'
runuser -u erik -- /bin/bash --noprofile --norc -c 'test -r "$1"' kaardid-permission-check /home/erik/.config/kaardid/migration-db.json
php -r 'if (!extension_loaded("soap") || !extension_loaded("gd") || !extension_loaded("pdo_pgsql")) { exit(1); } echo "PHP runtime extensions verified.\n";'
test -S /run/php/php8.5-fpm-kaardid.sock
nginx -t
echo 'Foundation prepared. Existing test site is still active; no application data was imported.'
echo 'No public cutover, migration, backup schedule or GitHub runner installation was performed.'
echo 'KAARDID_SERVER_PREPARE_COMPLETE'
