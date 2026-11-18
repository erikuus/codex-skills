#!/usr/bin/env python3
"""Read-only VM overview; sent over SSH stdin, never installed on the server."""
from datetime import datetime, timedelta, timezone
import http.client
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from zoneinfo import ZoneInfo


def properties(unit, fields):
    result = subprocess.run(['systemctl','show',unit,'--no-pager','--timestamp=unix',
                             '--property='+','.join(fields)],
                            text=True,capture_output=True,timeout=10)
    if result.returncode and not result.stdout:
        return {'LoadState':'unknown'}
    return dict(line.split('=',1) for line in result.stdout.splitlines() if '=' in line)


def epoch(value):
    return int(value[1:]) if re.fullmatch(r'@[0-9]{1,12}', value or '') else None


def display_time(value):
    timestamp = epoch(value)
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat() if timestamp else None


def safe_run(run):
    if not isinstance(run, dict):
        raise ValueError('Invalid run.')
    options = {
        'source': ('manual','timer'),
        'outcome': ('completed','warning','failed','skipped'),
        'stage': (None,'lock','checkpoint','additions','deletions','thumbnails'),
    }
    if any(run.get(key) not in allowed for key, allowed in options.items()):
        raise ValueError('Invalid run category.')
    timestamps = ('startedAt','finishedAt','intervalFrom','checkpointAfter')
    for key in timestamps:
        value = run.get(key)
        if value is None and key in ('intervalFrom','checkpointAfter'):
            continue
        if type(value) is not int or not 0 < value <= 253402300799:
            raise ValueError('Invalid run time.')
    keys = ('dgsPages','mapsAdded','imagesAdded','imagesRemoved','thumbnailsSaved','thumbnailFailures')
    counts = run.get('counts')
    if counts is not None:
        if not isinstance(counts, dict) or any(type(counts.get(key)) is not int or counts[key]<0 for key in keys):
            raise ValueError('Invalid run counts.')
        counts = {key:counts[key] for key in keys}
    return {**{key:run.get(key) for key in (*options,*timestamps)},'counts':counts}


def updater_history(path):
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(descriptor, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size > 16384:
                raise ValueError('Invalid history file.')
            history = json.loads(stream.read(16385))
        if history['version']!=1 or not isinstance(history['runs'], list) or len(history['runs'])>7:
            raise ValueError('Unsupported history.')
        aggregate = {}
        for key in ('lastAdditionAt','lastCheckpointAt','noAdditionsStreak'):
            value = history.get(key)
            limit = 10000000 if key=='noAdditionsStreak' else 253402300799
            aggregate[key] = value if type(value) is int and 0<=value<=limit else None
        scheduled = history['lastScheduledRun']
        return dict(historyStatus='available', runs=[safe_run(run) for run in history['runs']],
                    lastScheduledRun=safe_run(scheduled) if scheduled is not None else None, **aggregate)
    except FileNotFoundError:
        status = 'empty'
    except (OSError, ValueError, KeyError, TypeError):
        status = 'unavailable'
    return dict(historyStatus=status, runs=[], lastScheduledRun=None,
                lastAdditionAt=None, lastCheckpointAt=None, noAdditionsStreak=None)


def missed_updater_run(timer, service, scheduled, now):
    active_since = epoch(timer.get('ActiveEnterTimestamp'))
    calendar = re.fullmatch(r'\{ OnCalendar=\*-\*-\* (\d\d:\d\d:\d\d) Europe/Tallinn ; next_elapse=[^}]+ \}',
                            timer.get('TimersCalendar','').strip())
    if timer.get('ActiveState')!='active' or not active_since or not calendar:
        return None
    local_now = datetime.fromtimestamp(now, ZoneInfo('Europe/Tallinn'))
    hour, minute, second = map(int, calendar[1].split(':'))
    if hour>23 or minute>59 or second>59:
        return None
    due = local_now.replace(hour=hour, minute=minute, second=second, microsecond=0)
    if due.timestamp()>now:
        due -= timedelta(days=1)
    due_at = int(due.timestamp())
    if due_at<active_since:
        return None
    triggered = epoch(timer.get('LastTriggerUSec'))
    if not triggered or triggered<due_at:
        return {'at':due_at,'stage':'trigger'} if now>due_at+15*60 else None
    if scheduled and scheduled['startedAt']>=triggered-2:
        return None
    if service.get('Result') not in (None,'success') and (epoch(service.get('StateChangeTimestamp')) or 0)>=triggered:
        return None  # The service failure is already reported separately.
    if now>triggered+2*3600+15*60:
        return {'at':due_at,'stage':'completion'}
    return None


def production_updater(timer, service, path, now):
    history = updater_history(path)
    result = service.get('Result')
    service_outcome = None
    if result in ('exit-code','timeout','signal','core-dump','resources','protocol','watchdog','start-limit-hit','oom-kill'):
        service_outcome = 'skipped' if result=='exit-code' and service.get('ExecMainStatus')=='75' else 'failed'
    return dict(**history, missed=missed_updater_run(timer, service, history['lastScheduledRun'], now),
                active={'active':True,'inactive':False,'failed':False}.get(timer.get('ActiveState')),
                lastTriggerAt=epoch(timer.get('LastTriggerUSec')),
                nextRunAt=epoch(timer.get('NextElapseUSecRealtime')),
                serviceOutcome=service_outcome,
                serviceAt=epoch(service.get('StateChangeTimestamp')) if service_outcome else None)


def release(pointer):
    try:
        if not stat.S_ISLNK(pointer.lstat().st_mode):return 'UNEXPECTED RELEASE ENTRY'
        target = pointer.resolve(strict=True)
        return target.name if re.fullmatch('[a-f0-9]{40}',target.name) else 'UNEXPECTED TARGET'
    except FileNotFoundError:
        return 'NOT ACTIVATED' if not pointer.is_symlink() else 'UNKNOWN (broken link)'
    except (OSError, RuntimeError):
        return 'UNKNOWN (unreadable or broken link)'


def maintenance(root):
    try:
        (root/'shared/config/.maintenance').stat()
        return 'ON'
    except FileNotFoundError:return 'OFF'
    except OSError:return 'UNKNOWN (unreadable)'


def main():
    now = datetime.now(timezone.utc)
    print('Kaardid VM status — '+now.isoformat(timespec='seconds'))
    print('Live read-only check; no jobs, deployments or migrations are started.\n')
    root = Path('/srv/kaardid')
    print('REHEARSAL')
    print('  Active release: '+release(root/'rehearsal'))
    print('  Rollback release: '+release(root/'previous'))
    print('  Maintenance: '+maintenance(root))
    connection = http.client.HTTPConnection('127.0.0.1',18080,timeout=10)
    try:
        connection.request('GET','/')
        response = connection.getresponse();response.read()
        print('  Home: HTTP '+str(response.status))
    except (OSError, http.client.HTTPException):
        print('  Home: UNKNOWN (HTTP check failed)')
    finally:connection.close()
    print('\nPRODUCTION ON THIS VM')
    production = Path('/srv/kaardid-production')
    print('  Active release: '+release(production/'current'))
    previous=production/'previous'
    print('  Rollback release: '+(release(previous) if previous.exists() or previous.is_symlink() else 'NONE RETAINED'))
    print('  Maintenance: '+maintenance(production))
    if (production/'preview').is_symlink():
        print('  VPN preview (rehearsal test data): '+release(production/'preview'))
        preview = http.client.HTTPConnection('127.0.0.1',18082,timeout=10)
        try:
            preview.request('GET','/',headers={'Host':'kaardid.arhiiv.ee'})
            response=preview.getresponse();response.read()
            identity=response.getheader('X-Kaardid-Data')
            print('  VPN preview home: '+('HTTP '+str(response.status) if identity=='rehearsal-copy'
                                          else 'UNKNOWN (unexpected backend)'))
        except (OSError,http.client.HTTPException):
            print('  VPN preview home: UNKNOWN (HTTP check failed)')
        finally: preview.close()
    print('  Public DNS/proxy and the legacy server are not checked here.')

    print('\nKAARDID SCHEDULED JOBS')
    prepared = {name for name in sys.argv[1:] if re.fullmatch(r'kaardid[\w-]*\.timer',name)}
    installed = subprocess.run(['systemctl','list-unit-files','--type=timer','--no-pager',
                                '--no-legend'],text=True,capture_output=True,timeout=10)
    names = prepared | {line.split()[0] for line in installed.stdout.splitlines()
                        if line.split() and re.fullmatch(r'kaardid[\w-]*\.timer',line.split()[0])}
    if installed.returncode:
        print('  Installed timer inventory: UNKNOWN (systemctl check failed)')
    for name in sorted(names):
        print('  '+name+(' (definition in ops/systemd/)' if name in prepared else ''))
        timer = properties(name,['LoadState','UnitFileState','ActiveState',
                                 'NextElapseUSecRealtime','LastTriggerUSec','TimersCalendar','Unit','ActiveEnterTimestamp'])
        if timer.get('LoadState')=='not-found':
            print('    NOT INSTALLED — no scheduled run from this timer on this VM')
        elif timer.get('LoadState')=='unknown':
            print('    UNKNOWN (cannot inspect timer)')
        else:
            print('    Installed: '+timer.get('LoadState','unknown')+
                  '; enabled: '+timer.get('UnitFileState','unknown')+
                  '; state: '+timer.get('ActiveState','unknown'))
            print('    Installed schedule: '+(timer.get('TimersCalendar') or 'not reported'))
            print('    Next run: '+(display_time(timer.get('NextElapseUSecRealtime')) or 'none scheduled'))
            print('    Last trigger: '+(display_time(timer.get('LastTriggerUSec')) or 'none recorded'))
        service = properties(timer.get('Unit') or name.removesuffix('.timer')+'.service',
                             ['LoadState','ActiveState','Result','ExecMainStartTimestamp',
                              'ExecMainExitTimestamp','ExecMainStatus','StateChangeTimestamp'])
        if service.get('LoadState')=='not-found':
            print('    Service: NOT INSTALLED')
        else:
            print('    Service state: '+service.get('ActiveState','unknown'))
            started = display_time(service.get('ExecMainStartTimestamp'))
            finished = display_time(service.get('ExecMainExitTimestamp'))
            print('    Last recorded run: '+(started+'; '+('finished: '+finished+'; result: '+service.get('Result','unknown')
                                                          if finished else 'completion not recorded')
                                             if started else 'none reported'))
        if name=='kaardid-update.timer':
            summary = production_updater(timer, service, production/'shared/runtime/updater-runs.json',
                                         int(now.timestamp()))
            print('    Production updater JSON: '+json.dumps(summary,separators=(',',':')))
    if not names:print('  No prepared or installed Kaardid timers found.')

    print('\nBACKUPS')
    backups = Path.home()/'.kaardid-setup'
    show_backups(backups/'rehearsal-backups', 'kaart.dump', 'Rehearsal', 'Latest')
    show_backups(backups/'production-backups', 'kaart_prod.dump', 'Production', 'Production latest')
    print('  Off-VM/managed backups: not verified by this check; see PROJECT_STATUS.md.')


def show_backups(backups, filename, environment, latest_label):
    label = environment+' pre-deploy DB dumps on this VM'
    try:
        backups.stat()
    except FileNotFoundError:
        print('  '+label+': 0')
        print('  '+latest_label+': none found')
        return
    except OSError:
        print('  '+label+': UNKNOWN (unreadable)')
        return
    try:
        dumps = []
        for attempt in backups.iterdir():
            dump = attempt/filename
            try:
                info = dump.lstat()
            except (FileNotFoundError, NotADirectoryError):
                continue
            if stat.S_ISREG(info.st_mode):
                dumps.append((info.st_mtime, attempt.name))
        print('  '+label+': '+str(len(dumps)))
        print('  '+latest_label+': '+(max(dumps)[1] if dumps else 'none found'))
    except OSError:
        print('  '+label+': UNKNOWN (unreadable)')


if __name__ == '__main__':
    main()
