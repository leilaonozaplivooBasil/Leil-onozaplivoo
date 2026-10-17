import { valoresCarregados } from "@/lib/metricas";
import { papelAtual, eConselho } from "@/lib/papel";
import { Aviso, Cartao, Etiqueta, Grade, NotaRevisao, Pagina, Secao, Tabela } from "@/components/ui";

export const dynamic = "force-dynamic";

const NIVEIS = [
  ["8", "Conselho estratégico", "visão e cultura"],
  ["7", "Mentalidade do CEO", "formação de novos fundadores"],
  ["6", "Diretoria executiva", "convite · resultado · cultura"],
  ["5", "Mentalidade do Diretor", "gestão sistêmica · 3 meses"],
  ["4", "Diretor operacional", "liderança em formação"],
  ["3", "Mentalidade do Executivo", "liderança · 6 meses"],
  ["2", "Licenciado", "gestão comercial · distribuição"],
  ["1", "Vendedor", "produto · vendas · relacionamento"],
];

// Como publicado no site institucional (valuationleilaonozap.com) em 17/10/2026.
const DIRETORIA = [
  ["Luiz Sant'Anna", "CEO, fundador e conselheiro"],
  ["Elohá Sant'Anna", "co-fundadora e conselheira"],
  ["Diogo Archanjo", "diretor de tecnologia, fundador e conselheiro"],
  ["Flávio Monteiro", "diretor jurídico, fundador e conselheiro"],
  ["Luciano Pinheiro", "diretor de captação de investimentos, fundador e conselheiro"],
  ["José Amâncio", "diretor de relacionamento, fundador e conselheiro"],
  ["Luciene Soares", "fundadora e conselheira"],
];
const EM_FORMACAO = ["Financeiro e administrativo", "Operações", "Comercial", "Logística", "Relacionamento", "Comunicação"];

export default async function Governanca() {
  const [{ ultimo }, papel] = await Promise.all([valoresCarregados(), papelAtual()]);
  const conselho = eConselho(papel);
  const lic = ultimo.get("LICENSEES_TOTAL");
  const licRole = ultimo.get("LICENSEES_ROLE");
  const licAtivo = ultimo.get("LICENSEES_ACTIVE_30D");

  return (
    <Pagina
      sobretitulo="30 minutos"
      titulo="Governança e time"
      descricao="Quem lidera, como a carreira é organizada dentro da rede e o que separa fundador de sócio. A narrativa é da administração; as contagens vêm do sistema."
    >
      <Secao sobretitulo="Liderança" titulo="Diretoria executiva e conselho">
        <Tabela cabecalho={["Nome", "Papel"]} linhas={DIRETORIA.map((d) => [d[0], <span key="p" className="text-muted">{d[1]}</span>])} />
        <Grade colunas={2}>
          <Cartao titulo="Futuros diretores operacionais (em formação)">
            <p className="text-muted">Seis pessoas em formação para as áreas de {EM_FORMACAO.join(", ").toLowerCase()} — poderão integrar a diretoria executiva.</p>
          </Cartao>
          <Cartao titulo="Trajetória do fundador">
            <p className="text-muted">
              Fuzileiros Navais; telecomunicações e franquias (Sky, Nextel); varejo próprio; oito anos em marketing de relacionamento com
              liderança de estruturas de mais de 30 mil pessoas; correspondente bancário certificado; operação de captação de
              investimentos; criação da metodologia X-EOS.
            </p>
            <p className="mt-2 text-xs text-muted">
              Os números dessa trajetória (R$ 100 mi originados em crédito, R$ 22 mi captados, R$ 4 mi de valuation da X-EOS) são{" "}
              <Etiqueta tipo="MANAGEMENT_DATA" pequena /> — currículo do fundador, com documento no data room quando houver. Entram no
              valuation só como critério qualitativo, não como ativo da empresa.
            </p>
          </Cartao>
        </Grade>
      </Secao>

      <Secao sobretitulo="Carreira na rede" titulo="Oito níveis — evolução por desenvolvimento, não só por cargo">
        <Tabela
          cabecalho={["Nível", "Nome", "O que forma"]}
          linhas={NIVEIS.map((n) => [<span key="n" className="num font-semibold">{n[0]}</span>, n[1], <span key="o" className="text-muted">{n[2]}</span>])}
        />
        <p className="text-xs text-muted">
          <Etiqueta tipo="VERIFIED" pequena /> A escala bate com o campo de nível de carreira do banco do app (vendedor, licenciado, executivo,
          diretoria, CEO…).
        </p>
        <Grade colunas={3}>
          <Cartao titulo="Licenciados por cargo">
            <p className="num text-2xl font-semibold">{lic?.valor ?? "—"}</p>
            <p className="text-xs text-muted">definição provisória · DEC-3 pendente</p>
          </Cartao>
          <Cartao titulo="Licenciados por papel de acesso">
            <p className="num text-2xl font-semibold">{licRole?.valor ?? "—"}</p>
            <p className="text-xs text-muted">contagem alternativa, para mostrar a divergência</p>
          </Cartao>
          <Cartao titulo="Com acesso nos últimos 30 dias">
            <p className="num text-2xl font-semibold">{licAtivo?.valor ?? "—"}</p>
            <p className="text-xs text-muted">só por login; o app não guarda histórico</p>
          </Cartao>
        </Grade>
        <Aviso tipo="info" titulo="Por que três números">
          “Licenciado” tem seis sentidos no app e quatro contagens possíveis (15, 23, 84 com contexto preenchido, 8 ativos). O site público
          diz “80+ ativos” e “~40 ativos” sem definição. A decisão DEC-3 fixa uma: licenciado = pagou adesão ou comprou o kit; ativo =
          comprou ou indicou nos últimos 30 dias.
        </Aviso>
      </Secao>

      <Secao sobretitulo="Estrutura" titulo="Fundador não é sócio, sócio não é fundador">
        <Grade colunas={2}>
          <Cartao titulo="Fundador">Título que reconhece quem participou da construção na fase inicial: contribuição, construção e alinhamento com a visão. Executivos formados antes do lançamento oficial podem receber o reconhecimento.</Cartao>
          <Cartao titulo="Sócio">Participação societária segue critério de mercado: valuation, investimento e aquisição formal de participação, com alteração contratual.</Cartao>
        </Grade>
        <Cartao titulo="1% do faturamento bruto global ao ecossistema de fundadores">
          <p className="text-muted">
            Política de reconhecimento declarada pela administração. Para o investidor é <strong className="text-foreground">custo</strong>:
            reduz o resultado e muda quem fica com o quê. Entra no modelo como linha própria assim que a base de cálculo for definida
            (receita bruta global? só o app?) — decisão DEC-10.
          </p>
        </Cartao>
        <Cartao titulo="Quadro societário">
          <p className="text-muted">
            O contrato social disponível é de 12/08/2025. O quadro atual, com as participações de hoje e a titularidade do código, da marca
            e dos domínios, ainda não está no data room — é o primeiro item da lista de pendências.{" "}
            <Etiqueta tipo="NAO_DISPONIVEL" pequena />
          </p>
        </Cartao>
      </Secao>

      <Secao sobretitulo="Cultura" titulo="A empresa como escola">
        <div className="prosa max-w-3xl">
          <p>
            A administração descreve a Leilão NoZap como uma escola de vendas, liderança, gestão, tecnologia e empreendedorismo, com três
            trilhas internas — Mentalidade do Executivo, do Diretor e do CEO — sobre a metodologia X-EOS. A tese: empresas crescem na
            velocidade dos seus líderes, não dos seus sistemas.
          </p>
          <p>
            Isso é narrativa e cultura, não métrica. O portal não atribui valor em reais a metodologia, trilhas ou “Vale do Recreio”; eles
            entram no scorecard qualitativo do valuation e no memorando.
          </p>
        </div>
      </Secao>

      <NotaRevisao
        conselho={conselho}
        itens={[
          "No contrato social de 12/08/2025 as 500.000 cotas estão em nome de uma única sócia; o CEO e os demais \"fundadores\" não aparecem. Falta o quadro atual (DEC-1).",
          "Os nomes da diretoria vêm do site público; nenhum dado pessoal além do nome e do papel entra no portal.",
          "\"Capital intelectual do fundador\" saiu da composição do valuation (Anexo A, item 4) e veio para esta página.",
        ]}
      />
    </Pagina>
  );
}
