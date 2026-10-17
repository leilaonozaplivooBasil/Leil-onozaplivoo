import Image from "next/image";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { valoresCarregados } from "@/lib/metricas";
import { papelAtual, eConselho } from "@/lib/papel";
import { mesCurto } from "@/lib/etiquetas";
import { Etiqueta, NotaRevisao, SeloReferencia, brl, inteiro } from "@/components/ui";
import { Capitulo, Cartao, Citacao, Conteiner, Faixa, Grade, Hoje, NumeroGrande, Tag, Texto, Titulo } from "@/components/marca";

export const dynamic = "force-dynamic";

const METODOS = [
  ["Múltiplos de empresas listadas (com desconto de tamanho e liquidez)", "25%", "única referência externa observável; porte muito diferente"],
  ["Método VC (valor de saída ÷ retorno exigido)", "20%", "é a conta que um investidor de risco faz; depende do plano"],
  ["Transações precedentes", "15%", "preço real pago por empresas parecidas; escasso no Brasil"],
  ["Soma das partes (varejo · leilão · loja · licenciamento · tecnologia)", "15%", "cada negócio tem perfil e comparável diferente"],
  ["Fluxo de caixa descontado (cenários ponderados)", "10%", "baixo até haver 12 meses de série de dinheiro real"],
  ["Piso: custo de reposição da tecnologia + patrimônio ajustado", "10%", "o valor não cai abaixo do que se reconstrói ou liquida"],
  ["Economia por unidade (LTV/CAC)", "5%", "sobe para 15–20% quando houver CAC e margem por venda"],
  ["Scorecard / Berkus (conferência)", "0%", "só para mostrar se o resultado destoa de um padrão de mercado"],
];

const MERCADOS = [
  "Desburocratização do Leilão", "Recommerce Inteligente", "Venda Direta de Fábrica", "Social Commerce via WhatsApp", "CAC Positivo",
  "Entretenimento Transacional", "Liquidez de Estoques", "Infraestrutura Nacional de Recommerce", "Economia Circular de Consumo",
];

// Valuation: a vitrine do site de valuation, com o "painel vivo" no lugar da planilha e a metodologia que vai gerar o número independente.
export default async function Valuation() {
  const [{ ultimo, serie }, papel] = await Promise.all([valoresCarregados(), papelAtual()]);
  const conselho = eConselho(papel);
  const v = (id: string) => ultimo.get(id)?.valor ?? null;
  const mes = (id: string, iso: string) => serie.get(id)?.find((x) => x.periodo === iso)?.valor ?? null;
  const r = (x: number | null) => (x === null ? "—" : brl(x));
  const n = (x: number | null) => (x === null ? "—" : inteiro(x));
  const loc = v("TECH_LOC");
  const estoque = v("INVENTORY_AT_COST");
  const carteira = v("WALLET_LIABILITY_TOTAL");
  const parceiros = v("PARTNER_CAPITAL_LIABILITY");
  const vencidas = v("EXPENSES_OVERDUE");
  const entAgo = mes("CASH_IN_GROSS", "2026-08-01");
  const entSet = mes("CASH_IN_GROSS", "2026-09-01");
  const arrSet = mes("GMV_AUCTION", "2026-09-01");
  const arrOut = mes("GMV_AUCTION", "2026-10-01");

  // O painel vivo: as linhas que entram no modelo, mês a mês.
  const PERIODOS = ["2026-08-01", "2026-09-01", "2026-10-01"];
  const PAINEL: { rotulo: string; id?: string; calc?: (p: string) => number | null; etiqueta: string; nota?: string; forte?: boolean }[] = [
    { rotulo: "Entradas pagas no app (inclui depósitos)", id: "CASH_IN_GROSS", etiqueta: "VERIFIED" },
    { rotulo: "Depósitos de carteira (saldo do cliente, não receita)", id: "WALLET_DEPOSITS", etiqueta: "VERIFIED" },
    { rotulo: "Mercadoria vendida e paga (GMV)", id: "GMV_GOODS", etiqueta: "VERIFIED", forte: true },
    { rotulo: "  dos quais, arremates de leilão", id: "GMV_AUCTION", etiqueta: "VERIFIED" },
    { rotulo: "Taxas e adesões", id: "REVENUE_FEES", etiqueta: "VERIFIED" },
    { rotulo: "Comissão retida (receita reconhecida pelo app)", id: "REVENUE_COMMISSION_RETAINED", etiqueta: "VERIFIED" },
    { rotulo: "Despesas pagas (lançamento manual)", id: "EXPENSES_PAID", etiqueta: "MANAGEMENT_DATA" },
    { rotulo: "Remuneração dos parceiros de compra", calc: (p) => (p === "2026-08-01" ? 0 : p === "2026-09-01" ? 1600 : 15000), etiqueta: "VERIFIED", nota: "pagos e conferidos no extrato" },
    {
      rotulo: "Retrato de caixa do app: GMV + taxas − despesas − parceiros",
      calc: (p) => {
        const g = mes("GMV_GOODS", p), f = mes("REVENUE_FEES", p), d = mes("EXPENSES_PAID", p);
        if (g === null || d === null) return null;
        return g + (f ?? 0) - d - (p === "2026-08-01" ? 0 : p === "2026-09-01" ? 1600 : 15000);
      },
      etiqueta: "MANAGEMENT_DATA",
      forte: true,
    },
    { rotulo: "Lances registrados", id: "BIDS_COUNT", etiqueta: "VERIFIED" },
  ];
  const celula = (l: (typeof PAINEL)[number], p: string) => {
    const x = l.id ? mes(l.id, p) : l.calc ? l.calc(p) : null;
    if (x === null) return "—";
    return l.id === "BIDS_COUNT" ? inteiro(x) : brl(x);
  };

  return (
    <div>
      {/* CAPA — como no site de valuation */}
      <section className="relative isolate overflow-hidden text-center">
        <Image src="/m/cap9-valuation.jpg" alt="" fill priority sizes="100vw" className="-z-10 object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-black/70 via-black/80 to-black" aria-hidden />
        <Conteiner className="py-20 sm:py-28">
          <div className="relative mx-auto aspect-[610/900] w-40 sm:w-56">
            <Image src="/m/logo.png" alt="Leilão NoZap" fill priority sizes="224px" className="object-contain" />
          </div>
          <p className="mt-8 font-display text-4xl font-semibold text-white sm:text-5xl">LEILÃO NOZAP</p>
          <p className="mt-3 font-display text-xl font-light text-white/90 sm:text-2xl">A Nova Infraestrutura do Recommerce Brasileiro</p>
          <p className="mt-4 text-sm font-light text-texto">
            {loc ? `${Math.round(loc / 1000)} mil linhas de código` : ""} · arremates de outubro (16 dias) {arrOut !== null && arrSet !== null && arrOut > arrSet ? "acima de setembro inteiro" : "em crescimento"} · série oficial desde 01/08/2026
          </p>
          <div className="mx-auto my-10 h-px max-w-3xl bg-white/20" />
          <p className="font-display text-2xl font-light text-white">Valuation Corporativo</p>
          <p className="num mt-4 font-display text-5xl font-bold tracking-tight text-accent sm:text-8xl">R$ 25.000.000</p>
          <div className="mt-4"><SeloReferencia /></div>
          <p className="mx-auto mt-6 max-w-3xl font-light text-texto">
            É o valor que o fundador declara e que foi usado na venda de 1%. Abaixo, cada ativo que sustenta esse valor aparece ao lado do número que o sistema mede hoje — e, no fim, o método que vai gerar o valuation independente.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <a href="#painel" className="rounded-md bg-accent px-5 py-3 font-semibold text-accent-ink hover:brightness-110">Ver o painel vivo</a>
            <a href="#metodologia" className="rounded-md border border-white/40 px-5 py-3 font-semibold text-white hover:bg-white/10">Ver a metodologia</a>
          </div>
        </Conteiner>
      </section>

      {/* O QUE VALE R$ 25 MI — cada ativo com o dado de hoje */}
      <Faixa id="ativos">
        <Titulo tag="Ativos que sustentam o valuation">O Que Vale R$ 25.000.000</Titulo>
        <p className="mt-4 max-w-4xl font-light text-texto">
          No site, os ativos aparecem como afirmação. Aqui, cada um traz o número medido no sistema, a etiqueta de qualidade e o link para a prova.
        </p>
        <Grade colunas={2} className="mt-8">
          <Cartao tom="lateral" titulo="Tecnologia proprietária" rodape={<Hoje href="/app/prova/TECH_LOC">{`${n(loc)} linhas em 2.033 arquivos (site: 178 mil / 883)`}</Hoje>}>
            Marketplace, aplicativo, leilão com reserva de saldo, analisador de lotes, CRM, financeiro e comissionamento — código próprio sobre infraestrutura de mercado.
          </Cartao>
          <Cartao tom="lateral" titulo="Operação validada" rodape={<Hoje href="/app/prova/CASH_IN_GROSS">{`entradas no app: ago ${r(entAgo)} → set ${r(entSet)}`}</Hoje>}>
            Vendas reais, pagas e conciliadas ao centavo entre o app, o gateway e os bancos.
          </Cartao>
          <Cartao tom="lateral" titulo="Leilão inteligente" rodape={<Hoje href="/app/prova/GMV_AUCTION">{`arremates: set ${r(arrSet)} · out (16 dias) ${r(arrOut)}`}</Hoje>}>
            O motor de escala já em operação: reserva de saldo por lance e devolução automática a quem não vence.
          </Cartao>
          <Cartao tom="lateral" titulo="Rede comercial nacional" rodape={<Hoje href="/app/prova/LICENSEES_TOTAL">{`${n(v("LICENSEES_TOTAL"))} licenciados por cargo · ${n(v("LICENSEES_ACTIVE_30D"))} ativos em 30 dias (site: “80+”)`}</Hoje>}>
            Licenciados, executivos, vendedores e parceiros, organizados em oito níveis de carreira.
          </Cartao>
          <Cartao tom="lateral" titulo="Base de clientes" rodape={<Hoje href="/app/prova/CUSTOMERS_PAYING_90D">{`${n(v("USERS_REGISTERED"))} contas · ${n(v("CUSTOMERS_PAYING_90D"))} pagantes em 90 dias · ${n(v("BUYERS_REPEAT"))} recorrentes`}</Hoje>}>
            Compradores ativos que compram pelo WhatsApp e pelo aplicativo.
          </Cartao>
          <Cartao tom="lateral" titulo="Modelo de licenciamento" rodape={<Hoje href="/app/prova/REVENUE_FEES">{`adesões e taxas: ago ${r(mes("REVENUE_FEES", "2026-08-01"))} · set ${r(mes("REVENUE_FEES", "2026-09-01"))} · receita recorrente contratada: ${r(v("REVENUE_RECURRING"))}`}</Hoje>}>
            Licença com adesão; a recorrência (mensalidade) ainda não existe e entra no valuation como opção, não como receita.
          </Cartao>
          <Cartao tom="lateral" titulo="Ecossistema integrado" rodape={<Hoje href="/app/prova/INVENTORY_AT_COST">{`estoque a custo de ${r(estoque)}`}</Hoje>}>
            Leilão NoZap, ComparAI, Top College e X-EOS — empresas complementares que se reforçam.
          </Cartao>
          <Cartao tom="lateral" titulo="Propriedade intelectual" rodape={<Hoje etiqueta="NAO_DISPONIVEL">titularidade do código, marca e domínios a documentar no data room</Hoje>}>
            Plataforma, marca e domínios. Para entrar no valor, precisa do registro e dos contratos de cessão.
          </Cartao>
        </Grade>
        <Citacao className="mt-10 !font-light">
          O valor de R$ 25.000.000 é a referência do fundador. O valuation independente reflete o que os dados sustentam — e mostra, ativo por ativo, o que falta para a faixa subir.
        </Citacao>
      </Faixa>

      {/* PAINEL VIVO — no lugar da planilha */}
      <section id="painel" className="scroll-mt-20 border-y border-white/10 bg-surface py-16 sm:py-24">
        <Conteiner>
          <Titulo tag="Painel vivo · no lugar da planilha" sub="Os números que entram no modelo, mês a mês, direto do sistema">O Modelo em Tempo Real</Titulo>
          <div className="mt-8 overflow-x-auto rounded-lg border border-white/15">
            <table className="w-full min-w-[720px] text-left text-[15px]">
              <thead className="bg-accent text-accent-ink">
                <tr>
                  <th className="px-5 py-3 font-semibold">Linha</th>
                  {PERIODOS.map((p) => (
                    <th key={p} className="px-5 py-3 text-right font-semibold">{mesCurto(p)}{p === "2026-10-01" ? " (até 16)" : ""}</th>
                  ))}
                  <th className="px-5 py-3 font-semibold">Etiqueta</th>
                </tr>
              </thead>
              <tbody className="bg-black/40 text-white">
                {PAINEL.map((l) => (
                  <tr key={l.rotulo} className={`border-t border-white/10 ${l.forte ? "bg-accent/10 font-medium" : "font-light"}`}>
                    <td className="px-5 py-3">
                      {l.id ? (
                        <Link href={`/app/prova/${l.id}`} className="hover:underline">{l.rotulo.trim()}</Link>
                      ) : (
                        l.rotulo.trim()
                      )}
                      {l.nota && <span className="block text-xs text-muted">{l.nota}</span>}
                    </td>
                    {PERIODOS.map((p) => (
                      <td key={p} className="num px-5 py-3 text-right">{celula(l, p)}</td>
                    ))}
                    <td className="px-5 py-3"><Etiqueta tipo={l.etiqueta} pequena /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-4 text-sm font-light text-muted">
            A planilha tradicional mistura número verificado com número digitado. Aqui cada linha tem dono, data e prova — e muda sozinha a cada carga. A DRE completa, com as linhas que ainda não existem e o motivo, está em{" "}
            <Link href="/app/dre" className="text-pill underline underline-offset-2">DRE</Link>.
          </p>
          <div className="mt-10 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
            <NumeroGrande valor={r(estoque)} rotulo="Estoque a custo" sub="ativo na ponte do valor" compacto etiqueta="VERIFIED" href="/app/prova/INVENTORY_AT_COST" />
            <NumeroGrande valor={r(carteira)} rotulo="Saldos de clientes e rede" compacto sub="obrigação (sai do valor)" etiqueta="VERIFIED" href="/app/prova/WALLET_LIABILITY_TOTAL" />
            <NumeroGrande valor={r(parceiros)} rotulo="Capital de parceiros" compacto sub="a devolver em 2028" etiqueta="VERIFIED" href="/app/parceiros" />
            <NumeroGrande valor={r(vencidas)} rotulo="Despesas vencidas" compacto sub="lançamento do app, a conferir" etiqueta="MANAGEMENT_DATA" href="/app/prova/EXPENSES_OVERDUE" />
          </div>
        </Conteiner>
      </section>

      {/* MERCADO E MOMENTO — conteúdo do site de valuation */}
      <Capitulo numero="Tamanho do mercado" titulo="Mercados Bilionários. Uma Única Plataforma." imagem="/m/bilhoes-parados.jpg" lado="esquerda">
        <p>A Leilão NoZap está posicionada na interseção de múltiplos mercados que, individualmente, movimentam centenas de bilhões de reais por ano no Brasil. A convergência desses mercados em uma única plataforma cria uma oportunidade estrutural.</p>
      </Capitulo>
      <Faixa>
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <NumeroGrande valor="R$185B+" rotulo="E-commerce Brasil" sub="volume anual" />
          <NumeroGrande valor="R$40B+" rotulo="Logística reversa" sub="devoluções anuais" />
          <NumeroGrande valor="R$25B+" rotulo="Estoques excedentes" sub="capital represado" />
          <NumeroGrande valor="35% a.a." rotulo="Recommerce global" sub="crescimento" />
        </div>
        <p className="mt-6 text-center text-xs text-muted">
          <Etiqueta tipo="MANAGEMENT_DATA" pequena /> Estimativas citadas pela administração; fonte, ano e método serão anexados ao data room antes de entrarem em qualquer cálculo.
        </p>
        <div className="mt-16">
          <Titulo tag="Mercados disruptados">9 Mercados Convergindo para Uma Plataforma</Titulo>
          <div className="mt-8 flex flex-wrap gap-3">
            {MERCADOS.map((m) => (
              <span key={m} className="rounded-full border border-accent/60 bg-accent/10 px-4 py-2 font-display text-base font-light text-white">{m}</span>
            ))}
          </div>
          <p className="mt-6 max-w-4xl font-light text-texto">Cada um desses mercados representa uma camada de valor independente. A combinação de todos eles em um único ecossistema é o diferencial competitivo que torna a Leilão NoZap estruturalmente difícil de replicar.</p>
        </div>
      </Faixa>

      <Capitulo numero="Janela de oportunidade" titulo="Por Que Agora?" sub="Há 5 anos faltava tecnologia. Daqui a 5 anos existirão concorrentes." imagem="/m/agora.jpg">
        <p>Inteligência artificial disponível pela primeira vez. WhatsApp como principal canal de comunicação e venda do país. E-commerce maduro e devoluções em alta. Consumidor acostumado a comprar online. Economia circular como tendência global.</p>
        <p>A infraestrutura para resolver esse problema de forma integrada ainda não existe no Brasil. A Leilão NoZap está construindo essa infraestrutura — agora.</p>
      </Capitulo>

      <Faixa>
        <Titulo tag="Infraestrutura nacional">A Nova Camada de Liquidez do E-commerce Brasileiro</Titulo>
        <p className="mt-4 max-w-4xl font-light text-texto">Complementando os grandes players, não competindo com eles.</p>
        <Grade colunas={3} className="mt-8">
          <Cartao titulo="Para os marketplaces">Liquidação rápida de devoluções — passivo vira receita.</Cartao>
          <Cartao titulo="Para as fábricas e PMEs">Acesso direto a compradores nacionais, sem estrutura própria.</Cartao>
          <Cartao titulo="Para os consumidores">Produtos de qualidade com descontos reais — não promoções artificiais.</Cartao>
        </Grade>
        <div className="mt-10 grid gap-5 md:grid-cols-2">
          <Cartao tom="escuro" titulo="O modelo atual">Devolução → custo → depreciação → descarte. Todos perdem.</Cartao>
          <Cartao tom="cheio" titulo="O modelo Leilão NoZap">Devolução → anúncio → venda → liquidez → comissão. Todos ganham.</Cartao>
        </div>
        <div className="mt-10">
          <p className="font-display text-2xl font-light text-accent">Modelo econômico declarado</p>
          <Grade colunas={3} className="mt-4">
            <Cartao tom="escuro" titulo="Aquisição de lotes">Compra a 20–25% do valor de mercado. <span className="mt-2 block"><Etiqueta tipo="MANAGEMENT_DATA" pequena /></span></Cartao>
            <Cartao tom="escuro" titulo="Venda ao consumidor">20% abaixo do mercado, para giro rápido. <span className="mt-2 block"><Etiqueta tipo="MANAGEMENT_DATA" pequena /></span></Cartao>
            <Cartao tom="escuro" titulo="Margem por venda">Será medida quando o custo de cada venda for gravado no app. <span className="mt-2 block"><Etiqueta tipo="NAO_DISPONIVEL" pequena /></span></Cartao>
          </Grade>
        </div>
      </Faixa>

      <section className="grid lg:grid-cols-[minmax(0,62%)_minmax(0,38%)]">
        <div className="bg-[#070707] px-5 py-16 sm:px-12 lg:px-16">
          <Tag>Ecossistema estratégico</Tag>
          <h2 className="mt-4 font-display text-3xl font-light text-white sm:text-5xl">Um Grupo de Empresas. Uma Infraestrutura Integrada.</h2>
          <div className="mt-8 space-y-5">
            {[
              ["/m/logo.png", "Leilão NoZap", "Plataforma central de recommerce, leilões e distribuição inteligente via WhatsApp."],
              ["/m/eco-comparai.jpg", "ComparAI", "Inteligência artificial para análise e precificação de lotes."],
              ["/m/eco-topcollege.png", "Top College", "Faculty of Entrepreneurs — formação executiva e capacitação de licenciados."],
              ["/m/eco-xeos.jpg", "X-EOS", "Estrutura de operações e expansão que sustenta a rede."],
            ].map(([src, t, d]) => (
              <div key={t} className="flex items-center gap-5">
                <div className="relative h-16 w-16 shrink-0 overflow-hidden rounded-xl bg-white/5">
                  <Image src={src} alt={t} fill sizes="64px" className="object-contain" />
                </div>
                <div>
                  <p className="font-display text-xl font-light text-accent">{t}</p>
                  <p className="text-[15px] font-light text-texto">{d}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="relative min-h-[46vh]">
          <Image src="/m/ecossistema-rede.jpg" alt="" fill sizes="(min-width:1024px) 38vw, 100vw" className="object-cover" />
        </div>
      </section>

      <Faixa>
        <Titulo tag="Roadmap">Dois Anos para Escala Nacional</Titulo>
        <div className="mt-10 grid gap-10 md:grid-cols-3">
          <NumeroGrande valor="300" rotulo="Licenciados em 2026" sub={`meta · hoje ${n(v("LICENSEES_TOTAL"))} por cargo, ${n(v("LICENSEES_ACTIVE_30D"))} ativos`} etiqueta="FORECAST" />
          <NumeroGrande valor="1.000" rotulo="Licenciados em 2027" sub="meta de escala nacional" etiqueta="FORECAST" />
          <NumeroGrande valor="10K" rotulo="Vendedores em 2027" sub="base de revendedores ativos" etiqueta="FORECAST" />
        </div>
        <p className="mt-6 text-center text-sm font-light text-muted">
          Plano × realizado e simulador por alavancas em <Link href="/app/roadmap" className="text-pill underline underline-offset-2">Metas e simulação</Link>.
        </p>
      </Faixa>

      {/* METODOLOGIA — como o número independente vai nascer */}
      <Capitulo id="metodologia" numero="Metodologia v1.0 · proposta" titulo="Como o Valuation Independente Vai Nascer" sub="Nove métodos, pesos fixados antes de ver o resultado" imagem="/m/ia.jpg" lado="direita">
        <p>O valor independente sai como faixa (baixo · central · alto), com confiança e score de risco, só depois de: metodologia v1.0 aprovada, pesos registrados com impressão digital, primeiro fechamento oficial e decisão sobre o perímetro avaliado. A primeira rodada é privada, só para o conselho.</p>
      </Capitulo>

      <Faixa>
        <Grade colunas={2}>
          <Cartao tom="verde" titulo="Referência do fundador">
            <p className="num font-display text-4xl font-semibold text-accent">R$ 25.000.000</p>
            <div className="mt-2"><SeloReferencia /></div>
            <p className="mt-3">Lacrada com impressão digital antes da primeira rodada, para que o cálculo não seja puxado por ela. Depois, comparada com o resultado, com a explicação de cada diferença.</p>
          </Cartao>
          <Cartao tom="azul" titulo="Valuation independente">
            <p className="font-display text-4xl font-light text-white">Não calculado</p>
            <div className="mt-2"><Etiqueta tipo="NAO_DISPONIVEL" pequena /></div>
            <p className="mt-3">Nasce com o primeiro fechamento oficial. Nunca escolhemos método por dar valor maior; método sem dado suficiente tem peso zero e aparece como “não calculado”.</p>
          </Cartao>
        </Grade>

        <div className="mt-14">
          <Titulo tag="Antes de qualquer número">O Que Está Sendo Avaliado</Titulo>
          <Grade colunas={3} className="mt-8">
            <Cartao tom="escuro" titulo="A. Compras Full Comércio Ltda">A empresa com CNPJ, contas, contabilidade e o nome fantasia Leilão NoZap. É o perímetro padrão enquanto a titularidade dos outros ativos não for documentada.</Cartao>
            <Cartao tom="escuro" titulo="B. Ecossistema">A + app, marca, rede, ComparAI e parcerias. Só faz sentido se um único CNPJ (ou contrato) reunir esses ativos.</Cartao>
            <Cartao tom="escuro" titulo="C. Só a plataforma">Código, marca, domínios e rede de licenciados. Exige saber quem é o dono de cada um.</Cartao>
          </Grade>
        </div>

        <div className="mt-14">
          <Titulo tag="Os métodos">Nove Métodos, Um Resultado em Faixa</Titulo>
          <div className="mt-8 overflow-x-auto rounded-lg border border-white/15">
            <table className="w-full min-w-[640px] text-left text-[15px]">
              <thead className="bg-accent text-accent-ink">
                <tr><th className="px-5 py-3 font-semibold">Método</th><th className="px-5 py-3 font-semibold">Peso</th><th className="px-5 py-3 font-semibold">Por quê</th></tr>
              </thead>
              <tbody className="bg-black/40 text-white">
                {METODOS.map((m) => (
                  <tr key={m[0]} className="border-t border-white/10">
                    <td className="px-5 py-3 font-light">{m[0]}</td>
                    <td className="num px-5 py-3 font-semibold text-pill">{m[1]}</td>
                    <td className="px-5 py-3 font-light text-texto">{m[2]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <Texto className="mt-6">
            <p>Cada premissa entra como <strong>faixa</strong>, não como ponto. Milhares de sorteios produzem a distribuição de valor por método; a mistura pelos pesos dá a faixa final (percentis 25, 50 e 75). Qualidade de dado baixa alarga a faixa por regra. Mudar peso é versão nova da metodologia, com data, autor, motivo e impacto registrados.</p>
          </Texto>
        </div>

        <div className="mt-14">
          <Titulo tag="Do valor da operação ao valor do sócio">A Ponte — O Que Entra e o Que Sai</Titulo>
          <div className="mt-8 overflow-x-auto rounded-lg border border-white/15">
            <table className="w-full min-w-[720px] text-left text-[15px]">
              <thead className="bg-white/5 text-xs uppercase tracking-wider text-muted">
                <tr><th className="px-5 py-3">Item</th><th className="px-5 py-3">Sinal</th><th className="px-5 py-3">Hoje</th><th className="px-5 py-3">Etiqueta</th></tr>
              </thead>
              <tbody className="font-light text-white">
                {[
                  ["Valor da operação (EV) — triangulação dos métodos", "+", "não calculado", "NAO_DISPONIVEL"],
                  ["Caixa verificado", "+", "extratos de 2025 e de todas as contas não disponíveis", "NAO_DISPONIVEL"],
                  ["Estoque a custo", "+", r(estoque), "VERIFIED"],
                  ["Cotas de consórcio no nome da empresa, líquidas do saldo devedor", "+", "21 cartas (2 contempladas); saldo devedor a informar", "MANAGEMENT_DATA"],
                  ["Saldos de clientes e rede (carteira, comissões, crédito de vendedor)", "−", r(carteira), "VERIFIED"],
                  ["Capital dos parceiros de compra (principal)", "−", r(parceiros), "VERIFIED"],
                  ["Remuneração dos parceiros acima do custo de mercado (valor presente)", "−", "a calcular na metodologia", "NAO_DISPONIVEL"],
                  ["Despesas vencidas em aberto (lançamento do app)", "−", r(vencidas), "MANAGEMENT_DATA"],
                  ["Tributos e encargos a pagar", "−", "R$ 83,2 mil + R$ 85,0 mil em 31/12/2025; situação atual desconhecida", "MANAGEMENT_DATA"],
                  ["Obrigação do 1% do faturamento bruto aos fundadores", "−", "base de cálculo a definir", "NAO_DISPONIVEL"],
                  ["= Valor do equity × participação de cada sócio", "", "contrato social atual não disponível", "NAO_DISPONIVEL"],
                ].map(([item, sinal, hoje, et]) => (
                  <tr key={item} className="border-t border-white/10">
                    <td className="px-5 py-3">{item}</td>
                    <td className="px-5 py-3 font-semibold">{sinal}</td>
                    <td className="num px-5 py-3 text-texto">{hoje}</td>
                    <td className="px-5 py-3"><Etiqueta tipo={et} pequena /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-14">
          <Grade colunas={2}>
            <Cartao tom="escuro" titulo="O que sustenta valor">
              <ul className="list-disc space-y-1 pl-5">
                <li>Motor de leilão em operação e acelerando: {n(mes("BIDS_COUNT", "2026-10-01"))} lances em outubro (até o dia 17).</li>
                <li>Pagamentos conciliados ao centavo entre app, Mercado Pago e bancos (jul–out/2026).</li>
                <li>Código próprio de porte: {n(loc)} linhas medidas no repositório.</li>
                <li>Rede em formação, metodologia de formação e marca com história.</li>
              </ul>
            </Cartao>
            <Cartao tom="escuro" titulo="O que ainda limita o valor">
              <ul className="list-disc space-y-1 pl-5">
                <li>Margem por venda não comprovada: o app ainda não grava o custo de cada venda.</li>
                <li>Série histórica curta: dinheiro real auditável desde 01/08/2026.</li>
                <li>Obrigações fixas (parceiros, consórcios, contas) maiores que a receita reconhecida.</li>
                <li>Perímetro, quadro societário e titularidade dos ativos a documentar.</li>
              </ul>
              <Link href="/app/riscos" className="mt-3 inline-flex items-center gap-1 text-sm text-pill underline underline-offset-2">Riscos e o que reduz cada um <ArrowRight className="h-3.5 w-3.5" aria-hidden /></Link>
            </Cartao>
          </Grade>
        </div>

        <div className="mt-14">
          <Titulo tag="Comparáveis candidatos" sub="Ponto de partida de pesquisa — nada aqui é número final">Com Quem a Leilão NoZap Será Comparada</Titulo>
          <Grade colunas={3} className="mt-8">
            <Cartao tom="escuro" titulo="Liquidity Services (EUA)">Marketplaces de leilão de excedente e devolução de consumo.</Cartao>
            <Cartao tom="escuro" titulo="Enjoei (Brasil)">Recommerce brasileiro de pequeno porte; sob pressão na bolsa.</Cartao>
            <Cartao tom="escuro" titulo="ThredUp · RealReal · eBay · Copart · RB Global">Recommerce e leilões — referência de múltiplo, com desconto de tamanho.</Cartao>
            <Cartao tom="escuro" titulo="Mercado Livre · Magazine Luiza">Grande porte: referência de teto, não comparação direta.</Cartao>
            <Cartao tom="escuro" titulo="Naver × Poshmark (2022)">Transação de recommerce ≈ 3,7× a receita — outro porte, outro mercado, outro momento.</Cartao>
            <Cartao tom="azul" titulo="Regra que não muda">Nunca afirmaremos que o sistema é “mais preciso que humanos” antes de dezenas de transações reais comparadas. Para uma transação, um laudo de terceiro continua sendo o padrão.</Cartao>
          </Grade>
        </div>

        {conselho && (
          <div className="mt-14">
            <Titulo tag="Só para o conselho">Números que Já Circulam — e Não São Valuation do Motor</Titulo>
            <div className="mt-6 overflow-x-auto rounded-lg border border-white/15">
              <table className="w-full min-w-[720px] text-left text-[15px] font-light text-white">
                <thead className="bg-white/5 text-xs uppercase tracking-wider text-muted">
                  <tr><th className="px-5 py-3">Número</th><th className="px-5 py-3">Onde</th><th className="px-5 py-3">Método</th><th className="px-5 py-3">Leitura</th></tr>
                </thead>
                <tbody>
                  {[
                    ["R$ 25.000.000", "sites e documento oficial do app", "nenhum visível", "referência do fundador"],
                    ["R$ 373.788 – R$ 747.576", "painel do Parceiro (código do app)", "3× a 6× o lucro anual “apurado” (R$ 124.596)", "ilustrativo; o próprio código diz “não é laudo”"],
                    ["R$ 7,97 mi – R$ 15,9 mi", "painel do Parceiro (código do app)", "mesmos múltiplos sobre lucro projetado com R$ 1 mi/mês", "cenário, não valor atual"],
                  ].map((l) => (
                    <tr key={l[0]} className="border-t border-white/10">{l.map((c, i) => <td key={i} className="px-5 py-3">{c}</td>)}</tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="mt-4">
              <NotaRevisao
                conselho
                itens={[
                  "Esta primeira rodada não pode ser cega: o R$ 25 mi já circulou. O modo cego (referência lacrada, aberta só depois) vale para as próximas rodadas e para qualquer terceiro.",
                  "A distância entre os três valores que circulam (R$ 25 mi × R$ 0,37–0,75 mi × R$ 8–16 mi) é o primeiro ponto que um investidor levanta — por isso a ponte, não a defesa do número.",
                  "Retirados do site de valuation nesta versão: a seção que compara o produto a plataformas de aposta, “ROI elevado por ciclo”, “30% de comissão para licenciados” (o código mostra percentuais por papel), Livoo e “50% de ativação / ~40 ativos”.",
                ]}
              />
            </div>
          </div>
        )}
      </Faixa>
    </div>
  );
}
