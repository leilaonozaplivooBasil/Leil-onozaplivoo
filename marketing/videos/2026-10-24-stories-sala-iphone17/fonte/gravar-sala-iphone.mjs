// Grava a reprodução do leilão do ar-condicionado na sala real, quadro a quadro (30 fps), com o relógio do Playwright.
import { chromium } from '/home/user/leilonozap/node_modules/playwright/index.mjs';
import { createServer } from 'node:http';
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const SAIDA = '/tmp/claude-0/banca-repro-iphone';
const QUADROS = process.env.QUADROS || '/tmp/claude-0/quadros-sala';
const SO = (process.env.SO || '').split(',').filter(Boolean).map(Number); // prévia: só estes quadros
mkdirSync(QUADROS, { recursive: true });
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.webp': 'image/webp', '.woff2': 'font/woff2', '.png': 'image/png' };
const srv = createServer((req, res) => { const rel = decodeURIComponent((req.url || '/').split('?')[0]); const arq = path.join(SAIDA, rel === '/' ? 'reproducao-iphone.html' : rel); if (!existsSync(arq)) { res.writeHead(404).end(); return; } res.writeHead(200, { 'content-type': TIPOS[path.extname(arq)] || 'application/octet-stream' }); res.end(readFileSync(arq)); });
await new Promise((ok) => srv.listen(0, '127.0.0.1', ok));

const BRT = (s) => Date.parse(`${s}-03:00`);
const FPS = 30;
// trechos: [quadros, de, até, modo]  (modo 'pula' = fastForward; 'anda' = runFor, os relógios da tela andam)
const TRECHOS = [
  [75, BRT('2026-09-28T10:00:00'), BRT('2026-09-28T10:00:00'), 'parado'],   // 0–2,5 s    abertura
  [165, BRT('2026-09-28T10:00:00'), BRT('2026-10-02T17:42:00'), 'pula'],    // 2,5–8 s    primeiros lances (5 dias)
  [300, BRT('2026-10-02T17:42:00'), BRT('2026-10-02T17:59:30'), 'anda'],    // 8–18 s     últimos minutos (~63x)
  [230, BRT('2026-10-02T17:59:30'), BRT('2026-10-02T18:01:29'), 'anda'],    // 18–25,7 s  o final (~16x)
  [40, BRT('2026-10-02T18:01:29'), BRT('2026-10-02T18:01:33'), 'anda'],     // 25,7–27 s  a sala vira ARREMATADO
  [90, BRT('2026-10-02T18:01:33'), BRT('2026-10-02T18:01:36'), 'anda'],     // 27–30 s    o resumo
];

const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5 });
const p = await ctx.newPage();
const inicio = TRECHOS[0][1];
await p.clock.install({ time: inicio - 4000 });
await p.goto(`http://127.0.0.1:${srv.address().port}/`);
await p.clock.pauseAt(inicio); // daqui em diante o relógio da página só anda quando a gravação manda
await p.waitForTimeout(1500);
await p.clock.runFor(1000); await p.waitForTimeout(500);
// esconde o "Boa sorte!" do sistema? não: a sala fica como é. Só some a barra de rolagem.
await p.addStyleTag({ content: '::-webkit-scrollbar{display:none} html,body,#raiz{background:#07140E!important;min-height:100vh}' });

const marcas = []; // para o som: { q, tipo }
let q = 0; let agora = inicio + 1000; let lancesAntes = 0; let acrescAntes = 0; let flashAte = -1; let flashTxt = '';
const legenda = (x) => p.evaluate((y) => window.__legenda && window.__legenda(y), x);
const brl = (v) => v.toLocaleString('pt-BR');

for (const [n, de, ate, modo] of TRECHOS) {
  for (let i = 0; i < n; i += 1, q += 1) {
    const alvo = modo === 'parado' ? de : de + Math.round(((i + 1) / n) * (ate - de));
    const passo = alvo - agora;
    if (passo > 0) {
      if (modo === 'pula') await p.clock.fastForward(passo); else await p.clock.runFor(passo);
      agora = alvo;
    }
    const est = await p.evaluate((t) => window.__emitirAte(t), agora);
    if (est.lances > lancesAntes) { marcas.push({ q, tipo: 'lance', valor: est.preco }); lancesAntes = est.lances; }
    if (est.acrescimos > acrescAntes) { marcas.push({ q, tipo: 'acrescimo' }); acrescAntes = est.acrescimos; flashAte = q + 22; flashTxt = '⏱ +22 s · ACRÉSCIMO!'; }
    // as legendas, por tempo do vídeo
    const s = q / FPS;
    const hora = new Date(agora).toLocaleTimeString('pt-BR', { timeZone: 'America/Sao_Paulo', hour: '2-digit', minute: '2-digit' });
    const dia = new Date(agora).toLocaleDateString('pt-BR', { timeZone: 'America/Sao_Paulo', day: '2-digit', month: '2-digit' });
    let x = { selo: '', topo: '', meio: '', flash: '' };
    if (s < 2.5) x.meio = '<div style="font:800 15px Inter;letter-spacing:.14em;color:#FFE08A">O ÚLTIMO IPHONE DO NOSSO LEILÃO · 02/10</div><div style="margin-top:10px">Apple iPhone 17<br>512 GB</div><div style="margin-top:14px;font:900 40px Inter;color:#3dff8a">Começou em R$ 27</div><div style="margin-top:12px;font:600 15px Inter;color:rgba(255,255,255,.7)">Reprodução dos lances reais · nomes ocultos</div>';
    const sub = (t) => `<br><span style="font-size:14px;color:#FFE08A">${t}</span>`;
    const rel = (t) => `<div style="margin-top:4px;font:700 11px Inter,system-ui;letter-spacing:.06em;color:rgba(255,255,255,.75)">${t}</div>`;
    if (s >= 2.5 && s < 8) x.topo = `⏩ Os primeiros lances${sub('5 dias de leilão em 5 segundos')}${rel(`${dia} · ${hora}`)}`;
    else if (s >= 8 && s < 18) x.topo = (agora < BRT('2026-10-02T17:55:00') ? '⏰ Últimos 20 minutos' : agora < BRT('2026-10-02T17:58:00') ? `🔥 Faltando 5 minutos: R$ 2.900` : `😮 Lance em cima de lance${sub('Lance nos 2 últimos minutos = +22 s no relógio')}`) + rel(`⏩ VÍDEO ACELERADO · ${hora}`);
    else if (s >= 18 && s < 25.7) x.topo = (agora < BRT('2026-10-02T18:00:00') ? `💥 R$ 3.100 → R$ 3.900 de uma vez` : agora < BRT('2026-10-02T18:00:40') ? `😮 Era pra acabar às 18h…${sub('…e o lance final entrou às 18:00:31')}` : '⏳ Os últimos segundos…') + rel(`⏩ VÍDEO ACELERADO · ${hora}`);
    else if (s >= 25.7 && s < 27) x.topo = '🔨 Martelo batido!';
    else if (s >= 27) x.meio = `<div style="font:800 15px Inter;letter-spacing:.14em;color:#FFE08A">MARTELO BATIDO · 02/10 · 18:01</div><div style="margin-top:8px;font:900 46px Inter;color:#3dff8a">R$ 4.400</div><div style="margin-top:6px">Arrematado!</div><div style="margin-top:14px;font:700 19px/1.4 Inter;color:rgba(255,255,255,.9)">Na nossa loja: <s style="text-decoration-color:#FFE08A">R$ 8.000</s><br><b style="color:#FFE08A">45% abaixo</b><br>Começou em R$ 27 · 25 lances · 9 pessoas</div><div style="margin-top:18px;display:inline-block;padding:12px 22px;border-radius:999px;background:#3dff8a;color:#03200f;font:900 19px Inter">Hoje 18h: iPhone 17 Pro Max · link na bio</div>`;
    if (q <= flashAte && s >= 8 && s < 25.7) x.flash = flashTxt;
    await legenda(x);
    await p.waitForTimeout(12); // deixa o React aplicar o lance antes do próximo tique
    if (!SO.length || SO.includes(q)) {
      await p.waitForTimeout(SO.length ? 400 : 30);
      await p.screenshot({ path: path.join(QUADROS, `q${String(q).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 90 });
    }
  }
}
writeFileSync(path.join(QUADROS, 'marcas.json'), JSON.stringify(marcas));
console.log(JSON.stringify(await p.evaluate(() => window.__finais)));
console.log('quadros', q, 'lances', lancesAntes, 'acrescimos', acrescAntes);
await b.close(); srv.close();
