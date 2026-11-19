#!/usr/bin/env bash
# Publish the prepared rehearsal on VM loopback only. Public port 80 stays unchanged.
set -euo pipefail
umask 027
export LC_ALL=C.UTF-8
report_exit() {
    local status=$?
    if (( status != 0 )); then
        echo "Private preview activation did not complete (exit $status)." >&2
    fi
}
trap report_exit EXIT
if [[ $EUID -ne 0 || ${SUDO_USER:-} != erik || $(hostname -f) != kaardid.arhiiv.ee || $# -ne 1 ||
      ( $1 != --nginx-only && ! $1 =~ ^[0-9a-f]{40}$ ) ]]; then
    echo 'Run with sudo as erik on the Kaardid VM, supplying the prepared commit SHA or --nginx-only.' >&2
    exit 1
fi
site=/etc/nginx/sites-available/kaardid-rehearsal
enabled=/etc/nginx/sites-enabled/kaardid-rehearsal
nginx_config="$(dirname -- "$0")/kaardid-rehearsal.conf"
if [[ ! -f "$nginx_config" || $(head -1 "$nginx_config") != '# Managed by Kaardid activate-rehearsal' ||
      $(awk '$1 == "listen" { print $2 }' "$nginx_config") != '127.0.0.1:18080;' ]]; then
    echo 'Expected managed, loopback-only rehearsal nginx template is missing.' >&2
    exit 1
fi

if [[ $1 == --nginx-only ]]; then
    if [[ ! -f "$site" || -L "$site" || $(stat -c '%u' "$site") != 0 ||
          $(head -1 "$site") != '# Managed by Kaardid activate-rehearsal' ||
          ! -L "$enabled" || $(readlink "$enabled") != "$site" ]]; then
        echo 'Expected installed rehearsal nginx site is missing.' >&2
        exit 1
    fi
    exec 9</home/erik/.kaardid-setup/rehearsal-deploy.lock
    flock -n 9 || { echo 'Another rehearsal operation is running.' >&2; exit 1; }
    backup_dir=$(mktemp -d /var/backups/kaardid-rehearsal-nginx.XXXXXXXX)
    backup="$backup_dir/kaardid-rehearsal.conf"
    cp -p "$site" "$backup"
    candidate=$(mktemp /etc/nginx/sites-available/.kaardid-rehearsal.XXXXXXXX)
    reloaded=false
    restore_nginx_on_failure() {
        local status=$?
        if (( status != 0 )); then
            if ! { install -o root -g root -m 0644 "$backup" "$candidate" && mv -Tf "$candidate" "$site"; }; then
                echo 'Could not restore the rehearsal site file. Restore it from the backup before reloading.' >&2
            elif "$reloaded" && ! { nginx -t && systemctl reload nginx; }; then
                echo 'Restored the rehearsal site file but could not reload nginx.' >&2
            fi
            echo "Rehearsal nginx update failed. Previous config saved at $backup." >&2
        fi
        rm -f "$candidate"
        exit "$status"
    }
    trap restore_nginx_on_failure EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    install -o root -g root -m 0644 "$nginx_config" "$candidate"
    mv -Tf "$candidate" "$site"
    nginx -t
    reloaded=true
    systemctl reload nginx

    check_rehearsal_http() {
        local expected=$1 route=$2 status
        shift 2
        status=$(curl --silent --show-error --max-time 10 --output /dev/null --write-out '%{http_code}' \
            "$@" "http://127.0.0.1:18080$route")
        if [[ $status != "$expected" ]]; then
            echo "Rehearsal $route returned HTTP $status (expected $expected)." >&2
            return 1
        fi
        echo "Rehearsal $route returned HTTP $status."
    }
    check_rehearsal_http 200 /
    check_rehearsal_http 200 /index.php/map/search
    check_rehearsal_http 302 /index.php/et/site/clientLogin
    check_rehearsal_http 200 /robots.txt
    check_rehearsal_http 404 /protected/config/private/ips.php
    check_rehearsal_http 200 / -H 'X-Real-IP: 57.141.20.1' -H 'X-Forwarded-For: 57.141.20.1'
    echo "Previous rehearsal nginx config: $backup"
    echo 'KAARDID_REHEARSAL_NGINX_UPDATED'
    exit 0
fi

release="/srv/kaardid/releases/$1"
app="$release/apps/kaardid"
require_check() {
    local description=$1
    shift
    if ! "$@"; then
        echo "Activation preflight failed: $description" >&2
        exit 1
    fi
}
# This VM's external /usr/bin/test incorrectly rejects supplementary-group
# reads. Use Bash's builtin, verified against actual open() on the VM.
as_account_test() {
    local account=$1
    shift
    runuser -u "$account" -- /bin/bash --noprofile --norc -c 'test "$@"' kaardid-permission-check "$@"
}
echo 'Checking prepared release, FPM socket and service-account permissions.'
require_check "release manifest missing: $release/release.json" test -f "$release/release.json"
require_check "application entry point missing: $app/index.php" test -f "$app/index.php"
require_check 'dedicated PHP-FPM socket missing' test -S /run/php/php8.5-fpm-kaardid.sock
python3 - "$release/release.json" "$1" <<'PY'
import json,sys
m=json.load(open(sys.argv[1]))
if m.get('commit')!=sys.argv[2] or m.get('purpose')!='private-rehearsal':
    raise SystemExit('Wrong release identity; no nginx changes made.')
PY
runuser -u erik -- python3 - "$app" <<'PY'
from pathlib import Path
import os,sys
path=Path(sys.argv[1])/'protected/config/private'
target='/srv/kaardid/shared/config'
if path.is_symlink():
    if os.readlink(path)!=target:raise SystemExit('Unexpected private configuration link.')
else:
    path.rmdir()  # Only an empty packaged directory may be replaced.
    path.symlink_to(target,target_is_directory=True)
PY
for file in /etc/kaardid/app-db.json /srv/kaardid/shared/config/integrations.json /srv/kaardid/shared/config/environment.json "$app/index.php"; do
    require_check "kaardid cannot read $file" as_account_test kaardid -r "$file"
done
require_check "www-data cannot read $app/index.php" as_account_test www-data -r "$app/index.php"
for account in kaardid www-data; do
    if as_account_test "$account" -w "$app/index.php" || as_account_test "$account" -w "$app"; then
        echo 'A runtime account can modify release code; refusing activation.' >&2
        exit 1
    fi
done
if find "$release" -xdev ! -type l -perm /0022 -print -quit | grep -q .; then
    echo 'Group/world-writable release code found; refusing activation.' >&2
    exit 1
fi
if as_account_test www-data -r /etc/kaardid/app-db.json; then
    echo 'Unexpected nginx access to database credentials; refusing activation.' >&2
    exit 1
fi
for directory in /srv/kaardid/shared/runtime /srv/kaardid/shared/assets /srv/kaardid/shared/upload; do
    require_check "kaardid cannot write $directory" as_account_test kaardid -w "$directory"
done

# Yii must preserve the static-reader group at every published directory level.
# Repair already published rehearsal assets as their service owner, never as root.
runuser -u kaardid -- /usr/bin/python3 - <<'ASSETS'
import grp,os,pathlib
root=pathlib.Path('/srv/kaardid/shared/assets')
group=grp.getgrnam('kaardid-code').gr_gid
paths=[root,*root.rglob('*')]
if any(p.is_symlink() for p in paths):
    raise SystemExit('Unexpected symlink in published assets; refusing repair.')
if any(p.stat().st_uid!=os.geteuid() for p in paths):
    raise SystemExit('Unexpected published-asset owner; refusing repair.')
for p in paths:
    os.chown(p,-1,group)
    os.chmod(p,0o2750 if p.is_dir() else 0o640)
print('Published asset groups and inherited directory permissions verified.')
ASSETS

echo 'Service-account permissions passed; preparing shared media and private nginx site.'
if [[ -d /srv/kaardid/shared/upload-staged ]]; then
    if find /srv/kaardid/shared/upload-staged -type l -print -quit | grep -q .; then
        echo 'Unexpected symlink in staged upload data; refusing to copy it.' >&2
        exit 1
    fi
    rsync -rt --ignore-existing --chown=kaardid:kaardid-code --chmod=D2750,F0640 \
        /srv/kaardid/shared/upload-staged/ /srv/kaardid/shared/upload/
fi

link=/srv/kaardid/rehearsal
if [[ -e "$site" ]] && ! head -1 "$site" | grep -qx '# Managed by Kaardid activate-rehearsal'; then
    echo 'Unmanaged nginx site exists; refusing to overwrite it.' >&2
    exit 1
fi
if [[ -e "$enabled" || -L "$enabled" ]]; then
    if [[ ! -L "$enabled" || $(readlink "$enabled") != "$site" ]]; then
        echo 'Unexpected existing enabled-site entry.' >&2
        exit 1
    fi
fi
if [[ -e "$link" && ! -L "$link" ]]; then
    echo 'Rehearsal link path is occupied by a regular directory/file.' >&2
    exit 1
fi
previous_link=''
if [[ -L "$link" ]]; then previous_link=$(readlink "$link"); fi
previous_enabled=false
if [[ -L "$enabled" ]]; then previous_enabled=true; fi
backup=$(mktemp /etc/nginx/sites-available/.kaardid-rehearsal-backup.XXXXXX)
previous_site=false
if [[ -e "$site" ]]; then cp -p "$site" "$backup"; previous_site=true; fi
rollback() {
    if "$previous_site"; then cp -p "$backup" "$site"; else rm -f "$site"; fi
    if ! "$previous_enabled"; then rm -f "$enabled"; fi
    if [[ -n "$previous_link" ]]; then
        ln -s "$previous_link" "$link.rollback-$$"
        mv -Tf "$link.rollback-$$" "$link"
    else
        rm -f "$link"
    fi
    rm -f "$backup"
    if nginx -t; then systemctl reload nginx; fi
}
trap 'rollback' ERR
ln -s "$release" "$link.next-$$"
mv -Tf "$link.next-$$" "$link"
install -o root -g root -m 0644 "$nginx_config" "$site"
if [[ ! -L "$enabled" ]]; then ln -s "$site" "$enabled"; fi
nginx -t
systemctl reload nginx
status=$(curl --silent --show-error --max-time 30 --output /dev/null --write-out '%{http_code}' http://127.0.0.1:18080/index.php/site/index)
if [[ "$status" != 200 ]]; then
    echo "Home-page smoke check returned HTTP $status; restoring the previous private-site configuration." >&2
    false
fi
for path in /protected/config/production.php /index-dev.php /index.php/test/login /cron.php; do
    status=$(curl --silent --show-error --max-time 15 --output /dev/null --write-out '%{http_code}' "http://127.0.0.1:18080$path")
    if [[ "$status" != 404 ]]; then
        echo "Expected private-site route restriction failed: $path returned HTTP $status" >&2
        false
    fi
done
for asset in $(curl --silent --show-error --max-time 15 http://127.0.0.1:18080/ | grep -oE '/assets/[a-zA-Z0-9_./-]+\.(css|js)' | sort -u); do
    status=$(curl --silent --show-error --max-time 15 --output /dev/null --write-out '%{http_code}' "http://127.0.0.1:18080$asset")
    if [[ "$status" != 200 ]]; then
        echo "Published asset health check failed: $asset returned HTTP $status" >&2
        false
    fi
done
trap - ERR
rm -f "$backup"
echo "Private rehearsal active for commit $1 on 127.0.0.1:18080."
echo 'Home/assets HTTP 200 and protected/dev/test-route HTTP 404 checks passed.'
echo 'The existing port-80 test site and current production deployment were not switched.'
echo 'KAARDID_REHEARSAL_ACTIVATE_COMPLETE'
