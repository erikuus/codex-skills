#!/usr/bin/env bash
# Read-only heuristic scan. Hits need review; no matches does not prove compatibility.
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 || ( $# -eq 2 && "$2" != --include-vendor ) ]]; then
  echo "Usage: $0 <app-root> [--include-vendor]" >&2
  exit 2
fi
command -v rg >/dev/null 2>&1 || { echo 'ripgrep (rg) is required' >&2; exit 2; }
[[ -d "$1" ]] || { echo "Directory not found: $1" >&2; exit 2; }
scan_root="$(cd -- "$1" && pwd)"
scan_args=(--no-ignore --hidden --color never --line-number
  --glob '!**/.git/**' --glob '!**/node_modules/**'
  --glob '!**/runtime/**' --glob '!**/assets/**' --glob '!**/cache/**'
  --glob '!**/*.min.js' --glob '!**/yii-1.1.*/**')
if [[ "${2:-}" != --include-vendor ]]; then
  scan_args+=(--glob '!**/vendor/**')
fi

scan() {
  local title="$1" pattern="$2" status
  shift 2
  printf '\n## %s\n' "$title"
  # rg resolves competing globs in order: exclusions must follow file types.
  if rg "$@" "${scan_args[@]}" -- "$pattern" "$scan_root"; then
    :
  else
    status=$?
    if [[ $status -eq 1 ]]; then
      echo '(no heuristic matches)'
    else
      echo "Scan failed (rg exit $status); results are incomplete." >&2
      exit "$status"
    fi
  fi
}

printf '# Yii 1.1.33-dev / PHP 8.5 upgrade surface\nRoot: %s\n' "$scan_root"
printf 'Heuristics only. Generated assets, runtime/cache, node_modules and versioned Yii directories are excluded.\n'
printf 'Vendor inclusion: %s. Follow external/symlinked extension paths separately.\n' "${2:-excluded}"

scan 'Framework entrypoints and test bridges' 'yii-1\.1\.|yii(lite|t)?\.php|PHPUnit_Framework_|PHPUnit_Runner_|CTestCase|CDbTestCase|CWebTestCase' \
  --glob '*.php' --glob '*.json' --glob '*.xml' --glob '*.yml' --glob '*.yaml' --glob '*.sh'
scan 'PHP 8.4: nullable signatures (single-line heuristic)' '(array|callable|[A-Za-z_\\][A-Za-z0-9_\\]*)\s+&?\$[A-Za-z_][A-Za-z0-9_]*\s*=\s*null' --glob '*.php'
scan 'PHP 8.4: sessions, CSV and error handling' 'E_STRICT|E_USER_ERROR|session_set_save_handler|session\.(sid_length|sid_bits_per_character|use_only_cookies|use_trans_sid|trans_sid_tags|trans_sid_hosts|referer_check)|\bSID\b|\b(fgetcsv|fputcsv|str_getcsv|setCsvControl)\s*\(' --glob '*.php' --glob '*.ini'
scan 'PHP 8.4: extension/API review' 'ReflectionMethod|stream_context_set_option|xml_set_object|xml_set_.*handler|mysqli_(ping|kill|refresh)|pg_(fetch_result|field_prtlen|field_is_null)|IntlCalendar|IntlGregorianCalendar|is_resource\s*\(' --glob '*.php'
scan 'PHP 8.5: cast syntax candidates (inspect strings/comments)' '\(\s*(boolean|integer|double|binary)\s*\)' --glob '*.php'
scan 'PHP 8.5: cleanup, reflection and other deprecated APIs' '\b(curl_close|curl_share_close|finfo_close|imagedestroy|xml_parser_free|socket_set_timeout|mysqli_execute)\s*\(|setAccessible\s*\(|\$http_response_header|SplObjectStorage|ArrayObject|ArrayIterator|__debugInfo|__sleep|__wakeup|ob_start|\b(chr|ord|readdir|rewinddir|closedir)\s*\(' --glob '*.php'
scan 'PHP 8.5: switch labels/backticks (review syntax)' '(^|[;{}[:space:]])(case\b[^;]*|default)[[:space:]]*;|`' --glob '*.php'
scan 'PHP 8.5: array keys and destructuring candidates' '\[\s*null\s*\]|array_key_exists\s*\(|\blist\s*\(|getPrimaryKey\s*\(|getId\s*\(' --glob '*.php'
scan 'PDO drivers and PHP runtime configuration' 'PDO::(MYSQL_|PGSQL_|SQLITE_|DBLIB_|ODBC_|FB_|FETCH_)|->(pgsql[A-Z][A-Za-z]*|sqliteCreate[A-Za-z]*)\s*\(|pdoClass|uri:|zend_extension.*opcache|disable_classes|report_memleaks|register_argc_argv|intl\.error_level' --glob '*.php' --glob '*.ini' --glob '*.conf' --glob '*.json'
scan 'Older PHP blockers and nullable filters' '\b(create_function|each|split|ereg|mysql_[A-Za-z_]+|mcrypt_[A-Za-z_]+|get_magic_quotes_gpc|set_magic_quotes_runtime)\s*\(|\$HTTP_RAW_POST_DATA|\b(trim|strip_tags|mb_strlen)\s*\(|["\x27]filter["\x27]\s*=>' --glob '*.php'
scan 'Legacy frontend APIs and Yii integration' '\.(live|die|andSelf|size|bind|unbind|delegate|undelegate)\s*\(|\$\.browser|CJui|ui-front|ui-tabs-selected|radioButtonList|checkBoxList|scriptMap|fancybox|select2|CHtmlPurifier|HTMLPurifier' --glob '*.php' --glob '*.js' --glob '*.css'

printf '\n## Plugin asset filenames (including asset directories)\n'
if rg --files --no-ignore --hidden --glob '*fancybox*' --glob '*select2*' --glob '*jquery*' \
  --glob '!**/.git/**' --glob '!**/node_modules/**' -- "$scan_root"; then
  :
else
  status=$?
  [[ $status -eq 1 ]] || exit "$status"
fi
