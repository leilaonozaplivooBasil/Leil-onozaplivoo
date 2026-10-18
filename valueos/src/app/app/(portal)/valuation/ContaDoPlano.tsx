import Link from "next/link";
import { Etiqueta, brl, inteiro } from "@/components/ui";
import { Cartao, Citacao, Faixa, Grade, Hoje, NumeroGrande, Titulo } from "@/components/marca";
import { CENARIOS, CUSTOS_VARIAVEIS, MESES_APP, POPULACAO, RETORNO, VEZES_EBITDA, calcula, conversaoMedida, gastoMes, valorPlano, type Medido } from "@/lib/plano";

const mi = (x: number) => `R$ ${(x / 1_000_000).toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })} mi`;
const pct = (x: number, casas = 1) => `${(100 * x).toLocaleString("pt-BR", { maximumFractionDigits: casas })}%`;
const milPessoas = (x: number) => `${(x / 1000).toLocaleString("pt-BR", { maximumFractionDigits: 1 })} mil`;

// A conta dos R$ 35 milhões: faturamento do plano (A Recreio + B digital), lucro, valor — e o que precisa ser verdade.
export function ContaDoPlano({ v, clientes2026, meses2026 }: { v: (id: string) => number | null; clientes2026: number; meses2026: number }) {
  const medido: Medido = { cadastros: v("USERS_REGISTERED") ?? 0, compradores: v("APP_BUYERS") ?? 0, compras: v("APP_PAID_PURCHASES") ?? 0 };
  const conv = conversaoMedida(medido);
  const gasto = gastoMes(medido);
  const [cons, base, alto] = CENARIOS.map((c) => calcula(c, medido));
  const b = CENARIOS[1];
  const valor = valorPlano(medido);
  const fixoHoje = v("FIXED_COST_BUDGET_M");
  const fechado = v("PIPELINE_CLOSED");
  const ponderada = v("PIPELINE_WEIGHTED");
  const carteira = v("WALLET_LIABILITY_TOTAL");
  const custoParceiro = base.giro * 0.0375 * 12;
  const naCarteira = base.receita * 0.06;

  const LINHAS: { rotulo: string; hoje: string; cel: (c: (typeof CENARIOS)[number], r: ReturnType<typeof calcula>) => string; forte?: boolean; destaque?: boolean }[] = [
    { rotulo: "Recreio: pessoas que compram no ano", hoje: "—", cel: (c, r) => `${milPessoas(r.clientesRecreio)} (${pct(c.recreioPct, 0)})` },
    { rotulo: "Valor de cada compra", hoje: `${brl(v("AUCTION_TICKET_AVG") ?? 0)} no arremate · R$ 321 na média`, cel: (c) => brl(c.ticket) },
    { rotulo: "Compras por cliente no ano", hoje: "2,7 em 4,5 meses", cel: (c) => inteiro(c.comprasAno) },
    { rotulo: "Cadastros no app", hoje: inteiro(medido.cadastros), cel: (c) => milPessoas(c.cadastros) },
    { rotulo: "Cadastros que compram", hoje: pct(conv), cel: (_c, r) => pct(r.conversao) },
    { rotulo: "Gasto do comprador por mês", hoje: brl(gasto), cel: () => brl(gasto) },
    { rotulo: "A · Faturamento no Recreio", hoje: "", cel: (_c, r) => mi(r.recreio) },
    { rotulo: "B · Faturamento digital", hoje: "", cel: (_c, r) => mi(r.digital) },
    { rotulo: "= Faturamento do ano", hoje: `${mi((clientes2026 / meses2026) * 12)} por ano (ritmo de 2026)`, cel: (_c, r) => mi(r.receita), forte: true },
    { rotulo: "Margem depois dos custos variáveis", hoje: "não medida", cel: (c) => pct(c.margem, 0) },
    { rotulo: "Custos fixos no ano", hoje: fixoHoje ? `${mi(fixoHoje * 12)} (orçamento)` : "—", cel: (_c, r) => mi(r.fixo) },
    { rotulo: "= Lucro operacional (EBITDA)", hoje: "negativo", cel: (_c, r) => (r.ebitda < 0 ? `− ${mi(-r.ebitda)}` : mi(r.ebitda)), forte: true },
    { rotulo: "Vezes o faturamento, daqui a 12 meses", hoje: "—", cel: (c) => `${c.multiplo}×` },
    { rotulo: `Valor hoje pelo faturamento (÷ ${RETORNO})`, hoje: "", cel: (_c, r) => mi(r.hoje), forte: true, destaque: true },
    { rotulo: `Valor hoje pelo lucro (${VEZES_EBITDA}× o EBITDA)`, hoje: "", cel: (_c, r) => (r.peloLucro === null ? "não se aplica" : mi(r.peloLucro)) },
  ];

  return (
    <Faixa id="plano">
      <Titulo tag="Valuation pelo plano · projeção" sub="A + B: o que a empresa vende em 12 meses, quanto sobra e quanto isso vale hoje">
        {`A Conta dos ${brl(valor)}`}
      </Titulo>
      <p className="mt-4 max-w-4xl font-light text-texto">
        Esta é a conta do plano, linha por linha. Cada número medido traz a prova; cada número de plano traz a etiqueta de projeção. Quem discordar de uma premissa troca a
        premissa — a conta fica aberta. O valuation independente, com nove métodos, continua na metodologia mais abaixo.
      </p>

      <div className="mt-10 grid gap-5 lg:grid-cols-3">
        <Cartao tom="lateral" titulo="A · Recreio" rodape={<Hoje href="/app/prova/AUCTION_TICKET_AVG">{`arremate pago custa em média ${brl(v("AUCTION_TICKET_AVG") ?? 0)}`}</Hoje>}>
          <p className="num font-display text-2xl font-light text-white">
            {inteiro(POPULACAO)} × {pct(b.recreioPct, 0)} × {brl(b.ticket)}
          </p>
          <p className="mt-2">
            {milPessoas(base.clientesRecreio)} pessoas da região comprando uma vez por ano, a {brl(b.ticket)} por compra, com o distribuidor, o galpão e três lojas até
            março de 2027.
          </p>
          <p className="num mt-3 font-display text-3xl text-accent">{mi(base.recreio)}</p>
          <span className="mt-2 block"><Etiqueta tipo="FORECAST" pequena /></span>
        </Cartao>
        <Cartao tom="lateral" titulo="B · Digital" rodape={<Hoje href="/app/prova/APP_BUYERS">{`${inteiro(medido.cadastros)} cadastros · ${inteiro(medido.compradores)} compradores · ${brl(gasto)} por mês cada`}</Hoje>}>
          <p className="num font-display text-2xl font-light text-white">
            {milPessoas(b.cadastros)} × {pct(base.conversao)} × {brl(gasto)} × 12
          </p>
          <p className="mt-2">
            {milPessoas(b.cadastros)} cadastros em 12 meses. A parte que compra e o quanto cada comprador gasta são os de hoje, medidos no app: {inteiro(Math.round(base.compradores))}{" "}
            compradores.
          </p>
          <p className="num mt-3 font-display text-3xl text-accent">{mi(base.digital)}</p>
          <span className="mt-2 block"><Etiqueta tipo="FORECAST" pequena /></span>
        </Cartao>
        <Cartao tom="cheio" titulo="= O ano 1 do plano">
          <p className="num font-display text-4xl font-semibold">{mi(base.receita)}</p>
          <p className="mt-1">de faturamento no ano</p>
          <p className="num mt-4 font-display text-2xl font-semibold">{mi(base.ebitda)}</p>
          <p className="mt-1">
            de lucro operacional (EBITDA): {pct(b.margem, 0)} de margem menos {mi(base.fixo)} de custos fixos
          </p>
          <p className="mt-4">
            {mi(base.receita)} × {b.multiplo} = {mi(base.futuro)} daqui a 12 meses. Dividido por {RETORNO}, porque quem investe agora quer dobrar o dinheiro em um ano:
          </p>
          <p className="num mt-2 font-display text-4xl font-semibold">{mi(base.hoje)} hoje</p>
        </Cartao>
      </div>

      <div className="mt-12 grid gap-10 sm:grid-cols-2">
        <NumeroGrande cor="verde" valor={mi(base.hoje)} rotulo="Pelo faturamento" sub={`${b.multiplo} vezes o faturamento do ano 1, dividido por ${RETORNO} (método do investidor de risco)`} etiqueta="FORECAST" />
        <NumeroGrande cor="verde" valor={base.peloLucro === null ? "—" : mi(base.peloLucro)} rotulo="Pelo lucro" sub={`${VEZES_EBITDA} vezes o lucro operacional (EBITDA) do ano 1`} etiqueta="FORECAST" />
      </div>
      <p className="mt-4 text-center text-sm font-light text-muted">Dois caminhos diferentes chegam no mesmo lugar: entre {mi(Math.min(base.hoje, base.peloLucro ?? base.hoje))} e {mi(Math.max(base.hoje, base.peloLucro ?? base.hoje))}.</p>

      <div className="mt-12">
        <Titulo tag="Três cenários" sub="A mesma conta com premissas mais duras e mais otimistas">Do Conservador ao Alto</Titulo>
        <div className="mt-8 overflow-x-auto rounded-lg border border-white/15">
          <table className="w-full min-w-[820px] text-left text-[15px]">
            <thead className="bg-accent text-accent-ink">
              <tr>
                <th className="px-5 py-3 font-semibold">Linha</th>
                <th className="px-5 py-3 font-semibold">Hoje, medido</th>
                {CENARIOS.map((c) => (
                  <th key={c.nome} className="px-5 py-3 text-right font-semibold">{c.nome}</th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-black/40 text-white">
              {LINHAS.map((l) => (
                <tr key={l.rotulo} className={`border-t border-white/10 ${l.destaque ? "bg-accent/20 font-semibold" : l.forte ? "bg-accent/10 font-medium" : "font-light"}`}>
                  <td className="px-5 py-3">{l.rotulo}</td>
                  <td className="px-5 py-3 text-texto">{l.hoje}</td>
                  {CENARIOS.map((c, i) => (
                    <td key={c.nome} className="num whitespace-nowrap px-5 py-3 text-right">{l.cel(c, [cons, base, alto][i])}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-sm font-light text-muted">
          <Etiqueta tipo="VERIFIED" pequena /> “Hoje, medido” vem do app e dos extratos (vendas no app desde jun/2026, {MESES_APP.toLocaleString("pt-BR")} meses).{" "}
          <Etiqueta tipo="FORECAST" pequena /> As três colunas são plano.
        </p>
      </div>

      <Grade colunas={2} className="mt-12">
        <Cartao tom="escuro" titulo="De onde vem a margem de 35%">
          <p>De cada R$ 100 vendidos no cenário base, saem:</p>
          <ul className="mt-3 space-y-2">
            {CUSTOS_VARIAVEIS.map(([item, valor, porque]) => (
              <li key={item} className="flex gap-3">
                <span className="num w-12 shrink-0 text-right font-semibold text-pill">R$ {valor}</span>
                <span><strong className="font-medium text-white">{item}</strong> — {porque}</span>
              </li>
            ))}
          </ul>
          <p className="mt-3">Sobram R$ {100 - CUSTOS_VARIAVEIS.reduce((s, [, x]) => s + x, 0)} para pagar a estrutura e dar lucro. <Etiqueta tipo="AI_ASSUMPTION" pequena /></p>
        </Cartao>
        <Cartao tom="escuro" titulo="“Com 10 mil clientes, R$ 1 milhão por mês”">
          <p>
            A frase do fundador vale quando <strong className="font-medium text-white">cliente é quem compra</strong>: medido, cada comprador gasta {brl(gasto)} por mês no app — 10
            mil compradores dariam {mi(10_000 * gasto)} por mês.
          </p>
          <p className="mt-3">
            Se cliente for <strong className="font-medium text-white">cadastro</strong>, a conta muda: hoje {pct(conv)} dos cadastros compram, e 10 mil cadastros dariam cerca de{" "}
            R$ {Math.round((10_000 * conv * gasto) / 1000)} mil por mês. Por isso o plano conta cadastros e compradores separados.
          </p>
          <p className="mt-3">
            Nos últimos 30 dias entraram 380 cadastros: o app foi de {inteiro(medido.cadastros - 380)} para {inteiro(medido.cadastros)}.
          </p>
        </Cartao>
      </Grade>

      <div className="mt-12">
        <Titulo tag="O combustível e o motor" sub="Quem paga a mercadoria e quem faz o plano acontecer">Esteira, Carteira e Time</Titulo>
        <Grade colunas={3} className="mt-8">
          <Cartao
            tom="lateral"
            titulo="Esteira de parceiros de compra"
            rodape={<Hoje href="/app/prova/PIPELINE_CLOSED">{`${fechado === null ? "—" : brl(fechado)} fechados · R$ 400 mil nos extratos de setembro`}</Hoje>}
          >
            <p className="num font-display text-3xl font-light text-white">{mi(v("PIPELINE_OPEN") ?? 0)}</p>
            <p>em negociação, em 25 conversas — {ponderada === null ? "—" : mi(ponderada)} pela chance de cada etapa <Etiqueta tipo="FORECAST" pequena /></p>
            <p className="mt-3">
              O plano base precisa de cerca de {mi(base.giro)} em mercadoria girando: 30% da venda, três giros por ano. É {ponderada ? pct(base.giro / ponderada, 0) : "—"} da esteira
              ponderada.
            </p>
            <p className="mt-3 text-sm text-muted">
              O capital de parceiro custa de 3% a 4,5% ao mês: cerca de {mi(custoParceiro)} por ano no plano base. É custo financeiro, abaixo do EBITDA.
            </p>
          </Cartao>
          <Cartao tom="lateral" titulo="Carteira: a captação mais barata" rodape={<Hoje href="/app/prova/WALLET_LIABILITY_TOTAL">{`${carteira === null ? "—" : brl(carteira)} em saldos de clientes e rede`}</Hoje>}>
            <p>
              Quem dá lance deposita antes. Parte do dinheiro fica na carteira até virar compra — hoje, {v("WALLET_UNSPENT_SHARE")?.toLocaleString("pt-BR") ?? "—"}% do que foi
              depositado ainda não foi gasto.
            </p>
            <p className="mt-3">
              Se 6% do faturamento ficar parado na carteira, como diz o fundador, são cerca de {mi(naCarteira)} no plano base — dinheiro que não paga 3% ao mês a ninguém{" "}
              <Etiqueta tipo="MANAGEMENT_DATA" pequena />.
            </p>
            <p className="mt-3 text-sm text-muted">É dinheiro do cliente: obrigação, não lucro. Por isso não entra no valor.</p>
          </Cartao>
          <Cartao tom="lateral" titulo="O time que executa" rodape={<Hoje href="/app/prova/TEAM_DELIVERIES_PROVEN">{`${inteiro(v("TEAM_DELIVERIES_PROVEN") ?? 0)} entregas com prova desde 03/09`}</Hoje>}>
            <p>
              O time trabalha pelo Método Top College: oito hábitos, metas diárias com prova, ranking e avaliação entre colegas no X-GAME. O hábito 06 — Acompanhamento e
              Fechamento — é onde ficam a esteira e o CRM.
            </p>
            <ul className="mt-3 space-y-1">
              <li>{inteiro(v("TEAM_XGAME_ACTIVE") ?? 0)} pessoas ativas no X-GAME</li>
              <li>{inteiro(v("CRM_CONTACTS") ?? 0)} contatos no CRM do time</li>
              <li>{inteiro(v("LICENSEES_TOTAL") ?? 0)} licenciados e uma rede de vendedores e influenciadores</li>
            </ul>
          </Cartao>
        </Grade>
      </div>

      <div className="mt-12">
        <Titulo tag="O que precisa ser verdade" sub="Cada premissa do cenário base ao lado de onde ela está hoje">O Que o Plano Ainda Precisa Provar</Titulo>
        <div className="mt-8 overflow-x-auto rounded-lg border border-white/15">
          <table className="w-full min-w-[720px] text-left text-[15px]">
            <thead className="bg-white/5 text-xs uppercase tracking-wider text-muted">
              <tr><th className="px-5 py-3">Premissa</th><th className="px-5 py-3">Onde está hoje</th><th className="px-5 py-3">Etiqueta</th></tr>
            </thead>
            <tbody className="font-light text-white">
              {[
                [`${milPessoas(base.clientesRecreio)} pessoas do Recreio comprando no ano, com três lojas e o distribuidor até mar/2027`, `${inteiro(v("CUSTOMER_BASE_UNIQUE") ?? 0)} pessoas na base hoje; distribuidor informado pelo fundador; nenhuma loja licenciada ainda`, "MANAGEMENT_DATA", "/app/prova/CUSTOMER_BASE_UNIQUE"],
                [`${milPessoas(b.cadastros)} cadastros em 12 meses`, `${inteiro(medido.cadastros)} hoje, 380 nos últimos 30 dias: o salto depende da parceria de tráfego em negociação e do tráfego pago do plano`, "FORECAST", "/app/prova/USERS_REGISTERED"],
                [`${pct(conv)} dos cadastros comprando e gastando ${brl(gasto)} por mês`, `medido com ${inteiro(medido.compradores)} compradores; precisa se manter com um público muito maior`, "VERIFIED", "/app/prova/APP_BUYERS"],
                ["Margem de 35% depois dos custos variáveis", "o app ainda não grava o custo de cada venda; o lote custa cerca de 19% do valor de mercado", "NAO_DISPONIVEL", "/app/prova/LOTS_BOUGHT_MARKET_VALUE"],
                [`${mi(base.giro)} de capital de giro em mercadoria`, `${fechado === null ? "—" : brl(fechado)} fechados; ${ponderada === null ? "—" : mi(ponderada)} ponderados na esteira`, "MANAGEMENT_DATA", "/app/prova/PIPELINE_WEIGHTED"],
              ].map(([premissa, hoje, et, href]) => (
                <tr key={premissa} className="border-t border-white/10 align-top">
                  <td className="px-5 py-3">{premissa}</td>
                  <td className="px-5 py-3 text-texto">
                    {hoje}{" "}
                    <Link href={href} className="text-xs text-pill underline underline-offset-2">ver prova</Link>
                  </td>
                  <td className="px-5 py-3"><Etiqueta tipo={et} pequena /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Grade colunas={2} className="mt-12">
        <Cartao tom="escuro" titulo="O que não entra na conta (e pode subir o valor)">
          <ul className="list-disc space-y-1 pl-5">
            <li>A parceria de tráfego em negociação, que pode trazer os 100 mil cadastros antes de dezembro — o plano dá 12 meses.</li>
            <li>A esteira acima do capital de giro: {ponderada === null ? "—" : mi(ponderada)} ponderados contra {mi(base.giro)} necessários.</li>
            <li>Adesões da escada de licenças: loja física (R$ 350 mil) e distribuidor (R$ 4 milhões).</li>
            <li>O dinheiro parado na carteira e o ecossistema (Top College, X-EOS e ComparAI).</li>
          </ul>
        </Cartao>
        <Cartao tom="escuro" titulo="O que pode derrubar o valor">
          <ul className="list-disc space-y-1 pl-5">
            <li>Os cadastros não chegarem a 100 mil: com 30 mil, a conta vai para o cenário conservador ({mi(cons.hoje)}).</li>
            <li>A margem real, quando medida venda a venda, ficar abaixo de 35%.</li>
            <li>O capital de parceiro, caro, crescer mais rápido que a venda.</li>
            <li>A parceria de tráfego e o uso da carteira dependem de parecer jurídico antes de rodar.</li>
          </ul>
          <Link href="/app/riscos" className="mt-3 inline-flex items-center gap-1 text-sm text-pill underline underline-offset-2">Riscos e o que reduz cada um</Link>
        </Cartao>
      </Grade>

      <Citacao className="mt-12 !font-light">
        {`${brl(valor)} é o valor de hoje para quem acredita no plano de 12 meses e cobra o retorno de quem corre risco. A cada mês o portal mede de novo — e o número sobe ou desce com o que acontecer de verdade.`}
      </Citacao>
    </Faixa>
  );
}
