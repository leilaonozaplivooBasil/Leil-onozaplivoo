import Link from "next/link";
import { criarClienteServidor } from "@/lib/supabase/server";
import { ETIQUETA, formata, mesCurto, type Etiqueta } from "@/lib/etiquetas";

export const dynamic = "force-dynamic";

type Valor = { metric_id: string; periodo: string; valor: number | null; etiqueta: string };

// Linha da DRE: soma de métricas (com sinal) ou "não disponível" com o motivo.
type Linha =
  | { rotulo: string; metricas: { id: string; sinal: 1 | -1 }[]; total?: boolean; destaque?: boolean }
  | { rotulo: string; indisponivel: string; total?: boolean; destaque?: boolean };

const LINHAS: Linha[] = [
  { rotulo: "Mercadoria vendida e paga (GMV)", metricas: [{ id: "GMV_GOODS", sinal: 1 }] },
  { rotulo: "Taxas e adesões", metricas: [{ id: "REVENUE_FEES", sinal: 1 }] },
  { rotulo: "Receita bruta (visão principal: a empresa vende o estoque)", metricas: [{ id: "GMV_GOODS", sinal: 1 }, { id: "REVENUE_FEES", sinal: 1 }], total: true },
  { rotulo: "(−) Custo das mercadorias vendidas", indisponivel: "o app não grava o custo por venda (mudança D1, zona vermelha)" },
  { rotulo: "(−) Comissões pagas à rede", indisponivel: "o app mistura comissão paga e retida em financial_income (mudança D8)" },
  { rotulo: "(−) Taxa do gateway", indisponivel: "≈ 1,6% do bruto no Mercado Pago (Anexo C10); só gravada por venda desde 03/10" },
  { rotulo: "= Lucro bruto", indisponivel: "depende do custo das mercadorias", total: true },
  { rotulo: "(−) Despesas pagas (lançamento manual, sem categoria)", metricas: [{ id: "EXPENSES_PAID", sinal: -1 }] },
  { rotulo: "= EBITDA", indisponivel: "não calculável sem custo das mercadorias; a linha abaixo é o retrato de caixa", total: true },
  { rotulo: "Retrato de caixa do app: receita bruta − despesas pagas", metricas: [{ id: "GMV_GOODS", sinal: 1 }, { id: "REVENUE_FEES", sinal: 1 }, { id: "EXPENSES_PAID", sinal: -1 }], total: true, destaque: true },
  { rotulo: "(−) Remuneração dos parceiros de compra (contratos A e B)", metricas: [{ id: "PARTNER_CAPITAL_SERVICE_M", sinal: -1 }] },
  { rotulo: "(−) Parcelas de consórcio identificadas", metricas: [{ id: "CONSORTIUM_PAYMENTS_M", sinal: -1 }] },
  { rotulo: "(−) Impostos", indisponivel: "sem PGDAS/DAS de 2026; estimativa entra como PREMISSA na Fase 2" },
  { rotulo: "Para comparar: receita reconhecida pelo app (visão agente — só a comissão retida)", metricas: [{ id: "REVENUE_COMMISSION_RETAINED", sinal: 1 }] },
  { rotulo: "Para comparar: depósitos de carteira (não é receita)", metricas: [{ id: "WALLET_DEPOSITS", sinal: 1 }] },
  { rotulo: "Para comparar: entradas de terceiros nos bancos (inclui aportes)", metricas: [{ id: "BANK_INFLOWS_THIRD_PARTY", sinal: 1 }] },
];

const PERIODOS = ["2026-08-01", "2026-09-01", "2026-10-01"];

export default async function Dre() {
  const supabase = await criarClienteServidor();
  const { data } = await supabase
    .from("vos_valores")
    .select("metric_id, periodo, valor, etiqueta")
    .in("periodo", PERIODOS);
  const valores = (data ?? []) as Valor[];
  const mapa = new Map<string, Valor>();
  for (const v of valores) mapa.set(`${v.metric_id}|${v.periodo}`, v);

  function celula(linha: Linha, periodo: string) {
    if ("indisponivel" in linha) return { valor: null as number | null, etiqueta: "NAO_DISPONIVEL" as Etiqueta };
    let soma = 0;
    let pior: Etiqueta = "VERIFIED";
    let achou = false;
    for (const m of linha.metricas) {
      const v = mapa.get(`${m.id}|${periodo}`);
      if (!v || v.valor === null) continue;
      achou = true;
      soma += m.sinal * Number(v.valor);
      if (v.etiqueta === "MANAGEMENT_DATA" && pior === "VERIFIED") pior = "MANAGEMENT_DATA";
      if (v.etiqueta === "AI_ASSUMPTION" || v.etiqueta === "FORECAST") pior = v.etiqueta as Etiqueta;
    }
    return achou ? { valor: soma, etiqueta: pior } : { valor: null, etiqueta: "NAO_DISPONIVEL" as Etiqueta };
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">DRE conceitual — ago a out/2026</h1>
        <p className="mt-1 text-sm text-muted">
          Cada linha vem de métricas com prova (clique no nome). Linha cinza = o dado ainda não existe, e o motivo está escrito. Outubro vai até o dia 16.
        </p>
      </div>
      <div className="overflow-x-auto rounded-2xl border border-border bg-surface">
        <table className="w-full text-sm">
          <thead className="text-left text-xs uppercase text-muted">
            <tr>
              <th className="px-4 py-3">Linha</th>
              {PERIODOS.map((p) => (
                <th key={p} className="px-4 py-3 text-right">{mesCurto(p)}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {LINHAS.map((linha) => (
              <tr key={linha.rotulo} className={`border-t border-border ${linha.total ? "font-semibold" : ""} ${linha.destaque ? "bg-accent/5" : ""}`}>
                <td className="px-4 py-3">
                  <div>{linha.rotulo}</div>
                  {"indisponivel" in linha ? (
                    <div className="text-xs font-normal text-muted">{linha.indisponivel}</div>
                  ) : (
                    <div className="text-xs font-normal text-muted">
                      {linha.metricas.map((m, i) => (
                        <span key={m.id}>
                          {i > 0 && " · "}
                          <Link href={`/app/prova/${m.id}`} className="font-mono underline">{m.id}</Link>
                        </span>
                      ))}
                    </div>
                  )}
                </td>
                {PERIODOS.map((p) => {
                  const c = celula(linha, p);
                  const et = ETIQUETA[c.etiqueta];
                  return (
                    <td key={p} className="px-4 py-3 text-right align-top">
                      <div className="font-mono">{formata(c.valor, "BRL")}</div>
                      <span className={`rounded-full px-1.5 py-0.5 text-[10px] font-semibold ${et.classe}`}>{et.texto}</span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-muted">
        Visão principal × agente: o app registra como receita só a comissão retida; o investidor compara com margem de varejo, que usa a venda. As duas aparecem até a decisão DEC-2. EBITDA e lucro bruto só nascem quando o custo por venda for gravado no app.
      </p>
    </div>
  );
}
