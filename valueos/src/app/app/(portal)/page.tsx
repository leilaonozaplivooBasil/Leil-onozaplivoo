import { criarClienteServidor } from "@/lib/supabase/server";

export const dynamic = "force-dynamic";

type Valor = {
  metric_id: string;
  periodo: string;
  valor: number | null;
  etiqueta: string;
  fonte: string;
  nota: string | null;
};
type Metrica = { metric_id: string; nome: string; familia: string; unidade: string };

const ETIQUETA = {
  VERIFIED: { texto: "VERIFICADO", classe: "bg-accent/15 text-accent" },
  MANAGEMENT_DATA: { texto: "DADO DA ADMINISTRAÇÃO", classe: "bg-warn/15 text-warn" },
  FORECAST: { texto: "PROJEÇÃO", classe: "bg-sky-400/15 text-sky-300" },
  AI_ASSUMPTION: { texto: "PREMISSA", classe: "bg-danger/15 text-danger" },
  NAO_DISPONIVEL: { texto: "NÃO DISPONÍVEL", classe: "bg-muted/15 text-muted" },
} as const;

function formata(valor: number | null, unidade: string) {
  if (valor === null || valor === undefined) return "—";
  if (unidade === "BRL")
    return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });
  if (unidade === "%") return `${valor.toLocaleString("pt-BR", { maximumFractionDigits: 1 })}%`;
  return valor.toLocaleString("pt-BR");
}

export default async function Overview() {
  const supabase = await criarClienteServidor();
  const [{ data: metricas }, { data: valores }, { data: snapshots }] = await Promise.all([
    supabase.from("vos_metricas").select("metric_id, nome, familia, unidade").eq("ativo", true).order("familia").order("metric_id"),
    supabase.from("vos_valores").select("metric_id, periodo, valor, etiqueta, fonte, nota").order("periodo", { ascending: false }),
    supabase.from("vos_snapshots").select("tipo, periodo, fechado_em").eq("tipo", "official").order("periodo", { ascending: false }).limit(1),
  ]);

  const ultimoPorMetrica = new Map<string, Valor>();
  for (const v of (valores ?? []) as Valor[]) {
    if (!ultimoPorMetrica.has(v.metric_id)) ultimoPorMetrica.set(v.metric_id, v);
  }

  const todas = (metricas ?? []) as Metrica[];
  const comValor = todas.filter((m) => ultimoPorMetrica.has(m.metric_id));
  const verificadas = comValor.filter((m) => ultimoPorMetrica.get(m.metric_id)!.etiqueta === "VERIFIED").length;
  const qualidade = todas.length ? Math.round((100 * (verificadas + 0.5 * (comValor.length - verificadas))) / todas.length) : 0;
  const oficial = snapshots?.[0];

  const familias = Array.from(new Set(todas.map((m) => m.familia)));

  return (
    <div className="space-y-8">
      <section className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-2xl border border-border bg-surface p-5">
          <p className="text-xs uppercase tracking-widest text-muted">Valuation independente</p>
          <p className="mt-2 text-2xl font-semibold">Ainda não calculado</p>
          <p className="mt-1 text-xs text-muted">
            Só nasce depois do fechamento oficial e da metodologia v1.0 travada. Referência do fundador: R$ 25 mi (não é resultado).
          </p>
        </div>
        <div className="rounded-2xl border border-border bg-surface p-5">
          <p className="text-xs uppercase tracking-widest text-muted">Qualidade do dado</p>
          <p className="mt-2 text-2xl font-semibold">{qualidade}/100</p>
          <p className="mt-1 text-xs text-muted">
            {verificadas} verificadas · {comValor.length - verificadas} informadas/estimadas · {todas.length - comValor.length} sem valor
          </p>
        </div>
        <div className="rounded-2xl border border-border bg-surface p-5">
          <p className="text-xs uppercase tracking-widest text-muted">Último fechamento oficial</p>
          <p className="mt-2 text-2xl font-semibold">{oficial ? new Date(oficial.periodo).toLocaleDateString("pt-BR", { month: "short", year: "numeric" }) : "Nenhum"}</p>
          <p className="mt-1 text-xs text-muted">Snapshot oficial é imutável. Até lá, tudo é leitura ao vivo.</p>
        </div>
      </section>

      {familias.length === 0 && (
        <p className="rounded-xl border border-border bg-surface p-5 text-sm text-muted">
          O dicionário de métricas ainda está vazio. A primeira carga entra na Fase 1.
        </p>
      )}

      {familias.map((familia) => (
        <section key={familia}>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-widest text-muted">{familia}</h2>
          <div className="overflow-x-auto rounded-2xl border border-border bg-surface">
            <table className="w-full text-sm">
              <thead className="text-left text-xs uppercase text-muted">
                <tr>
                  <th className="px-4 py-3">Métrica</th>
                  <th className="px-4 py-3">Período</th>
                  <th className="px-4 py-3 text-right">Valor</th>
                  <th className="px-4 py-3">Etiqueta</th>
                  <th className="px-4 py-3">Origem</th>
                </tr>
              </thead>
              <tbody>
                {todas.filter((m) => m.familia === familia).map((m) => {
                  const v = ultimoPorMetrica.get(m.metric_id);
                  const et = ETIQUETA[(v?.etiqueta ?? "NAO_DISPONIVEL") as keyof typeof ETIQUETA];
                  return (
                    <tr key={m.metric_id} className="border-t border-border">
                      <td className="px-4 py-3">
                        <div className="font-medium">{m.nome}</div>
                        <div className="font-mono text-xs text-muted">{m.metric_id}</div>
                      </td>
                      <td className="px-4 py-3 text-muted">{v ? new Date(v.periodo).toLocaleDateString("pt-BR", { month: "short", year: "numeric" }) : "—"}</td>
                      <td className="px-4 py-3 text-right font-mono">{formata(v?.valor ?? null, m.unidade)}</td>
                      <td className="px-4 py-3"><span className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ${et.classe}`}>{et.texto}</span></td>
                      <td className="px-4 py-3 text-xs text-muted">{v?.fonte ?? "—"}{v?.nota ? ` · ${v.nota}` : ""}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      ))}
    </div>
  );
}
