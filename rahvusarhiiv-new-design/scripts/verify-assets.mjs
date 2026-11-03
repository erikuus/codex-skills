import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=name=>fs.readFileSync(path.join(root,name),'utf8');
const manifest=JSON.parse(read('references/retained-assets.json'));
for(const [name,hash] of Object.entries(manifest.sha256)){
 assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,name))).digest('hex'),hash,name+' differs from retained baseline');
}
const source=read('assets/reference/advanced-layout-alt.html');
const start=source.indexOf('    <!-- Neljas valge ala -->');
const end=source.indexOf('  </body>',start);
assert.ok(start>=0&&end>start);
assert.equal(read('assets/html/footer.html'),source.slice(start,end),'exact footer subtree');
const preview=read('assets/starter/preview.html');
assert.ok(!preview.includes('<!-- CONTENT -->')&&!preview.includes('<!-- FOOTER -->'),'preview assembled');
for(const name of ['shell','components','footer'])assert.ok(!read('assets/html/'+name+'.html').includes('<?'),'plain HTML specimen: '+name);
assert.ok(!fs.existsSync(path.join(root,'assets/extensions')),'no framework component payload');
console.log('PASS retained source assets, exact footer, plain HTML and preview assembly');
