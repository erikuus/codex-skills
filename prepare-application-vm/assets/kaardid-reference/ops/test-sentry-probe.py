#!/usr/bin/env python3
"""Disposable VM-only probe HTTP server: no production site or database use."""
import http.client
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time


def main():
    if len(sys.argv)!=2 or not re.fullmatch(r'/srv/kaardid/releases/[a-f0-9]{40}/apps/kaardid',sys.argv[1]):
        raise SystemExit('Supply the tested rehearsal app path.')
    source=Path(__file__).resolve().parent
    app=Path(sys.argv[1])
    marker='KAARDID_SENTRY_'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())
    with tempfile.TemporaryDirectory(prefix='sentry-probe-',dir=str(Path.home()/'.kaardid-setup')) as directory:
        root=Path(directory)
        for name in ('runtime','sessions','config'):(root/name).mkdir(mode=0o700)
        for name in ('sentry-probe-router.php','XSentryProbeAction.php'):
            shutil.copyfile(source/name,root/name)
        for name in ('Environment.php','sentry.php'):shutil.copyfile(source/name,root/'config'/name)
        (root/'config/private').symlink_to('/srv/kaardid-production/shared/config')
        with socket.socket() as listener:
            listener.bind(('127.0.0.1',0));port=listener.getsockname()[1]
        token=secrets.token_hex(32)
        environment={k:v for k,v in os.environ.items() if not k.startswith(('SENTRY_','PG'))}
        environment.update(KAARDID_MONITORING_TEST='1',KAARDID_MONITORING_APP=str(app),
                           SENTRY_PROBE_TOKEN=token,SENTRY_PROBE_MARKER=marker,SENTRY_ENVIRONMENT='prod',
                           SENTRY_SERVER_NAME='kaardid-vm-monitoring-test',SENTRY_RELEASE='kaardid-monitoring-test')
        with (root/'server.log').open('w') as log:
            server=subprocess.Popen(['/usr/bin/php8.5','-S','127.0.0.1:'+str(port),str(root/'sentry-probe-router.php')],
                env=environment,stdout=log,stderr=log,stdin=subprocess.DEVNULL,cwd=app)
            try:
                for _ in range(50):
                    try:
                        with socket.create_connection(('127.0.0.1',port),timeout=.1):break
                    except OSError:time.sleep(.1)
                def request(authorize):
                    connection=http.client.HTTPConnection('127.0.0.1',port,timeout=30)
                    try:
                        connection.request('GET','/index.php/site/sentryProbe',headers={'Authorization':'Bearer '+token} if authorize else {})
                        response=connection.getresponse();body=response.read()
                        if token.encode() in body:raise RuntimeError('Probe credential appeared in the response.')
                        return response.status
                    finally:connection.close()
                if request(False)!=403:raise RuntimeError('Unauthenticated probe was not rejected.')
                # 1 initial + 1 suppressed + 1 summary in each temporary 10s window.
                # Five Sentry events exercise existing first/persistent prod rules.
                for window in range(3):
                    for _ in range(3 if window<2 else 1):
                        if request(True)!=500:raise RuntimeError('Expected probe HTTP 500 not observed.')
                    if window<2:time.sleep(10.2)
                print(json.dumps({'marker':marker,'expectedEvents':5,'temporaryWindowSeconds':10,
                    'temporarySummaryThreshold':3,'databaseConfigured':False,'productionActivated':False}))
            finally:
                server.terminate()
                try:server.wait(timeout=5)
                except subprocess.TimeoutExpired:server.kill();server.wait()
    print('Disposable server, credential, session and cache files removed.')


if __name__=='__main__':main()
