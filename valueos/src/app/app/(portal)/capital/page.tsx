import Link from "next/link";
import type { ReactNode } from "react";
import { ArrowRight } from "lucide-react";
import { valoresCarregados } from "@/lib/metricas";
import { papelAtual, eConselho } from "@/lib/papel";
import { Etiqueta, brl, inteiro } from "@/components/ui";
import { Capitulo, Cartao, Citacao, Conteiner, Faixa, GraficoBarras, Grade, LinhaDoTempo, Nota, NumeroGrande, Texto, Titulo } from "@/components/marca";

export const dynamic = "force-dynamic";

const MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
const rotuloMes = (iso: string) => `${MESES[Number(iso.slice(5, 7)) - 1]}/${iso.slice(2, 4)}`;

// Tabela no padrão do painel vivo: cabeçalho verde, linhas sobre fundo escuro, total destacado.
function Quadro({ cabecalho, linhas, total, minimo = 720 }: { cabecalho: string[]; linhas: ReactNode[][]; total?: ReactNode[]; minimo?: number }) {
  return (
    <div className="mt-8 overflow-x-auto rounded-lg border border-white/15">
      <table className="w-full text-left text-[15px]" style={{ minWidth: minimo }}>
        <thead className="bg-accent text-accent-ink">
          <tr>
            {cabecalho.map((c) => (
              <th key={c} className="px-5 py-3 font-semibold">{c}</th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-black/40 font-light text-white">
          {linhas.map((l, i) => (
            <tr key={i} className="border-t border-white/10 align-top">
              {l.map((c, j) => (
                <td key={j} className="px-5 py-3">{c}</td>
              ))}
            </tr>
          ))}
          {total && (
            <tr className="border-t border-white/20 bg-accent/10 font-medium">
              {total.map((c, j) => (
                <td key={j} className="px-5 py-3">{c}</td>
              ))}
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

const Valor = ({ children }: { children: ReactNode }) => <span className="num whitespace-nowrap">{children}</span>;
const Obs = ({ children }: { children: ReactNode }) => <span className="mt-1 block text-xs text-muted">{children}</span>;

// O livro do capital: de onde veio o dinheiro, o que ele construiu, quanto custa e o que ainda falta provar.
export default async function Capital() {
  const [{ ultimo, serie }, papel] = await Promise.all([valoresCarregados(), papelAtual()]);
  const conselho = eConselho(papel);
  const v = (id: string) => ultimo.get(id)?.valor ?? null;
  const r = (x: number | null) => (x === null ? "—" : brl(x));

  const fundadores = v("CAPITAL_FOUNDERS_DECLARED");
  const mesDe = (id: string, iso: string) => serie.get(id)?.find((x) => x.periodo === iso) ?? null;
  const declarado = (serie.get("REVENUE_TAX_DECLARED_M") ?? []).filter((x) => x.periodo >= "2026-01-01").reduce((s, x) => s + (x.valor ?? 0), 0);
  const bancoJanMai = (serie.get("BANK_SMALL_PIX_IN") ?? []).filter((x) => x.periodo <= "2026-05-01").reduce((s, x) => s + (x.valor ?? 0), 0);
  const balancete2025 = v("ACCOUNTING_REVENUE_Y");
  const compra1pct = v("EQUITY_SUBSCRIPTION");
  const terceiros = v("THIRD_PARTY_CAPITAL");
  const custoCapital = v("CAPITAL_COST_M");
  const naoGasto = v("WALLET_UNSPENT_SHARE");
  const orcamento = v("FIXED_COST_BUDGET_M");
  const cadastrado = v("FIXED_COST_REGISTERED_M");
  const pagoSet = serie.get("EXPENSES_PAID")?.find((x) => x.periodo === "2026-09-01")?.valor ?? null;
  const vencidas = v("EXPENSES_OVERDUE");
  const galpaoTotal = v("WAREHOUSE_TOTAL_PAID");
  const mediaMes = terceiros && custoCapital ? (100 * custoCapital) / terceiros : 0;
  const aoAno = (Math.pow(1 + mediaMes / 100, 12) - 1) * 100;
  const receitaPropriaSet =
    (serie.get("REVENUE_COMMISSION_RETAINED")?.find((x) => x.periodo === "2026-09-01")?.valor ?? 0) +
    (serie.get("REVENUE_FEES")?.find((x) => x.periodo === "2026-09-01")?.valor ?? 0);

  // Vendas registradas antes do app (registro da gestão).
  const antes = (serie.get("SALES_HISTORY_MGMT") ?? []).map((x) => ({ periodo: x.periodo, valor: x.valor, tom: "gestao" as const }));
  const ateMaio = antes.filter((x) => x.periodo <= "2026-05-01").reduce((s, x) => s + (x.valor ?? 0), 0);

  // O caixa de 2026, conciliado nos extratos: o que entrou, o que saiu e para onde foi.
  const somaSerie = (id: string) => (serie.get(id) ?? []).reduce((s, x) => s + (x.valor ?? 0), 0);
  const deClientes = somaSerie("CASH_IN_CUSTOMERS_M");
  const deCapital = somaSerie("CASH_IN_CAPITAL_M");
  const saidas = somaSerie("CASH_OUT_M");
  const semNome = somaSerie("CASH_OUT_UNNAMED_M");
  const mesesCaixa = (serie.get("CASH_OUT_M") ?? []).map((x) => x.periodo).sort();
  const parteVenda = saidas ? Math.round((100 * deClientes) / saidas) : 0;
  const recebido = (fundadores ?? 0) + deCapital;
  const TRES = ["2026-08-01", "2026-09-01", "2026-10-01"];
  const doMes = (id: string, iso: string) => mesDe(id, iso)?.valor ?? 0;
  const nosTres = (id: string) => TRES.reduce((s, p) => s + doMes(id, p), 0);
  const saidasTres = nosTres("CASH_OUT_M");
  const gastos = [
    { id: "CASH_OUT_CARDS_M", tipo: "Cartões usados pela empresa", oque: "faturas dos cartões de uma executiva e de um investidor" },
    { id: "CASH_OUT_TEAM_M", tipo: "Time, vendas e comissões", oque: "pessoas da equipe, vendedores e comissão por venda" },
    { id: "CASH_OUT_ADMIN_M", tipo: "Administração e sócios", oque: "repasses à administradora da operação e retiradas" },
    { id: "CASH_OUT_RENT_M", tipo: "Galpão, escritório e aluguéis", oque: "galpão (R$ 23.036 por mês), outros aluguéis e o hotel do escritório" },
    { id: "CASH_OUT_CAPITAL_M", tipo: "Rendimentos, consórcio e capitalização", oque: "o custo do capital de terceiros" },
    { id: "CASH_OUT_STOCK_M", tipo: "Estoque, compras e frete", oque: "lotes e mercadoria para o leilão e a loja" },
    { id: "CASH_OUT_TECH_M", tipo: "Plataformas e tecnologia", oque: "assinaturas, meios de pagamento e marketing pagos pela conta" },
    { id: "CASH_OUT_OPS_M", tipo: "Operação e outras despesas", oque: "alimentação, transporte, contas, bancos e fornecedores menores" },
  ].sort((a, b) => nosTres(b.id) - nosTres(a.id));
  const cartoesMes = nosTres("CASH_OUT_CARDS_M") / 3;
  // Jan a jul o banco não identifica quem recebeu: a divisão usa o que o fundador informa, e o resto fica junto.
  const estimativas = [
    { id: "CASH_JJ_TECH_EST", tipo: "Tecnologia e plataformas" },
    { id: "CASH_JJ_CONSUMPTION_EST", tipo: "Consumo do dia a dia" },
    { id: "CASH_JJ_OFFICE_EST", tipo: "Escritório" },
  ];
  const restoJJ = semNome - estimativas.reduce((s, e) => s + (v(e.id) ?? 0), 0);

  // O lado social: o Conexão, medido no app do Vale do Recreio.
  const encontros = v("SOCIAL_MEETINGS");
  const pessoas = v("SOCIAL_PEOPLE");
  const confirmacoes = v("SOCIAL_CONFIRMATIONS");
  const chegadas = v("SOCIAL_CHECKINS");
  const doacoes = v("SOCIAL_DONATIONS");
  const n = (x: number | null) => (x === null ? "—" : inteiro(x));

  // Dinheiro de clientes mês a mês: dez/2025 pelo registro da operação; 2026 pelos extratos, que são a prova mais forte.
  const clientes = [
    ...antes.filter((x) => x.periodo < "2026-01-01"),
    ...(serie.get("CASH_IN_CUSTOMERS_M") ?? []).map((x) => ({ periodo: x.periodo, valor: x.valor, tom: "verificado" as const })),
  ].sort((a, b) => a.periodo.localeCompare(b.periodo));
  const totalClientes = clientes.reduce((s, x) => s + (x.valor ?? 0), 0);
  const registrado = (iso: string) => (iso < "2026-08-01" ? mesDe("SALES_HISTORY_MGMT", iso) : mesDe("GMV_GOODS", iso));
  const totalRegistrado = clientes.reduce((s, x) => s + (registrado(x.periodo)?.valor ?? 0), 0);
  const melhor = clientes.reduce((m, x) => ((x.valor ?? 0) > (m?.valor ?? 0) ? x : m), clientes[0]);
  const clientesJanMai = clientes.filter((x) => x.periodo >= "2026-01-01" && x.periodo <= "2026-05-01").reduce((s, x) => s + (x.valor ?? 0), 0);
  const movimentado = v("CASH_MOVED_2026");
  const outrasEntradas = movimentado !== null ? movimentado - saidas - deClientes - deCapital : null;

  return (
    <div>
      {/* CAPA */}
      <Capitulo
        numero="Livro do capital · atualizado em 18/10/2026"
        titulo="A História do Dinheiro"
        sub="De onde veio cada real, o que ele construiu e quanto custa manter a empresa de pé."
        imagem="/m/bilhoes-parados.jpg"
      >
        <p>
          Este retrato junta os documentos dos fundadores, as planilhas de venda da operação, os extratos do Itaú, do Santander e do Mercado Pago, o
          financeiro e a carteira do aplicativo. Cada número diz de
          onde veio. O que já tem prova aparece como <strong>verificado</strong>; o que ainda depende de comprovante aparece como <strong>dado da administração</strong>.
        </p>
      </Capitulo>

      {/* OS QUATRO NÚMEROS */}
      <Faixa>
        <Titulo tag="Em uma linha">Quatro Números Que Resumem a História</Titulo>
        <div className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <NumeroGrande compacto valor={r(fundadores)} rotulo="investidos pelos fundadores" sub="declarado até dez/2025" etiqueta="MANAGEMENT_DATA" href="/app/prova/CAPITAL_FOUNDERS_DECLARED" />
          <NumeroGrande compacto valor={r(declarado || null)} rotulo="de receita declarada ao Simples" sub="jan a mai/2026 · 2025 zerado" etiqueta="MANAGEMENT_DATA" href="/app/prova/REVENUE_TAX_DECLARED_M" />
          <NumeroGrande compacto valor={r(terceiros)} rotulo="de capital de terceiros" sub={`custa ${r(custoCapital)} por mês`} etiqueta="MANAGEMENT_DATA" href="/app/prova/THIRD_PARTY_CAPITAL" />
          <NumeroGrande compacto valor={naoGasto === null ? "—" : `${inteiro(Math.round(naoGasto))}%`} rotulo="do depósito do cliente fica na plataforma" sub="ainda não virou compra" etiqueta="VERIFIED" href="/app/prova/WALLET_UNSPENT_SHARE" cor="verde" />
        </div>
      </Faixa>

      {/* TRÊS FASES */}
      <section className="border-y border-white/10 bg-surface py-16 sm:py-24">
        <Conteiner>
          <Titulo tag="Linha do tempo do dinheiro" sub="Uma mesma empresa (Compras Full Comércio Ltda), três canais de venda">Do WhatsApp ao Aplicativo</Titulo>
          <Grade colunas={3} className="mt-10">
            <Cartao tom="cinza" titulo="1 · O MVP no WhatsApp">
              Venda direta pelo WhatsApp, Facebook e OLX e depois pelo site leilaowhatsapp.com, com pagamento por Pix — ainda sem pagamento integrado. O fundador
              informa <strong>cerca de 8 mil produtos vendidos e cerca de 10 mil clientes impactados</strong> desde o início <Etiqueta tipo="MANAGEMENT_DATA" pequena />. O
              site está fora do ar; o case documentado é o de cerca de 600 produtos vendidos da casa do fundador — e a conta que sustenta os dois números está na seção de lotes.
            </Cartao>
            <Cartao tom="cinza" titulo="2 · Catálogo, showroom e NEXUS">
              De dez/2025 a jul/2026: catálogo leilaonozap.com, showroom no Recreio, time de vendedores e o NEXUS registrando cada comprovante. É a fase com
              série mensal, de {r(clientes[0]?.valor ?? null)} no primeiro mês até {r(melhor?.valor ?? null)} de clientes no banco em {melhor ? rotuloMes(melhor.periodo) : "—"}, e
              com lotes do Mercado Livre: {n(v("LOTS_BOUGHT"))} lotes e {n(v("LOTS_BOUGHT_PIECES"))} peças.
            </Cartao>
            <Cartao tom="lateral" titulo="3 · O aplicativo e o leilão">
              Desde jul/2026, leilaonozap.net com carteira, loja e leilão. A venda pelo WhatsApp foi reduzida de propósito para levar a base para o app — por isso a
              curva cai em julho e volta a subir com o leilão. O canal novo tem três meses.
            </Cartao>
          </Grade>
          <LinhaDoTempo
            itens={[
              { quando: "2024–2025", texto: "O MVP: venda pelo WhatsApp, Facebook e OLX e o site leilaowhatsapp.com, com pagamento por Pix. Cerca de 3 lotes comprados no começo (~1.200 peças), segundo o fundador.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Nov/2025", texto: "A empresa recomeça no Vale do Recreio. Primeira compra às cegas: 551 produtos, cerca de R$ 34 mil, com o último recurso do fundador.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Dez/2025", texto: "Primeiro mês de vendas registradas: R$ 26.358. O documento dos fundadores soma R$ 1.231.000 investidos.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Jan/2026", texto: "Catálogo leilaonozap.com no ar e primeiro aporte externo, de R$ 5 mil (29/01).", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Mar/2026", texto: "Escritório no Hotel Atlântico Sul, no Recreio: R$ 10 mil por mês desde então.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Abr/2026", texto: "Dois lotes do Mercado Livre: 4.549 peças, R$ 351 mil a valor de mercado. O NEXUS passa a registrar cada venda. Melhor mês de dinheiro de clientes no banco: R$ 91.963.", etiqueta: "VERIFIED" },
              { quando: "Mai/2026", texto: "Mais dois lotes: 2.592 peças, R$ 280 mil a valor de mercado. O estoque chega perto de R$ 1 milhão a preço de venda, segundo o fundador.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Jun/2026", texto: "Pico da venda pelo WhatsApp: R$ 74.438 no mês, pela planilha diária.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Jul/2026", texto: "O aplicativo ganha carteira e loja (as vendas pelo app começaram em junho). Primeiro depósito de cliente em 18/07 e primeiros leilões encerrados. Entrada do galpão: R$ 20 mil, em 23 e 27/07.", etiqueta: "VERIFIED" },
              { quando: "Ago/2026", texto: "Parceiro de compra B entra com R$ 50 mil, a 3% ao mês. O analisador de lotes passa a avaliar lotes do Mercado Livre: 33 lotes e 82 mil peças até outubro.", etiqueta: "VERIFIED" },
              { quando: "Set/2026", texto: "Parceiro A entra com R$ 200 mil, a 4,5% ao mês. Um diretor compra 1% por R$ 250 mil — R$ 200 mil já entraram no Itaú.", etiqueta: "VERIFIED", novo: true },
              { quando: "Out/2026", texto: `${inteiro(v("USERS_REGISTERED") ?? 0)} contas no app e ${r(v("GMV_AUCTION"))} em arremates até o dia 16.`, etiqueta: "VERIFIED", novo: true },
            ]}
          />
        </Conteiner>
      </section>

      {/* VENDAS DESDE O PRIMEIRO DIA */}
      <Faixa>
        <Titulo tag="Quanto os clientes já pagaram" sub="Dinheiro de clientes que entrou nas contas da empresa, mês a mês">{`${r(totalClientes)} Pagos por Clientes desde Dez/2025`}</Titulo>
        <GraficoBarras
          titulo="Cinza: registro da operação (dez/2025) · Verde: dinheiro de clientes nos extratos do Itaú, Santander e Mercado Pago (2026)"
          formato={(x) => (x >= 1000 ? `${inteiro(Math.round(x / 1000))} mil` : inteiro(Math.round(x)))}
          dados={clientes.map((x) => ({ rotulo: rotuloMes(x.periodo), valor: x.valor, tom: x.tom }))}
        />
        <Quadro
          cabecalho={["Mês", "Dinheiro de clientes nas contas", "Vendas registradas", "Declarado ao Simples", "De onde vem"]}
          minimo={860}
          linhas={clientes.map((x) => {
            const banco = x.periodo >= "2026-01-01" ? mesDe("CASH_IN_CUSTOMERS_M", x.periodo) : null;
            const reg = registrado(x.periodo);
            const simples = mesDe("REVENUE_TAX_DECLARED_M", x.periodo);
            return [
              x.periodo === "2026-10-01" ? `${rotuloMes(x.periodo)} (até 16)` : rotuloMes(x.periodo),
              <span key="v"><Valor>{r(x.valor)}</Valor><span className="ml-2 inline-block align-middle"><Etiqueta tipo={banco ? "VERIFIED" : "MANAGEMENT_DATA"} pequena /></span></span>,
              <span key="r"><Valor>{reg ? r(reg.valor) : "—"}</Valor>{reg?.fonte && <Obs>{reg.fonte}</Obs>}</span>,
              <Valor key="s">{simples ? r(simples.valor) : "—"}</Valor>,
              <span key="f">{banco ? banco.nota ?? "extratos" : "registro da operação (NEXUS)"}</span>,
            ];
          })}
          total={["Total", <Valor key="t">{r(totalClientes)}</Valor>, <Valor key="g">{r(totalRegistrado)}</Valor>, <Valor key="s">{r(declarado || null)}</Valor>, "dez/2025 a 16/out/2026"]}
        />
        <Grade colunas={2} className="mt-10">
          <Cartao tom="lateral" titulo="Três fontes que ainda não conversam">
            O extrato do banco confirma a venda do WhatsApp: são centenas de Pix pequenos por mês ({r(clientesJanMai)} de clientes de jan a mai/2026). A
            declaração do Simples informa {r(declarado || null)} no mesmo período e 2025 zerado; o balancete de 2025 do contador registra {r(balancete2025)} de
            receita naquele ano. Fechar essas três contas com o contador é o primeiro passo da due diligence.
          </Cartao>
          <Cartao tom="lateral" titulo="Por que julho cai">
            Em julho a empresa deixou de vender pelo WhatsApp para levar a base para o aplicativo e o leilão. Agosto é o mês mais baixo ({r(mesDe("CASH_IN_CUSTOMERS_M", "2026-08-01")?.valor ?? null)}
            de clientes); setembro e outubro voltam a subir com o leilão. A base do WhatsApp tem {n(v("WHATSAPP_BASE"))} contatos, e a maior parte ainda não entrou no app.
          </Cartao>
        </Grade>
      </Faixa>

      {/* LOTES E ESTOQUE */}
      <section className="border-y border-white/10 bg-surface py-16 sm:py-24">
        <Conteiner>
          <Titulo tag="Lotes e estoque" sub="Lotes de devolução e excedente do Mercado Livre, comprados e analisados — pelo registro do aplicativo">
            {`${r(v("LOTS_BOUGHT_MARKET_VALUE"))} em Lotes Comprados`}
          </Titulo>
          <div className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            <NumeroGrande compacto valor={n(v("LOTS_BOUGHT_PIECES"))} rotulo="peças compradas em lotes" sub={`${n(v("LOTS_BOUGHT"))} lotes, abr a jul/2026`} etiqueta="VERIFIED" href="/app/prova/LOTS_BOUGHT" />
            <NumeroGrande compacto valor={r(v("INVENTORY_PEAK_DECLARED"))} rotulo="pico do estoque" sub="a preço de venda, em maio" etiqueta="MANAGEMENT_DATA" href="/app/prova/INVENTORY_PEAK_DECLARED" />
            <NumeroGrande compacto valor={r(v("LOTS_ANALYZED_MARKET_VALUE"))} rotulo="em lotes analisados" sub={`${n(v("LOTS_ANALYZED"))} lotes e ${n(v("LOTS_ANALYZED_PIECES"))} peças, ago a out/2026`} etiqueta="VERIFIED" href="/app/prova/LOTS_ANALYZED_MARKET_VALUE" cor="verde" />
            <NumeroGrande compacto valor={r(v("INVENTORY_AT_COST"))} rotulo="em estoque hoje, a custo" sub="o que sobrou depois das vendas" etiqueta="VERIFIED" href="/app/prova/INVENTORY_AT_COST" />
          </div>
          <Grade colunas={3} className="mt-10">
            <Cartao tom="lateral" titulo="Como a empresa compra">
              Lote de devolução e excedente do Mercado Livre, comprado por uma fração do valor de mercado: nos lotes já comprados, o valor registrado é cerca de{" "}
              {v("LOTS_BOUGHT_MARKET_VALUE") ? `${Math.round((100 * 123484.19) / (v("LOTS_BOUGHT_MARKET_VALUE") ?? 1))}%` : "—"} do valor de mercado das peças. Cada lote vira
              produto cadastrado no app — {n(3305)} produtos saíram dos lotes de abril a julho.
            </Cartao>
            <Cartao tom="cheio" titulo="Como os números da administração se sustentam">
              <strong>Clientes:</strong> {n(v("WHATSAPP_BASE"))} contatos medidos no WhatsApp da empresa; se cada um alcança ao menos mais duas pessoas, são cerca de{" "}
              {n((v("WHATSAPP_BASE") ?? 0) * 3)} pessoas — o fundador fala em 10 mil. Somando CRM e app, sem repetir, a base medida é de {n(v("CUSTOMER_BASE_UNIQUE"))} pessoas.{" "}
              <strong>Produtos:</strong> {n(v("LOTS_BOUGHT_PIECES"))} peças em lotes com registro no app + cerca de {n(v("LOTS_BEFORE_APP_PIECES"))} em 3 lotes comprados antes
              do app = ~{n((v("LOTS_BOUGHT_PIECES") ?? 0) + (v("LOTS_BEFORE_APP_PIECES") ?? 0))} peças. Hoje há {n(v("INVENTORY_PIECES"))} peças em estoque; o fundador
              informa cerca de {n(v("PRODUCTS_SOLD_DECLARED"))} produtos vendidos desde o início.
            </Cartao>
            <Cartao tom="lateral" titulo="O analisador de lotes">
              Desde agosto, o app lê o manifesto de cada lote do Mercado Livre, classifica e precifica as peças. Já passaram por ele {n(v("LOTS_ANALYZED"))} lotes de 14
              centros de distribuição em SP, MG e RJ — {n(v("LOTS_ANALYZED_PIECES"))} peças avaliadas. Analisar não é comprar: é o funil de onde saem as próximas compras.
            </Cartao>
          </Grade>
        </Conteiner>
      </section>

      {/* DE ONDE VEIO O DINHEIRO */}
      <section className="border-y border-white/10 bg-surface py-16 sm:py-24">
        <Conteiner>
          <Titulo tag="De onde veio o dinheiro" sub="O que os fundadores declararam até dez/2025, separado entre dinheiro e contribuição não financeira">
            O Investimento dos Fundadores
          </Titulo>
          <Quadro
            cabecalho={["Fundador", "O que colocou", "Dinheiro e serviços pagos", "Não financeiro"]}
            linhas={[
              ["Luiz (fundador e CEO)", "Marketing 40 mil · tecnologia 50 mil · primeira compra 30 mil · marca e logo 9 mil · plano de negócio 20 mil · estrutura no Recreio 60 mil · regularização do CNPJ 72 mil", <Valor key="a">R$ 281.000</Valor>, <span key="b"><Valor>R$ 432.000</Valor><Obs>capital intelectual: 1,5 ano × 80 h/mês × R$ 300/h</Obs></span>],
              ["Luciano (captação)", "Investimento direto · escritório Le Monde (6 salas)", <Valor key="a">R$ 121.000</Valor>, <span key="b"><Valor>R$ 360.000</Valor><Obs>ativo físico agregado ao grupo</Obs></span>],
              ["Flávio (jurídico)", "Aporte em dinheiro e entregáveis", <Valor key="a">R$ 30.000</Valor>, <Valor key="b">—</Valor>],
              ["Geovane (administrativo)", "Aporte em dinheiro", <Valor key="a">R$ 7.000</Valor>, <Valor key="b">—</Valor>],
            ]}
            total={["Total declarado", r(fundadores), <Valor key="a">R$ 439.000</Valor>, <Valor key="b">R$ 792.000</Valor>]}
          />
          <p className="mt-4 text-sm font-light text-muted">
            Fonte: Resumo Executivo Leilão NoZap (17/12/2025). Os valores são declarados pelos fundadores e passam a verificado quando cada item tiver nota ou
            comprovante no data room. <Etiqueta tipo="MANAGEMENT_DATA" pequena />
          </p>

          <Titulo className="mt-16" sub="O que entrou na empresa depois de dez/2025 e foi encontrado nos extratos e no financeiro do app">
            O Dinheiro de 2026
          </Titulo>
          <Quadro
            cabecalho={["Quando", "De quem", "Valor", "Como entrou", "Etiqueta"]}
            linhas={[
              [<Valor key="d">29/01 e 23/07/2026</Valor>, "Investidor 2 (primeiro aporte externo)", <Valor key="v">R$ 20.000</Valor>, <span key="c">rendimento de R$ 500 por mês<Obs>R$ 5 mil (29/01) e R$ 10 mil (23/07) conferidos no extrato; o restante a confirmar</Obs></span>, <Etiqueta key="e" tipo="MANAGEMENT_DATA" pequena />],
              [<Valor key="d">mar/2026</Valor>, "Dois cartões de pessoas da equipe", <Valor key="v">R$ 15.000</Valor>, "compras da empresa pagas com cartão pessoal, lançadas como investimento", <Etiqueta key="e" tipo="MANAGEMENT_DATA" pequena />],
              [<Valor key="d">11/08/2026</Valor>, "Parceiro de compra B", <Valor key="v">R$ 50.000</Valor>, "contrato · 3% ao mês", <Etiqueta key="e" tipo="VERIFIED" pequena />],
              [<Valor key="d">2026</Valor>, "Investidor 1 (familiar de um diretor)", <Valor key="v">R$ 70.000</Valor>, <span key="c">R$ 50 mil em um carro, que lastreia uma carta de crédito, e R$ 20 mil em limite de cartão de crédito<Obs>não entrou como dinheiro em conta; rende R$ 3.600 por mês</Obs></span>, <Etiqueta key="e" tipo="MANAGEMENT_DATA" pequena />],
              [<Valor key="d">01/09/2026</Valor>, "Parceiro de compra A", <Valor key="v">R$ 200.000</Valor>, "contrato · 4,5% ao mês", <Etiqueta key="e" tipo="VERIFIED" pequena />],
              [<Valor key="d">24–30/09/2026</Valor>, "Um diretor, comprando 1%", <Valor key="v">{r(compra1pct)}</Valor>, <span key="c">compra de participação por R$ 250 mil — faltam R$ 50 mil<Obs>entrada conferida no extrato do Itaú; contrato e origem dos recursos a documentar</Obs></span>, <Etiqueta key="e" tipo="VERIFIED" pequena />],
              [<Valor key="d">jan a jul/2026</Valor>, "Aportes dos sócios e outras entradas grandes", <Valor key="v">R$ 375.813</Valor>, "Santander, sem o nome de quem mandou", <Etiqueta key="e" tipo="VERIFIED" pequena />],
            ]}
            total={["2026", "Total de capital que entrou nas contas", <Valor key="v">{r(deCapital)}</Valor>, "pelos extratos; o carro, o limite de cartão e os cartões da equipe não passaram pela conta", <Etiqueta key="e" tipo="VERIFIED" pequena />]}
          />
          <div className="mt-6">
          <Nota>
            <strong>Aportes dos sócios em 2026:</strong> os documentos param em dez/2025, mas o extrato não. De janeiro a julho, a conta Santander recebeu
            cerca de R$ 376 mil em valores grandes — é aí que estão os aportes que o fundador seguiu fazendo para pagar sala, galpão e equipe.
          </Nota>
          </div>
        </Conteiner>
      </section>

      {/* PARA ONDE FOI O DINHEIRO */}
      <Faixa>
        <Titulo tag="Conciliação dos extratos" sub="Itaú, Santander e Mercado Pago, de 01/01 a 16/10/2026, sem contar transferência entre contas da própria empresa">
          Para Onde Foi o Dinheiro
        </Titulo>
        <div className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <NumeroGrande compacto valor={r(saidas)} rotulo="saíram das contas" sub="jan a 16/out/2026" etiqueta="VERIFIED" href="/app/prova/CASH_OUT_M" />
          <NumeroGrande compacto valor={r(deClientes)} rotulo="vieram de clientes" sub="Pix, depósitos e vendas" etiqueta="VERIFIED" href="/app/prova/CASH_IN_CUSTOMERS_M" cor="verde" />
          <NumeroGrande compacto valor={r(deCapital)} rotulo="vieram de aportes e capital" sub="sócios, investidores e parceiros" etiqueta="VERIFIED" href="/app/prova/CASH_IN_CAPITAL_M" />
          <NumeroGrande compacto valor={`${parteVenda}%`} rotulo="dos gastos pagos com venda" sub="o restante veio de capital" etiqueta="VERIFIED" />
        </div>
        <Quadro
          cabecalho={["Mês", "De clientes", "Aportes e capital", "Saíram", "Sobrou ou faltou"]}
          minimo={820}
          linhas={mesesCaixa.map((p) => {
            const c = doMes("CASH_IN_CUSTOMERS_M", p);
            const k = mesDe("CASH_IN_CAPITAL_M", p);
            const s = doMes("CASH_OUT_M", p);
            return [
              p === "2026-10-01" ? `${rotuloMes(p)} (até 16)` : rotuloMes(p),
              <Valor key="c">{r(c)}</Valor>,
              <span key="k"><Valor>{r(k?.valor ?? 0)}</Valor>{k?.nota && <Obs>{k.nota}</Obs>}</span>,
              <Valor key="s">{r(s)}</Valor>,
              <Valor key="d">{r(c + (k?.valor ?? 0) - s)}</Valor>,
            ];
          })}
          total={["Total", <Valor key="c">{r(deClientes)}</Valor>, <Valor key="k">{r(deCapital)}</Valor>, <Valor key="s">{r(saidas)}</Valor>, <Valor key="d">{r(deClientes + deCapital - saidas)}</Valor>]}
        />
        <p className="mt-4 text-sm font-light text-muted">
          Pix e depósitos de até R$ 5 mil na conta Santander de jan a jul contam como cliente; acima disso, como aporte. Mais {r(outrasEntradas)} de estornos e
          rendimentos completam o que entrou. Valores que entraram e saíram iguais
          (R$ 117 mil em 15/01, 17–18/03, 13–16/04 e 22/06) ficam fora, como transferência. O saldo que já estava nas contas em 01/01 não entra na conta.{" "}
          <Etiqueta tipo="VERIFIED" pequena />
        </p>

        <Titulo className="mt-16" sub="Agosto a outubro: os meses em que todas as contas mostram o nome de quem recebeu">
          {`${r(saidasTres)} em Três Meses, por Tipo de Gasto`}
        </Titulo>
        <Quadro
          cabecalho={["Tipo de gasto", "Ago", "Set", "Out (até 16)", "Total", "Parte"]}
          minimo={860}
          linhas={gastos.map((g) => [
            <span key="t">{g.tipo}<Obs>{g.oque}</Obs></span>,
            ...TRES.map((p) => <Valor key={p}>{r(doMes(g.id, p))}</Valor>),
            <Valor key="t3">{r(nosTres(g.id))}</Valor>,
            <Valor key="pc">{saidasTres ? `${Math.round((100 * nosTres(g.id)) / saidasTres)}%` : "—"}</Valor>,
          ])}
          total={["Total", ...TRES.map((p) => <Valor key={p}>{r(doMes("CASH_OUT_M", p))}</Valor>), <Valor key="t3">{r(saidasTres)}</Valor>, "100%"]}
        />

        <Titulo className="mt-16" sub="Até 19/07 a conta principal era a do Santander, e o banco não imprime quem recebeu cada pagamento. O total é do extrato; a divisão usa o que o fundador informa.">
          {`Janeiro a Julho: ${r(semNome)} Pelo Santander`}
        </Titulo>
        <Quadro
          cabecalho={["Para onde foi", "Valor", "Como foi calculado", "Etiqueta"]}
          minimo={760}
          linhas={[
            ...estimativas.map((e) => {
              const x = ultimo.get(e.id);
              return [e.tipo, <Valor key="v">{r(x?.valor ?? null)}</Valor>, x?.nota ?? "—", <Etiqueta key="e" tipo={x?.etiqueta ?? "NAO_DISPONIVEL"} pequena />];
            }),
            ["Equipe, estoque, comissões e demais pagamentos", <Valor key="v">{r(restoJJ)}</Valor>, "o que sobra do total", <Etiqueta key="e" tipo="MANAGEMENT_DATA" pequena />],
          ]}
          total={["Total que saiu do Santander", <Valor key="v">{r(semNome)}</Valor>, "comprovantes diários do banco, 15/01 a 19/07", <Etiqueta key="e" tipo="VERIFIED" pequena />]}
        />
        <Grade colunas={3} className="mt-10">
          <Cartao tom="lateral" titulo="Os cartões que a empresa usa">
            A empresa usa dois cartões de pessoas físicas como cartões da empresa — o de uma executiva, que o deixou à disposição, e o de um investidor — e paga
            as faturas todo mês: em média {r(cartoesMes)} de agosto a outubro. Pelos cartões passam o aluguel do escritório (R$ 10 mil), as plataformas e
            sistemas (cerca de R$ 5 mil) e o consumo do dia a dia (R$ 5 a 10 mil), segundo o fundador <Etiqueta tipo="MANAGEMENT_DATA" pequena />. O
            restante se separa com as faturas na mão.
          </Cartao>
          <Cartao tom="lateral" titulo="Tecnologia">
            O aplicativo foi construído por um time de quatro desenvolvedores contratados por serviço. Nas contas com nome eles quase não aparecem, porque foram
            pagos pela conta Santander de jan a jul e pelos cartões. O financeiro do app registra R$ 2.680 por mês de construção do aplicativo desde fev/2026, e
            o fundador informa cerca de R$ 10 mil por mês em tecnologia, somando pessoas e plataformas <Etiqueta tipo="MANAGEMENT_DATA" pequena />.
          </Cartao>
          <Cartao tom="cheio" titulo="Quanto a empresa recebeu para chegar até aqui">
            {r(fundadores)} declarados pelos fundadores até dez/2025 e {r(deCapital)} de capital que entrou nas contas em 2026: {r(recebido)}. Parte é dinheiro
            de sócio, parte é capital de terceiros que paga rendimento todo mês e {r(compra1pct)} são compra de participação.
          </Cartao>
        </Grade>
      </Faixa>

      {/* QUANTO CUSTA O DINHEIRO DE FORA */}
      <section className="border-y border-white/10 bg-surface py-16 sm:py-24">
        <Conteiner>
        <Titulo tag="O custo do capital" sub="Dinheiro de terceiros que a empresa remunera todo mês — não é participação societária">
          {`${r(terceiros)} a ${r(custoCapital)} por Mês`}
        </Titulo>
        <Quadro
          cabecalho={["Quem", "Desde", "Capital", "Paga por mês", "Ao mês", "Fonte"]}
          linhas={[
            ["Parceiro de compra A", "01/09/2026", <Valor key="a">R$ 200.000</Valor>, <Valor key="b">R$ 9.000</Valor>, "4,5%", <span key="f">contrato<Obs>não está cadastrado no financeiro do app</Obs></span>],
            ["Investidor 1", "2026", <Valor key="a">R$ 70.000</Valor>, <Valor key="b">R$ 3.600</Valor>, "5,1%", "fundador + extratos"],
            ["Parceiro de compra B", "11/08/2026", <Valor key="a">R$ 50.000</Valor>, <Valor key="b">R$ 1.500</Valor>, "3%", "contrato"],
            ["Investidor 2", "jan/2026", <Valor key="a">R$ 20.000</Valor>, <Valor key="b">R$ 500</Valor>, "2,5%", "fundador + extratos"],
          ]}
          total={["Total", "", <Valor key="a">{r(terceiros)}</Valor>, <Valor key="b">{r(custoCapital)}</Valor>, `${mediaMes.toLocaleString("pt-BR", { maximumFractionDigits: 1 })}% em média`, ""]}
        />
        <Grade colunas={2} className="mt-10">
          <Cartao tom="azul" titulo="O que isso significa">
            Em setembro, a receita própria do app (comissões e taxas) foi de {r(receitaPropriaSet)}. O custo desse capital é de {r(custoCapital)} por mês — maior que
            a receita própria. É dinheiro que funcionou para comprar estoque, mas é caro: perto de {inteiro(Math.round(aoAno))}% ao ano.
          </Cartao>
          <Cartao tom="cheio" titulo="O primeiro uso de um aporte">
            Trocar dinheiro caro por dinheiro paciente. Quitar {r(terceiros)} de capital remunerado libera {r(custoCapital)} por mês de caixa — antes de qualquer
            venda nova.
          </Cartao>
        </Grade>
        </Conteiner>
      </section>

      {/* A CARTEIRA DO CLIENTE */}
      <Faixa>
          <Titulo tag="O dinheiro do cliente" sub="Quem deposita para dar lance deixa metade guardada para o próximo leilão">
            Metade do Depósito Fica na Plataforma
          </Titulo>
          <div className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            <NumeroGrande compacto valor="R$ 61.452" rotulo="depositados" sub="49 pessoas, desde 18/07" etiqueta="VERIFIED" />
            <NumeroGrande compacto valor="R$ 25.087" rotulo="viraram arremate" sub="41% do depositado" etiqueta="VERIFIED" />
            <NumeroGrande compacto valor="R$ 4.946" rotulo="viraram compra na loja" sub="8% do depositado" etiqueta="VERIFIED" />
            <NumeroGrande compacto valor="R$ 31.419" rotulo="ainda não gastos" sub="51% · hoje R$ 27.079 em 47 carteiras" etiqueta="VERIFIED" cor="verde" href="/app/prova/WALLET_UNSPENT_SHARE" />
          </div>
          <Grade colunas={2} className="mt-10">
            <Cartao tom="lateral" titulo="Por que é bom sinal">
              O cliente não deposita e some: ele deixa o saldo esperando o próximo leilão. Do que já foi gasto, 84% foi em arremate e 16% na loja. O fundador fala em
              52%; a conta do sistema dá 51%.
            </Cartao>
            <Cartao tom="lateral" titulo="O cuidado que vem junto">
              Esse saldo é do cliente. Não é receita e não paga conta da empresa: fica separado e só vira receita a comissão de quando ele compra. Por isso aparece no
              painel como obrigação, não como caixa.
            </Cartao>
          </Grade>
      </Faixa>

      {/* QUANTO CUSTA MANTER A EMPRESA */}
      <section className="border-y border-white/10 bg-surface py-16 sm:py-24">
        <Conteiner>
        <Titulo tag="Custo fixo" sub="O orçamento da diretoria, o que está cadastrado no app e o que foi pago de fato">Quanto Custa Manter a Empresa por Mês</Titulo>
        <div className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-3">
          <NumeroGrande compacto valor={r(orcamento)} rotulo="orçamento mensal" sub="aprovado em set/2026" etiqueta="MANAGEMENT_DATA" href="/app/prova/FIXED_COST_BUDGET_M" />
          <NumeroGrande compacto valor={r(cadastrado)} rotulo="contas cadastradas" sub="vencimento em nov/2026" etiqueta="MANAGEMENT_DATA" href="/app/prova/FIXED_COST_REGISTERED_M" />
          <NumeroGrande compacto valor={r(pagoSet)} rotulo="pago de fato" sub="em set/2026" etiqueta="MANAGEMENT_DATA" href="/app/prova/EXPENSES_PAID" />
        </div>
        <Quadro
          cabecalho={["Item", "Orçamento (set/26)", "Cadastrado no app (nov/26)", "Observação"]}
          linhas={[
            ["Pessoas — diretoria e equipe", <Valor key="a">R$ 182.000</Valor>, <Valor key="b">R$ 70.900</Valor>, "não é folha tradicional: parte é retirada e parte é participação por meta"],
            ["Galpão", <Valor key="a">R$ 23.100</Valor>, <Valor key="b">R$ 23.036</Valor>, `até out/2026: entrada, três mensalidades e frete para trazer os produtos — ${r(galpaoTotal)}`],
            ["Escritório no Recreio", <Valor key="a">R$ 10.000</Valor>, <Valor key="b">R$ 20.000</Valor>, "lançado duas vezes no app; o valor real é R$ 10 mil"],
            ["Tecnologia", <Valor key="a">R$ 5.000</Valor>, <Valor key="b">R$ 5.208</Valor>, "inclui R$ 2.680 por mês da construção do aplicativo"],
            ["Marketing", <Valor key="a">R$ 5.000</Valor>, <Valor key="b">R$ 105</Valor>, "o plano do ranking prevê R$ 36 a 40 mil por mês de tráfego"],
            ["Cartão corporativo, contabilidade e consumo", <Valor key="a">R$ 11.000</Valor>, <Valor key="b">—</Valor>, "não cadastrados no app"],
            ["Custo do capital de terceiros", <Valor key="a">—</Valor>, <Valor key="b">R$ 5.600</Valor>, "mais R$ 9.000 do parceiro A, fora do app"],
            ["Outras despesas cadastradas", <Valor key="a">—</Valor>, <Valor key="b">R$ 71.227</Valor>, "em revisão: alimentação, parcelas de cartão, consórcio, aluguéis e capitalização"],
          ]}
          total={["Total", <Valor key="a">{r(orcamento)}</Valor>, <Valor key="b">{r(cadastrado)}</Valor>, `com o tráfego planejado (R$ 36 a 40 mil), o orçamento vai a ${r((orcamento ?? 0) + 36000)} a ${r((orcamento ?? 0) + 40000)}`]}
        />
        <Grade colunas={2} className="mt-10">
          <Cartao tom="lateral" titulo="A sala e o galpão">
            O galpão custa R$ 23.036 por mês e já são quatro meses pagos: R$ 20 mil de entrada, três mensalidades de R$ 23 mil e cerca de R$ 3 mil de frete
            para trazer os produtos — {r(galpaoTotal)} até outubro. A entrada (Pix de R$ 10 mil em 23/07 e em 27/07, à imobiliária da proprietária) e duas mensalidades (08/09 por boleto e 08/10 por
            Pix) estão no extrato com nome <Etiqueta tipo="VERIFIED" pequena />; a outra mensalidade e o frete são informados pelo fundador{" "}
            <Etiqueta tipo="MANAGEMENT_DATA" pequena />. O escritório custa R$ 10 mil por mês desde mar/2026; no app falta dar baixa em três meses e corrigir um lançamento em dobro.
          </Cartao>
          <Cartao tom="lateral" titulo="Contas vencidas no app">
            {r(vencidas)} aparecem como vencidas. Boa parte são meses de aluguel pagos e não baixados no sistema: a limpeza desse número é o próximo passo para o
            financeiro do app virar prova.
          </Cartao>
        </Grade>
        </Conteiner>
      </section>

      {/* O LADO SOCIAL */}
      <Capitulo
        id="social"
        numero="O lado social"
        titulo="Conexão: o Café de Toda Sexta"
        sub="Toda sexta de manhã, a empresa abre a porta e serve café para quem quiser chegar."
        imagem="/m/vale-recreio.jpg"
        lado="esquerda"
      >
        <p>
          O Conexão é a parte social da empresa. Toda sexta, das 9h às 13h, no Vale do Recreio, um café da manhã gratuito com o tema “Desconectar para
          conectar” — e o Conexão Delas, feito por mulheres e para mulheres. São quase dois anos de encontros, e desde out/2025 cada um fica registrado no
          aplicativo do Vale do Recreio, com quem confirmou e quem chegou.
        </p>
      </Capitulo>
      <Faixa>
        <Titulo tag="Medido no app do Vale do Recreio" sub="Registros de out/2025 a 16/10/2026; os encontros anteriores aconteceram antes de o app existir">
          Um Ano de Encontros, Registrado
        </Titulo>
        <div className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-5">
          <NumeroGrande compacto valor={n(encontros)} rotulo="encontros" sub="quase todas as sextas" etiqueta="VERIFIED" href="/app/prova/SOCIAL_MEETINGS" />
          <NumeroGrande compacto valor={n(pessoas)} rotulo="pessoas diferentes" sub="por e-mail ou telefone" etiqueta="VERIFIED" href="/app/prova/SOCIAL_PEOPLE" cor="verde" />
          <NumeroGrande compacto valor={n(confirmacoes)} rotulo="confirmações" sub="feitas no app" etiqueta="VERIFIED" href="/app/prova/SOCIAL_CONFIRMATIONS" />
          <NumeroGrande compacto valor={n(chegadas)} rotulo="chegadas na porta" sub="marcadas no dia" etiqueta="VERIFIED" href="/app/prova/SOCIAL_CHECKINS" />
          <NumeroGrande compacto valor={doacoes === null ? "—" : `+ ${r(doacoes)}`} rotulo="em doações e café" sub="em quase dois anos" etiqueta="MANAGEMENT_DATA" href="/app/prova/SOCIAL_DONATIONS" />
        </div>
        <Grade colunas={2} className="mt-10">
          <Cartao tom="lateral" titulo="Por que isso entra no livro do capital">
            É dinheiro que a empresa tira do caixa sem esperar venda em troca. Uma comunidade que se encontra toda semana há quase dois anos, com presença
            medida, é um ativo que não se copia comprando anúncio.
          </Cartao>
          <Cartao tom="lateral" titulo="O que falta provar">
            Os encontros e as presenças vêm do banco do app do Vale <Etiqueta tipo="VERIFIED" pequena />. O valor das doações é informado pelo fundador e passa a
            verificado com as notas e os Pix do café e das doações.
          </Cartao>
        </Grade>
      </Faixa>

      {/* SÓ CONSELHO: O QUE AJUSTAR ANTES DE MOSTRAR A UM INVESTIDOR */}
      {conselho && (
        <section className="border-y border-warn/30 bg-warn/[0.04] py-16 sm:py-24">
          <Conteiner>
            <Titulo tag="Só para o conselho" sub="O que um analista do investidor vai achar — e que precisa estar resolvido antes">Antes de Abrir Para o Investidor</Titulo>
            <Grade colunas={2} className="mt-10">
              <Cartao tom="escuro" titulo="1 · Totais trocados no documento dos fundadores">
                Os itens do Luiz somam R$ 713 mil (o título diz R$ 723 mil); os do Luciano somam R$ 481 mil (o título diz R$ 471 mil). O total de R$ 1.231.000 fecha
                com a soma dos itens. O escritório Le Monde aparece como R$ 360 mil em dez/2025 e R$ 350 mil em out/2026.
              </Cartao>
              <Cartao tom="escuro" titulo="2 · O preço da participação mudou quatro vezes">
                Dez/2025: 3% por R$ 207 mil (R$ 6,9 milhões). Mar/2026: 2% por R$ 500 mil (R$ 25 milhões). Ago/2026: 0,5% vale R$ 125 mil e +1% custa R$ 500 mil (R$
                50 milhões). Out/2026: 1% por R$ 900 mil (R$ 90 milhões). O investidor vai perguntar qual vale.
              </Cartao>
              <Cartao tom="escuro" titulo="3 · Promessa de rendimento fixo">
                A rodada de R$ 10 milhões (dez/2025) promete 4% ao mês “sem risco”, e o plano de captação (ago/2026) paga 1% ao mês sobre a carteira. Rendimento
                fixo prometido a investidor pode ser tratado como oferta pública: precisa de parecer jurídico antes de circular.
              </Cartao>
              <Cartao tom="escuro" titulo="4 · Despesas a separar da empresa">
                No financeiro do app há, por mês: R$ 24,6 mil de restaurante do hotel e R$ 10,3 mil de dois aluguéis de moradia. As faturas do cartão emprestado (R$ 23
                mil por mês, R$ 179 mil lançados até abr/2027) precisam das notas de cada compra. Nos extratos de set e out também saem da conta da empresa
                gastos pessoais (restaurantes, lazer, loja de celular) e cerca de R$ 20 mil em parcelas a bancos e dívidas sem contrato no data room.
                Classificar o que é da empresa e o que é pessoa física.
              </Cartao>
              <Cartao tom="escuro" titulo="5 · Lançamentos com erro">
                Aluguel do escritório lançado duas vezes por mês (R$ 10 mil a mais). Título de capitalização de R$ 10 mil por mês, cuja descrição diz R$ 1 mil. O
                parceiro A (R$ 9 mil por mês) não está cadastrado.
              </Cartao>
              <Cartao tom="escuro" titulo="6 · “8 mil produtos” e “10 mil clientes”">
                São estimativas da administração. Os 10 mil clientes saem de {n(v("WHATSAPP_BASE"))} contatos no WhatsApp × 3 (cada contato alcança ao menos mais duas
                pessoas); os 8 mil produtos, de ~8,5 mil peças compradas. O que tem prova: {n(v("CUSTOMER_BASE_UNIQUE"))} pessoas na base, {n(v("CUSTOMER_PAYMENTS_2026"))}
                pagamentos de clientes em 2026 e {n(v("LOTS_BOUGHT_PIECES"))} peças em lotes registrados. A conta das peças (compradas menos o estoque de hoje) dá cerca de 6 mil
                saídas dos lotes, mais o MVP — perto, mas abaixo dos 8 mil: os lotes do começo e as vendas da fase WhatsApp fecham a diferença. O app já tirou da home o
                “+10 mil produtos leiloados”, que vinha de um modelo de exemplo.
              </Cartao>
              <Cartao tom="escuro" titulo="7 · Compromissos de integralização">
                Dez/2025 previa R$ 500 mil de capital operacional do Luciano (jan/2026), R$ 200 mil do Geovane (até 24/03/2026) e R$ 70 mil de outros dois diretores
                (até 24/12/2027); a proposta de mar/2026 previa R$ 500 mil por 2%. Dizer o que virou dinheiro.
              </Cartao>
              <Cartao tom="escuro" titulo="8 · Simples, balancete e banco não fecham">
                A declaração do Simples (transmitida em 15/05/2026) traz 2025 zerado e {r(declarado || null)} de jan a mai/2026 — maio inteiro declarado no dia 15.
                O balancete de 2025 traz {r(balancete2025)} de receita, R$ 616 mil de lucro e R$ 706 mil em caixa. O banco mostra {r(bancoJanMai)} em Pix de
                clientes de jan a mai/2026 (só a conta Santander, com alguns dias faltando) e registros internos de {r(ateMaio)}. Uma receita declarada maior que a real paga imposto à toa e não se sustenta numa
                auditoria: o contador precisa reconciliar.
              </Cartao>
              <Cartao tom="escuro" titulo="9 · A compra de 1% por um diretor">
                Os {r(compra1pct)} entraram assim: R$ 130 mil por Pix de três pagadores que não são o comprador (duas pessoas e uma empresa) e R$ 70 mil em dinheiro
                vivo, em 43 depósitos de até R$ 2 mil no mesmo dia (24/09). Depósito em espécie fracionado é exatamente o movimento que o banco comunica ao COAF. Antes
                de registrar a participação: contrato assinado, declaração de origem de cada pagador e do dinheiro em espécie, com o contador e o advogado. E o
                preço — 1% por R$ 250 mil — é o de uma empresa de R$ 25 milhões, não o de R$ 90 milhões do documento de out/2026.
              </Cartao>
              <Cartao tom="escuro" titulo="10 · O cartão de um familiar de diretor">
                O investidor 1 entrou com um carro (R$ 50 mil, que lastreia uma carta de crédito) e R$ 20 mil de limite de cartão, e recebe cerca de 5% ao mês. A
                empresa usa esse cartão e paga a fatura todo mês (R$ 20 a 23 mil). Funciona, mas compra em cartão de pessoa física é difícil de provar como despesa
                da empresa: o caminho é migrar para cartão da empresa e documentar o carro como garantia.
              </Cartao>
              <Cartao tom="escuro" titulo="11 · O investimento em tecnologia não aparece com nome">
                O fundador informa que o aplicativo foi construído por Ávila, Elismar, Luiz Santana e Diogo Archanjo. Nas contas com nome aparecem só cerca de R$
                2 mil pagos a eles (jul a set). O resto saiu pela conta Santander sem nome e pelos cartões. Sem esse número, o principal ativo do valuation — o
                aplicativo — fica sem custo comprovado: contratos ou recibos de serviço de cada um resolvem.
              </Cartao>
              <Cartao tom="escuro" titulo={`12 · Só ${parteVenda}% dos gastos foram pagos com venda`}>
                De jan a 16/out saíram {r(saidas)} das contas; os clientes trouxeram {r(deClientes)}. Os outros {r(saidas - deClientes)} vieram de capital — e
                uma parte é capital de terceiros que cobra juros. O investidor vai ler isso como um gasto acima da venda de cerca de{" "}
                {r((saidas - deClientes) / 9.5)} por mês. A resposta é a receita própria do app crescendo e o custo do capital caindo.
              </Cartao>
            </Grade>
            <Titulo className="mt-16" sub="O que falta o fundador mandar para fechar a conta">A Lista de Pendências</Titulo>
            <ol className="mt-6 max-w-4xl list-decimal space-y-2 pl-6 text-[15px] font-light leading-relaxed text-texto">
              <li>Comprovantes da sala de abr, jun e ago/2026 e a correção do lançamento em dobro.</li>
              <li>Compra de 1% pelo diretor: contrato e declaração de origem dos R$ 200 mil (três pagadores e R$ 70 mil em espécie).</li>
              <li>Quanto cada sócio colocou de jan a out/2026, com comprovante.</li>
              <li>Declarações do Simples de jun a set/2026 e a reconciliação do contador entre Simples, balancete e banco.</li>
              <li>Prova das vendas da fase leilaowhatsapp.com: extratos Pix, envios ou exportação do site.</li>
              <li>Confirmar se o orçamento de pessoas (R$ 182 mil) já é pago ou é meta; o fundador fala em R$ 200 a 250 mil de orçamento total por mês.</li>
              <li>Faturas dos dois cartões de ago a out/2026, para separar escritório, plataformas, consumo e o que for pessoal.</li>
              <li>Contratos ou recibos de serviço dos desenvolvedores do aplicativo.</li>
              <li>Notas e Pix do café e das doações do Conexão.</li>
            </ol>
          </Conteiner>
        </section>
      )}

      {/* FECHO */}
      <Faixa>
        <Citacao verde>
          Uma empresa que começou com 551 produtos e o último recurso do fundador movimentou {r(movimentado)} nas suas contas em 2026, recebeu {r(deClientes)} de
          clientes, comprou lotes que valem {r(v("LOTS_BOUGHT_MARKET_VALUE"))} a preço de mercado, construiu um aplicativo próprio e hoje tem clientes que deixam
          metade do depósito esperando o próximo leilão — e toda sexta abre a porta para a comunidade. O que falta não é história: é
          trocar o dinheiro caro e provar cada número.
        </Citacao>
        <Texto className="mt-8">
          <p>
            Todos os números desta página estão em <Link href="/app/numeros" className="text-pill underline underline-offset-2">Números com prova</Link>, na família
            “Capital e história”, com a fonte e a impressão digital de cada carga.
          </p>
        </Texto>
        <Link
          href="/app/dataroom"
          className="mt-8 inline-flex items-center gap-2 rounded-lg bg-accent px-5 py-3 text-sm font-semibold text-accent-ink transition hover:bg-accent/90"
        >
          Ver o que já está no data room <ArrowRight className="h-4 w-4" aria-hidden />
        </Link>
      </Faixa>
    </div>
  );
}
