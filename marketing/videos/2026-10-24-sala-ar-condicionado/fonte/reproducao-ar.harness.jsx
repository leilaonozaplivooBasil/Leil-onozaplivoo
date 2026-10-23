/**
 * REPRODUÇÃO (marketing, 23/10/2026) — NÃO é prova e NÃO vai para o app.
 * A sala REAL (src/pages/AuctionRoom.jsx) tocando os 27 lances reais do leilão do Ar-condicionado Split Philco 12.000 BTUs
 * (02/10 → 07/10/2026, fim 18:05:08). O relógio da página é o do Playwright (page.clock); a gravação chama
 * window.__emitirAte(ms) a cada quadro e os lances entram no tempo real em que entraram, com a mesma regra do servidor:
 * lance nos últimos 142 s soma 22 s ao fim. Nomes escondidos (sem autorização de quem deu lance).
 */
import React from 'react';
import { createRoot } from 'react-dom/client';
import { MemoryRouter } from 'react-router-dom';
import '@/index.css';
import AuctionRoom from '@/pages/AuctionRoom';

const ID = 'ar-philco-07-10';
const BRT = (s) => new Date(`${s}-03:00`).getTime();
// [quando (Brasília), lance, quem] — do banco (auction_messages, message_type = 'bid'); "quem" é só um apelido estável por pessoa
const LANCES = [
  ['2026-10-02T19:08:27', 27, 'a'], ['2026-10-05T08:07:13', 400, 'b'], ['2026-10-05T18:09:33', 500, 'c'], ['2026-10-06T11:52:21', 550, 'd'],
  ['2026-10-06T15:37:46', 600, 'c'], ['2026-10-06T20:46:34', 650, 'd'], ['2026-10-07T16:16:42', 750, 'e'], ['2026-10-07T16:53:34', 800, 'f'],
  ['2026-10-07T17:32:21', 900, 'g'], ['2026-10-07T17:34:34', 950, 'h'], ['2026-10-07T17:44:59', 1050, 'g'], ['2026-10-07T17:48:06', 1100, 'h'],
  ['2026-10-07T17:57:17', 1150, 'f'], ['2026-10-07T17:58:39', 1200, 'd'], ['2026-10-07T17:59:28', 1250, 'f'], ['2026-10-07T17:59:31', 1400, 'i'],
  ['2026-10-07T17:59:43', 1900, 'g'], ['2026-10-07T18:00:03', 2000, 'i'], ['2026-10-07T18:00:28', 2100, 'g'], ['2026-10-07T18:01:08', 2200, 'i'],
  ['2026-10-07T18:01:17', 2250, 'g'], ['2026-10-07T18:02:27', 2300, 'i'], ['2026-10-07T18:02:34', 2350, 'g'], ['2026-10-07T18:03:32', 2400, 'i'],
  ['2026-10-07T18:03:39', 2500, 'g'], ['2026-10-07T18:04:20', 2550, 'j'], ['2026-10-07T18:04:26', 2650, 'g'],
].map(([q, v, p]) => ({ em: BRT(q), valor: v, quem: p }));
const NOMES = { a: 'Ro••••• A.', b: 'Ma••• C.', c: 'Jo•• P.', d: 'An•• L.', e: 'Fe••••• S.', f: 'Ca•••• M.', g: 'He••••• M.', h: 'Lu••• R.', i: 'Di••• F.', j: 'Pa••• T.' };
const FIM_ORIGINAL = BRT('2026-10-07T18:00:00');
const CONTAGEM = 142; const ACRESCIMO = 22;

const LEILAO = {
  id: ID, title: 'Ar-condicionado Split Philco 12.000 BTUs', status: 'active',
  starting_price: 27, current_price: 27, increment: 50, buy_now_price: 0, frete_reservado_valor: 0,
  end_time: new Date(FIM_ORIGINAL).toISOString(), created_date: new Date(BRT('2026-10-02T17:55:00')).toISOString(),
  image_urls: ['./ar-repro.webp'], category: 'eletrodomesticos', bid_count: 0, winner_id: null, winner_name: null,
  seller_name: 'Leilão NoZap', description: 'Ar Condicionado Split Inverter Philco 12000 Btus Frio 220v.', version: 1,
};
const MENSAGENS = [];
window.__entidadesFalsas = { get Auction() { return [LEILAO]; }, AuctionMessage: MENSAGENS };
window.__bancoFalso = { tabelas: {}, escritas: [] };
localStorage.setItem('currentUser', JSON.stringify({ id: 'u-visitante', full_name: 'Visitante', email: 'v@exemplo.com', role: 'user', terms_accepted: true,
  address_zip_code: '01310100', address_street: 'Avenida Paulista', address_number: '1000', address_neighborhood: 'Bela Vista', address_city: 'São Paulo', address_state: 'SP' }));
window.__usuarioFalso = JSON.parse(localStorage.getItem('currentUser'));
sessionStorage.setItem('isLoggedIn', '1');

let fim = FIM_ORIGINAL;
let emitidos = 0;
window.__estado = { acrescimos: 0, ultimoAcrescimoEm: 0, lances: 0 };
// toca os lances até o instante `ms` (relógio da página)
window.__emitirAte = (ms) => {
  while (emitidos < LANCES.length && LANCES[emitidos].em <= ms) {
    const l = LANCES[emitidos]; emitidos += 1;
    if (Math.floor((fim - l.em) / 1000) <= CONTAGEM) { fim += ACRESCIMO * 1000; window.__estado.acrescimos += 1; window.__estado.ultimoAcrescimoEm = l.em; }
    Object.assign(LEILAO, { current_price: l.valor, winner_id: `u-${l.quem}`, winner_name: NOMES[l.quem], end_time: new Date(fim).toISOString(), bid_count: emitidos, version: emitidos + 1 });
    const msg = { id: `m${emitidos}`, auction_id: ID, message_type: 'bid', sender_id: `u-${l.quem}`, sender_name: NOMES[l.quem], bid_amount: l.valor, content: `R$ ${l.valor}`, created_date: new Date(l.em).toISOString() };
    MENSAGENS.unshift(msg);
    window.__estado.lances = emitidos;
    window.__realtimeFalso.emitir('AuctionMessage', { eventType: 'INSERT', old: {}, new: msg });
    window.__realtimeFalso.emitir('Auction', { eventType: 'UPDATE', old: { id: ID }, new: { ...LEILAO } });
  }
  return { ...window.__estado, fim, preco: LEILAO.current_price };
};

window.__plataformaFalsa.respostas = {
  getServerTime: () => ({ timestamp: Date.now() }),
  getDigitalWalletBalance: { success: true, balance: 0, bonus_livre: 0 },
  getMyWallet: { success: true, saldo_disponivel: 0, bonus: { saldo: 0 } },
  cotarFrete: { success: true, endereco_completo: true, endereco_atual: { street: 'Avenida Paulista', number: '1000', neighborhood: 'Bela Vista', city: 'São Paulo', state: 'SP' }, opcoes: [{ id: 'pac', nome: 'PAC', preco: 32.14, selo: 'f1.banca.banca' }] },
  finalizeAuction: async () => {
    // como o servidor de verdade: se um lance acabou de abrir acréscimo, ainda falta tempo
    const falta = Math.ceil((new Date(LEILAO.end_time).getTime() - Date.now()) / 1000);
    (window.__finais ||= []).push({ agora: new Date(Date.now()).toISOString(), fim: LEILAO.end_time, falta });
    if (falta > 0) return { success: false, seconds_remaining: falta };
    Object.assign(LEILAO, { status: 'ended', order_status: 'awaiting_payment' });
    const vitoria = { id: 'm-vitoria', auction_id: ID, message_type: 'victory', sender_id: 'sistema', sender_name: 'Leiloeiro', content: `🏆 ${LEILAO.winner_name} arrematou por R$ 2.650,00`, created_date: new Date().toISOString() };
    MENSAGENS.unshift(vitoria);
    setTimeout(() => {
      window.__realtimeFalso.emitir('Auction', { eventType: 'UPDATE', new: { ...LEILAO }, old: { id: ID } });
      window.__realtimeFalso.emitir('AuctionMessage', { eventType: 'INSERT', new: vitoria, old: {} });
    }, 100);
    return { success: true, result: { status: 'ended', winner_id: LEILAO.winner_id, winner_name: LEILAO.winner_name, final_price: 2650, order_status: 'awaiting_payment' } };
  },
};

// a camada de legenda (o texto do vídeo), por cima da sala
function Legenda() {
  const [l, setL] = React.useState({ topo: '', meio: '', selo: '', flash: '' });
  React.useEffect(() => { window.__legenda = (x) => setL((a) => ({ ...a, ...x })); }, []);
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 2147483000, pointerEvents: 'none', fontFamily: 'Inter, system-ui, sans-serif' }}>
      {l.selo && <div style={{ position: 'absolute', top: 10, right: 10, padding: '4px 9px', borderRadius: 999, background: 'rgba(0,0,0,.65)', color: '#FFE08A', font: '800 11px/1 Inter, system-ui, sans-serif', letterSpacing: '.08em' }}>{l.selo}</div>}
      {l.topo && <div style={{ position: 'absolute', left: 16, right: 16, top: 104, padding: '10px 12px', borderRadius: 16, background: 'linear-gradient(160deg,#019049,#016A37)', color: '#fff', textAlign: 'center', font: '800 20px/1.2 Inter, system-ui, sans-serif', boxShadow: '0 10px 24px rgba(0,0,0,.45), 0 0 0 2px #FFE08A' }} dangerouslySetInnerHTML={{ __html: l.topo }} />}
      {l.flash && <div style={{ position: 'absolute', left: '50%', top: '54%', transform: 'translate(-50%,-50%) rotate(-4deg)', padding: '10px 18px', borderRadius: 14, background: '#FFE08A', color: '#0A2A18', font: '900 25px/1 Inter, system-ui, sans-serif', boxShadow: '0 12px 30px rgba(0,0,0,.5)', whiteSpace: 'nowrap' }}>{l.flash}</div>}
      {l.meio && <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'rgba(0,24,13,.93)', color: '#fff', textAlign: 'center', padding: 24, font: '800 30px/1.15 Inter, system-ui, sans-serif' }}><div dangerouslySetInnerHTML={{ __html: l.meio }} /></div>}
    </div>
  );
}

createRoot(document.getElementById('raiz')).render(
  <>
    <MemoryRouter initialEntries={[`/AuctionRoom?id=${ID}`]}>
      <AuctionRoom />
    </MemoryRouter>
    <Legenda />
  </>,
);
