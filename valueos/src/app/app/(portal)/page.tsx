import Image from "next/image";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { criarClienteServidor } from "@/lib/supabase/server";
import { valoresCarregados } from "@/lib/metricas";
import { mesCurto } from "@/lib/etiquetas";
import { Etiqueta, Legenda, SeloReferencia, brl, inteiro } from "@/components/ui";
import { Conteiner, Faixa, NumeroGrande, Tag } from "@/components/marca";

export const dynamic = "force-dynamic";

const PORTAS = [
  { href: "/app/memorando", imagem: "/m/fundador.jpg", tempo: "1 minuto para a tese", titulo: "Memorando de investimento", texto: "Carta do fundador e os 12 capítulos — edição atualizada com os números do sistema." },
  { href: "/app/numeros", imagem: "/m/comparai.jpg", tempo: "5 minutos", titulo: "Números com prova", texto: "Cada métrica com definição única, origem e impressão digital. Clique e veja de onde veio." },
  { href: "/app/capital", imagem: "/m/bilhoes-parados.jpg", tempo: "10 minutos", titulo: "A história do dinheiro", texto: "De onde veio cada real, quanto custa o capital, o custo fixo e o que fica na carteira do cliente." },
  { href: "/app/valuation", imagem: "/m/cap5-modelo.jpg", tempo: "30 minutos", titulo: "Valuation", texto: "Referência do fundador, metodologia de nove métodos e a ponte do valor da empresa ao valor do sócio." },
];

// A capa do portal: o que a empresa é, o que já está provado e para onde ir.
export default async function Inicio() {
  const supabase = await criarClienteServidor();
  const [{ data: metricas }, { ultimo, serie }, { data: snapshots }] = await Promise.all([
    supabase.from("vos_metricas").select("metric_id").eq("ativo", true),
    valoresCarregados(),
    supabase.from("vos_snapshots").select("tipo, periodo").eq("tipo", "official").order("periodo", { ascending: false }).limit(1),
  ]);

  const todas = (metricas ?? []).map((m) => m.metric_id);
  const comValor = todas.filter((id) => ultimo.has(id));
  const verificadas = comValor.filter((id) => ultimo.get(id)!.etiqueta === "VERIFIED").length;
  const qualidade = todas.length ? Math.round((100 * (verificadas + 0.5 * (comValor.length - verificadas))) / todas.length) : 0;
  const oficial = snapshots?.[0];
  const u = (id: string) => ultimo.get(id);
  const arremates = u("GMV_AUCTION");
  const lances = u("BIDS_COUNT");
  const pagantes = u("CUSTOMERS_PAYING_90D");
  const gmv = u("GMV_GOODS");
  const passivo = u("PARTNER_CAPITAL_LIABILITY");
  const anterior = (id: string) => {
    const lista = serie.get(id) ?? [];
    return lista.length >= 2 ? lista[lista.length - 2] : null;
  };
  const arrAnt = anterior("GMV_AUCTION");
  const lancesAnt = anterior("BIDS_COUNT");
  const compara = (atual: number | null | undefined, ant: { valor: number | null; periodo: string } | null, fmt: (x: number) => string) =>
    atual != null && ant?.valor != null
      ? `${atual >= ant.valor ? "já acima de" : "contra"} ${mesCurto(ant.periodo)} inteiro (${fmt(ant.valor)})`
      : "";
  const carteira = u("WALLET_LIABILITY_TOTAL");

  return (
    <div>
      <section className="relative isolate overflow-hidden">
        <Image src="/m/capa.jpg" alt="" fill priority sizes="100vw" className="-z-10 object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-black via-black/85 to-black/40" aria-hidden />
        <Conteiner className="py-24 sm:py-32">
          <Tag>Área do investidor · confidencial</Tag>
          <h1 className="mt-5 max-w-4xl font-display text-4xl font-light leading-[1.1] text-white sm:text-6xl">
            A nova infraestrutura do <span className="text-accent">recommerce brasileiro</span> — com cada número rastreável.
          </h1>
          <p className="mt-6 max-w-2xl text-lg font-light text-texto">
            Memorando, números do sistema, contratos e riscos num só lugar. O que foi verificado está marcado, o que foi informado está
            marcado, e o que ainda não existe diz por quê.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/app/memorando" className="inline-flex items-center gap-2 rounded-md bg-accent px-5 py-3 font-semibold text-accent-ink hover:brightness-110">
              Ler o memorando <ArrowRight className="h-4 w-4" aria-hidden />
            </Link>
            <Link href="/app/numeros" className="rounded-md border border-white/40 px-5 py-3 font-semibold text-white hover:bg-white/10">
              Ver os números com prova
            </Link>
          </div>
        </Conteiner>
      </section>

      <Faixa>
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <Tag>30 segundos · o que já está provado</Tag>
            <h2 className="mt-3 font-display text-3xl font-light text-white sm:text-4xl">
              {gmv ? mesCurto(gmv.periodo) : ""}, direto do banco do aplicativo
            </h2>
          </div>
          <Link href="/app/numeros" className="text-sm text-pill underline underline-offset-4">{`todos os ${todas.length} números`}</Link>
        </div>
        <div className="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <NumeroGrande valor={arremates?.valor != null ? brl(arremates.valor) : "—"} rotulo="Arremates pagos" compacto sub={`${arremates?.nota ?? ""} · ${compara(arremates?.valor, arrAnt, brl)}`} etiqueta={arremates?.etiqueta} href="/app/prova/GMV_AUCTION" />
          <NumeroGrande valor={lances?.valor != null ? inteiro(lances.valor) : "—"} rotulo="Lances" compacto sub={`${lances?.nota ?? ""} · ${compara(lances?.valor, lancesAnt, inteiro)}`} etiqueta={lances?.etiqueta} href="/app/prova/BIDS_COUNT" />
          <NumeroGrande valor={gmv?.valor != null ? brl(gmv.valor) : "—"} rotulo="Mercadoria vendida e paga" compacto sub="sem depósitos, sem adesões" etiqueta={gmv?.etiqueta} href="/app/prova/GMV_GOODS" />
          <NumeroGrande valor={pagantes?.valor != null ? inteiro(pagantes.valor) : "—"} rotulo="Clientes pagantes" compacto sub="contas distintas, últimos 90 dias" etiqueta={pagantes?.etiqueta} href="/app/prova/CUSTOMERS_PAYING_90D" />
        </div>
      </Faixa>

      <section className="border-y border-white/10 bg-surface">
        <Conteiner className="grid gap-px py-0 md:grid-cols-3">
          <div className="py-10 md:pr-8">
            <p className="text-xs uppercase tracking-widest text-muted">Valuation</p>
            <p className="num mt-3 font-display text-4xl font-semibold text-accent">R$ 25.000.000</p>
            <div className="mt-2"><SeloReferencia /></div>
            <p className="mt-3 text-sm font-light text-texto">
              O valuation independente sai com método, pesos fixados antes e faixa — depois da metodologia v1.0 e do primeiro fechamento oficial.
            </p>
            <Link href="/app/valuation" className="mt-3 inline-block text-sm text-pill underline underline-offset-4">ver metodologia</Link>
          </div>
          <div className="border-white/10 py-10 md:border-l md:px-8">
            <p className="text-xs uppercase tracking-widest text-muted">Qualidade do dado</p>
            <p className="num mt-3 font-display text-4xl font-light text-white">{qualidade}<span className="text-2xl text-muted">/100</span></p>
            <p className="mt-3 text-sm font-light text-texto">
              {verificadas} verificadas · {comValor.length - verificadas} informadas · {todas.length - comValor.length} sem valor. A nota mede a prova por trás dos números.
            </p>
            <p className="mt-3 text-xs text-muted">Último fechamento oficial: {oficial ? mesCurto(oficial.periodo) : "nenhum ainda"} · série oficial desde 01/08/2026</p>
          </div>
          <div className="border-white/10 py-10 md:border-l md:pl-8">
            <p className="text-xs uppercase tracking-widest text-muted">Obrigações já conhecidas</p>
            <p className="num mt-3 font-display text-4xl font-light text-white">
              {passivo?.valor != null && carteira?.valor != null ? brl(passivo.valor + carteira.valor) : "—"}
            </p>
            <p className="mt-3 text-sm font-light text-texto">
              Capital de parceiros de compra a devolver ({passivo?.valor != null ? brl(passivo.valor) : "—"}) + saldos de clientes e rede ({carteira?.valor != null ? brl(carteira.valor) : "—"}).
            </p>
            <div className="mt-3 flex items-center gap-3"><Etiqueta tipo="VERIFIED" pequena /><Link href="/app/parceiros" className="text-sm text-pill underline underline-offset-4">ver contratos</Link></div>
          </div>
        </Conteiner>
      </section>

      <Faixa>
        <Tag>Por onde começar</Tag>
        <div className="mt-8 grid gap-5 md:grid-cols-2">
          {PORTAS.map((p) => (
            <Link key={p.href} href={p.href} className="group relative isolate flex min-h-[260px] flex-col justify-end overflow-hidden rounded-xl border border-white/10 p-7">
              <Image src={p.imagem} alt="" fill sizes="(min-width:768px) 50vw, 100vw" className="-z-10 object-cover transition duration-500 group-hover:scale-[1.03]" />
              <div className="absolute inset-0 -z-10 bg-gradient-to-t from-black via-black/75 to-black/20" aria-hidden />
              <p className="text-xs uppercase tracking-widest text-pill">{p.tempo}</p>
              <p className="mt-2 font-display text-3xl font-light text-white">{p.titulo}</p>
              <p className="mt-2 max-w-md text-[15px] font-light text-texto">{p.texto}</p>
              <span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-pill">Abrir <ArrowRight className="h-4 w-4" aria-hidden /></span>
            </Link>
          ))}
        </div>
        <div className="mt-8 grid gap-3 text-sm sm:grid-cols-3">
          {[["/app/dre", "DRE ago–out/26"], ["/app/parceiros", "Parceiros de compra"], ["/app/riscos", "Riscos e o que reduz cada um"], ["/app/governanca", "Governança e time"], ["/app/roadmap", "Metas e simulação"], ["/app/dataroom", "Data room"]].map(([href, t]) => (
            <Link key={href} href={href} className="flex items-center justify-between rounded-lg border border-white/10 bg-surface px-4 py-3 text-white hover:border-accent/60">
              {t} <ArrowRight className="h-4 w-4 text-pill" aria-hidden />
            </Link>
          ))}
        </div>
      </Faixa>

      <Conteiner className="pb-16">
        <Legenda />
      </Conteiner>
    </div>
  );
}
