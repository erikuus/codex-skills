#!/usr/bin/env bash
# Managed by Kaardid monitoring preparation. No production site/updater activation.
set -euo pipefail
umask 077
export LC_ALL=C.UTF-8
if [[ $EUID -ne 0 || ${SUDO_USER:-} != erik || $(hostname -f) != kaardid.arhiiv.ee || $# -ne 2 || ! "$2" =~ ^[a-f0-9]{40}$ || ! "$1" =~ ^/home/erik/\.kaardid-setup/monitoring\.[a-zA-Z0-9]{8}$ ]]; then
    echo 'Run through bin/monitoring-install as erik on the Kaardid VM.' >&2; exit 1
fi
stage=$1
sha=$2
if [[ -e /srv/kaardid-production/current || -L /srv/kaardid-production/current ]]; then
    echo 'Production is active; this preparation helper refuses changes.' >&2; exit 1
fi
for unit in kaardid-update.service kaardid-update.timer; do
    if [[ $(systemctl show "$unit" -p LoadState --value) != not-found ]]; then
        echo 'Expected updater units to remain uninstalled; no monitoring changes made.' >&2; exit 1
    fi
done
# Freeze the source while copying SDK code; never acquire the production DB role.
exec 9</srv/kaardid/shared/runtime/operations.lock
flock -n 9 || { echo 'Rehearsal operation busy; retry preparation later.' >&2; exit 1; }
if [[ $(readlink /srv/kaardid/rehearsal) != "/srv/kaardid/releases/$sha" ]]; then
    echo 'Rehearsal changed; retry with the tested source.' >&2; exit 1
fi
source="/srv/kaardid/releases/$sha/apps/kaardid/protected/extensions/vendors"
target=/opt/kaardid-monitoring
python3 - "$source" "$stage" <<'PY'
import os,stat,sys
from pathlib import Path
for root in map(Path,sys.argv[1:]):
    for path in [root,*root.rglob('*')]:
        info=path.lstat()
        if not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)) or info.st_mode&0o022:
            raise SystemExit('Unexpected monitoring source type/permissions; refusing privileged copy.')
PY
test -f "$source/autoload.php"
test -f "$source/sentry/sentry/src/functions.php"
reporter_hash=$(sha256sum "$stage/report-job-failure.php" | awk '{print $1}')
unit=/etc/systemd/system/kaardid-job-failure@.service
if [[ -e "$unit" ]] && ! cmp -s "$stage/kaardid-job-failure@.service" "$unit"; then
    echo 'Existing notifier unit differs; review an explicit upgrade.' >&2; exit 1
fi
if [[ -e "$target" || -L "$target" ]]; then
    if [[ -L "$target" || ! -f "$target/reporter.sha256" || $(cat "$target/reporter.sha256") != "$reporter_hash" ]]; then
        echo 'Existing monitoring installation differs; review an explicit upgrade.' >&2; exit 1
    fi
    python3 - "$target" "$reporter_hash" <<'PY'
import hashlib,stat,sys
from pathlib import Path
root=Path(sys.argv[1])
for path in [root,*root.rglob('*')]:
    info=path.lstat()
    if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)) or info.st_uid!=0 or info.st_mode&0o022:
        raise SystemExit('Unsafe existing monitoring installation.')
if hashlib.sha256((root/'report-job-failure.php').read_bytes()).hexdigest()!=sys.argv[2]:
    raise SystemExit('Installed reporter checksum differs.')
PY
else
    temporary=$(mktemp -d /opt/.kaardid-monitoring.XXXXXXXX)
    trap 'rm -rf -- "$temporary"' EXIT
    cp -a "$source" "$temporary/sdk"
    install -m 0640 "$stage/report-job-failure.php" "$temporary/report-job-failure.php"
    printf '%s\n' "$reporter_hash" > "$temporary/reporter.sha256"
    chown -R root:kaardid-production "$temporary"
    find "$temporary" -type d -exec chmod 0750 {} +
    find "$temporary" -type f -exec chmod 0640 {} +
    mv "$temporary" "$target"
    trap - EXIT
fi
flock -u 9
exec 9<&-
install -d -o kaardid-production -g kaardid-production -m 2750 /srv/kaardid-production/shared/runtime/monitoring
systemd-analyze verify "$stage/kaardid-job-failure@.service"
install -o root -g root -m 0644 "$stage/kaardid-job-failure@.service" "$unit"
systemctl daemon-reload

# Test the real OnFailure chain with /usr/bin/false, never cron.php/update.
marker=$(date -u +%Y%m%dT%H%M%SZ)
probe="kaardid-monitoring-probe-$marker.service"
receipt="/srv/kaardid-production/shared/runtime/monitoring/$probe.json"
cleanup() {
    systemctl reset-failed "$probe" >/dev/null 2>&1 || true
}
trap cleanup EXIT
systemd-run --no-block --unit="$probe" --description='Controlled Kaardid failure-alert test' \
    --property=Type=oneshot --property="OnFailure=kaardid-job-failure@$probe.service" /usr/bin/false
for ((attempt=0; attempt<60; attempt++)); do
    [[ -f "$receipt" ]] && break
    sleep 1
done
python3 - "$receipt" "$probe" <<'PY'
import json,sys
from pathlib import Path
path=Path(sys.argv[1])
if not path.is_file():raise SystemExit('No notification receipt; inspect the notifier privately. Production/updater were not started.')
receipt=json.loads(path.read_text())
if receipt.get('unit')!=sys.argv[2] or receipt.get('service_result')!='exit-code' or receipt.get('exit_status')!='1':
    raise SystemExit('Unexpected failure-probe result.')
print(json.dumps(receipt,indent=2))
PY
for unit in kaardid-update.service kaardid-update.timer; do
    [[ $(systemctl show "$unit" -p LoadState --value) == not-found ]]
done
[[ ! -e /srv/kaardid-production/current && ! -L /srv/kaardid-production/current ]]
echo 'Only the static notifier was installed and a disposable false-service tested.'
echo 'Production and its scheduled updater remain inactive.'
echo KAARDID_MONITORING_FAILURE_CHAIN_VERIFIED
