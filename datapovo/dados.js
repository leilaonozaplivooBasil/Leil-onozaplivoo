// Camada de dados: grava no Supabase quando configurado; senão, só neste aparelho (modo teste).
(() => {
  'use strict';
  const C = window.DATAPOVO;
  const remoto = !!(C.SUPABASE_URL && C.SUPABASE_KEY);
  const LKEY = 'datapovo:local';

  async function rpc(nome, args) {
    const r = await fetch(`${C.SUPABASE_URL.replace(/\/$/, '')}/rest/v1/rpc/${nome}`, {
      method: 'POST',
      headers: { apikey: C.SUPABASE_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify(args || {}),
      credentials: 'omit',          // sem cookies
      referrerPolicy: 'no-referrer', // sem dizer de qual página veio
      cache: 'no-store',
    });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const t = await r.text();
    return t ? JSON.parse(t) : null;
  }

  const lerLocal = () => {
    try { return JSON.parse(localStorage.getItem(LKEY)) || { votos: {}, contatos: [] }; }
    catch { return { votos: {}, contatos: [] }; }
  };
  const gravarLocal = d => localStorage.setItem(LKEY, JSON.stringify(d));

  // Cria elemento sem usar innerHTML (textos vêm como texto, nunca como HTML).
  function h(tag, props, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(props || {})) {
      if (v == null || v === false) continue;
      if (k === 'class') e.className = v;
      else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
      else if (k === 'value' || k === 'checked' || k === 'disabled' || k === 'hidden') e[k] = v;
      else e.setAttribute(k, v === true ? '' : v);
    }
    e.append(...kids.flat().filter(k => k != null && k !== false));
    return e;
  }

  window.DP = {
    remoto,
    h,
    async votar(opcao) {
      if (remoto) return rpc('votar', { p_opcao: opcao });
      const d = lerLocal();
      d.votos[opcao] = (d.votos[opcao] || 0) + 1;
      gravarLocal(d);
    },
    // O contato fica numa tabela separada: não há ligação com o voto.
    async deixarContato(nome, whatsapp, consentimento) {
      if (remoto) return rpc('deixar_contato', { p_nome: nome, p_whatsapp: whatsapp, p_consentimento: consentimento });
      const d = lerLocal();
      if (!d.contatos.some(c => c.whatsapp === whatsapp)) d.contatos.push({ nome, whatsapp, consentimento, em: new Date().toISOString() });
      gravarLocal(d);
    },
    // Texto de rodapé: o que é (enquete aberta) e quem fez.
    aviso() {
      return 'Enquete de opinião aberta, sem método estatístico: não representa toda a população e não é votação oficial nem pesquisa eleitoral.' +
        (C.RESPONSAVEL ? ' Realizada por ' + C.RESPONSAVEL + '.' : '');
    },
    // Compartilha o link da urna (menu do celular ou, no computador, copia o link).
    async compartilhar() {
      const url = new URL('./', location.href).href;
      try {
        if (navigator.share) { await navigator.share({ title: C.TITULO, text: C.PERGUNTA, url }); return ''; }
        await navigator.clipboard.writeText(url);
        return 'Link copiado!';
      } catch (e) {
        return e && e.name === 'AbortError' ? '' : 'Copie o link: ' + url;
      }
    },
    // Devolve { '1': 10, '2': 4, BRANCO: 1, NULO: 0 }
    async resultado() {
      if (remoto) {
        const rows = await rpc('resultado');
        return Object.fromEntries(rows.map(r => [r.opcao, Number(r.votos)]));
      }
      return lerLocal().votos;
    },
  };
})();
