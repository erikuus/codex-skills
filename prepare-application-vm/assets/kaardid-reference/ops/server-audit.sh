#!/usr/bin/env bash
# Read-only privileged inspection. No package, database, web or access changes.
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo 'Run this audit with sudo on the Kaardid VM.' >&2
    exit 1
fi
if [[ $(hostname -f) != kaardid.arhiiv.ee ]]; then
    echo 'Unexpected server; refusing to inspect a different machine.' >&2
    exit 1
fi

printf 'Kaardid privileged audit: %s\n' "$(date -Is)"
hostname -f
cat /etc/os-release
printf '\nRuntime services and packages\n'
systemctl is-active nginx php8.5-fpm postgresql
php -v
php -m
pg_lsclusters
apt-cache policy php8.5-soap php8.5-gd postgresql-17-postgis-3 composer
nginx -t

printf '\nDatabase metadata (no application rows or password hashes)\n'
runuser -u postgres -- /usr/lib/postgresql/17/bin/psql \
    -X --no-password -h /var/run/postgresql -p 5432 -U postgres \
    --dbname=postgres --set=ON_ERROR_STOP=1 <<'SQL'
SELECT current_user, current_database(), version();
SHOW listen_addresses;
SHOW ssl;
SHOW password_encryption;
SELECT datname, pg_get_userbyid(datdba) AS owner,
       pg_size_pretty(pg_database_size(oid)) AS size, datallowconn
FROM pg_database ORDER BY datname;
SELECT rolname, rolsuper, rolcreatedb, rolcreaterole, rolcanlogin
FROM pg_roles ORDER BY rolname;
SELECT extname, extversion FROM pg_extension ORDER BY extname;
SELECT name, default_version, installed_version
FROM pg_available_extensions WHERE name IN ('postgis', 'tablefunc', 'pg_trgm');
SELECT type, database, user_name, address, netmask, auth_method, error
FROM pg_hba_file_rules ORDER BY rule_number;
SQL

printf '\nStorage and deployment directory permissions\n'
df -h / /var/lib/postgresql
for directory in /home/erik /srv /opt /var/www /var/www/html /var/backups; do
    stat -c '%A %U:%G %n' "$directory"
done
printf '\nScheduled job names (command bodies intentionally omitted)\n'
systemctl list-timers --all --no-pager
find /etc/cron.d /etc/cron.daily /etc/cron.weekly -maxdepth 1 -type f -printf '%p\n'
printf '\nRoot/postgres crontab presence\n'
for account in root postgres; do
    if crontab -u "$account" -l >/dev/null 2>&1; then
        printf '%s: crontab exists; backup commands need separate review\n' "$account"
    else
        printf '%s: no crontab\n' "$account"
    fi
done
printf '\nKAARDID_ADMIN_AUDIT_COMPLETE\n'
