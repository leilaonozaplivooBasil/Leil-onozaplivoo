// node render.js <pagina.html> <saida.png> <largura> <altura> [escala]
const { chromium } = require('playwright'); const path=require('path');
(async()=>{const [pg,out,w,h,s]=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:+(s||1)});
const [f,hs]=pg.split('#');await p.goto('file://'+path.resolve(__dirname,f)+(hs?'#'+hs:''));await p.waitForTimeout(600);
await p.screenshot({path:out});await b.close();})();
