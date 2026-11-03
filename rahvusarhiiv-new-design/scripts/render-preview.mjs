import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = name => fs.readFileSync(path.join(root, 'assets/html', name), 'utf8');
const html = read('shell.html').replace('<!-- CONTENT -->', () => read('components.html')).replace('<!-- FOOTER -->', () => read('footer.html'));
const output = path.join(root, 'assets/starter/preview.html');
fs.writeFileSync(output, html);
console.log(output);
