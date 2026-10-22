import { chromium } from '/home/user/leilonozap/node_modules/playwright/index.mjs';
const [,, pasta, resta, modo, dur] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto(`file://${pasta}/cena.html?resta=${resta}&lance=600`);
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(300);
if (modo === 'foto') { await p.evaluate(() => window.quadro(0.5)); await p.screenshot({ path: `${pasta}/prev.png` }); }
else for (let i = 0; i < Math.round(30 * Number(dur)); i++) {
  await p.evaluate((t) => window.quadro(t), i / 30);
  await p.screenshot({ path: `${pasta}/q/${String(i).padStart(4, '0')}.png` });
}
await b.close();
