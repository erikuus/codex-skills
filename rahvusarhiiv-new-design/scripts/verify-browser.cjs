const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
(async()=>{
 const root=path.resolve(__dirname,'..');const starter=path.join(root,'assets/starter');
 const html=fs.readFileSync(path.join(starter,'preview.html'),'utf8');
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
 try {
  const pages=[];
  for(const legacy of [true,false]){
   const page=await browser.newPage();
   await page.route('http://design.local/**',async route=>{
    const url=new URL(route.request().url());
    if(url.pathname==='/'){
     let markup=html;
     if(legacy)for(const variant of ['first','last','odd','hover'])for(const el of ['tr','th','td'])markup=markup.replaceAll('prose-'+el+':'+variant+':',variant+':prose-'+el+':');
     return route.fulfill({contentType:'text/html',body:markup});
    }
    let file=path.resolve(starter,'.'+decodeURIComponent(url.pathname));
    if(legacy&&url.pathname==='/css/style.css')file=path.join(root,'assets/reference/vau-frozen.css');
    if(legacy&&url.pathname.startsWith('/css/fonts/'))file=path.join(starter,'fonts',path.basename(url.pathname));
    if(!file.startsWith(starter+path.sep)&&file!==path.join(root,'assets/reference/vau-frozen.css'))return route.abort();
    if(!fs.existsSync(file))return route.abort();
    return route.fulfill({path:file});
   });
   await page.goto('http://design.local/');await page.evaluate(()=>document.fonts.ready);pages.push(page);
  }
  const approvedGradient=await pages[0].evaluate(()=>{const el=document.createElement('div');el.className='bg-theme-ais';document.body.append(el);const value=getComputedStyle(el).backgroundImage;el.remove();return value;});
  assert.notEqual(approvedGradient,'none');
  async function metrics(page){return page.evaluate(()=>{
   const css=s=>getComputedStyle(document.querySelector(s));
   const color=value=>{const canvas=document.createElement('canvas');canvas.width=canvas.height=1;const ctx=canvas.getContext('2d');ctx.fillStyle=value;ctx.fillRect(0,0,1,1);return [...ctx.getImageData(0,0,1,1).data];};
   const rect=s=>{const r=document.querySelector(s).getBoundingClientRect();return {x:r.x,right:r.right,width:r.width,y:r.y};};
   const shadow=s=>css(s).boxShadow.replaceAll('rgba(0, 0, 0, 0) 0px 0px 0px 0px, ','');
   return {headers:[...document.querySelectorAll('header')].map(el=>el.getBoundingClientRect().height),main:rect('main'),bodyFont:css('body').fontFamily,gradient:css('.bg-theme-vau').backgroundImage,radius:css('body>div').borderBottomLeftRadius,shellShadow:shadow('body>div'),tableShadow:shadow('#table-surface'),tableHeader:css('#records-table th').fontSize,cellPadding:css('#records-table td').paddingTop,stripe:css('#records-table tbody tr').backgroundColor,cellRadius:css('#records-table td').borderTopLeftRadius,icon:rect('#records-table td svg').width,detailBg:color(css('#detail-table').backgroundColor),detailPadding:css('#detail-table td').paddingTop,footerHeight:document.querySelector('footer').getBoundingClientRect().height,footerDividers:[...document.querySelectorAll('footer > div > .divide-gray-700 > div')].map(el=>{const c=getComputedStyle(el);return [el.getBoundingClientRect().height,c.borderTopWidth,c.borderLeftWidth,c.borderRightWidth,c.borderBottomWidth,c.borderColor];})};
  });}
  for(const width of [390,768,1024,1440,1600]){
   for(const page of pages)await page.setViewportSize({width,height:1000});
   const expected=await metrics(pages[0]),actual=await metrics(pages[1]);
   for(const key of Object.keys(expected))assert.deepEqual(actual[key],key==='gradient'?approvedGradient:expected[key],key+' at '+width);
   const bounds=await pages[1].evaluate(()=>{
    const box=s=>{const r=document.querySelector(s).getBoundingClientRect();return {x:r.x,right:r.right,width:r.width,y:r.y};};
    return {detail:box('#detail'),detailTable:box('#detail-table'),detailLabel:box('#detail-table th'),detailLabelBottom:getComputedStyle(document.querySelector('#detail-table th')).paddingBottom,detailTitle:box('#detail>div'),form:box('#form-example'),formTitle:box('#form-example>div'),labelVisible:getComputedStyle(document.querySelector('#detail-table th')).display!=='none',range:[box('#example-start'),box('#example-end')],fieldGap:document.querySelector('label[for=example-width]').getBoundingClientRect().top-document.querySelector('#example-start').getBoundingClientRect().bottom,unit:box('#example-width'),overflow:document.documentElement.scrollWidth>innerWidth};
   });
   assert.ok(bounds.detail.width<=736);assert.ok(bounds.form.width<=576);
   assert.equal(bounds.detail.x,bounds.detailTitle.x);assert.equal(bounds.detail.right,bounds.detailTitle.right);
   assert.equal(bounds.form.x,bounds.formTitle.x);assert.equal(bounds.form.right,bounds.formTitle.right);
   if(width<768){assert.equal(bounds.detailLabel.width,bounds.detailTable.width);assert.equal(bounds.detailLabelBottom,'0px');}assert.equal(bounds.labelVisible,true);assert.equal(bounds.overflow,false);
   assert.equal(bounds.range[0].width,96);assert.equal(bounds.range[1].width,96);assert.equal(bounds.range[0].y,bounds.range[1].y);assert.equal(bounds.unit.width,112);assert.ok(bounds.fieldGap>=24,'field gap at '+width);
   console.log('PASS source design and HTML layout at '+width+'px');
  }
  const page=pages[1];
  await page.locator('#records-table tbody tr').first().hover();
  assert.equal(await page.locator('#records-table tbody tr').first().evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(233, 247, 238)');
  await page.mouse.move(0,0);
  assert.equal(await page.locator('#secondary-button').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(255, 255, 255)');
  await page.locator('#secondary-button').hover();
  assert.equal(await page.locator('#secondary-button').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(232, 235, 240)');
  await page.evaluate(()=>{window.feedbackCalls=[];window.open=(...args)=>window.feedbackCalls.push(args);});
  await page.getByRole('button',{name:'Tagasiside',exact:true}).click();
  assert.equal(await page.evaluate(()=>feedbackCalls[0][0]),'https://www.ra.ee/vau/index.php/helpdesk/message/feedback?language=et&dialog=1&url=');
  await page.setViewportSize({width:768,height:1000});
  const opener=page.locator('[data-ra-open]');
  await opener.click();assert.equal(await opener.getAttribute('aria-expanded'),'true');
  assert.equal(await page.evaluate(()=>document.documentElement.style.overflow),'hidden');
  // Native modal navigation can visit browser chrome (reported as body), never a background control.
  for(let i=0;i<6;i++){await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement===document.body||document.querySelector('dialog').contains(document.activeElement)),true);}
  await page.evaluate(()=>document.querySelector('#example-name').focus());
  assert.equal(await page.locator('#example-name').evaluate(el=>el===document.activeElement),false);
  await page.locator('[data-ra-close]').focus();
  await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.querySelector('dialog').open && document.querySelector('[data-ra-open]').getAttribute('aria-expanded')==='false');
  assert.equal(await opener.getAttribute('aria-expanded'),'false');assert.equal(await opener.evaluate(el=>el===document.activeElement),true);
  await opener.click();await page.locator('[data-ra-close]').click();await page.waitForFunction(()=>!document.querySelector('dialog').open && document.querySelector('[data-ra-open]').getAttribute('aria-expanded')==='false');
  await opener.click();await page.mouse.click(10,500);await page.waitForFunction(()=>!document.querySelector('dialog').open && document.querySelector('[data-ra-open]').getAttribute('aria-expanded')==='false');
  await opener.click();await page.setViewportSize({width:1440,height:1000});await page.waitForFunction(()=>!document.querySelector('dialog').open && document.querySelector('[data-ra-open]').getAttribute('aria-expanded')==='false');
  assert.equal(await page.evaluate(()=>document.documentElement.style.overflow),'');
  console.log('PASS row/secondary hover, exact footer action and drawer dismissal/resize/focus');
  if(process.env.RA_SCREENSHOT_DIR){fs.mkdirSync(process.env.RA_SCREENSHOT_DIR,{recursive:true});for(const width of [390,1440]){await page.setViewportSize({width,height:1000});await page.screenshot({path:path.join(process.env.RA_SCREENSHOT_DIR,'html-'+width+'.png'),fullPage:true});}}
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
