#!/usr/bin/env python3
"""Stage Joyful theme and shared extensions separately; refuse every conflict."""
import argparse
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('app', type=Path)
    parser.add_argument('--extensions-root', type=Path, required=True,
                        help='The resolved Yii ext alias directory (not its components directory)')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    skill = Path(__file__).resolve().parents[1]
    app = args.app.resolve()
    extensions = args.extensions_root.resolve()
    if not (app / 'protected').is_dir():
        parser.error('Target must contain protected/')
    if not extensions.is_dir():
        parser.error('Resolve an existing ext alias directory before staging')
    if extensions == app or extensions == app / 'protected/components':
        parser.error('Use the extension root, not the application/component directory')
    planned, conflicts, identical = [], [], 0
    for source, target in [(skill / 'assets/app', app), (skill / 'assets/extensions', extensions)]:
        for path in sorted(source.rglob('*')):
            if (not path.is_file() or 'node_modules' in path.parts
                    or path.name == 'sources.generated.css'
                    or path.relative_to(source).as_posix() == 'themes/joyful/css/style.css'):
                continue
            dest = target / path.relative_to(source)
            if not dest.resolve().is_relative_to(target):
                conflicts.append(str(dest) + ' (symlink escapes declared destination)')
            elif dest.exists():
                if not dest.is_file() or dest.read_bytes() != path.read_bytes():
                    conflicts.append(str(dest))
                else:
                    identical += 1
            else:
                planned.append((path, dest))
    print(f'{len(planned)} missing; {identical} identical; {len(conflicts)} conflicts')
    print('Theme destination:', app / 'themes/joyful')
    print('Shared component destination:', extensions / 'components/tailwind')
    if conflicts:
        for entry in conflicts:
            print('CONFLICT ' + entry)
        print('Nothing copied. Inspect existing/shared consumers and merge deliberately.')
        return 1
    if args.apply:
        for source, dest in planned:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
        print('Copied. Configure ext.components.tailwind.*, build Tailwind CSS, and complete the application integration.')
    else:
        for _, dest in planned:
            print('COPY ' + str(dest))
        print('Preview only. --apply copies files; it does not change aliases, config, menus or existing views.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
