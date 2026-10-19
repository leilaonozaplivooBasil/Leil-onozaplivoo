const { chromium } = require('/home/user/leilonozap/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(700);
await p.screenshot({path:process.argv[3]});await b.close();})();
