// node render.js "<hash>" saida.png
const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.resolve(__dirname,'banner.html')+'#'+process.argv[2]);await p.waitForTimeout(600);
await p.screenshot({path:process.argv[3]});await b.close();})();
