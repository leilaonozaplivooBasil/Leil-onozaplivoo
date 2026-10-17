import { papelAtual, eConselho } from "@/lib/papel";
import { Aviso, Cartao, Grade, Pagina, Secao, Tabela } from "@/components/ui";

export const dynamic = "force-dynamic";

// Para o investidor: fatores de risco em linguagem direta, com o que reduz cada um.
const FATORES = [
  ["Histórico curto", "A série de dinheiro real do app tem cerca de 2,5 meses (desde 01/08/2026). Projeção e fluxo de caixa descontado carregam incerteza alta.", "Faixa larga declarada; peso baixo do DCF; fechamento mensal oficial para crescer a série."],
  ["Margem por venda não comprovada", "O app não grava o custo por venda; o valor de mercado do estoque foi apagado em setembro. Unit economics fica sem fonte.", "Gravar custo por venda no app (mudança D1, zona vermelha, com ordem do dono). Até lá, margem marcada como premissa."],
  ["Receita sem definição única", "Memorando, declaração ao banco, livros, PGDAS e extratos trazem valores diferentes para o mesmo período.", "Uma definição de receita (DEC-2) e radar de discrepâncias entre as fontes."],
  ["Dependência de aportes", "As obrigações fixas (parceiros R$ 10,5 mil/mês, consórcios, contas vencidas) superam a receita reconhecida pelo app.", "Teste de sustentabilidade permanente: \"pagaria sem novos aportes?\"."],
  ["Concentração", "100% dos pagamentos do app passam por um único gateway; poucas pessoas respondem pela maior parte das entradas bancárias.", "Segundo meio de pagamento; base de clientes mais larga."],
  ["Perímetro e titularidade", "Quadro societário atual e dono do código, da marca e dos domínios não documentados.", "Contrato social atual e contratos de cessão no data room (DEC-1)."],
  ["Varejo em queda", "A planilha do varejo físico/WhatsApp mostra jun R$ 72 mil → jul R$ 11,8 mil → ago R$ 3,4 mil → sem lançamento depois.", "Lançar as vendas do varejo no app ou integrar a planilha; separar os dois negócios na soma das partes."],
  ["Passivos fora do balanço do app", "Saldos de clientes (≈ R$ 45 mil), capital de parceiros (R$ 250 mil), tributos a pagar (R$ 83 mil em 2025), consórcios, contas vencidas (≈ R$ 168 mil lançadas).", "Ponte completa do valor da operação ao valor do sócio, com todos os itens tipo dívida."],
  ["Linguagem de oferta", "\"Sem perda financeira\", comparação com apostas, \"retorno elevado sobre capital\": frases do material público que atraem leitura regulatória.", "Revisão jurídica do texto; este portal usa etiquetas e a frase \"não é oferta\" em toda tela."],
  ["Material inconsistente", "80 ativos × 40 ativos × 23 no banco; 960% × 1.000% de crescimento; \"R$ 40 bi\" com dois significados.", "Números vindos do registro de métricas, com janela e definição no nome."],
];

// Para o conselho: os dez que eu trataria primeiro, com os sinais que exigem advogado e contador.
const PRIMEIRO = [
  ["R-L1", "Origem dos recursos: créditos redondos, 43 depósitos em dinheiro fracionados no mesmo dia (24/09, R$ 70 mil), pagadores diferentes do parceiro. Pode ter explicação legítima; é o padrão que banco, auditor e investidor tratam como alerta.", "Advogado + contador antes de qualquer data room; contrato/recibo e quem pagou para cada lançamento."],
  ["R-L2 / R-L3", "Declaração de faturamento com total que não confere; receitas diferentes para Receita Federal, livros e banco; mudança de regime sem documento.", "Contador independente; medir o passivo fiscal potencial."],
  ["R-F2", "Perímetro: 100% das cotas com uma só sócia no contrato de 08/2025.", "Contrato social atual + titularidade do app, marca e domínios."],
  ["R-V1", "Os sites afirmam o que o código não confirma: TikTok Shop ativo, \"99%\", PHIZ, IA proprietária de preço, Livoo (saiu em 17/10).", "Retirar/reescrever antes de qualquer divulgação nova (Anexo A)."],
  ["R-S1 / R-S5", "Rota do termo de sigilo devolve dados pessoais por id; valuation, CNPJ e PGDAS no pacote público do app.", "Itens S2, S3, S4 da Parte 10, um a um, na janela de deploy."],
  ["R-D1", "Quatro ou cinco \"receitas\" para o mesmo negócio.", "DEC-2 + registry + radar."],
  ["R-D3", "Caixa de R$ 705,9 mil no balanço de 2025 × R$ 42 nas contas conhecidas em 01/01/2026.", "Extratos de 2025 e de todas as contas."],
  ["R-D2", "Série nov/25–mai/26 sem rastro (Nexus antigo inacessível).", "Exportar o Nexus antigo ou assumir a série oficial desde 01/08/2026."],
  ["R-L6 / R-L7", "Documentos pessoais de sócios em pasta compartilhada do Drive.", "Tirar as pastas 08, 12 e 14 do compartilhamento."],
  ["R-F4 / R-L5", "Aportes com repasse prometido e consórcios sem livro próprio.", "Livro de aportes e consórcios com contrato."],
];

export default async function Riscos() {
  const conselho = eConselho(await papelAtual());
  return (
    <Pagina
      sobretitulo="5 minutos"
      titulo="Riscos"
      descricao="Um portal de investidor que esconde risco não vale nada. Aqui estão os fatores que alargam a faixa de valor e o que reduz cada um. Nenhum item é parecer jurídico ou contábil."
    >
      <Secao sobretitulo="Fatores de risco" titulo="Os dez que mais pesam hoje">
        <Tabela
          cabecalho={["Fator", "O que é", "O que reduz"]}
          linhas={FATORES.map((f) => [<strong key="f">{f[0]}</strong>, <span key="o" className="text-muted">{f[1]}</span>, <span key="r" className="text-muted">{f[2]}</span>])}
        />
      </Secao>

      <Secao sobretitulo="Como o risco entra no valuation" titulo="Score de risco e confiança">
        <Grade colunas={2}>
          <Cartao titulo="Score de risco (0–100)">Soma 13 fatores: concentração de receita, cliente e fornecedor; dependência do fundador; regulatório; jurídico; tecnologia; margem; liquidez; dívida; governança; qualidade do dado; concorrência. Hoje ainda não calculado — aparece com a primeira rodada.</Cartao>
          <Cartao titulo="Confiança (0–100)">Mede a robustez da análise (dado, reconciliação, aderência dos comparáveis, estabilidade do resultado), não a probabilidade de “acertar”. Qualidade de dado baixa → faixa mais larga, por regra.</Cartao>
        </Grade>
        <Aviso tipo="regra">O caminho para subir o valor defensável é o mesmo caminho para subir a qualidade do dado: fechar as lacunas e reconciliar as quatro fontes (app, planilha, contabilidade, bancos).</Aviso>
      </Secao>

      {conselho && (
        <Secao sobretitulo="Só para o conselho" titulo="Os dez que eu trataria primeiro, nesta ordem">
          <Tabela
            cabecalho={["#", "Risco", "O que fazer"]}
            linhas={PRIMEIRO.map((r, i) => [<span key="i" className="num">{i + 1} · {r[0]}</span>, <span key="o" className="text-muted">{r[1]}</span>, <span key="f" className="text-muted">{r[2]}</span>])}
          />
          <p className="text-xs text-muted">Mapa completo (P × I, 40+ riscos) na Parte 11 do estudo. Nada foi corrigido por mim: nenhuma linha do app, do banco, dos sites ou da produção foi alterada.</p>
        </Secao>
      )}
    </Pagina>
  );
}
