#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

if ! command -v rg >/dev/null 2>&1; then
  echo "ripgrep (rg) is required" >&2
  exit 1
fi

if [[ ! -d "$ROOT" ]]; then
  echo "Path not found: $ROOT" >&2
  exit 1
fi

ROOT="$(cd "$ROOT" && pwd)"

echo "# Yii 1.1.32 Upgrade Surface Scan"
echo
printf -- '- root: `%s`\n' "$ROOT"
echo

echo "## 1) Hard-coded Yii framework paths"
rg -n 'yii-1\.1\.8|yii-1\.1\.[0-9]+' "$ROOT"/index*.php "$ROOT"/cron.php "$ROOT"/protected/tests/bootstrap.php -S || true
echo

echo "## 2) jQuery deprecated APIs in app/wrapper code"
rg -n '\.live\(|\.die\(|\.andSelf\(|\$\.browser|\.size\(' \
  "$ROOT"/js "$ROOT"/protected \
  -S --glob '!**/*.min.js' --glob '!**/assets/**' || true
echo

echo "## 3) Legacy delegated/event APIs in app/wrapper code"
rg -n '\.bind\(|\.unbind\(|\.delegate\(|\.undelegate\(' \
  "$ROOT"/js "$ROOT"/protected \
  -S --glob '!**/*.min.js' --glob '!**/assets/**' || true
echo

echo "## 4) Yii jQuery UI wrappers and custom themes"
rg -n "CJui|jquery\.ui|registerCoreScript\('jquery\.ui'\)|ui-tabs-selected|ui-state-default|jui" \
  "$ROOT"/protected "$ROOT"/css "$ROOT"/js -S || true
echo

echo "## 5) Legacy JS plugin assets present"
find "$ROOT"/protected/extensions "$ROOT"/js -type f \( \
  -name 'jquery.fancybox-1.3.4.js' -o \
  -name 'jquery.fancybox-1.3.4.pack.js' -o \
  -name 'select2.js' -o \
  -name 'select2.min.js' -o \
  -name 'mootools-core-*.js' -o \
  -name 'mootools-more-*.js' -o \
  -name 'iipmooviewer-*.js' -o \
  -name 'jquery.scrollUp.js' \
\) | sort || true
echo

echo "## 6) PHP 5-era compatibility risks (PHP files only)"
rg -n 'create_function\(|split\(|ereg\(|mysql_|mcrypt|set_magic_quotes_runtime|get_magic_quotes_gpc|\$HTTP_RAW_POST_DATA|preg_replace\s*\(.*?/e' \
  "$ROOT" --glob '**/*.php' -S || true
echo

echo "## 7) Yii compatibility hotspots (PHP files only)"
rg -n 'CGridView|CActiveForm|CClientScript|CJavaScript::encode|CJSON::encode|CDbMigration|safeUp|safeDown' \
  "$ROOT" --glob '**/*.php' -S || true
