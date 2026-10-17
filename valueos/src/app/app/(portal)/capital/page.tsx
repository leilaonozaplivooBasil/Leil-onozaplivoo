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
  const mediaMes = terceiros && custoCapital ? (100 * custoCapital) / terceiros : 0;
  const aoAno = (Math.pow(1 + mediaMes / 100, 12) - 1) * 100;
  const receitaPropriaSet =
    (serie.get("REVENUE_COMMISSION_RETAINED")?.find((x) => x.periodo === "2026-09-01")?.valor ?? 0) +
    (serie.get("REVENUE_FEES")?.find((x) => x.periodo === "2026-09-01")?.valor ?? 0);

  // Vendas mês a mês: antes do app (registro da gestão) e depois (sistema).
  const antes = (serie.get("SALES_HISTORY_MGMT") ?? []).map((x) => ({ periodo: x.periodo, valor: x.valor, tom: "gestao" as const }));
  const depois = (serie.get("GMV_GOODS") ?? []).map((x) => ({ periodo: x.periodo, valor: x.valor, tom: "verificado" as const }));
  const vendas = [...antes, ...depois].sort((a, b) => a.periodo.localeCompare(b.periodo));
  const totalVendas = vendas.reduce((s, x) => s + (x.valor ?? 0), 0);
  const ateMaio = antes.filter((x) => x.periodo <= "2026-05-01").reduce((s, x) => s + (x.valor ?? 0), 0);

  return (
    <div>
      {/* CAPA */}
      <Capitulo
        numero="Livro do capital · atualizado em 17/10/2026"
        titulo="A História do Dinheiro"
        sub="De onde veio cada real, o que ele construiu e quanto custa manter a empresa de pé."
        imagem="/m/bilhoes-parados.jpg"
      >
        <p>
          Este retrato junta os documentos dos fundadores, as planilhas de venda da operação, o financeiro e a carteira do aplicativo. Cada número diz de
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
              Venda direta pelo WhatsApp, Facebook e OLX, com pagamento por Pix — ainda sem pagamento integrado. O registro que sobrou dessa fase é o de <strong>595 produtos</strong> vendidos
              no MVP. O fundador informa mais de 10 mil produtos vendidos e mais de 10 mil clientes impactados pelo site leilaowhatsapp.com, hoje fora do ar — esse
              número entra no portal quando houver extrato que o comprove.
            </Cartao>
            <Cartao tom="cinza" titulo="2 · Catálogo, showroom e NEXUS">
              De dez/2025 a jul/2026: catálogo leilaonozap.com, showroom no Recreio, time de vendedores e o NEXUS registrando cada comprovante. É a fase com
              série mensal de vendas, de {r(vendas[0]?.valor ?? null)} no primeiro mês até {r(antes.find((x) => x.periodo === "2026-06-01")?.valor ?? null)} em junho.
            </Cartao>
            <Cartao tom="lateral" titulo="3 · O aplicativo e o leilão">
              Desde jul/2026, leilaonozap.net com carteira, loja e leilão. A venda pelo WhatsApp foi reduzida de propósito para levar a base para o app — por isso a
              curva cai em julho e volta a subir com o leilão. O canal novo tem três meses.
            </Cartao>
          </Grade>
          <LinhaDoTempo
            itens={[
              { quando: "Nov/2025", texto: "A empresa recomeça no Vale do Recreio. Primeira compra às cegas: 551 produtos, cerca de R$ 34 mil, com o último recurso do fundador.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Dez/2025", texto: "Primeiro mês de vendas registradas: R$ 26.358. O documento dos fundadores soma R$ 1.231.000 investidos.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Jan/2026", texto: "Catálogo leilaonozap.com no ar e primeiro aporte externo, de R$ 5 mil (29/01).", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Mar/2026", texto: "Escritório no Hotel Atlântico Sul, no Recreio: R$ 10 mil por mês desde então.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Abr/2026", texto: "Lotes do Mercado Livre (4.549 peças) e o NEXUS passando a registrar cada venda. Melhor mês até ali: R$ 69.891 até o dia 23.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Jun/2026", texto: "Pico da venda pelo WhatsApp: R$ 74.438 no mês, pela planilha diária.", etiqueta: "MANAGEMENT_DATA" },
              { quando: "Jul/2026", texto: "O aplicativo entra no ar com carteira e loja. Primeiro depósito de cliente em 18/07.", etiqueta: "VERIFIED" },
              { quando: "Ago/2026", texto: "Mudança para o galpão. Parceiro de compra B entra com R$ 50 mil, a 3% ao mês. Começam os leilões com lance.", etiqueta: "VERIFIED" },
              { quando: "Set/2026", texto: "Galpão a R$ 23.036 por mês. Parceiro A entra com R$ 200 mil, a 4,5% ao mês. Mais R$ 200 mil entram no Itaú, origem a confirmar.", etiqueta: "VERIFIED", novo: true },
              { quando: "Out/2026", texto: `${inteiro(v("USERS_REGISTERED") ?? 0)} contas no app e ${r(v("GMV_AUCTION"))} em arremates até o dia 16.`, etiqueta: "VERIFIED", novo: true },
            ]}
          />
        </Conteiner>
      </section>

      {/* VENDAS DESDE O PRIMEIRO DIA */}
      <Faixa>
        <Titulo tag="Quanto já foi vendido" sub="Mercadoria vendida por mês, somando todos os canais">{`${r(totalVendas)} em Onze Meses`}</Titulo>
        <GraficoBarras
          titulo="Cinza: registro da operação (PDV, WhatsApp, NEXUS, planilha) · Verde: medido no aplicativo"
          formato={(x) => (x >= 1000 ? `${inteiro(Math.round(x / 1000))} mil` : inteiro(Math.round(x)))}
          dados={vendas.map((x) => ({ rotulo: rotuloMes(x.periodo), valor: x.valor, tom: x.tom }))}
        />
        <Quadro
          cabecalho={["Mês", "Vendas registradas", "Pix de clientes no banco", "Declarado ao Simples", "De onde vem a venda"]}
          minimo={860}
          linhas={vendas.map((x) => {
            const fonte = (x.tom === "gestao" ? serie.get("SALES_HISTORY_MGMT") : serie.get("GMV_GOODS"))?.find((y) => y.periodo === x.periodo);
            const banco = mesDe("BANK_SMALL_PIX_IN", x.periodo);
            const simples = mesDe("REVENUE_TAX_DECLARED_M", x.periodo);
            return [
              rotuloMes(x.periodo),
              <span key="v"><Valor>{r(x.valor)}</Valor><span className="ml-2 inline-block align-middle"><Etiqueta tipo={fonte?.etiqueta ?? "NAO_DISPONIVEL"} pequena /></span></span>,
              <span key="b"><Valor>{banco ? r(banco.valor) : "—"}</Valor>{banco?.nota && <Obs>{banco.nota}</Obs>}</span>,
              <Valor key="s">{simples ? r(simples.valor) : "—"}</Valor>,
              <span key="f">
                {fonte?.fonte}
                {fonte?.nota && <Obs>{fonte.nota}</Obs>}
              </span>,
            ];
          })}
          total={["Total", <Valor key="t">{r(totalVendas)}</Valor>, "", <Valor key="s">{r(declarado || null)}</Valor>, "dez/2025 a out/2026 (outubro até o dia 16)"]}
        />
        <Grade colunas={2} className="mt-10">
          <Cartao tom="lateral" titulo="Três fontes que ainda não conversam">
            O extrato do banco confirma a venda do WhatsApp: são centenas de Pix pequenos por mês ({r(bancoJanMai)} de jan a mai/2026 só na conta Santander). A
            declaração do Simples informa {r(declarado || null)} no mesmo período e 2025 zerado; o balancete de 2025 do contador registra {r(balancete2025)} de
            receita naquele ano. Fechar essas três contas com o contador é o primeiro passo da due diligence.
          </Cartao>
          <Cartao tom="lateral" titulo="Por que julho cai">
            Em julho a empresa deixou de vender pelo WhatsApp para lançar o aplicativo e o leilão. O número de agosto em diante é só o que passou pelo app, pago e
            conferido — sem a venda de balcão e de grupo, que antes fazia o volume.
          </Cartao>
        </Grade>
      </Faixa>

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
            ]}
          />
          <div className="mt-6">
          <Nota>
            <strong>Aportes dos sócios em 2026:</strong> os documentos param em dez/2025. O fundador informa que seguiu colocando capital próprio — sala, galpão e
            equipe. Esses valores entram aqui assim que cada um tiver data, valor e comprovante.
          </Nota>
          </div>
        </Conteiner>
      </section>

      {/* QUANTO CUSTA O DINHEIRO DE FORA */}
      <Faixa>
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
      </Faixa>

      {/* A CARTEIRA DO CLIENTE */}
      <section className="border-y border-white/10 bg-surface py-16 sm:py-24">
        <Conteiner>
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
        </Conteiner>
      </section>

      {/* QUANTO CUSTA MANTER A EMPRESA */}
      <Faixa>
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
            ["Galpão", <Valor key="a">R$ 23.100</Valor>, <Valor key="b">R$ 23.036</Valor>, "o fundador informa cerca de R$ 100 mil investidos na obra — falta comprovante"],
            ["Escritório no Recreio", <Valor key="a">R$ 10.000</Valor>, <Valor key="b">R$ 20.000</Valor>, "lançado duas vezes no app; o valor real é R$ 10 mil"],
            ["Tecnologia", <Valor key="a">R$ 5.000</Valor>, <Valor key="b">R$ 5.208</Valor>, "inclui R$ 2.680 por mês da construção do aplicativo"],
            ["Marketing", <Valor key="a">R$ 5.000</Valor>, <Valor key="b">R$ 105</Valor>, "o plano do ranking prevê R$ 36 a 40 mil por mês de tráfego"],
            ["Cartão corporativo, contabilidade e consumo", <Valor key="a">R$ 11.000</Valor>, <Valor key="b">—</Valor>, "não cadastrados no app"],
            ["Custo do capital de terceiros", <Valor key="a">—</Valor>, <Valor key="b">R$ 5.600</Valor>, "mais R$ 9.000 do parceiro A, fora do app"],
            ["Outras despesas cadastradas", <Valor key="a">—</Valor>, <Valor key="b">R$ 71.227</Valor>, "em revisão: alimentação, parcelas de cartão, consórcio, aluguéis e capitalização"],
          ]}
          total={["Total", <Valor key="a">{r(orcamento)}</Valor>, <Valor key="b">{r(cadastrado)}</Valor>, "com o tráfego planejado, o orçamento vai a R$ 271.100"]}
        />
        <Grade colunas={2} className="mt-10">
          <Cartao tom="lateral" titulo="A sala e o galpão">
            O galpão custa R$ 23.036 por mês e já são quatro meses: setembro e outubro foram pagos direto à imobiliária, e estão no extrato
            <Etiqueta tipo="VERIFIED" pequena />. Os primeiros meses foram pagos por repasse a uma pessoa; no extrato aparecem Pix sem nome que batem com o
            relato (15/06 e 16/07). O escritório custa R$ 10 mil por mês desde mar/2026; no app falta dar baixa em três meses e corrigir um lançamento em dobro.
          </Cartao>
          <Cartao tom="lateral" titulo="Contas vencidas no app">
            {r(vencidas)} aparecem como vencidas. Boa parte são meses de aluguel pagos e não baixados no sistema: a limpeza desse número é o próximo passo para o
            financeiro do app virar prova.
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
                mil por mês, R$ 179 mil lançados até abr/2027) precisam das notas de cada compra. Classificar o que é da empresa e o que é pessoa física.
              </Cartao>
              <Cartao tom="escuro" titulo="5 · Lançamentos com erro">
                Aluguel do escritório lançado duas vezes por mês (R$ 10 mil a mais). Título de capitalização de R$ 10 mil por mês, cuja descrição diz R$ 1 mil. O
                parceiro A (R$ 9 mil por mês) não está cadastrado.
              </Cartao>
              <Cartao tom="escuro" titulo="6 · “10 mil produtos”">
                A página inicial do app chegou a mostrar “+10 mil produtos leiloados”, vindo de um modelo de exemplo; saiu por não ter base no banco, e um teste
                automático impede que volte. Até chegar o extrato da fase leilaowhatsapp.com, o número defensável é 595 produtos no MVP e a série mensal desta página.
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
            </Grade>
            <Titulo className="mt-16" sub="O que falta o fundador mandar para fechar a conta">A Lista de Pendências</Titulo>
            <ol className="mt-6 max-w-4xl list-decimal space-y-2 pl-6 text-[15px] font-light leading-relaxed text-texto">
              <li>Confirmar os Pix do galpão pagos por repasse (15/06: R$ 10 mil + R$ 5 mil; 16/07: 2 × R$ 10 mil) e o mês de agosto; somar a obra, se houver.</li>
              <li>Comprovantes da sala de abr, jun e ago/2026 e a correção do lançamento em dobro.</li>
              <li>Compra de 1% pelo diretor: contrato e declaração de origem dos R$ 200 mil (três pagadores e R$ 70 mil em espécie).</li>
              <li>De quem é cada entrada grande sem nome no Santander: 19 e 28/01 (R$ 10 mil cada), 03/02 (R$ 18 mil), 02/03 (R$ 10 mil), 17/03 (R$ 50 mil, que saiu no dia seguinte), 08 e 09/04 (R$ 50 mil cada), 19/05 (R$ 40 mil + R$ 60 mil), 21/05 (R$ 27 mil), 22/06 (R$ 45 mil, que saiu no mesmo dia) e 16/07 (R$ 15 mil + R$ 5 mil).</li>
              <li>Quanto cada sócio colocou de jan a out/2026, com comprovante.</li>
              <li>Declarações do Simples de jun a set/2026 e a reconciliação do contador entre Simples, balancete e banco.</li>
              <li>Prova das vendas da fase leilaowhatsapp.com: extratos Pix, envios ou exportação do site.</li>
              <li>Confirmar se o orçamento de pessoas (R$ 182 mil) já é pago ou é meta; o fundador fala em R$ 200 a 250 mil de orçamento total por mês.</li>
            </ol>
          </Conteiner>
        </section>
      )}

      {/* FECHO */}
      <Faixa>
        <Citacao verde>
          Uma empresa que começou com 551 produtos e o último recurso do fundador, registrou mais de R$ 300 mil em vendas em onze meses, construiu um aplicativo próprio e hoje
          tem clientes que deixam metade do depósito esperando o próximo leilão. O que falta não é história: é trocar o dinheiro caro e provar cada número.
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
