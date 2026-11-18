#!/usr/bin/env python3
"""Build the pushed commit and an identified local Yii snapshot for rehearsal."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile

os.umask(0o027)
repo=Path(__file__).resolve().parent.parent
if len(sys.argv)!=2 or not Path(sys.argv[1]).is_dir():
    raise SystemExit('Usage: build-release.py <private output directory>')
output=Path(sys.argv[1]).resolve()
def git(*arguments):
    return subprocess.check_output(['git','-C',str(repo),*arguments],text=True).strip()
commit=git('rev-parse','HEAD')
remote_heads=git('ls-remote','--heads','origin').splitlines()
if not any(line.split()[0]==commit for line in remote_heads):
    raise SystemExit('Current HEAD is not a pushed branch head on origin.')
release=output/commit
if release.exists():
    raise SystemExit('Release output already exists; refusing to replace it.')
app=release/'apps/kaardid';app.mkdir(parents=True)
archive=output/'app-source.tar'
subprocess.run(['git','-C',str(repo),'archive','--format=tar','--output='+str(archive),commit],check=True)
with tarfile.open(archive) as source:
    source.extractall(app,filter='data')
archive.unlink()
# PHP configuration is the same tracked source on Mac and VM. Private JSON is
# never packaged; the deployment links this empty directory to server settings.
private=app/'protected/config/private'
if private.exists() or private.is_symlink():
    raise SystemExit('Private configuration must not be tracked or included in a release.')
for name in ['docs','protected/tests','bin','ops','.github','.codex','test-results']:
    path=app/name
    if path.is_dir():shutil.rmtree(path)
for name in ['index-dev.php','index-test.php','dev-router.php','phpunit.xml','playwright.config.js','package.json','package-lock.json','README.md','learnings.md','AGENTS.md','PROJECT_STATUS.md']:
    (app/name).unlink(missing_ok=True)
for name in ['assets','upload','protected/runtime','protected/migrations','protected/config/private']:
    (app/name).mkdir(parents=True,exist_ok=True)
# No cron job is installed or scheduled by this builder.
framework=repo.parent.parent/'yii/yii-1.1.33-dev'
shutil.copytree(framework,release/'yii/yii-1.1.33-dev',ignore=shutil.ignore_patterns('.git','.DS_Store','__pycache__'))
# Web and console profiles both use apps/kaardid/protected/extensions.
composer=['php',str(repo/'protected/tests/composer.phar'),'install','--working-dir='+str(app),
    '--no-dev','--prefer-dist','--no-interaction','--no-progress','--no-scripts','--no-plugins','--optimize-autoloader']
with (output/'composer-build.log').open('w') as log:
    if subprocess.run(composer,stdout=log,stderr=log).returncode:
        raise SystemExit('Production dependency installation failed; inspect the private build log.')
framework_digest=hashlib.sha256()
for path in sorted((release/'yii/yii-1.1.33-dev').rglob('*')):
    if path.is_file():
        framework_digest.update(str(path.relative_to(release)).encode()+b'\0'+hashlib.sha256(path.read_bytes()).digest())
manifest={'commit':commit,'purpose':'private-rehearsal','source_repository':git('remote','get-url','origin'),
    'yii_content_sha256':framework_digest.hexdigest(),'console_extensions':'app-owned',
    'composer_lock_sha256':hashlib.sha256((app/'composer.lock').read_bytes()).hexdigest(),
    'dependencies':'composer install --no-dev --no-scripts --no-plugins','config_templates':'protected/config',
    'private_config':'separate server files; excluded from this artifact'}
config_digest=hashlib.sha256()
for path in sorted((app/'protected/config').glob('*.php')):
    config_digest.update(path.name.encode()+b'\0'+hashlib.sha256(path.read_bytes()).digest())
manifest['config_templates_sha256']=config_digest.hexdigest()
(release/'release.json').write_text(json.dumps(manifest,indent=2)+'\n')
for path in (app/'protected/config').glob('*.php'):
    subprocess.run(['php','-l',str(path)],check=True,capture_output=True)
# Runtime accounts may read code; only the deployment owner may change it.
for path in [release,*release.rglob('*')]:
    if path.is_symlink():
        continue
    path.chmod(0o2750 if path.is_dir() else (0o750 if path.stat().st_mode & 0o111 else 0o640))
bundle=output/(commit+'.tar.gz')
with tarfile.open(bundle,'w:gz') as target:
    target.add(release,arcname=commit)
manifest['artifact_sha256']=hashlib.file_digest(bundle.open('rb'),'sha256').hexdigest()
(output/'release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'commit':commit,'artifact':str(bundle),'artifact_sha256':manifest['artifact_sha256'],
    'yii_content_sha256':manifest['yii_content_sha256']},indent=2))
