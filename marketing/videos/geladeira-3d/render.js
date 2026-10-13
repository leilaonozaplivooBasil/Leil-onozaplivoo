// node render.js <v1|v2|v3> <fps> <segundos> <pastaFrames> [t1,t2,... para prévias]
// Serve a pasta via HTTP local (módulos ES) e usa WebGL por SwiftShader no Chromium headless.
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs'); const http=require('http');
const types={'.html':'text/html','.js':'text/javascript','.png':'image/png','.json':'application/json'};
(async()=>{
  const [v,fps,dur,out,only]=[process.argv[2],+process.argv[3],+process.argv[4],process.argv[5],process.argv[6]];
  fs.mkdirSync(out,{recursive:true});
  const srv=http.createServer((q,r)=>{const f=path.join(__dirname,decodeURIComponent(q.url.split('?')[0].split('#')[0]));
    fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end()}r.writeHead(200,{'Content-Type':types[path.extname(f)]||'application/octet-stream'});r.end(d)})});
  await new Promise(ok=>srv.listen(0,ok));
  const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  p.on('pageerror',e=>console.error('pageerror',e.message));
  await p.goto(`http://localhost:${srv.address().port}/video.html#${v}`);
  await p.waitForFunction(()=>window.ready===true,null,{timeout:60000});
  const times= only ? only.split(',').map(Number) : Array.from({length:Math.round(fps*dur)},(_,i)=>i/fps);
  for(let i=0;i<times.length;i++){
    await p.evaluate(t=>window.render(t),times[i]);
    await p.screenshot({path:path.join(out,String(i).padStart(4,'0')+'.jpg'),type:'jpeg',quality:93});
  }
  await b.close(); srv.close();
})();
