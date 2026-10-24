import { chromium } from '/home/user/leilonozap/node_modules/playwright/index.mjs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [f, h] of [['feed', 1350], ['story', 1920]]) {
  const p = await b.newPage({ viewport: { width: 1080, height: h } });
  await p.goto('file:///tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/plantao/plantao.html?f=' + f + '&lance=' + (process.env.LANCE || '1210')); await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/plantao/plantao-' + f + '.jpg', type: 'jpeg', quality: 93 });
}
await b.close();
