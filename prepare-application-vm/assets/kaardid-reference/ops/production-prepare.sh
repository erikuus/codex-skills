#!/usr/bin/env bash
# Create an inactive production foundation. No nginx site, import or cutover.
set -euo pipefail
umask 077
export LC_ALL=C.UTF-8
if [[ $EUID -ne 0 || ${SUDO_USER:-} != erik || $(hostname -f) != kaardid.arhiiv.ee ]]; then
    echo 'Run with sudo as erik on kaardid.arhiiv.ee only.' >&2
    exit 1
fi
test -x /usr/lib/postgresql/17/bin/psql
test -x /usr/sbin/php-fpm8.5
systemctl is-active --quiet postgresql
systemctl is-active --quiet php8.5-fpm
php -r 'exit(extension_loaded("soap") && extension_loaded("gd") && extension_loaded("pdo_pgsql") ? 0 : 1);'

account=kaardid-production
code_group=kaardid-production-code
root=/srv/kaardid-production
if getent passwd "$account" >/dev/null; then
    entry=$(getent passwd "$account")
    if [[ $(cut -d: -f6 <<< "$entry") != "$root" || $(cut -d: -f7 <<< "$entry") != /usr/sbin/nologin ]]; then
        echo 'Unexpected existing production service account; refusing takeover.' >&2
        exit 1
    fi
else
    useradd --system --user-group --home-dir "$root" --no-create-home --shell /usr/sbin/nologin "$account"
fi
getent group "$code_group" >/dev/null || groupadd --system "$code_group"
usermod -a -G "$account,$code_group" erik
usermod -a -G "$code_group" "$account"
usermod -a -G "$code_group" www-data
install -d -o root -g "$account" -m 0750 /etc/kaardid-production
install -d -o erik -g erik -m 0700 /home/erik/.config /home/erik/.config/kaardid

python3 - <<'PY'
import base64,grp,hashlib,hmac,json,os,pwd,secrets,subprocess
from pathlib import Path

PSQL=['runuser','-u','postgres','--','/usr/lib/postgresql/17/bin/psql',
      '-X','--no-password','-h','/var/run/postgresql','-p','5432','-U','postgres',
      '--set=ON_ERROR_STOP=1','-Atq']
def sql(statement,database='postgres'):
    result=subprocess.run(PSQL+['--dbname='+database],input=statement,text=True,capture_output=True)
    if result.returncode:
        raise SystemExit('Production database preparation failed; no credential values are printed.')
    return result.stdout.strip()
def write_json(path,value,owner,group,mode):
    path=Path(path);temporary=path.with_name(path.name+'.new')
    fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as stream:json.dump(value,stream,indent=2);stream.write('\n')
    os.chown(temporary,pwd.getpwnam(owner).pw_uid,grp.getgrnam(group).gr_gid)
    os.chmod(temporary,mode);os.replace(temporary,path)
def verifier(password):
    salt=secrets.token_bytes(16)
    salted=hashlib.pbkdf2_hmac('sha256',password.encode('ascii'),salt,4096)
    stored=hashlib.sha256(hmac.new(salted,b'Client Key',hashlib.sha256).digest()).digest()
    server=hmac.new(salted,b'Server Key',hashlib.sha256).digest()
    encode=lambda value:base64.b64encode(value).decode('ascii')
    return 'SCRAM-SHA-256$4096:'+encode(salt)+'$'+encode(stored)+':'+encode(server)

names=['kaart_prod_owner','kaart_prod_migrate','kaart_prod_app','kaart_prod_readonly']
existing=set(sql("SELECT rolname FROM pg_roles WHERE rolname IN ('kaart_prod_owner','kaart_prod_migrate','kaart_prod_app','kaart_prod_readonly');").splitlines())
database_exists=sql("SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname='kaart_prod');")=='t'
state_path=Path('/etc/kaardid-production/bootstrap-secrets.json')
if database_exists and sql("SELECT pg_get_userbyid(datdba) FROM pg_database WHERE datname='kaart_prod';")!='kaart_prod_owner':
    raise SystemExit('Unexpected production database owner; refusing takeover.')
if state_path.exists():
    state=json.loads(state_path.read_text())
    if state.get('managed_roles')!=names or state.get('database')!='kaart_prod':
        raise SystemExit('Unexpected production bootstrap state.')
else:
    if existing or database_exists:
        raise SystemExit('Production database/roles already exist without bootstrap state; refusing takeover.')
    state={'managed_roles':names,'database':'kaart_prod','app_password':secrets.token_urlsafe(36),
           'migration_password':secrets.token_urlsafe(36)}
    write_json(state_path,state,'root','root',0o600)
if sql("SELECT EXISTS(SELECT 1 FROM pg_roles WHERE rolname='erik' AND rolcanlogin AND NOT rolsuper);")!='t':
    raise SystemExit('Expected the existing non-superuser personal login erik.')

statements=['BEGIN;']
for name in names:
    if name not in existing:statements.append('CREATE ROLE '+name+';')
    login='LOGIN' if name in ('kaart_prod_app','kaart_prod_migrate') else 'NOLOGIN'
    statements.append('ALTER ROLE '+name+' '+login+' INHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;')
for name,field in [('kaart_prod_app','app_password'),('kaart_prod_migrate','migration_password')]:
    statements.append("ALTER ROLE "+name+" PASSWORD '"+verifier(state[field])+"';")
statements+=['GRANT kaart_prod_owner TO kaart_prod_migrate;',
             'GRANT kaart_prod_readonly TO erik;','COMMIT;']
sql('\n'.join(statements))
if not database_exists:sql("CREATE DATABASE kaart_prod OWNER kaart_prod_owner TEMPLATE template0 ENCODING 'UTF8';")
sql('''
BEGIN;
REVOKE ALL ON DATABASE kaart_prod FROM PUBLIC;
GRANT CONNECT ON DATABASE kaart_prod TO kaart_prod_migrate,kaart_prod_app,kaart_prod_readonly;
ALTER SCHEMA public OWNER TO kaart_prod_owner;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO kaart_prod_app,kaart_prod_readonly;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS tablefunc;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO kaart_prod_app,kaart_prod_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_prod_owner IN SCHEMA public GRANT SELECT ON TABLES TO kaart_prod_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_prod_owner IN SCHEMA public GRANT SELECT,INSERT,UPDATE,DELETE ON TABLES TO kaart_prod_app;
ALTER DEFAULT PRIVILEGES FOR ROLE kaart_prod_owner IN SCHEMA public GRANT USAGE,SELECT ON SEQUENCES TO kaart_prod_app;
COMMIT;
''','kaart_prod')
sql('''
BEGIN;
SET ROLE kaart_prod_owner;
CREATE TABLE public.__kaardid_production_privilege_probe (id serial PRIMARY KEY,value text);
RESET ROLE;
SET ROLE kaart_prod_app;
INSERT INTO public.__kaardid_production_privilege_probe(value) VALUES('probe');
UPDATE public.__kaardid_production_privilege_probe SET value='updated';
DO $$ BEGIN
  IF has_schema_privilege(current_user,'public','CREATE') OR
     has_database_privilege('kaart_app','kaart_prod','CONNECT') OR
     has_database_privilege(current_user,'kaart','CONNECT') THEN
    RAISE EXCEPTION 'Unexpected cross-environment or schema privileges';
  END IF;
END $$;
RESET ROLE;
SET ROLE erik;
SELECT count(*) FROM public.__kaardid_production_privilege_probe;
DO $$ BEGIN
  IF has_table_privilege(current_user,'public.__kaardid_production_privilege_probe','UPDATE') OR
     has_schema_privilege(current_user,'public','CREATE') THEN
    RAISE EXCEPTION 'Personal production role is not read only';
  END IF;
END $$;
RESET ROLE;
ROLLBACK;
''','kaart_prod')
base={'host':'127.0.0.1','port':5432,'database':'kaart_prod'}
write_json('/etc/kaardid-production/app-db.json',dict(base,user='kaart_prod_app',password=state['app_password']),
           'root','kaardid-production',0o640)
write_json('/home/erik/.config/kaardid/production-migration-db.json',
           dict(base,user='kaart_prod_migrate',password=state['migration_password'],role='kaart_prod_owner'),
           'erik','erik',0o600)
print('Production database, isolated roles and rolled-back privilege checks passed.')
PY

install -d -o erik -g "$code_group" -m 2750 "$root" "$root/releases" "$root/shared"
install -d -o erik -g "$account" -m 2750 "$root/shared/config"
install -d -o "$account" -g "$account" -m 2770 "$root/shared/runtime"
install -d -o "$account" -g "$account" -m 0700 "$root/shared/runtime/tmp" "$root/shared/runtime/sessions"
install -d -o "$account" -g "$code_group" -m 2750 "$root/shared/assets" "$root/shared/upload"
install -d -o erik -g "$account" -m 0700 "$root/shared/runtime-console"
install -d -o root -g root -m 0700 /var/backups/kaardid-production

pool=/etc/php/8.5/fpm/pool.d/kaardid-production.conf
if [[ -e "$pool" ]] && ! head -1 "$pool" | grep -qx '; Managed by Kaardid production-prepare'; then
    echo 'Unexpected existing production PHP-FPM pool; refusing overwrite.' >&2
    exit 1
fi
backup=$(mktemp /etc/php/8.5/fpm/pool.d/.kaardid-production-backup.XXXXXX)
existed=false
if [[ -e "$pool" ]]; then cp -p "$pool" "$backup"; existed=true; fi
restore_pool() {
    if "$existed"; then cp -p "$backup" "$pool"; else rm -f "$pool"; fi
    rm -f "$backup"
}
cat > "$pool" <<'FPM'
; Managed by Kaardid production-prepare
[kaardid-production]
user = kaardid-production
group = kaardid-production
listen = /run/php/php8.5-fpm-kaardid-production.sock
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
env[SENTRY_ENVIRONMENT] = production
php_admin_flag[display_errors] = off
php_admin_flag[log_errors] = on
php_admin_value[upload_tmp_dir] = /srv/kaardid-production/shared/runtime/tmp
php_admin_value[session.save_path] = /srv/kaardid-production/shared/runtime/sessions
FPM
chmod 0644 "$pool"
if ! /usr/sbin/php-fpm8.5 --test; then restore_pool; exit 1; fi
if ! systemctl reload php8.5-fpm; then restore_pool; systemctl reload php8.5-fpm || true; exit 1; fi
rm -f "$backup"

as_account_test() {
    local user=$1; shift
    runuser -u "$user" -- /bin/bash --noprofile --norc -c 'test "$@"' kaardid-permission-check "$@"
}
as_account_test "$account" -r /etc/kaardid-production/app-db.json
for other in kaardid www-data; do
    if as_account_test "$other" -r /etc/kaardid-production/app-db.json; then
        echo 'Unexpected access to production database credentials.' >&2; exit 1
    fi
done
if as_account_test "$account" -r /etc/kaardid/app-db.json; then
    echo 'Production service can read rehearsal credentials unexpectedly.' >&2; exit 1
fi
as_account_test erik -r /home/erik/.config/kaardid/production-migration-db.json
for ((attempt=0; attempt<20; attempt++)); do
    [[ -S /run/php/php8.5-fpm-kaardid-production.sock ]] && break
    sleep 0.1
done
systemctl is-active --quiet php8.5-fpm
test -S /run/php/php8.5-fpm-kaardid-production.sock
echo 'Inactive production foundation prepared for https://kaardid.ra.ee.'
echo 'No application data imported, migrations applied, nginx site activated or public traffic switched.'
echo 'Backups, fresh production data, deployment promotion and the public proxy are still to configure.'
echo 'KAARDID_PRODUCTION_PREPARE_COMPLETE'
