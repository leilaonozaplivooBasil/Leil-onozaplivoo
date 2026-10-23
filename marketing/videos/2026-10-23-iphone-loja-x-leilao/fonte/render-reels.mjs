import { chromium } from '/home/user/leilonozap/node_modules/playwright/index.mjs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file:///tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/iphone-reels/cena.html?lance=' + (process.env.LANCE || '800') + '&resta=' + (process.env.RESTA || '0')); await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready);
const FPS = 30, DUR = 16;
for (let i = 0; i < FPS * DUR; i++) {
  await p.evaluate((t) => window.quadro(t), i / FPS);
  await p.screenshot({ path: '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/iphone-reels/quadros/q' + String(i).padStart(4, '0') + '.jpg', type: 'jpeg', quality: 92 });
}
await b.close();
