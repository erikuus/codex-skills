#!/usr/bin/env bash
# Run as root on the Kaardid VM, via bin/production-backend-tls.
set -euo pipefail
umask 077
[[ $EUID -eq 0 && ${SUDO_USER:-} == erik && $(hostname -f) == kaardid.arhiiv.ee ]]
stage=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
available=/etc/nginx/sites-available
enabled=/etc/nginx/sites-enabled
preview=kaardid-production-preview
backend=kaardid-backend-tls
production=kaardid-production
current=/srv/kaardid-production/current
[[ ! -e $current && ! -L $current ]]
[[ $(readlink "$enabled/$preview") == "$available/$preview" ]]
cmp -s "$available/$preview" "$stage/$preview.conf"
for site in "$backend" "$production"; do
    [[ ! -e $available/$site && ! -L $available/$site ]]
    [[ ! -e $enabled/$site && ! -L $enabled/$site ]]
done
cert=/etc/ssl/certs/kaardid.arhiiv.ee.crt
key=/etc/ssl/private/kaardid.arhiiv.ee.key
[[ -f $key && $(stat -Lc '%u' "$key") == 0 ]]
if (( 8#$(stat -Lc '%a' "$key") & 0037 )); then
    echo 'Backend TLS key permissions are too broad.' >&2
    exit 1
fi
openssl verify -verify_hostname kaardid.arhiiv.ee "$cert"
nginx -t

# Keep the preview on loopback and save the exact installed file for rollback.
saved=$(mktemp -d /var/backups/kaardid-backend-tls.XXXXXXXX)
cp -p -- "$available/$preview" "$saved/$preview"
sed '/^    listen 172\.20\.20\.142:80;$/d' "$saved/$preview" > "$saved/preview-loopback"
restore() {
    echo "Restoring original nginx configuration from $saved" >&2
    rm -f -- "$enabled/$backend" "$enabled/$production" "$available/$backend" "$available/$production"
    install -m 0644 "$saved/$preview" "$available/$preview"
    nginx -t && systemctl reload nginx
}
trap 'status=$?; if (( status )); then restore; fi' EXIT
trap 'exit 1' HUP INT TERM
install -m 0644 "$saved/preview-loopback" "$available/$preview"
install -m 0644 "$stage/$backend.conf" "$available/$backend"
install -m 0644 "$stage/$production.conf" "$available/$production"
ln -s "$available/$backend" "$enabled/$backend"
ln -s "$available/$production" "$enabled/$production"
nginx -t
systemctl reload nginx

verify() {
    local redirect tls
    redirect=$(curl --noproxy '*' -sS --max-time 5 -o /dev/null -w '%{http_code} %{redirect_url}' \
        --resolve kaardid.arhiiv.ee:80:172.20.20.142 'http://kaardid.arhiiv.ee/test?probe=1') || return 1
    [[ $redirect == '308 https://kaardid.arhiiv.ee/test?probe=1' ]] || return 1
    tls=$(curl --noproxy '*' -sS --max-time 5 -o /dev/null -w '%{http_code} %header{x-kaardid-environment}' \
        --resolve kaardid.arhiiv.ee:443:172.20.20.142 -H 'Host: kaardid.ra.ee' https://kaardid.arhiiv.ee/) || return 1
    [[ $tls == '503 production-backend-staging' ]] || return 1
    [[ $(curl --noproxy '*' -sS --max-time 5 -o /dev/null -w '%{http_code}' -H 'Host: kaardid.ra.ee' http://127.0.0.1:18081/) == 503 ]] || return 1
    [[ $(curl --noproxy '*' -sS --max-time 5 -o /dev/null -w '%{http_code} %header{x-kaardid-data}' -H 'Host: kaardid.arhiiv.ee' http://127.0.0.1:18082/) == '200 rehearsal-copy' ]] || return 1
    [[ $(curl --noproxy '*' -sS --max-time 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:18080/) == 200 ]]
}
for attempt in 1 2 3 4 5; do
    if verify; then
        trap - EXIT HUP INT TERM
        echo "Original nginx preview saved in $saved"
        echo 'KAARDID_BACKEND_TLS_STAGING_VERIFIED'
        exit 0
    fi
    sleep 1
done
echo 'Backend TLS, redirect or existing site health check failed.' >&2
exit 1
