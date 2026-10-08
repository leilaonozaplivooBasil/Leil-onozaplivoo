// node render.js <pagina.html> <saida.png> [#hash]
const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.resolve(__dirname,process.argv[2])+(process.argv[4]||''));await p.waitForTimeout(500);
await p.screenshot({path:process.argv[3],omitBackground:true});await b.close();})();
