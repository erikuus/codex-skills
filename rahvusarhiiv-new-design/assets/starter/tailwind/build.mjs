import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
const dir = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const sources = [];
let watch = false;
let output = path.resolve(dir, '../css/style.css');
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--watch') watch = true;
  else if (args[i] === '--source' && args[i + 1]) {
    const source = fs.realpathSync(path.resolve(args[++i]));
    const suffix = fs.statSync(source).isDirectory() ? '/**/*.{html,php,js,ts,jsx,tsx,vue,svelte,twig,erb,heex,eex}' : '';
    sources.push(path.relative(dir, source).split(path.sep).join('/') + suffix);
  } else if (args[i] === '--out' && args[i + 1]) output = path.resolve(args[++i]);
  else throw new Error('Unknown or incomplete argument: ' + args[i]);
}
if (!sources.length) throw new Error('Supply --source for the actual template/script directories or individual rendering files.');
const cli = path.join(dir, 'node_modules/@tailwindcss/cli/dist/index.mjs');
if (!fs.existsSync(cli)) throw new Error('Run npm ci in this Tailwind directory first.');
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(path.join(dir, 'sources.generated.css'), '/* Generated local paths; do not commit. */\n' + [...new Set(sources)].map(source => '@source ' + JSON.stringify(source) + ';').join('\n') + '\n');
const command = [cli, '--input', path.join(dir, 'input.css'), '--output', output, watch ? '--watch' : '--minify'];
const result = spawnSync(process.execPath, command, { cwd: dir, stdio: 'inherit' });
if (result.error) throw result.error;
process.exitCode = result.status ?? 1;
