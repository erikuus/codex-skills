/* Usage: PLAYWRIGHT_MODULE=/path/to/playwright node verify-browser.cjs /path/to/yii-1.1.33-dev */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
(async () => {
  const framework = process.argv[2];
  if (!framework) throw new Error('Supply the Yii framework root');
  const root = path.resolve(__dirname, '../assets/app');
  const browser = await chromium.launch({headless:true, ...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {})});
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.setContent(`<main class="joyful-container"><form id="first">
      <select id="choice"><option value="a">A</option><option value="b">B</option></select>
      <div class="choice selected_a"><input name="a" value="one"><input name="locked" disabled></div>
      <div class="choice selected_b"><input name="b" value="two"></div>
      <div><input type="radio" name="radio" checked><div class="dynamic-content">first</div></div>
      <div><input type="radio" name="radio"><div class="dynamic-content">second</div></div>
    </form><form id="other"><div class="choice selected_b"><input name="unrelated"></div></form>
    <div id="grid-one"><a href="https://example.test/reorder?id=1" data-joyful-column="actions">up</a></div>
    <div id="grid-two"><a href="https://example.test/reorder?id=2" data-joyful-column="actions">up</a></div>
    <div class="joyful-detail"><table><tbody><tr><th>Name</th><td>Record</td></tr></tbody></table></div></main>`);
    await page.addStyleTag({content:fs.readFileSync(path.join(root,'themes/joyful/css/style.css'),'utf8')});
    await page.addScriptTag({path:path.join(framework,'web/js/source/jquery.js')});
    await page.addScriptTag({path:path.resolve(root,'../extensions/components/tailwind/assets/joyful.js')});
    await page.evaluate(() => {
      joyfulDropdown({form:'first',input:'choice',area:'choice'});
      joyfulDropdown({form:'first',input:'choice',area:'choice'});
      joyfulToggle({form:'first',type:'radio',container:'dynamic-container',content:'dynamic-content',inline:'inline'});
    });
    assert.deepEqual(await page.evaluate(() => $('#first').serializeArray().map(x=>x.name)),['a','radio']);
    await page.selectOption('#choice','b');
    assert.deepEqual(await page.evaluate(() => $('#first').serializeArray().map(x=>x.name)),['b','radio']);
    await page.selectOption('#choice','a');
    assert.equal(await page.locator('[name=locked]').isDisabled(),true);
    assert.equal(await page.locator('[name=unrelated]').isDisabled(),false);
    await page.locator('input[type=radio]').nth(1).check();
    assert.equal(await page.locator('.dynamic-content').nth(0).isVisible(),false);
    assert.equal(await page.locator('.dynamic-content').nth(1).isVisible(),true);
    await page.evaluate(() => {
      window.requests=[]; window.updates=[];
      $.fn.yiiGridView={update:id=>updates.push(id)};
      $.ajax=options=>{requests.push(options);return $.Deferred().resolve().promise();};
      const setup = grid => joyfulGridAction({grid,column:'actions',data:{TOKEN:'fixture-token'},errorMessage:'Failed'});
      setup('grid-one'); setup('grid-one'); setup('grid-two');
      $('#grid-one').html('<a href="https://example.test/reorder?id=3" data-joyful-column="actions">replacement</a>');
    });
    await page.locator('#grid-one a').click();
    assert.deepEqual(await page.evaluate(() => updates),['grid-one']);
    assert.equal(await page.evaluate(() => requests.length),1);
    assert.equal(await page.evaluate(() => requests[0].type),'POST');
    assert.deepEqual(await page.evaluate(() => requests[0].data),{TOKEN:'fixture-token'});
    await page.locator('#grid-two a').click();
    assert.deepEqual(await page.evaluate(() => updates),['grid-one','grid-two']);
    await page.evaluate(() => {
      window.alerts=[];window.failures=0;window.alert=message=>alerts.push(message);
      $('#grid-one').on('joyful:action-error',()=>failures++);
      $.ajax=()=>$.Deferred().reject({status:500}).promise();
    });
    await page.locator('#grid-one a').click();
    assert.deepEqual(await page.evaluate(() => alerts),['Failed']);
    assert.equal(await page.evaluate(() => failures),1);
    assert.equal(await page.locator('#grid-one a').getAttribute('aria-busy'),null);
    await page.evaluate(() => { $('#grid-one').remove(); $.ajax=()=>$.Deferred().resolve().promise(); });
    await page.locator('#grid-two a').click();
    assert.deepEqual(await page.evaluate(() => updates),['grid-one','grid-two','grid-two']);
    for (const width of [390,768,1440]) {
      await page.setViewportSize({width,height:900});
      assert.equal(await page.locator('th').isVisible(),true);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth<=innerWidth),true);
    }
    assert.deepEqual(errors,[]);
    console.log('PASS browser: dependent fields, disabled state, form scoping, radio toggles, grid scoping, AJAX replacement, duplicate binding, POST/CSRF, failures, responsive detail labels');
  } finally {
    await browser.close();
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
