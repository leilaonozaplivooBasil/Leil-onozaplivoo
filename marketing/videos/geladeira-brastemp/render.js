// node render.js <fps> <segundos> <pastaFrames> [t1,t2,... para prévias]
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
(async()=>{
  const fps=+process.argv[2], dur=+process.argv[3], out=process.argv[4], only=process.argv[5];
  fs.mkdirSync(out,{recursive:true});
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+path.resolve(__dirname,'video.html')); await p.waitForTimeout(500);
  const times= only ? only.split(',').map(Number) : Array.from({length:Math.round(fps*dur)},(_,i)=>i/fps);
  for(let i=0;i<times.length;i++){
    await p.evaluate(t=>window.render(t),times[i]);
    await p.screenshot({path:path.join(out,String(i).padStart(4,'0')+'.jpg'),type:'jpeg',quality:92});
  }
  await b.close();
})();
