import Link from "next/link";
import { criarClienteServidor } from "@/lib/supabase/server";
import { valoresCarregados } from "@/lib/metricas";
import { formata, mesCurto } from "@/lib/etiquetas";
import { Etiqueta, Legenda, Pagina } from "@/components/ui";

export const dynamic = "force-dynamic";

type Metrica = { metric_id: string; nome: string; familia: string; unidade: string };

// Dicionário de métricas com o último valor carregado de cada uma. Cada linha leva à prova.
export default async function Numeros() {
  const supabase = await criarClienteServidor();
  const [{ data: metricas }, { ultimo }] = await Promise.all([
    supabase.from("vos_metricas").select("metric_id, nome, familia, unidade").eq("ativo", true).order("familia").order("metric_id"),
    valoresCarregados(),
  ]);
  const todas = (metricas ?? []) as Metrica[];
  const familias = Array.from(new Set(todas.map((m) => m.familia)));

  return (
    <Pagina
      sobretitulo="5 minutos"
      titulo="Números com prova"
      descricao="Trinta métricas, cada uma com definição única, origem e impressão digital. Clique no nome para ver de onde o número veio."
    >
      <Legenda />
      {familias.map((familia) => (
        <section key={familia} className="space-y-3">
          <h2 className="text-sm font-semibold uppercase tracking-widest text-muted">{familia}</h2>
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
                {todas
                  .filter((m) => m.familia === familia)
                  .map((m) => {
                    const v = ultimo.get(m.metric_id);
                    return (
                      <tr key={m.metric_id} className="border-t border-border">
                        <td className="px-4 py-3">
                          <Link href={`/app/prova/${m.metric_id}`} className="font-medium hover:underline">
                            {m.nome}
                          </Link>
                          <div className="font-mono text-xs text-muted">{m.metric_id} · clique para provar</div>
                        </td>
                        <td className="px-4 py-3 text-muted">{v ? mesCurto(v.periodo) : "—"}</td>
                        <td className="num px-4 py-3 text-right font-mono">{formata(v?.valor ?? null, m.unidade)}</td>
                        <td className="px-4 py-3">
                          <Etiqueta tipo={v?.etiqueta ?? "NAO_DISPONIVEL"} pequena />
                        </td>
                        <td className="px-4 py-3 text-xs text-muted">
                          {v?.fonte ?? "—"}
                          {v?.nota ? ` · ${v.nota}` : ""}
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>
          </div>
        </section>
      ))}
    </Pagina>
  );
}
