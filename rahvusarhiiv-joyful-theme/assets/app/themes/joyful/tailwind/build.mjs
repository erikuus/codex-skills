import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
const dir = path.dirname(fileURLToPath(import.meta.url));
const app = path.resolve(dir, '../../..');
const args = process.argv.slice(2);
let extensions = process.env.JOYFUL_EXTENSIONS_ROOT;
const extra = [];
let watch = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--watch') watch = true;
  else if (args[i] === '--extensions-root' && args[i + 1]) extensions = args[++i];
  else if (args[i] === '--source' && args[i + 1]) extra.push(path.resolve(args[++i]));
  else throw new Error('Unknown/incomplete argument: ' + args[i]);
}
if (!extensions) throw new Error('Pass --extensions-root with Yii::getPathOfAlias("ext"); never assume its location.');
extensions = path.resolve(extensions);
if (!fs.existsSync(path.join(extensions, 'components/tailwind/XTActiveForm.php'))) throw new Error('No Tailwind components in selected extension root.');
const candidates = [
  path.resolve(dir, '../views'), path.resolve(dir, '../js'),
  ...['views','portlets','components','widgets','modules'].map(p => path.join(app, 'protected', p)),
  ...['components/tailwind','widgets','modules'].map(p => path.join(extensions,p)), ...extra
];
const sources = [...new Set(candidates.filter(p => fs.existsSync(p)).map(p => fs.realpathSync(p)))];
const relative = p => path.relative(dir,p).split(path.sep).join('/');
fs.writeFileSync(path.join(dir, 'sources.generated.css'), '/* Generated local paths; do not commit. */\n' + sources.map(p => '@source ' + JSON.stringify(relative(p) + '/**/*.{php,html,js}') + ';').join('\n') + '\n');
const cli = path.join(dir, 'node_modules/@tailwindcss/cli/dist/index.mjs');
if (!fs.existsSync(cli)) throw new Error('Run npm ci in themes/joyful/tailwind first.');
const command = ['--input',path.join(dir,'input.css'),'--output',path.resolve(dir,'../css/style.css')];
command.push(watch ? '--watch' : '--minify');
const result=spawnSync(process.execPath,[cli,...command],{cwd:dir,stdio:'inherit'});
if(result.error) throw result.error;
process.exitCode=result.status ?? 1;
