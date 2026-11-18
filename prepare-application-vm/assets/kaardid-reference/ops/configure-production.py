#!/usr/bin/env python3
"""Prepare private production JSON only; never activate code or scheduled jobs."""
import argparse
import grp
import json
import os
from pathlib import Path
import pwd
import secrets
import stat
import tempfile


def private_json(path, uid, gid=None):
    info=path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_uid!=uid or info.st_mode&0o027
            or (gid is not None and info.st_gid!=gid)):
        raise ValueError('Unexpected private file ownership/type/permissions: '+str(path))
    value=json.loads(path.read_text())
    if not isinstance(value,dict):
        raise ValueError('Expected a private JSON object; values omitted.')
    return value


def write_new(path, value, gid):
    if path.exists() or path.is_symlink():
        raise ValueError('Refusing to overwrite private configuration: '+str(path))
    descriptor,temporary=tempfile.mkstemp(prefix='.production-config-',dir=path.parent)
    try:
        with os.fdopen(descriptor,'w') as output:
            os.fchown(output.fileno(),-1,gid)
            os.fchmod(output.fileno(),0o640)
            json.dump(value,output,indent=2);output.write('\n')
        # Publish without replacing a file created by another operator.
        os.link(temporary,path,follow_symlinks=False)
    finally:
        Path(temporary).unlink(missing_ok=True)


def configure(directory, template, gid, vau_source=None):
    info=directory.lstat();uid=os.geteuid()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid!=uid
            or info.st_gid!=gid or info.st_mode&0o027):
        raise ValueError('Production config directory has unexpected ownership/permissions.')
    if (template.get('environment')!='production' or template.get('databaseFile')!='/etc/kaardid-production/app-db.json'
            or template.get('migrationDatabaseFile')!='/home/erik/.config/kaardid/production-migration-db.json'
            or template.get('externalCallbackBaseUrl')!='https://kaardid.ra.ee'):
        raise ValueError('Unexpected production template; no configuration changed.')
    environment=directory/'environment.json'
    integrations=directory/'integrations.json'
    settings=private_json(environment,uid,gid) if environment.exists() or environment.is_symlink() else template
    if any(settings.get(key)!=value for key,value in template.items()):
        raise ValueError('Existing production settings differ; review privately instead of overwriting.')
    values=None
    if integrations.exists() or integrations.is_symlink():
        values=private_json(integrations,uid,gid)
        if any(not isinstance(values.get(key),str) or not values[key] or values[key].startswith('REPLACE_')
               for key in ('vauValidationKey','imageSignatureSecret')):
            raise ValueError('Existing production integration keys are incomplete; values omitted.')
    elif vau_source is not None:
        source=private_json(vau_source,uid)
        key=source.get('vauValidationKey')
        if not isinstance(key,str) or not key or key.startswith('REPLACE_'):
            raise ValueError('Existing VAU key is unavailable; values omitted.')
        # Only the explicitly chosen external VAU key crosses environments.
        # Database credentials, Gii and the rehearsal image secret are not copied.
        values={'vauValidationKey':key,'imageSignatureSecret':secrets.token_hex(32),'sentryDsn':None}
    created=[]
    if not environment.exists():
        write_new(environment,settings,gid);created.append(environment.name)
    if values is not None and not integrations.exists():
        write_new(integrations,values,gid);created.append(integrations.name)
    return {'created':created,'environmentReady':True,'integrationsReady':values is not None,
            'sentryConfigured':bool(values and values.get('sentryDsn'))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse-existing-vau-key',action='store_true',
                        help='explicitly reuse the existing Kaardid VAU key; generate an independent image key')
    parser.add_argument('template',type=Path)
    args=parser.parse_args()
    os.umask(0o077)
    import subprocess
    if (pwd.getpwuid(os.geteuid()).pw_name!='erik'
            or subprocess.check_output(['hostname','-f'],text=True).strip()!='kaardid.arhiiv.ee'):
        raise SystemExit('Run as erik on the Kaardid VM only.')
    current=Path('/srv/kaardid-production/current')
    if current.exists() or current.is_symlink():
        raise SystemExit('Production is already active; this preparation helper refuses live changes.')
    directory=Path('/srv/kaardid-production/shared/config')
    source=Path('/srv/kaardid/shared/config/integrations.json') if args.reuse_existing_vau_key else None
    result=configure(directory,json.loads(args.template.read_text()),grp.getgrnam('kaardid-production').gr_gid,source)
    print(json.dumps(result))
    print('No activation, database writes, migrations, nginx changes or timer changes performed.')
    print('KAARDID_PRODUCTION_CONFIG_PREPARED' if result['integrationsReady']
          else 'KAARDID_PRODUCTION_ENVIRONMENT_PREPARED — VAU key choice still required')


if __name__=='__main__':main()
