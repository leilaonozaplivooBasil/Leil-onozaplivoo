import { normalizarEdicao, normalizarPadrao, PADRAO_VIDEO, finalDoVideo } from '/home/user/leilonozap/src/lib/dudaVideo.js';
import fs from 'node:fs';
const legenda = [{"ini":3.3,"fim":6.0,"texto":"Chegou o ar-condicionado","destaque":"ar-condicionado"},{"ini":6.0,"fim":9.0,"texto":"Novo dono do PS5","destaque":"PS5"},{"ini":9.0,"fim":11.0,"texto":"Scooter elétrica entregue","destaque":"entregue"},{"ini":11.2,"fim":13.4,"texto":"Tudo certinho e lacrado","destaque":"lacrado"},{"ini":13.5,"fim":15.0,"texto":"E foi o iPhone 17 Pro Max","destaque":"iPhone 17 Pro Max"}];
const momentos = [{"t":0.2,"tipo":"produto","ativo":true,"frase":"Todos encontraram dono"}];
const ed = normalizarEdicao({ legenda, momentos, gancho: null }, 15.1);
const pedido = { etapa: 'montar', id: 'local', site: 'https://leilaonozap.net', retorno: {},
  origem_url: 'file:///home/user/Leil-onozaplivoo/marketing/videos/2026-11-03-encontrou-dono/cortes-limpos/COMPILADO-entregas-com-som.mp4',
  legenda: ed.legenda, momentos: ed.momentos, gancho: ed.gancho, clima: 'vitoria', semente: 446824, padrao: normalizarPadrao(PADRAO_VIDEO),
  prova: null, final: finalDoVideo(null), saidas: {} };
fs.writeFileSync(process.argv[2], JSON.stringify(pedido, null, 1));
console.log(JSON.stringify(ed.momentos), ed.legenda.length);
