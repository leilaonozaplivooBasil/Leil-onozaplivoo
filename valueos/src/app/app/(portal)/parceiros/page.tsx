import Link from "next/link";
import { valoresCarregados } from "@/lib/metricas";
import { papelAtual, eConselho } from "@/lib/papel";
import { mesCurto } from "@/lib/etiquetas";
import { Aviso, Cartao, Etiqueta, Grade, NotaRevisao, Numero, Pagina, Secao, Tabela, brl } from "@/components/ui";

export const dynamic = "force-dynamic";

// Parceiro de compra: o produto de captação da empresa, lido nos contratos e conferido nos extratos.
export default async function Parceiros() {
  const [{ ultimo, serie }, papel] = await Promise.all([valoresCarregados(), papelAtual()]);
  const conselho = eConselho(papel);
  const principal = ultimo.get("PARTNER_CAPITAL_LIABILITY");
  const servico = ultimo.get("PARTNER_CAPITAL_SERVICE_M");
  const comissao = serie.get("REVENUE_COMMISSION_RETAINED") ?? [];
  const gmv = serie.get("GMV_GOODS") ?? [];
  // Remuneração devida por mês: B entrou em 11/08 (1º repasse em 15/09); A entrou em 01/09 (1º repasse em 15/10).
  const DEVIDA: Record<string, number> = { "2026-08-01": 0, "2026-09-01": 1500, "2026-10-01": 10500 };

  return (
    <Pagina
      sobretitulo="5 minutos"
      titulo="Parceiros de compra"
      descricao="Capital de terceiros que a empresa usa para comprar lotes e remunera todo mês. Aqui estão os dois contratos que existem, o que cada um obriga e se a receita de hoje paga a conta."
    >
      <Grade colunas={3}>
        <Numero rotulo="Capital a devolver" valor={principal?.valor != null ? brl(principal.valor) : "—"} etiqueta={principal?.etiqueta} origem="contratos A e B · set/out de 2028" href="/app/prova/PARTNER_CAPITAL_LIABILITY" grande />
        <Numero rotulo="Remuneração mensal" valor={servico?.valor != null ? brl(servico.valor) : "—"} etiqueta={servico?.etiqueta} origem="todo dia 15, até ago/2028" href="/app/prova/PARTNER_CAPITAL_SERVICE_M" grande />
        <Numero rotulo="Obrigação total" valor="R$ 502.100" etiqueta="VERIFIED" origem="R$ 252.100 de remuneração + R$ 250.000 de principal" grande />
      </Grade>

      <Secao sobretitulo="O que é" titulo="Como o parceiro de compra funciona">
        <div className="prosa max-w-3xl">
          <p>
            O parceiro transfere dinheiro para a conta da empresa; o contrato diz que <strong>100% vai para a compra de lotes</strong> (não
            para estrutura, marketing ou folha). Em troca, recebe um repasse mensal durante 24 meses e, ao fim, o capital de volta.
            Pela leitura dos contratos assinados, a remuneração é <strong>fixa</strong> — um percentual do capital por mês — e não
            depende do lucro do lote.
          </p>
          <p>
            Por isso o portal trata o parceiro de compra como <strong>passivo financeiro</strong>: o principal entra como dívida na ponte do
            valor da empresa e a remuneração entra na DRE como custo, mês a mês. Não é receita, não é capital próprio.
          </p>
        </div>
      </Secao>

      <Secao sobretitulo="Os dois contratos" titulo="O que existe hoje (17/10/2026)">
        <Tabela
          cabecalho={["", "Parceiro A", "Parceiro B"]}
          linhas={[
            ["Capital", <span key="a" className="num">R$ 200.000</span>, <span key="b" className="num">R$ 50.000</span>],
            ["Entrada do dinheiro", "01/09/2026 · 2 PIX de R$ 100.000 (Santander)", "11/08/2026 · 1 PIX (Santander)"],
            ["Remuneração", "4,5% ao mês = R$ 9.000 (3% + 1,5% de fee de originação), fixa", "3% ao mês sobre o capital = R$ 1.500, fixa"],
            ["Prazo", "24 meses; principal integral de volta em até 30 dias após o 24º mês", "24 repasses mensais após 30 dias de estruturação; capital liberado ao fim"],
            ["Primeiro pagamento", "15/10/2026 · R$ 13.500 (pro rata de R$ 300/dia desde a compensação)", "15/09/2026 · R$ 1.600 (com pro rata)"],
            ["Assinatura", "Contrato individual datado de 01/09/2026, assinado por DocuSign", "Envelope DocuSign criado em 11/08/2026, mesmo dia do aporte"],
            ["Conferido no extrato", <Etiqueta key="ea" tipo="VERIFIED" pequena />, <Etiqueta key="eb" tipo="VERIFIED" pequena />],
          ]}
        />
        <p className="text-xs text-muted">
          Os parceiros aparecem como A e B: nome, CPF e conta ficam só nos contratos, fora do portal. O CEO informa que só existem estes
          dois contratos; qualquer novo aporte entra aqui com contrato.
        </p>
      </Secao>

      <Secao sobretitulo="Cronograma" titulo="Quanto sai, e quando">
        <Tabela
          cabecalho={["R$", "2026 (a partir de 15/09)", "2027", "2028", "Total"]}
          linhas={[
            ["Remuneração A", "31.500", "108.000", "76.500", <strong key="ta" className="num">216.000</strong>],
            ["Remuneração B", "6.100", "18.000", "12.000", <strong key="tb" className="num">36.100</strong>],
            [<strong key="r">Remuneração total</strong>, <strong key="r1" className="num">37.600</strong>, <strong key="r2" className="num">126.000</strong>, <strong key="r3" className="num">88.500</strong>, <strong key="r4" className="num">252.100</strong>],
            ["Devolução do principal", "—", "—", <span key="p" className="num">250.000 (set/out)</span>, <strong key="pt" className="num">250.000</strong>],
          ].map((l) => l.map((c, i) => (i === 0 ? c : <span key={i} className="num">{c}</span>)))}
        />
        <p className="text-xs text-muted">
          Calculado pelas cláusulas (30 dias de estruturação, depois todo dia 15). Já pagos e conferidos no Mercado Pago: R$ 1.600 (15/09, B),
          R$ 13.500 (15/10, A) e R$ 1.500 (15/10, B). Datas finais dependem da compensação real e da leitura jurídica da vigência.
        </p>
      </Secao>

      <Secao sobretitulo="Teste de sustentabilidade" titulo="A empresa pagaria os parceiros sem novos aportes?">
        <Grade colunas={3}>
          {comissao.map((c) => {
            const g = gmv.find((x) => x.periodo === c.periodo);
            return (
              <Cartao key={c.periodo} titulo={mesCurto(c.periodo)}>
                <dl className="space-y-1">
                  <div className="flex justify-between gap-2"><dt className="text-muted">Remuneração devida</dt><dd className="num">{brl(DEVIDA[c.periodo] ?? 10500)}</dd></div>
                  <div className="flex justify-between gap-2"><dt className="text-muted">Receita reconhecida pelo app (comissão)</dt><dd className="num">{c.valor != null ? brl(c.valor) : "—"}</dd></div>
                  <div className="flex justify-between gap-2"><dt className="text-muted">Mercadoria vendida (GMV)</dt><dd className="num">{g?.valor != null ? brl(g.valor) : "—"}</dd></div>
                </dl>
                <p className="mt-3 text-xs text-muted">
                  {c.valor != null && c.valor < (DEVIDA[c.periodo] ?? 10500)
                    ? "Pela receita reconhecida, não. Pela margem do varejo, só quando o custo por venda for gravado."
                    : "Pela receita reconhecida, sim."}
                </p>
              </Cartao>
            );
          })}
        </Grade>
        <Aviso tipo="atencao" titulo="Leitura honesta">
          Os repasses de setembro e outubro saíram da conta da empresa em dias em que ela foi abastecida por transferências próprias.
          Enquanto a margem por venda não for medida, o portal não consegue afirmar que o lote pago com o capital do parceiro devolve a
          remuneração; mostra os dois números lado a lado e deixa a conta aberta.
        </Aviso>
      </Secao>

      <Secao sobretitulo="Participação societária" titulo="A venda de 1% — informada, ainda sem contrato">
        <Grade colunas={3}>
          <Numero rotulo="Recebido" valor="R$ 200.000" etiqueta="VERIFIED" origem="Itaú, 24 e 30/09/2026" />
          <Numero rotulo="A receber" valor="R$ 50.000" etiqueta="MANAGEMENT_DATA" origem="contrato será assinado depois" />
          <Numero rotulo="Preço implícito da empresa" valor="R$ 25 mi" etiqueta="MANAGEMENT_DATA" origem="1% por R$ 250 mil · peso zero até o contrato" />
        </Grade>
        <p className="max-w-3xl text-sm text-muted">
          Entrou dinheiro, o comprador está identificado pela administração e o contrato só será assinado quando o restante entrar. Até lá
          o portal guarda a operação como <em>aporte informado</em> e não a usa como preço de transação: 1% minoritário, preço fixado pela
          administração e sem alteração contratual ainda não sustenta um valuation.
        </p>
      </Secao>

      <NotaRevisao
        conselho={conselho}
        itens={[
          "O painel do Parceiro no app diz \"não há retorno garantido, não é investimento\"; o contrato A fixa R$ 9.000/mês e devolução integral do principal. Texto e prática divergem — alinhar com o jurídico antes de nova captação (DEC-22).",
          "O memorando público fala em \"retorno elevado sobre capital investido a cada ciclo\". Esta página não repete a frase.",
          "A linha \"Parceiros de compra (5%)\" saiu dos cenários do app em 02/10/2026 (resultado anual R$ 88.884 → R$ 124.596). O portal usa o custo real dos contratos (DEC-23).",
          "No aporte A, os dois pagadores dos PIX não são o parceiro do contrato (origem dos recursos — advogado). No 1%, R$ 70 mil entraram em 43 depósitos em dinheiro no mesmo dia.",
          "Terceiro envelope na DocuSign \"aguardando 2 pessoas\" há 2 meses: o CEO dispensou; não entra aqui.",
        ]}
      />

      <p className="text-xs text-muted">
        Fontes: contratos A e B (Anexo C15), extratos Santander, Itaú e Mercado Pago (Anexo C13/C15b), informação do CEO em 17/10/2026 (Anexo C14).{" "}
        <Link href="/app/dre" className="underline">Ver o custo na DRE</Link>.
      </p>
    </Pagina>
  );
}
