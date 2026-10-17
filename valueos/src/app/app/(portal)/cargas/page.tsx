import { criarClienteServidor } from "@/lib/supabase/server";

export const dynamic = "force-dynamic";

// O que entrou no sistema, quando, de onde e com que impressão digital.
export default async function Cargas() {
  const supabase = await criarClienteServidor();
  const [{ data: cargas }, { data: contagem }] = await Promise.all([
    supabase
      .from("vos_cargas")
      .select("id, tipo, descricao, origem, arquivo_nome, hash_sha256, linhas, periodo_ini, periodo_fim, carregado_por, carregado_em")
      .order("carregado_em", { ascending: false }),
    supabase.from("vos_provas").select("carga_id"),
  ]);
  const provasPorCarga = new Map<string, number>();
  for (const p of contagem ?? []) provasPorCarga.set(p.carga_id, (provasPorCarga.get(p.carga_id) ?? 0) + 1);

  const TIPO: Record<string, string> = {
    app_query: "consulta no banco do app",
    upload: "arquivo enviado",
    manual: "lançamento manual",
  };

  return (
    <div className="mx-auto w-full max-w-6xl space-y-6 px-5 py-12 sm:px-8 sm:py-16">
      <div>
        <h1 className="font-display text-4xl font-light">Cargas</h1>
        <p className="mt-1 text-sm text-muted">
          Cada busca ou arquivo vira uma carga com data, autor e impressão digital. Nenhuma carga é apagada.
        </p>
      </div>
      <div className="space-y-3">
        {(cargas ?? []).map((c) => (
          <article key={c.id} className="rounded-2xl border border-border bg-surface p-5 text-sm">
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <p className="font-medium">{c.descricao}</p>
              <span className="rounded-full bg-muted/15 px-2 py-0.5 text-xs font-semibold uppercase text-muted">{TIPO[c.tipo] ?? c.tipo}</span>
            </div>
            <dl className="mt-2 grid gap-x-6 gap-y-1 text-xs text-muted sm:grid-cols-2">
              <div><dt className="inline font-semibold">Origem: </dt><dd className="inline">{c.origem}</dd></div>
              <div><dt className="inline font-semibold">Período: </dt><dd className="inline">{c.periodo_ini ?? "—"} a {c.periodo_fim ?? "—"}</dd></div>
              <div><dt className="inline font-semibold">Carregado: </dt><dd className="inline">{new Date(c.carregado_em).toLocaleString("pt-BR")} por {c.carregado_por}</dd></div>
              <div><dt className="inline font-semibold">Provas: </dt><dd className="inline">{provasPorCarga.get(c.id) ?? 0}</dd></div>
              <div className="sm:col-span-2"><dt className="inline font-semibold">Impressão digital: </dt><dd className="inline font-mono">{c.hash_sha256}</dd></div>
            </dl>
          </article>
        ))}
        {(cargas ?? []).length === 0 && <p className="text-sm text-muted">Nenhuma carga ainda.</p>}
      </div>
    </div>
  );
}
