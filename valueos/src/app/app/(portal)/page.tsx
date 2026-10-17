import Link from "next/link";
import { criarClienteServidor } from "@/lib/supabase/server";
import { valoresCarregados } from "@/lib/metricas";
import { mesCurto } from "@/lib/etiquetas";
import { Aviso, Cartao, Etiqueta, Grade, Legenda, Numero, SeloReferencia, brl, inteiro } from "@/components/ui";

export const dynamic = "force-dynamic";

// A capa: em 30 segundos, o que a empresa é, o que já está provado e para onde ir.
export default async function VisaoGeral() {
  const supabase = await criarClienteServidor();
  const [{ data: metricas }, { ultimo }, { data: snapshots }] = await Promise.all([
    supabase.from("vos_metricas").select("metric_id").eq("ativo", true),
    valoresCarregados(),
    supabase.from("vos_snapshots").select("tipo, periodo, fechado_em").eq("tipo", "official").order("periodo", { ascending: false }).limit(1),
  ]);

  const todas = (metricas ?? []).map((m) => m.metric_id);
  const comValor = todas.filter((id) => ultimo.has(id));
  const verificadas = comValor.filter((id) => ultimo.get(id)!.etiqueta === "VERIFIED").length;
  const qualidade = todas.length ? Math.round((100 * (verificadas + 0.5 * (comValor.length - verificadas))) / todas.length) : 0;
  const oficial = snapshots?.[0];

  const gmv = ultimo.get("GMV_GOODS");
  const entradas = ultimo.get("CASH_IN_GROSS");
  const clientes = ultimo.get("CUSTOMERS_PAYING_90D");
  const licenciados = ultimo.get("LICENSEES_ACTIVE_30D");
  const passivo = ultimo.get("PARTNER_CAPITAL_LIABILITY");
  const carteira = ultimo.get("WALLET_LIABILITY_TOTAL");
  const periodo = gmv ? mesCurto(gmv.periodo) : "—";

  return (
    <div className="space-y-12">
      <section className="space-y-6">
        <div className="max-w-3xl">
          <p className="text-xs font-semibold uppercase tracking-widest text-accent">Leilão NoZap · Compras Full Comércio Ltda</p>
          <h1 className="mt-2 text-3xl font-semibold leading-tight sm:text-5xl">
            Infraestrutura de recommerce, leilão e distribuição pelo WhatsApp — com cada número rastreável.
          </h1>
          <p className="mt-4 text-base text-muted">
            Este portal junta o memorando de investimento, os números recalculados do sistema, os contratos e os
            riscos. Nada aqui é promessa: o que foi verificado está marcado, o que foi informado está marcado, e o que
            ainda não existe diz por quê.
          </p>
        </div>
        <Legenda />
      </section>

      <section className="space-y-4">
        <h2 className="text-sm font-semibold uppercase tracking-widest text-muted">30 segundos · o que já está provado ({periodo})</h2>
        <Grade colunas={4}>
          <Numero rotulo="Mercadoria vendida e paga" valor={gmv?.valor != null ? brl(gmv.valor) : "—"} etiqueta={gmv?.etiqueta} origem={gmv?.nota ?? undefined} href="/app/prova/GMV_GOODS" grande />
          <Numero rotulo="Entradas brutas no app" valor={entradas?.valor != null ? brl(entradas.valor) : "—"} etiqueta={entradas?.etiqueta} origem="inclui depósito de carteira" href="/app/prova/CASH_IN_GROSS" grande />
          <Numero rotulo="Clientes pagantes (90 dias)" valor={clientes?.valor != null ? inteiro(clientes.valor) : "—"} etiqueta={clientes?.etiqueta} origem="contas distintas" href="/app/prova/CUSTOMERS_PAYING_90D" grande />
          <Numero rotulo="Licenciados com acesso (30 dias)" valor={licenciados?.valor != null ? inteiro(licenciados.valor) : "—"} etiqueta={licenciados?.etiqueta} origem="de 15 a 23, conforme a definição" href="/app/prova/LICENSEES_ACTIVE_30D" grande />
        </Grade>
        <Grade colunas={3}>
          <Cartao>
            <p className="text-xs uppercase tracking-widest text-muted">Valuation independente</p>
            <p className="mt-2 text-2xl font-semibold">Ainda não calculado</p>
            <p className="mt-2 text-xs text-muted">
              Só nasce depois da metodologia v1.0 travada e do primeiro fechamento oficial. Enquanto isso, a única
              referência é a declarada pelo fundador: <span className="num font-semibold text-foreground">R$ 25 mi</span>{" "}
              <SeloReferencia /> — é ponto de partida, não resultado.
            </p>
            <Link href="/app/valuation" className="mt-3 inline-block text-sm underline">
              Ver a metodologia
            </Link>
          </Cartao>
          <Cartao>
            <p className="text-xs uppercase tracking-widest text-muted">Qualidade do dado</p>
            <p className="num mt-2 text-2xl font-semibold">{qualidade}/100</p>
            <p className="mt-2 text-xs text-muted">
              {verificadas} verificadas · {comValor.length - verificadas} informadas · {todas.length - comValor.length} sem valor. A nota
              mede a prova por trás dos números, não o desempenho da empresa.
            </p>
            <Link href="/app/numeros" className="mt-3 inline-block text-sm underline">
              Ver os 30 números
            </Link>
          </Cartao>
          <Cartao>
            <p className="text-xs uppercase tracking-widest text-muted">Obrigações já conhecidas</p>
            <p className="num mt-2 text-2xl font-semibold">
              {passivo?.valor != null && carteira?.valor != null ? brl(passivo.valor + carteira.valor) : "—"}
            </p>
            <p className="mt-2 text-xs text-muted">
              Capital de parceiros de compra a devolver ({passivo?.valor != null ? brl(passivo.valor) : "—"}) + saldos de clientes e
              rede ({carteira?.valor != null ? brl(carteira.valor) : "—"}). <Etiqueta tipo="VERIFIED" pequena />
            </p>
            <Link href="/app/parceiros" className="mt-3 inline-block text-sm underline">
              Ver os contratos
            </Link>
          </Cartao>
        </Grade>
        <Aviso tipo="regra" titulo="Depósito não é receita">
          Dinheiro que o cliente coloca na carteira é obrigação da empresa com ele. Em setembro e outubro, cerca de dois
          terços das entradas do app foram depósitos — por isso a capa mostra mercadoria vendida, não entradas.
        </Aviso>
      </section>

      <section className="space-y-4">
        <h2 className="text-sm font-semibold uppercase tracking-widest text-muted">1 minuto · por que a empresa existe</h2>
        <Link href="/app/memorando" className="block rounded-2xl border border-border bg-surface p-6 transition hover:border-accent/60">
          <p className="text-xs font-semibold uppercase tracking-widest text-accent">Memorando de investimento · versão revisada</p>
          <p className="mt-2 text-xl font-semibold">O Brasil não sofre por falta de produto, de consumidor nem de empreendedor. Sofre por falta de conexão eficiente.</p>
          <p className="mt-2 text-sm text-muted">
            Carta do fundador, problema, oportunidade, solução, tecnologia, modelo de negócio, tração, governança, barreiras, roadmap e
            visão 2035 — doze capítulos, com cada número etiquetado e os dados do sistema ao lado do que a administração declara.
          </p>
          <span className="mt-3 inline-block text-sm underline">Ler o memorando →</span>
        </Link>
      </section>

      <section className="space-y-4">
        <h2 className="text-sm font-semibold uppercase tracking-widest text-muted">5 minutos · tração, financeiro e risco</h2>
        <Grade colunas={4}>
          <Numero rotulo="Números" valor="30 métricas" origem="definição, origem e hash" href="/app/numeros" />
          <Numero rotulo="DRE" valor="ago–out/26" origem="duas visões: venda e comissão" href="/app/dre" />
          <Numero rotulo="Parceiros de compra" valor="R$ 502 mil" origem="obrigação total dos 2 contratos" href="/app/parceiros" />
          <Numero rotulo="Riscos" valor="10 primeiros" origem="com o que reduz cada um" href="/app/riscos" />
        </Grade>
      </section>

      <section className="space-y-4">
        <h2 className="text-sm font-semibold uppercase tracking-widest text-muted">30 minutos · análise completa</h2>
        <Grade colunas={4}>
          <Numero rotulo="Valuation" valor="Metodologia v1.0" origem="9 métodos, pesos pré-registrados" href="/app/valuation" />
          <Numero rotulo="Governança" valor="8 níveis" origem="time, fundador × sócio, 1%" href="/app/governanca" />
          <Numero rotulo="Metas e simulação" valor="Plano × realizado" origem="o que precisa ser verdade" href="/app/roadmap" />
          <Numero rotulo="Data room" valor="9 pastas" origem="o que existe e o que falta" href="/app/dataroom" />
        </Grade>
      </section>

      <section className="grid gap-4 sm:grid-cols-2">
        <Cartao titulo="Último fechamento oficial">
          <p className="num text-xl font-semibold">{oficial ? mesCurto(oficial.periodo) : "Nenhum ainda"}</p>
          <p className="mt-1 text-xs text-muted">
            O fechamento oficial é um retrato imutável, com impressão digital. Até o primeiro, tudo o que você vê é leitura ao vivo
            da última carga — por isso ainda não há valuation.
          </p>
        </Cartao>
        <Cartao titulo="Série oficial">
          <p className="num text-xl font-semibold">desde 01/08/2026</p>
          <p className="mt-1 text-xs text-muted">
            É o marco do próprio app (“antes disso é teste, sem valor financeiro”). O histórico anterior aparece no memorando como dado
            da administração, nunca somado à série oficial.
          </p>
        </Cartao>
      </section>
    </div>
  );
}
