// A conta do plano de 12 meses que sustenta o valor de R$ 35 milhões.
// O que é medido chega do banco (Medido); o que é plano fica aqui, com etiqueta FORECAST nas telas.

export type Medido = {
  cadastros: number; // USERS_REGISTERED
  compradores: number; // APP_BUYERS
  compras: number; // APP_PAID_PURCHASES (R$, acumulado desde jun/2026)
};

export type Cenario = {
  nome: string;
  recreioPct: number; // parte da população da região que compra no ano
  ticket: number; // R$ por compra no Recreio
  comprasAno: number; // compras por cliente no ano, no Recreio
  cadastros: number; // cadastros no app em 12 meses
  conversao: number | null; // parte dos cadastros que compra; null = a medida hoje
  margem: number; // o que sobra de cada venda depois dos custos variáveis
  fixoMes: number; // custos fixos por mês
  multiplo: number; // vezes o faturamento anual, daqui a 12 meses
};

// Região do Recreio: 180 mil pessoas, segundo o fundador (o bairro tinha 140.437 no Censo 2022; o resto são os vizinhos).
export const POPULACAO = 180_000;
// Meses de venda no app até 17/10/2026 (desde 01/06).
export const MESES_APP = 4.5;
// Retorno que um investidor de risco cobra: dobrar o dinheiro em 12 meses (método VC).
export const RETORNO = 2;
// Conferência pelo lucro: vezes o lucro operacional (EBITDA) do ano 1 do plano.
export const VEZES_EBITDA = 10;

// O que sai de cada R$ 100 vendidos no cenário base.
export const CUSTOS_VARIAVEIS: [string, number, string][] = [
  ["Mercadoria (lote)", 30, "o lote custa cerca de 19% do valor de mercado e a venda é 20% abaixo do mercado: dá 24% do preço; 30% cobre as peças que não vendem"],
  ["Comissão da rede", 12, "a escada de licenças paga de 5% a 20%; 94% das vendas vêm de indicação"],
  ["Impostos sobre a venda", 10, "Simples Nacional na faixa de cima e regime normal acima de R$ 4,8 mi"],
  ["Devoluções e perdas", 6, "troca, defeito e quebra"],
  ["Frete e embalagem", 5, "entrega local e frete de lote"],
  ["Meios de pagamento", 2, "taxa do Mercado Pago"],
];

export const CENARIOS: Cenario[] = [
  { nome: "Conservador", recreioPct: 0.1, ticket: 321, comprasAno: 1, cadastros: 30_000, conversao: null, margem: 0.3, fixoMes: 300_000, multiplo: 2 },
  { nome: "Base", recreioPct: 0.2, ticket: 397, comprasAno: 1, cadastros: 100_000, conversao: null, margem: 0.35, fixoMes: 400_000, multiplo: 3 },
  { nome: "Alto", recreioPct: 0.2, ticket: 397, comprasAno: 2, cadastros: 100_000, conversao: 0.05, margem: 0.4, fixoMes: 500_000, multiplo: 3 },
];

export function conversaoMedida(m: Medido) {
  return m.cadastros ? m.compradores / m.cadastros : 0;
}

// Quanto um comprador gasta por mês no app, medido.
export function gastoMes(m: Medido) {
  return m.compradores ? m.compras / m.compradores / MESES_APP : 0;
}

export function calcula(c: Cenario, m: Medido) {
  const clientesRecreio = POPULACAO * c.recreioPct;
  const recreio = clientesRecreio * c.ticket * c.comprasAno;
  const conversao = c.conversao ?? conversaoMedida(m);
  const compradores = c.cadastros * conversao;
  const digital = compradores * gastoMes(m) * 12;
  const receita = recreio + digital;
  const contribuicao = receita * c.margem;
  const fixo = c.fixoMes * 12;
  const ebitda = contribuicao - fixo;
  const futuro = receita * c.multiplo;
  const hoje = futuro / RETORNO;
  const peloLucro = ebitda > 0 ? ebitda * VEZES_EBITDA : null;
  // Capital de giro: mercadoria do ano (30% da venda) girando três vezes por ano.
  const giro = (receita * 0.3) / 3;
  return { clientesRecreio, recreio, conversao, compradores, digital, receita, contribuicao, fixo, ebitda, futuro, hoje, peloLucro, giro };
}

// O valor de hoje do cenário base, arredondado ao milhão — o número que aparece nas capas.
export const valorPlano = (m: Medido) => Math.round(calcula(CENARIOS[1], m).hoje / 1_000_000) * 1_000_000;
