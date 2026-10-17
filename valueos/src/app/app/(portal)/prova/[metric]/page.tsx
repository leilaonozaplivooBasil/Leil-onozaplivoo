import Link from "next/link";
import { notFound } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/server";
import { ETIQUETA, formata, mesCurto, type Etiqueta } from "@/lib/etiquetas";

export const dynamic = "force-dynamic";

// "Clique para provar": de onde veio cada número desta métrica.
export default async function Prova({
  params,
}: {
  params: Promise<{ metric: string }>;
}) {
  const { metric } = await params;
  const supabase = await criarClienteServidor();

  const [{ data: metrica }, { data: valores }, { data: provas }, { data: perfil }] =
    await Promise.all([
      supabase.from("vos_metricas").select("*").eq("metric_id", metric).maybeSingle(),
      supabase
        .from("vos_valores")
        .select("id, periodo, valor, etiqueta, fonte, nota, carga_id, evidencia_id, criado_em")
        .eq("metric_id", metric)
        .order("periodo", { ascending: false }),
      supabase
        .from("vos_provas")
        .select("id, periodo, carga_id, hash, hash_anterior, criado_em")
        .eq("metric_id", metric),
      supabase.from("vos_profiles").select("papel").maybeSingle(),
    ]);

  if (!metrica) notFound();

  // Conselho e administração veem também a consulta e o resultado bruto.
  const detalhado = perfil && ["BOARD", "ADMIN"].includes(perfil.papel);
  const { data: evidencias } = detalhado
    ? await supabase
        .from("vos_evidencias")
        .select("id, consulta, resultado")
        .eq("metric_id", metric)
    : { data: null };

  const cargaIds = Array.from(new Set((valores ?? []).map((v) => v.carga_id).filter(Boolean)));
  const { data: cargas } = cargaIds.length
    ? await supabase
        .from("vos_cargas")
        .select("id, tipo, descricao, origem, hash_sha256, carregado_em, carregado_por")
        .in("id", cargaIds)
    : { data: [] };

  const provaPorEvidencia = new Map((provas ?? []).map((p) => [p.id, p]));
  const evidPorId = new Map((evidencias ?? []).map((e) => [e.id, e]));
  const cargaPorId = new Map((cargas ?? []).map((c) => [c.id, c]));

  return (
    <div className="space-y-8">
      <div>
        <Link href="/app" className="text-sm text-muted underline">
          ← Visão geral
        </Link>
        <p className="mt-4 text-xs uppercase tracking-widest text-muted">{metrica.familia}</p>
        <h1 className="mt-1 text-2xl font-semibold">{metrica.nome}</h1>
        <p className="font-mono text-xs text-muted">{metrica.metric_id} · {metrica.versao}</p>
      </div>

      <section className="grid gap-4 sm:grid-cols-2">
        <div className="rounded-2xl border border-border bg-surface p-5 text-sm">
          <p className="text-xs uppercase tracking-widest text-muted">Definição oficial</p>
          <p className="mt-2">{metrica.definicao}</p>
          <dl className="mt-4 space-y-1 text-xs text-muted">
            <div><dt className="inline font-semibold">Fonte primária: </dt><dd className="inline">{metrica.fonte_primaria}</dd></div>
            <div><dt className="inline font-semibold">Entidade: </dt><dd className="inline">{metrica.escopo_entidade}</dd></div>
            <div><dt className="inline font-semibold">Exclusões: </dt><dd className="inline">{metrica.exclusoes ?? "—"}</dd></div>
            <div><dt className="inline font-semibold">Se as fontes discordam: </dt><dd className="inline">{metrica.regra_conflito ?? "—"}</dd></div>
            <div><dt className="inline font-semibold">Série oficial desde: </dt><dd className="inline">{mesCurto(metrica.series_start)}</dd></div>
          </dl>
        </div>
        <div className="rounded-2xl border border-border bg-surface p-5 text-sm">
          <p className="text-xs uppercase tracking-widest text-muted">Como ler</p>
          <ul className="mt-2 space-y-2 text-muted">
            <li><span className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ${ETIQUETA.VERIFIED.classe}`}>VERIFICADO</span> veio do banco do app, de extrato ou de contrato, e dá para refazer.</li>
            <li><span className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ${ETIQUETA.MANAGEMENT_DATA.classe}`}>DADO DA ADMINISTRAÇÃO</span> informado pela empresa, sem documento que prove sozinho.</li>
            <li><span className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ${ETIQUETA.FORECAST.classe}`}>PROJEÇÃO</span> e <span className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ${ETIQUETA.AI_ASSUMPTION.classe}`}>PREMISSA</span> não são fatos.</li>
            <li>Cada prova tem um <strong>hash</strong> que inclui o hash da prova anterior: mudar uma quebra todas as seguintes.</li>
          </ul>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-sm font-semibold uppercase tracking-widest text-muted">Valores e provas</h2>
        {(valores ?? []).map((v) => {
          const et = ETIQUETA[(v.etiqueta as Etiqueta) ?? "NAO_DISPONIVEL"];
          const prova = v.evidencia_id ? provaPorEvidencia.get(v.evidencia_id) : undefined;
          const evid = v.evidencia_id ? evidPorId.get(v.evidencia_id) : undefined;
          const carga = v.carga_id ? cargaPorId.get(v.carga_id) : undefined;
          return (
            <article key={v.id} className="rounded-2xl border border-border bg-surface p-5">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <div>
                  <p className="text-xs uppercase tracking-widest text-muted">{mesCurto(v.periodo)}</p>
                  <p className="font-mono text-2xl">{formata(v.valor, metrica.unidade)}</p>
                </div>
                <span className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ${et.classe}`}>{et.texto}</span>
              </div>
              <dl className="mt-3 grid gap-x-6 gap-y-1 text-xs text-muted sm:grid-cols-2">
                <div><dt className="inline font-semibold">Origem: </dt><dd className="inline">{v.fonte}</dd></div>
                {v.nota && <div><dt className="inline font-semibold">Observação: </dt><dd className="inline">{v.nota}</dd></div>}
                {carga && (
                  <div className="sm:col-span-2">
                    <dt className="inline font-semibold">Carga: </dt>
                    <dd className="inline">{carga.descricao} · {new Date(carga.carregado_em).toLocaleString("pt-BR")} · impressão digital <span className="font-mono">{carga.hash_sha256.slice(0, 16)}…</span></dd>
                  </div>
                )}
                {prova && (
                  <div className="sm:col-span-2">
                    <dt className="inline font-semibold">Prova #{prova.id}: </dt>
                    <dd className="inline font-mono">{prova.hash.slice(0, 24)}… {prova.hash_anterior ? `(anterior ${prova.hash_anterior.slice(0, 12)}…)` : "(primeira da cadeia)"}</dd>
                  </div>
                )}
              </dl>
              {evid && (
                <details className="mt-3 text-xs">
                  <summary className="cursor-pointer text-muted">Consulta e resultado bruto (conselho/administração)</summary>
                  <pre className="mt-2 overflow-auto rounded-lg bg-background p-3 font-mono text-[11px] leading-relaxed">{evid.consulta}

{JSON.stringify(evid.resultado, null, 2)}</pre>
                </details>
              )}
            </article>
          );
        })}
        {(valores ?? []).length === 0 && (
          <p className="text-sm text-muted">Ainda não há valor carregado para esta métrica.</p>
        )}
      </section>
    </div>
  );
}
