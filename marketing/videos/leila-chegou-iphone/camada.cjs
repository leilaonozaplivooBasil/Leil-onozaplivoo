const { chromium } = require('/home/user/leilonozap/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const c of process.argv.slice(2)){await p.goto('file://'+__dirname+'/camadas.html?c='+c);await p.waitForTimeout(400);await p.screenshot({path:__dirname+'/camadas/'+c+'.png',omitBackground:true});}
await b.close();})();
