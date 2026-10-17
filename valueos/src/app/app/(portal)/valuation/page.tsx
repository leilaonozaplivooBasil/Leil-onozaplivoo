import Link from "next/link";
import { valoresCarregados } from "@/lib/metricas";
import { papelAtual, eConselho } from "@/lib/papel";
import { Aviso, Cartao, Etiqueta, Grade, NotaRevisao, Pagina, Secao, SeloReferencia, Tabela, brl } from "@/components/ui";

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

// Valuation: a referência do fundador fica à vista como referência; o independente só existe com método travado.
export default async function Valuation() {
  const [{ ultimo }, papel] = await Promise.all([valoresCarregados(), papelAtual()]);
  const conselho = eConselho(papel);
  const v = (id: string) => ultimo.get(id);
  const estoque = v("INVENTORY_AT_COST");
  const carteira = v("WALLET_LIABILITY_TOTAL");
  const parceiros = v("PARTNER_CAPITAL_LIABILITY");
  const vencidas = v("EXPENSES_OVERDUE");
  const loc = v("TECH_LOC");

  return (
    <Pagina
      sobretitulo="30 minutos"
      titulo="Valuation"
      descricao="Duas coisas diferentes: a referência que o fundador declara e o valor independente que o sistema vai calcular com método fixado antes de olhar o resultado. Hoje só a primeira existe."
    >
      <Grade colunas={2}>
        <Cartao>
          <p className="text-xs uppercase tracking-widest text-muted">Referência do fundador</p>
          <p className="num mt-2 text-4xl font-semibold">R$ 25.000.000</p>
          <div className="mt-2"><SeloReferencia /></div>
          <p className="mt-3 text-xs text-muted">
            Publicada nos dois sites e usada na venda de 1%. Nenhum método é mostrado: nem múltiplo, nem fluxo de caixa. Aqui ela é o
            ponto de comparação, lacrado com impressão digital, contra o qual o valor independente será explicado — nunca a manchete.
          </p>
        </Cartao>
        <Cartao destaque>
          <p className="text-xs uppercase tracking-widest text-muted">Valuation independente</p>
          <p className="mt-2 text-4xl font-semibold">Não calculado</p>
          <div className="mt-2"><Etiqueta tipo="NAO_DISPONIVEL" pequena /></div>
          <p className="mt-3 text-xs text-muted">
            Sai como faixa (baixo · central · alto), com confiança e score de risco, só depois de: metodologia v1.0 aprovada, pesos
            registrados com hash, primeiro fechamento oficial e decisão sobre o perímetro avaliado. A primeira rodada é privada (conselho).
          </p>
        </Cartao>
      </Grade>

      <Secao sobretitulo="Antes de qualquer número" titulo="O que está sendo avaliado">
        <Grade colunas={3}>
          <Cartao titulo="A. Compras Full Comércio Ltda">A empresa com CNPJ, contas, contabilidade e o nome fantasia Leilão NoZap. É o perímetro padrão enquanto a titularidade dos outros ativos não for documentada.</Cartao>
          <Cartao titulo="B. Ecossistema">A + app, marca, rede, ComparAI e parcerias. Só faz sentido se um único CNPJ (ou contrato) reunir esses ativos.</Cartao>
          <Cartao titulo="C. Só a plataforma">Código, marca, domínios e rede de licenciados. Exige saber quem é o dono de cada um.</Cartao>
        </Grade>
        <Aviso tipo="atencao" titulo="Decisão pendente (DEC-1)">
          O contrato social disponível é de 12/08/2025; o quadro societário atual e a titularidade do código, da marca e dos domínios ainda
          não estão no data room. Avaliar o perímetro errado invalida o resto.
        </Aviso>
      </Secao>

      <Secao sobretitulo="Metodologia v1.0 · proposta" titulo="Nove métodos, pesos fixados antes do resultado">
        <Tabela cabecalho={["Método", "Peso", "Por quê"]} linhas={METODOS.map((m) => [m[0], <span key="p" className="num font-semibold">{m[1]}</span>, <span key="j" className="text-muted">{m[2]}</span>])} />
        <div className="prosa max-w-3xl">
          <p>
            Um método sem dado suficiente tem <strong>peso zero e aparece como “não calculado”</strong> — nunca como valor baixo. Os pesos
            mudam com o estágio da empresa, mas <strong>nunca depois de ver o resultado</strong>: mudar peso é versão nova da metodologia,
            com data, autor, motivo e impacto registrados.
          </p>
          <p>
            Cada premissa entra como <strong>faixa</strong>, não como ponto; milhares de sorteios produzem a distribuição de valor por método;
            a mistura pelos pesos dá a faixa final (percentis 25, 50 e 75). Qualidade de dado baixa alarga a faixa por regra.
          </p>
        </div>
      </Secao>

      <Secao sobretitulo="Do valor da operação ao valor do sócio" titulo="A ponte — o que entra e o que sai">
        <Tabela
          cabecalho={["Item", "Sinal", "Hoje", "Etiqueta"]}
          linhas={[
            ["Valor da operação (EV) — triangulação dos métodos", "+", "não calculado", <Etiqueta key="1" tipo="NAO_DISPONIVEL" pequena />],
            ["Caixa verificado", "+", "extratos de 2025 e de todas as contas não disponíveis", <Etiqueta key="2" tipo="NAO_DISPONIVEL" pequena />],
            ["Estoque a custo", "+", <span key="e" className="num">{estoque?.valor != null ? brl(estoque.valor) : "—"}</span>, <Etiqueta key="3" tipo={estoque?.etiqueta ?? "NAO_DISPONIVEL"} pequena />],
            ["Cotas de consórcio no nome da empresa, líquidas do saldo devedor", "+", "21 cartas (2 contempladas); saldo devedor a informar", <Etiqueta key="4" tipo="MANAGEMENT_DATA" pequena />],
            ["Saldos de clientes e rede (carteira, comissões, crédito de vendedor)", "−", <span key="c" className="num">{carteira?.valor != null ? brl(carteira.valor) : "—"}</span>, <Etiqueta key="5" tipo={carteira?.etiqueta ?? "NAO_DISPONIVEL"} pequena />],
            ["Capital dos parceiros de compra (principal)", "−", <span key="p" className="num">{parceiros?.valor != null ? brl(parceiros.valor) : "—"}</span>, <Etiqueta key="6" tipo={parceiros?.etiqueta ?? "NAO_DISPONIVEL"} pequena />],
            ["Remuneração dos parceiros acima do custo de mercado (valor presente)", "−", "a calcular na metodologia", <Etiqueta key="7" tipo="NAO_DISPONIVEL" pequena />],
            ["Despesas vencidas em aberto (lançamento do app)", "−", <span key="v" className="num">{vencidas?.valor != null ? brl(vencidas.valor) : "—"}</span>, <Etiqueta key="8" tipo={vencidas?.etiqueta ?? "NAO_DISPONIVEL"} pequena />],
            ["Tributos e encargos a pagar", "−", "R$ 83,2 mil + R$ 85,0 mil em 31/12/2025; situação atual desconhecida", <Etiqueta key="9" tipo="MANAGEMENT_DATA" pequena />],
            ["Obrigação do 1% do faturamento bruto aos fundadores", "−", "base de cálculo a definir (DEC-10)", <Etiqueta key="10" tipo="NAO_DISPONIVEL" pequena />],
            ["= Valor do equity × participação de cada sócio", "", "contrato social atual não disponível", <Etiqueta key="11" tipo="NAO_DISPONIVEL" pequena />],
          ]}
        />
      </Secao>

      <Secao sobretitulo="O que já se consegue dizer" titulo="Sem número — mas com direção">
        <Grade colunas={2}>
          <Cartao titulo="O que sustenta valor">
            <ul className="list-disc space-y-1 pl-5 text-muted">
              <li>Motor de leilão maduro e em uso: em outubro, 16 leilões encerrados, 119 lances, 24 licitantes.</li>
              <li>Pagamentos conciliados ao centavo entre app, Mercado Pago e bancos (jul–out/2026).</li>
              <li>Código próprio de porte: <span className="num">{loc?.valor != null ? loc.valor.toLocaleString("pt-BR") : "—"}</span> linhas medidas no repositório.</li>
              <li>Rede em formação, metodologia de formação e marca com história (narrativa da administração).</li>
            </ul>
          </Cartao>
          <Cartao titulo="O que tira valor hoje">
            <ul className="list-disc space-y-1 pl-5 text-muted">
              <li>Margem por venda não comprovada: o app não grava o custo por venda.</li>
              <li>Receita sem definição única e série histórica sem rastro no sistema.</li>
              <li>Dependência de aportes para pagar obrigações fixas (parceiros, consórcios, contas vencidas).</li>
              <li>Perímetro, quadro societário e titularidade dos ativos não documentados.</li>
            </ul>
          </Cartao>
        </Grade>
        <Aviso tipo="regra" titulo="Regras que não mudam">
          Nenhum método é escolhido por dar valor maior. Nunca afirmaremos que o sistema é “mais preciso que humanos” antes de dezenas de
          transações reais comparadas. O resultado é defensável e rastreável; para uma transação, um laudo de terceiro continua sendo o
          padrão — o portal prepara tudo para esse terceiro refazer a conta em horas.
        </Aviso>
      </Secao>

      <Secao sobretitulo="Comparáveis candidatos" titulo="Ponto de partida de pesquisa — nada aqui é número final">
        <Tabela
          cabecalho={["Tipo", "Candidato", "Por que é parecido"]}
          linhas={[
            ["Listada (EUA)", "Liquidity Services", "marketplaces de leilão de excedente e devolução de consumo"],
            ["Listada (Brasil)", "Enjoei", "recommerce brasileiro de pequeno porte; sob pressão na bolsa"],
            ["Listadas (EUA)", "ThredUp · The RealReal · eBay · Copart · RB Global", "recommerce e leilões — referência de múltiplo, com desconto"],
            ["Teto", "Mercado Livre · Magazine Luiza", "grande porte; referência de teto, não comparação direta"],
            ["Transação", "Naver × Poshmark (2022)", "recommerce; ≈ 3,7× a receita — outro porte, outro mercado, outro momento"],
          ]}
        />
      </Secao>

      {conselho && (
        <Secao sobretitulo="Só para o conselho" titulo="Números que já circulam — e não são valuation do motor">
          <Tabela
            cabecalho={["Número", "Onde", "Método", "Leitura"]}
            linhas={[
              ["R$ 25.000.000", "sites e documento oficial do app", "nenhum visível", "referência do fundador"],
              ["R$ 373.788 – R$ 747.576", "painel do Parceiro (código do app)", "3× a 6× o lucro anual \"apurado\" (R$ 124.596)", "ilustrativo; o próprio código diz \"não é laudo\"; base fiscal de outra receita"],
              ["R$ 7,97 mi – R$ 15,9 mi", "painel do Parceiro (código do app)", "mesmos múltiplos sobre lucro projetado com R$ 1 mi/mês", "cenário, não valor atual"],
            ]}
          />
          <NotaRevisao
            conselho
            itens={[
              "Esta primeira rodada não pode ser cega: o R$ 25 mi já circulou. O modo cego (referência lacrada por hash, aberta só depois) vale para as próximas rodadas e para qualquer terceiro.",
              "A distância entre os três valores que circulam (R$ 25 mi × R$ 0,37–0,75 mi × R$ 8–16 mi) é o primeiro ponto que um investidor levanta — por isso a ponte, não a defesa do número.",
              "Palavras retiradas do site público nesta versão: \"valuation conservador\", \"baseado em ativos reais\". \"Capital intelectual do fundador\" foi movido para Governança: é currículo, não ativo da empresa.",
            ]}
          />
        </Secao>
      )}

      <p className="text-xs text-muted">
        Metodologia completa na Parte 8 do estudo (Valuation Engine). <Link href="/app/riscos" className="underline">Ver os riscos que alargam a faixa</Link>.
      </p>
    </Pagina>
  );
}
