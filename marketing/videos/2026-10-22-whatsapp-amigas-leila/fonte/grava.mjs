import { chromium } from '/home/user/leilonozap/node_modules/playwright/index.mjs';
const [,, pasta, modo, ...ts] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 390, height: 693 }, deviceScaleFactor: 1080 / 390 });
await p.goto('file://' + pasta + '/conversa.html');
await p.evaluate(() => document.fonts.ready);
if (modo === 'fotos') {
  for (const t of ts) { await p.evaluate((t) => window.quadro(t), Number(t)); await p.screenshot({ path: `${pasta}/prev_${t}.png` }); }
} else {
  const fps = 30, dur = Number(ts[0]);
  for (let i = 0; i < Math.round(fps * dur); i++) {
    await p.evaluate((t) => window.quadro(t), i / fps);
    await p.screenshot({ path: `${pasta}/q/${String(i).padStart(4, '0')}.png` });
  }
}
await b.close();
