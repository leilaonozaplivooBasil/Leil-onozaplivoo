import Link from "next/link";
import { valoresCarregados } from "@/lib/metricas";
import { papelAtual, eConselho } from "@/lib/papel";
import { mesCurto } from "@/lib/etiquetas";
import { Aviso, Barras, Cartao, Etiqueta, Grade, Legenda, NotaRevisao, Numero, Pagina, Secao, SeloReferencia, Tabela, brl, brlMil, inteiro } from "@/components/ui";

export const dynamic = "force-dynamic";

const CAPITULOS = [
  ["carta", "Carta do fundador"],
  ["resumo", "Resumo executivo"],
  ["problema", "1 · O problema"],
  ["oportunidade", "2 · A oportunidade"],
  ["solucao", "3 · A solução"],
  ["tecnologia", "4 · Tecnologia"],
  ["modelo", "5 · Modelo de negócio"],
  ["tracao", "6 · Tração e validação"],
  ["governanca", "7 · Governança e cultura"],
  ["barreiras", "8 · O que não se copia"],
  ["valuation", "9 · Valuation"],
  ["roadmap", "10 · Roadmap"],
  ["visao", "11 · Visão 2035"],
  ["investimento", "12 · Oportunidade de investimento"],
];

// Série do memorando público (nov/25–mai/26): dado da administração, sem rastro no sistema.
const SERIE_MEMORANDO = [
  ["nov/25", 16336], ["dez/25", 26358], ["jan/26", 27034], ["fev/26", 17191], ["mar/26", 23000], ["abr/26", 60374], ["mai/26", 181000],
] as const;
// Planilha do varejo (Nexus), lançamento manual.
const SERIE_NEXUS = [["jun/26", 72000], ["jul/26", 11800], ["ago/26", 3400]] as const;

export default async function Memorando() {
  const [{ ultimo, serie }, papel] = await Promise.all([valoresCarregados(), papelAtual()]);
  const conselho = eConselho(papel);
  const v = (id: string) => ultimo.get(id);
  const gmvSerie = serie.get("GMV_GOODS") ?? [];
  const entradasSerie = serie.get("CASH_IN_GROSS") ?? [];
  const loc = v("TECH_LOC");
  const licCargo = v("LICENSEES_TOTAL");
  const licRole = v("LICENSEES_ROLE");
  const licAtivo = v("LICENSEES_ACTIVE_30D");
  const contas = v("USERS_REGISTERED");
  const pagantes = v("CUSTOMERS_PAYING_90D");
  const recorrentes = v("BUYERS_REPEAT");
  const leiloes = v("AUCTIONS_PRODUCT_ENDED");
  const vencedores = v("AUCTIONS_WITH_WINNER");
  const lances = v("BIDS_COUNT");
  const licitantes = v("BIDDERS_DISTINCT");
  const estoque = v("INVENTORY_AT_COST");
  const comissao = v("REVENUE_COMMISSION_RETAINED");
  const fees = v("REVENUE_FEES");
  const periodo = gmvSerie.at(-1) ? mesCurto(gmvSerie.at(-1)!.periodo) : "—";

  return (
    <Pagina
      sobretitulo="1 minuto para a tese · 30 para o documento inteiro"
      titulo="Memorando de investimento"
      descricao={
        <>
          Versão revisada em 17/10/2026. A narrativa é da administração e foi mantida; os números ganharam etiqueta, origem e, onde o
          sistema mede, o valor medido ao lado do declarado. O que não tinha base saiu.
        </>
      }
    >
      <Legenda />
      <nav aria-label="Capítulos" className="flex flex-wrap gap-2 text-xs">
        {CAPITULOS.map((c) => (
          <a key={c[0]} href={`#${c[0]}`} className="rounded-full border border-border px-3 py-1 text-muted hover:border-accent hover:text-foreground">
            {c[1]}
          </a>
        ))}
      </nav>

      <Secao id="carta" sobretitulo="Carta do fundador" titulo="Não estamos construindo apenas uma empresa. Estamos construindo uma infraestrutura.">
        <div className="prosa max-w-3xl">
          <p>
            Ao longo de mais de duas décadas empreendendo, atuei em ambientes completamente diferentes entre si — e cada um deles contribuiu
            para a visão que deu origem à Leilão NoZap. A trajetória começou no Corpo de Fuzileiros Navais, onde aprendi disciplina,
            liderança e execução sob pressão. Passei por franquias, telecomunicações e varejo (Sky, Nextel), empreendi em restaurante
            próprio, e durante cerca de oito anos atuei no marketing de relacionamento, chegando à posição máxima de liderança em duas
            organizações consolidadas nacionalmente, com estruturas que alcançaram mais de 30 mil pessoas em mais de vinte estados.
          </p>
          <p>
            Depois mergulhei no mercado financeiro como correspondente bancário certificado, atuando em operações estruturadas de crédito;
            mais tarde construí uma operação de captação de investimentos totalmente digital, com uma equipe de cerca de oito pessoas. Dessa
            jornada nasceu a X-EOS, metodologia própria de desenvolvimento humano e expansão organizacional.
          </p>
          <blockquote>Escala não é consequência do tamanho da equipe. Escala é consequência da qualidade do sistema.</blockquote>
          <p>
            Ao estudar os mercados mais resilientes das próximas décadas, encontrei uma verdade simples: compra e venda existem desde que o
            mundo é mundo. Ao mesmo tempo, o crescimento do e-commerce gerava milhões de devoluções e estoques parados — e faltava uma
            infraestrutura eficiente conectando todas as partes. A Leilão NoZap nasceu para transformar riqueza parada em liquidez:
            estoques em receita, tecnologia em prosperidade, consumidores em empreendedores.
          </p>
          <p>
            Acreditamos que o principal ativo do mundo não é a tecnologia nem o capital: é o ser humano. Por isso investimos na formação de
            líderes e acreditamos que toda empresa deveria funcionar também como uma escola. A Leilão NoZap é a convergência de tudo o que
            aprendi — militarismo, empreendedorismo, tecnologia, mercado financeiro, desenvolvimento humano, distribuição inteligente. Estamos
            apenas no começo.
          </p>
          <p className="text-xs">— Luiz Sant’Anna, fundador e CEO</p>
        </div>
        <Aviso tipo="info">
          Os números da trajetória pessoal (R$ 100 mi originados em crédito, R$ 22 mi captados, R$ 4 mi de valuation da X-EOS, 30 mil pessoas)
          são <Etiqueta tipo="MANAGEMENT_DATA" pequena /> e ficam em <Link href="/app/governanca" className="underline">Governança e time</Link>: são
          currículo do fundador, não ativo da empresa.
        </Aviso>
        <NotaRevisao conselho={conselho} itens={["Carta mantida na íntegra em espírito, abreviada. Nenhum número dela entra no valuation (Anexo A, item 43)."]} />
      </Secao>

      <Secao id="resumo" sobretitulo="Resumo executivo" titulo="Infraestrutura brasileira de recommerce, distribuição inteligente e desenvolvimento humano">
        <div className="prosa max-w-3xl">
          <p>
            A Leilão NoZap é uma empresa brasileira de tecnologia, recommerce e distribuição criada para transformar estoques parados,
            devoluções de e-commerce, excedentes industriais e oportunidades comerciais em liquidez distribuída, por meio de uma
            infraestrutura própria que conecta fabricantes, distribuidores, vendedores, licenciados e consumidores finais — com o WhatsApp
            como canal principal.
          </p>
          <p>
            <strong>Nossa tese:</strong> o Brasil não sofre por falta de produtos, de consumidores nem de empreendedores. Sofre por falta de
            conexão eficiente entre essas partes. A Leilão NoZap existe para resolver essa ineficiência.
          </p>
        </div>
        <Grade colunas={3}>
          <Cartao titulo="Referência de valor">
            <p className="num text-2xl font-semibold">R$ 25 mi</p>
            <div className="mt-1"><SeloReferencia /></div>
            <p className="mt-2 text-xs text-muted">Declarada pelo fundador; o valor independente ainda não foi calculado. <Link href="/app/valuation" className="underline">Ver metodologia</Link>.</p>
          </Cartao>
          <Cartao titulo="Meta para dezembro de 2026">
            <p className="num text-2xl font-semibold">R$ 1 mi/mês</p>
            <div className="mt-1"><Etiqueta tipo="FORECAST" pequena /></div>
            <p className="mt-2 text-xs text-muted">300 licenciados ativos · 8 lojas físicas · 1 centro de distribuição · lançamento oficial. <Link href="/app/roadmap" className="underline">Plano × realizado</Link>.</p>
          </Cartao>
          <Cartao titulo="Hoje, no sistema ({periodo})">
            <p className="num text-2xl font-semibold">{gmvSerie.at(-1)?.valor != null ? brl(gmvSerie.at(-1)!.valor!) : "—"}</p>
            <div className="mt-1"><Etiqueta tipo="VERIFIED" pequena /></div>
            <p className="mt-2 text-xs text-muted">Mercadoria vendida e paga no app no mês, sem depósitos. <Link href="/app/prova/GMV_GOODS" className="underline">Prova</Link>.</p>
          </Cartao>
        </Grade>
      </Secao>

      <Secao id="problema" sobretitulo="Capítulo 1" titulo="O problema: a maior ineficiência oculta do comércio brasileiro">
        <div className="prosa max-w-3xl">
          <p>
            Durante décadas o varejo foi construído para vender — mas ninguém construiu uma infraestrutura eficiente para lidar com o que
            sobra. Produtos devolvidos, estoques excedentes, mercadorias paradas, fabricantes sem distribuição, consumidores sem acesso,
            empreendedores sem oportunidade: todos coexistem no mesmo sistema, sem conexão.
          </p>
          <p>
            Quanto mais vendas acontecem, mais devoluções acontecem; grande parte desses produtos tem valor comercial, mas não tem liquidez.
            Quando um produto para de girar, deixa de ser estoque e vira custo: ocupa espaço, consome capital, reduz margem. O problema é
            ainda mais grave para pequenas e médias empresas, com menos capital, tecnologia e canais.
          </p>
          <p>
            O fabricante produz, mas nem sempre consegue vender: domina a produção, não a distribuição. Do outro lado, milhões de brasileiros
            procuram produtos, renda e a possibilidade de empreender — e encontram barreiras de estoque, capital, tecnologia e acesso.{" "}
            <strong>O produto existe. O consumidor existe. O empreendedor existe. A conexão não.</strong>
          </p>
          <blockquote>Se milhões de produtos são devolvidos todos os anos, para onde eles vão?</blockquote>
        </div>
      </Secao>

      <Secao id="oportunidade" sobretitulo="Capítulo 2" titulo="A oportunidade: a próxima transformação acontece na redistribuição">
        <div className="prosa max-w-3xl">
          <p>
            As maiores empresas da última década não criaram mercados: identificaram mudanças de comportamento antes dos demais. O Uber não
            criou a mobilidade; o Airbnb não criou a hospedagem; o WhatsApp não criou a comunicação; o Mercado Livre não criou o comércio.
            Cada um transformou a forma de acesso. A Leilão NoZap acredita que a próxima grande transformação será a redistribuição
            inteligente de produtos, ativos e oportunidades — o quarto pilar do varejo, depois de produzir, distribuir e vender.
          </p>
          <p>
            <strong>Por que agora:</strong> a inteligência artificial eliminou gargalos de mão de obra (classificação, precificação,
            atendimento); o e-commerce amadureceu e as devoluções cresceram com ele; o consumidor consolidou o hábito de comprar online; e
            a pressão econômica faz consumidores buscarem economia, empresas buscarem liquidez e fabricantes buscarem distribuição. O Brasil
            soma a isso a presença do WhatsApp, a cultura de indicação e a sensibilidade a oportunidade.
          </p>
        </div>
        <Cartao titulo="Tamanho de mercado citado pela administração">
          <Tabela
            cabecalho={["Número", "Onde aparece", "Etiqueta"]}
            linhas={[
              ["E-commerce Brasil: R$ 185 bi+ por ano", "página de valuation", <Etiqueta key="1" tipo="MANAGEMENT_DATA" pequena />],
              ["Devoluções / logística reversa: R$ 40 bi+", "página de valuation", <Etiqueta key="2" tipo="MANAGEMENT_DATA" pequena />],
              ["Estoques excedentes: R$ 25 bi+ represados", "página de valuation", <Etiqueta key="3" tipo="MANAGEMENT_DATA" pequena />],
              ["Recommerce: +35% ao ano", "página de valuation", <Etiqueta key="4" tipo="MANAGEMENT_DATA" pequena />],
              ["WhatsApp: 147 milhões de usuários no Brasil", "página de valuation", <Etiqueta key="5" tipo="MANAGEMENT_DATA" pequena />],
            ]}
          />
          <p className="mt-2 text-xs text-muted">Nenhum traz fonte, ano ou metodologia. Entram aqui como declarados; viram verificados quando a fonte for anexada ao data room.</p>
        </Cartao>
        <NotaRevisao conselho={conselho} itens={["\"R$ 40 bi\" aparece com dois significados no site (devoluções anuais e capital represado) — item 35.", "Retirados: \"a única plataforma brasileira que conecta esses mercados\" e \"o líder nacional ainda não existe\" (superlativos sem prova — item 37)."]} />
      </Secao>

      <Secao id="solucao" sobretitulo="Capítulo 3" titulo="A solução: não construímos um marketplace. Construímos uma infraestrutura.">
        <div className="prosa max-w-3xl">
          <p>
            Enquanto a maioria das empresas resolve uma etapa, a Leilão NoZap conecta a cadeia: fabricante → análise de lotes → marketplace →
            rede de licenciados, vendedores, lojas e leilão → consumidor final → recompra e nova redistribuição. Mais canais, mais velocidade,
            mais liquidez.
          </p>
          <p>
            <strong>WhatsApp first.</strong> O Brasil já escolheu sua plataforma de comunicação; as pessoas compram, negociam e indicam pelo
            WhatsApp. A Leilão NoZap foi construída respeitando essa realidade — usa o WhatsApp como canal de relacionamento e distribuição,
            sem depender dele. A indicação continua sendo a forma mais poderosa de aquisição; a infraestrutura transforma relacionamento em
            distribuição.
          </p>
          <p>
            <strong>Rede de licenciados e vendedores.</strong> Cada licenciado é um ponto de expansão, com treinamento, tecnologia, produtos e
            suporte. Os vendedores formam a segunda camada: qualquer pessoa pode comercializar usando a infraestrutura, sem estoque e sem
            estrutura própria.
          </p>
          <p>
            <strong>Leilão inteligente.</strong> Transforma a compra em experiência: se vencer, compra abaixo do mercado; se não vencer, o
            saldo do lance volta para a carteira. O motor está em operação no app.
          </p>
          <p>
            <strong>Análise de lotes e ComparAI.</strong> Após a compra de um lote, a plataforma lê a planilha, classifica, estima valor de
            mercado, projeta margem, importa imagens e gera anúncios. A ComparAI é a camada de inteligência de precificação e comparação.
          </p>
        </div>
        <Grade colunas={4}>
          <Numero rotulo="Leilões encerrados (mês)" valor={leiloes?.valor != null ? inteiro(leiloes.valor) : "—"} etiqueta={leiloes?.etiqueta} origem={`${vencedores?.valor ?? "—"} com vencedor`} href="/app/prova/AUCTIONS_PRODUCT_ENDED" />
          <Numero rotulo="Lances (mês)" valor={lances?.valor != null ? inteiro(lances.valor) : "—"} etiqueta={lances?.etiqueta} origem={`${licitantes?.valor ?? "—"} licitantes distintos`} href="/app/prova/BIDS_COUNT" />
          <Numero rotulo="Lotes recebidos" valor="40" etiqueta="VERIFIED" origem="abr–out/2026, com itens e produtos gerados" />
          <Numero rotulo="ComparAI" valor="em uso limitado" etiqueta="VERIFIED" origem="117 consultas em cache; 1 produto com valor de mercado" />
        </Grade>
        <NotaRevisao
          conselho={conselho}
          itens={[
            "\"Leilão Inteligente 99% concluído\" → substituído pelos números reais do motor (está em operação).",
            "\"Live Commerce — Livoo Live: integração 99%, sociedade em fase final\" → retirado: a parceria foi encerrada em 17/10/2026 (DIR-258). O motor \"live commerce\" fica como ideia futura, sem número.",
            "\"TikTok Shop ativo e funcional\" → retirado: não há integração no código, só um link de perfil (item 20b).",
            "\"Centenas de produtos em minutos\" → sem medição de tempo; mantido como descrição do fluxo.",
          ]}
        />
      </Secao>

      <Secao id="tecnologia" sobretitulo="Capítulo 4" titulo="Tecnologia: a infraestrutura invisível que sustenta a escala">
        <div className="prosa max-w-3xl">
          <p>
            A maioria das empresas constrói tecnologia para vender; a Leilão NoZap constrói tecnologia para escalar. Empresas quebram porque
            vendem mais do que conseguem entregar — por isso a decisão de construir primeiro a infraestrutura e depois acelerar.
          </p>
        </div>
        <Grade colunas={3}>
          <Cartao titulo="Marketplace próprio">Centro da operação: distribui os produtos e conecta fornecedores, licenciados, vendedores e consumidores. Principal canal de liquidez.</Cartao>
          <Cartao titulo="Licenciamento">Cada licenciado recebe tecnologia, treinamento, metodologia, produtos e suporte — expansão sem a estrutura tradicional.</Cartao>
          <Cartao titulo="CRM comercial">Leads, clientes, licenciados, vendedores e histórico num só lugar.</Cartao>
          <Cartao titulo="Financeiro e comissionamento">Recebimentos, pagamentos, carteira dos clientes e a lógica de distribuição da rede, automatizada.</Cartao>
          <Cartao titulo="Leilão e análise de lotes">Motor de lances com reserva de saldo; importador de lotes com classificação e anúncios.</Cartao>
          <Cartao titulo="Painel executivo">Vendas, indicadores, licenciados e operação em tempo real.</Cartao>
        </Grade>
        <Grade colunas={3}>
          <Numero rotulo="Linhas de código (medidas)" valor={loc?.valor != null ? inteiro(loc.valor) : "—"} etiqueta={loc?.etiqueta} origem="2.033 arquivos, sem testes · 17/10/2026" href="/app/prova/TECH_LOC" />
          <Numero rotulo="Linhas de código (site público)" valor="178.000" etiqueta="MANAGEMENT_DATA" origem="883 arquivos · sem data de medição" />
          <Numero rotulo="Propriedade" valor="código próprio" etiqueta="MANAGEMENT_DATA" origem="sobre infraestrutura de mercado (Supabase, Vercel, Mercado Pago)" />
        </Grade>
        <Aviso tipo="info">
          “100% proprietária” é impreciso: o app usa Supabase, Vercel, Mercado Pago, Melhor Envio, Z-API, provedores de IA e bibliotecas
          abertas. “Código-fonte próprio sobre infraestrutura de mercado” é verdadeiro e resiste melhor a uma auditoria. Linha de código não é
          valor: a medição inclui ~37 mil linhas de legado e ~18 mil de SQL; a titularidade do código (quem escreveu, contratos) vai ao data room.
        </Aviso>
      </Secao>

      <Secao id="modelo" sobretitulo="Capítulo 5" titulo="Modelo de negócio: uma empresa, múltiplos motores de receita">
        <div className="prosa max-w-3xl">
          <p>
            Uma das maiores fragilidades das empresas tradicionais é depender de uma única fonte de faturamento. A Leilão NoZap foi desenhada
            para crescer por vários motores ao mesmo tempo. A coluna da direita diz o que o sistema já registra como dinheiro.
          </p>
        </div>
        <Tabela
          cabecalho={["Motor", "O que é", "Receita registrada no app"]}
          linhas={[
            ["01 Venda de produtos", "devoluções, oportunidades, fabricantes — loja e catálogo", <span key="1"><Etiqueta tipo="VERIFIED" pequena /> sim · GMV_GOODS</span>],
            ["02 Licenciamento", "adesões e expansão territorial", <span key="2"><Etiqueta tipo="VERIFIED" pequena /> {fees?.valor ? brl(fees.valor) : "R$ 0"} no mês · 1 adesão paga no histórico</span>],
            ["03 Marketplace", "comissão retida sobre a movimentação", <span key="3"><Etiqueta tipo="VERIFIED" pequena /> sim · {comissao?.valor != null ? brl(comissao.valor) : "—"} no mês</span>],
            ["04 Leilão", "arremates pagos", <span key="4"><Etiqueta tipo="VERIFIED" pequena /> sim · GMV_AUCTION</span>],
            ["05 Lojas físicas", "exposição e liquidez local", <span key="5"><Etiqueta tipo="NAO_DISPONIVEL" pequena /> sem venda por loja registrada</span>],
            ["06 Análise de lotes", "percentual e assinaturas futuras", <span key="6"><Etiqueta tipo="NAO_DISPONIVEL" pequena /> planejado</span>],
            ["07 Serviços a fornecedores", "infraestrutura para fabricantes parceiros", <span key="7"><Etiqueta tipo="NAO_DISPONIVEL" pequena /> planejado</span>],
            ["08 Live commerce", "vendas ao vivo", <span key="8"><Etiqueta tipo="NAO_DISPONIVEL" pequena /> ideia futura</span>],
            ["09 ComparAI", "inteligência de precificação", <span key="9"><Etiqueta tipo="NAO_DISPONIVEL" pequena /> sem linha de receita própria</span>],
          ]}
        />
        <Grade colunas={3}>
          <Cartao titulo="Aquisição de lotes">
            <p className="text-muted">Site: “compra a 20–25% do valor de mercado”. Banco (34 lotes): custo = 3,7% do valor de mercado cadastrado. Os dois números precisam do preço de venda realizado para valer.</p>
            <div className="mt-2"><Etiqueta tipo="MANAGEMENT_DATA" pequena /></div>
          </Cartao>
          <Cartao titulo="Preço ao consumidor">
            <p className="text-muted">Site: “vende 20% abaixo do mercado”. Só 1 de 1.469 produtos em estoque tem valor de mercado gravado — não verificável hoje.</p>
            <div className="mt-2"><Etiqueta tipo="NAO_DISPONIVEL" pequena /></div>
          </Cartao>
          <Cartao titulo="Comissões da rede">
            <p className="text-muted">Site: “30% para licenciados”. Código do app: licenciado 3–6%, vendedor 10%, loja física ~11%, distribuidor até 20%, indicação 10%, leilão retido ~24,5%. Não há um 30% único.</p>
            <div className="mt-2"><Etiqueta tipo="VERIFIED" pequena /></div>
          </Cartao>
        </Grade>
        <NotaRevisao conselho={conselho} itens={["\"Receita recorrente\" retirada da lista do que existe: o banco mostra uma adesão paga e nenhuma cobrança periódica (item 11).", "\"PHIZ Leilão 99%\" retirado dos motores: sem evidência; fica como ideia futura no capítulo 11.", "Margem aproximada medida no banco: loja +6% a +15%; arremate negativo em 42 pedidos com custo — a validar (item 30)."]} />
      </Secao>

      <Secao id="tracao" sobretitulo="Capítulo 6" titulo="Tração e validação: a operação foi validada antes da tecnologia estar pronta">
        <div className="prosa max-w-3xl">
          <p>
            Antes de qualquer aplicativo, mais de 600 produtos foram comercializados a partir da residência do fundador usando WhatsApp,
            Facebook e OLX, com mais de 60% vendidos rapidamente. O mercado já existia; o que faltava era infraestrutura. A operação seguinte
            foi construída majoritariamente com processos manuais — aderência de mercado antes da automação.
          </p>
        </div>
        <Grade colunas={2}>
          <Cartao titulo="Receita mensal declarada no memorando (nov/25 – mai/26)">
            <Barras dados={SERIE_MEMORANDO.map((s) => ({ rotulo: s[0], valor: s[1], etiqueta: "MANAGEMENT_DATA" }))} formato={brlMil} />
            <p className="mt-2 text-xs text-muted">
              <Etiqueta tipo="MANAGEMENT_DATA" pequena /> Não reproduzível no banco do app (as vendas do app começam em 01/06/2026). Provável
              origem: planilha do varejo físico/WhatsApp. Sem definição de “receita”. Fica fora da série oficial até haver exportação ou extrato.
            </p>
          </Cartao>
          <Cartao titulo="Mercadoria vendida e paga no app (série oficial)">
            <Barras dados={gmvSerie.map((s) => ({ rotulo: mesCurto(s.periodo), valor: s.valor, etiqueta: s.etiqueta }))} formato={brlMil} />
            <p className="mt-2 text-xs text-muted">
              <Etiqueta tipo="VERIFIED" pequena /> Recalculado do banco, sem depósitos e sem adesões; outubro até o dia 16. Entradas brutas (com
              depósitos): {entradasSerie.map((s) => `${mesCurto(s.periodo)} ${s.valor != null ? brlMil(s.valor) : "—"}`).join(" · ")}.
            </p>
          </Cartao>
        </Grade>
        <Cartao titulo="Varejo físico e WhatsApp — planilha da operação (jun–ago/26)">
          <Barras dados={SERIE_NEXUS.map((s) => ({ rotulo: s[0], valor: s[1], etiqueta: "MANAGEMENT_DATA" }))} formato={brlMil} altura={120} />
          <p className="mt-2 text-xs text-muted">
            <Etiqueta tipo="MANAGEMENT_DATA" pequena /> Lançamento manual por seis executivos; sem lançamento de setembro em diante. O
            memorando público termina em maio e não mostra esta queda. O portal mostra.
          </p>
        </Cartao>
        <Grade colunas={4}>
          <Numero rotulo="Contas de cliente" valor={contas?.valor != null ? inteiro(contas.valor) : "—"} etiqueta={contas?.etiqueta} origem="site: “2.000+ clientes”" href="/app/prova/USERS_REGISTERED" />
          <Numero rotulo="Pagantes (90 dias)" valor={pagantes?.valor != null ? inteiro(pagantes.valor) : "—"} etiqueta={pagantes?.etiqueta} origem="compra ou depósito pago" href="/app/prova/CUSTOMERS_PAYING_90D" />
          <Numero rotulo="Compradores recorrentes" valor={recorrentes?.valor != null ? inteiro(recorrentes.valor) : "—"} etiqueta={recorrentes?.etiqueta} origem="2+ compras desde jun/26" href="/app/prova/BUYERS_REPEAT" />
          <Numero rotulo="Licenciados" valor={`${licCargo?.valor ?? "—"} · ${licRole?.valor ?? "—"} · ${licAtivo?.valor ?? "—"}`} etiqueta="VERIFIED" origem="cargo · papel · ativos 30 d (site: “80+”)" href="/app/prova/LICENSEES_TOTAL" />
        </Grade>
        <Grade colunas={2}>
          <Cartao titulo="Expansão física">
            <p className="text-muted">Site: loja em Senador Camará, operação integrada em Bangu, novas unidades e centro de distribuição planejado. No banco: tabela de lojas vazia e uma conta com nível “loja física”. Falta a lista com endereço, contrato e venda por loja.</p>
            <div className="mt-2"><Etiqueta tipo="MANAGEMENT_DATA" pequena /></div>
          </Cartao>
          <Cartao titulo="Estoque a custo">
            <p className="num text-2xl font-semibold">{estoque?.valor != null ? brl(estoque.valor) : "—"}</p>
            <p className="text-xs text-muted">{estoque?.nota}</p>
            <div className="mt-2"><Etiqueta tipo={estoque?.etiqueta ?? "NAO_DISPONIVEL"} pequena /></div>
          </Cartao>
        </Grade>
        <NotaRevisao
          conselho={conselho}
          itens={[
            "\"+1.000%\" (base nov/25) e \"960% / 10x em 4 meses\" (base fev/26) são a mesma série com duas janelas — retirados; a janela passa a ir no nome da métrica (itens 8–9).",
            "A declaração de faturamento ao banco e os livros trazem, para nov e dez/25, R$ 105 mil e R$ 106 mil (≈ 4–6× o memorando); os livros registram receita desde jan/2025 (R$ 1,19 mi no ano). Ou a operação é anterior, ou a série dos livros precisa ser explicada (itens 47–48).",
            "\"600 produtos, 60% vendidos\" (ago/24): anterior ao sistema, sem rastro — mantido como narrativa (item 44).",
          ]}
        />
      </Secao>

      <Secao id="governanca" sobretitulo="Capítulo 7" titulo="Governança, cultura e desenvolvimento humano">
        <div className="prosa max-w-3xl">
          <p>
            Existe uma crença comum de que tecnologia é o principal ativo de uma startup. Nós discordamos: tecnologia acelera, pessoas
            constroem. A evolução dentro da companhia acontece por desenvolvimento, não só por cargo — oito níveis, do vendedor ao conselho
            estratégico, com as trilhas Mentalidade do Executivo, do Diretor e do CEO.
          </p>
          <p>
            A companhia diferencia <strong>fundador</strong> (quem participou da construção inicial) de <strong>sócio</strong> (participação
            societária por critérios de mercado). E declara uma política de reconhecimento: 1% do faturamento bruto global destinado ao
            ecossistema de fundadores.
          </p>
        </div>
        <Link href="/app/governanca" className="inline-block text-sm underline">Ver time, níveis e a leitura do 1% como custo →</Link>
      </Secao>

      <Secao id="barreiras" sobretitulo="Capítulo 8" titulo="O que não pode ser copiado">
        <div className="prosa max-w-3xl">
          <p>Copiar tecnologia é relativamente fácil. Copiar cultura é extremamente difícil. As barreiras que a administração aponta:</p>
        </div>
        <Grade colunas={3}>
          <Cartao titulo="Capital intelectual do fundador">Mais de duas décadas condensadas em um modelo: militarismo, telecomunicações, franquias, marketing de relacionamento, mercado financeiro, desenvolvimento humano.</Cartao>
          <Cartao titulo="Cultura e X-EOS">Metodologia própria de desenvolvimento humano, liderança e expansão; as três trilhas internas de formação.</Cartao>
          <Cartao titulo="Rede de licenciados">Crescimento de dentro para fora, como grandes comunidades — sem depender só de mídia paga.</Cartao>
          <Cartao titulo="Comunidade">Não só clientes: uma comunidade, com parcerias que combinam tecnologia e desenvolvimento humano.</Cartao>
          <Cartao titulo="Integração tecnológica">Marketplace, CRM, financeiro, comissionamento, leilão e analisador conectados num só sistema.</Cartao>
          <Cartao titulo="Vale do Recreio e visão longa">Primeira empresa operacional do Vale do Recreio; construção olhando para 2035, não para o próximo trimestre.</Cartao>
        </Grade>
        <p className="text-xs text-muted">Narrativa da administração; nenhuma barreira recebe valor em reais. Entram no scorecard qualitativo do valuation.</p>
        <NotaRevisao conselho={conselho} itens={["Referência à Livoo como parceria exclusiva retirada (parceria encerrada em 17/10/2026)."]} />
      </Secao>

      <Secao id="valuation" sobretitulo="Capítulo 9" titulo="Valuation: por que a administração declara R$ 25 milhões">
        <div className="prosa max-w-3xl">
          <p>
            A administração atribui o valor à combinação de sete ativos: tecnologia, operação validada, capital intelectual, rede comercial,
            metodologia, ecossistema e potencial de escala — e lista como “ainda não precificado” a expansão nacional, novos módulos e a
            internacionalização.
          </p>
        </div>
        <Tabela
          cabecalho={["Ativo declarado", "O que o sistema mostra", "Etiqueta"]}
          linhas={[
            ["Tecnologia", `${loc?.valor != null ? inteiro(loc.valor) : "—"} linhas medidas; motor de leilão em uso; pagamentos conciliados`, <Etiqueta key="1" tipo="VERIFIED" pequena />],
            ["Operação validada", `vendas pagas no app desde jun/26; ${periodo}: ${gmvSerie.at(-1)?.valor != null ? brl(gmvSerie.at(-1)!.valor!) : "—"} de mercadoria`, <Etiqueta key="2" tipo="VERIFIED" pequena />],
            ["Capital intelectual", "currículo do fundador — vai a Governança, não ao valuation", <Etiqueta key="3" tipo="MANAGEMENT_DATA" pequena />],
            ["Rede comercial", `${licCargo?.valor ?? "—"} licenciados por cargo · ${licAtivo?.valor ?? "—"} ativos em 30 dias`, <Etiqueta key="4" tipo="VERIFIED" pequena />],
            ["Metodologia e ecossistema", "X-EOS, trilhas, Vale do Recreio — qualitativo", <Etiqueta key="5" tipo="MANAGEMENT_DATA" pequena />],
            ["Potencial de escala", "cenário, não valor atual", <Etiqueta key="6" tipo="FORECAST" pequena />],
          ]}
        />
        <Aviso tipo="atencao" titulo="Nenhum dos sete recebe valor em reais">
          Por isso o R$ 25 mi é tratado como <SeloReferencia /> — comparação, não resultado. O valor independente sai com método, pesos
          fixados antes e faixa. <Link href="/app/valuation" className="underline">Ver a metodologia v1.0</Link>.
        </Aviso>
        <NotaRevisao conselho={conselho} itens={["Retirados: \"valuation conservador\" (conservador comparado a quê?) e \"baseado em ativos reais\" (estoque e caixa não aparecem na lista) — itens 2 e 3.", "\"Potencial não precificado\" contradiz \"não é projeção\" na mesma página — item 5."]} />
      </Secao>

      <Secao id="roadmap" sobretitulo="Capítulo 10" titulo="Roadmap 2026: objetivos até o lançamento oficial">
        <Grade colunas={4}>
          <Numero rotulo="Licenciados ativos" valor="300" etiqueta="FORECAST" origem={`hoje: ${licCargo?.valor ?? "—"} por cargo · ${licAtivo?.valor ?? "—"} ativos`} />
          <Numero rotulo="Lojas físicas" valor="8" etiqueta="FORECAST" origem="hoje: 0 registradas no sistema" />
          <Numero rotulo="Centro de distribuição" valor="Recreio" etiqueta="FORECAST" origem="planejado" />
          <Numero rotulo="Faturamento" valor="R$ 1 mi/mês" etiqueta="FORECAST" origem={`hoje: ${entradasSerie.at(-1)?.valor != null ? brlMil(entradasSerie.at(-1)!.valor!) : "—"} de entradas brutas`} />
        </Grade>
        <Cartao titulo="Projeção de receita declarada (2026–2028)">
          <Barras dados={[{ rotulo: "2026", valor: 12_000_000, etiqueta: "FORECAST" }, { rotulo: "2027", valor: 36_000_000, etiqueta: "FORECAST" }, { rotulo: "2028", valor: 96_000_000, etiqueta: "FORECAST" }]} formato={(v) => `R$ ${v / 1_000_000} mi`} altura={140} />
          <p className="mt-2 text-xs text-muted"><Etiqueta tipo="FORECAST" pequena /> Projeção da administração, baseada na ativação progressiva dos motores. Não é previsão do sistema; a previsão por alavancas está em <Link href="/app/roadmap" className="underline">Metas e simulação</Link>.</p>
        </Cartao>
        <NotaRevisao conselho={conselho} itens={["Jan–mai/26 somam R$ 308,6 mil pelo próprio gráfico; para fechar R$ 12 mi em 2026 faltariam R$ 1,67 mi/mês de junho a dezembro, mas a meta de dezembro é R$ 1 mi/mês. O 2026 projetado não fecha com a meta do próprio material (item 13)."]} />
      </Secao>

      <Secao id="visao" sobretitulo="Capítulo 11" titulo="Visão 2035: o futuro que estamos construindo">
        <div className="prosa max-w-3xl">
          <p>
            A maioria das empresas nasce para resolver um problema; a Leilão NoZap nasceu para participar de uma transformação. Estamos
            entrando numa era em que inteligência artificial, automação, conectividade e desenvolvimento humano redefinem como as pessoas
            trabalham, empreendem e geram riqueza. A pergunta não é se essa transformação acontecerá — é quem será beneficiado por ela.
          </p>
          <p>
            <strong>Tecnologia para o bem.</strong> Acreditamos que a tecnologia não deve substituir pessoas, mas potencializá-las. O principal
            ativo do planeta é o ser humano; o futuro pertence às organizações capazes de desenvolver pessoas na mesma velocidade em que
            avançam tecnologicamente.
          </p>
          <p>
            <strong>O recommerce será uma categoria dominante.</strong> Produtos devolvidos, open box, recondicionados e excedentes farão parte
            do consumo cotidiano, como já acontece em outros mercados. A distribuição será mais inteligente, automatizada e descentralizada; a
            próxima geração de empreendedores nascerá em plataformas.
          </p>
          <p>
            <strong>Vale do Recreio — onde a escassez será escassa.</strong> A Leilão NoZap é a primeira empresa operacional de um projeto maior,
            criado para demonstrar que o Brasil pode criar empresas tecnológicas de classe mundial. Trata-se de acesso: à tecnologia, ao
            conhecimento, à oportunidade.
          </p>
          <p>
            <strong>Ideias futuras, sem número:</strong> live commerce próprio (a administração pretende ter a própria operação de vendas ao
            vivo) e novos canais de comunicação e distribuição. Entram no portal quando tiverem entrega verificável.
          </p>
        </div>
        <NotaRevisao conselho={conselho} itens={["Retirados: \"TikTok Shop ativo\", \"Livoo Live 99% / sociedade em fase final\", \"PHIZ Leilão em fase final\" (itens 19, 20, 20b).", "Mantidas as comparações com PIX e WhatsApp como narrativa."]} />
      </Secao>

      <Secao id="investimento" sobretitulo="Capítulo 12" titulo="Oportunidade de investimento: o que existe, o que está à frente e para que serve o capital">
        <div className="prosa max-w-3xl">
          <p>
            Os maiores retornos costumam ser capturados por quem identifica tendências antes de se tornarem consenso. A administração
            apresenta a Leilão NoZap como assimetria: parte relevante dos riscos reduzida pela validação prática, grande parte da expansão
            ainda à frente — e um efeito de rede em que mais vendedores trazem mais produtos, mais consumidores, mais liquidez e mais
            fornecedores.
          </p>
        </div>
        <Grade colunas={3}>
          <Cartao titulo="O que existe hoje">
            <ul className="list-disc space-y-1 pl-5 text-muted">
              <li>Operação com vendas pagas no app desde junho de 2026 <Etiqueta tipo="VERIFIED" pequena /></li>
              <li>Tecnologia própria, marketplace e motor de leilão em uso <Etiqueta tipo="VERIFIED" pequena /></li>
              <li>Rede comercial em formação, diretoria e conselho declarados <Etiqueta tipo="MANAGEMENT_DATA" pequena /></li>
              <li>Cultura e metodologia de formação <Etiqueta tipo="MANAGEMENT_DATA" pequena /></li>
            </ul>
          </Cartao>
          <Cartao titulo="O que ainda está à frente">
            <ul className="list-disc space-y-1 pl-5 text-muted">
              <li>Lançamento oficial e expansão nacional</li>
              <li>Escala da rede de licenciados e do marketplace</li>
              <li>Margem por venda medida e EBITDA calculável</li>
              <li>Fechamento oficial mensal e primeira rodada de valuation</li>
            </ul>
          </Cartao>
          <Cartao titulo="Para que o capital serve (plano)">
            <ul className="list-disc space-y-1 pl-5 text-muted">
              <li>Expansão comercial e da rede</li>
              <li>Aceleração tecnológica</li>
              <li>Aquisição de estoque estratégico</li>
              <li>Operações físicas, marca e infraestrutura nacional</li>
            </ul>
            <div className="mt-2"><Etiqueta tipo="FORECAST" pequena /></div>
          </Cartao>
        </Grade>
        <Aviso tipo="regra" titulo="O que este memorando não é">
          Não é oferta pública de valores mobiliários, não promete retorno e não substitui a análise própria do investidor. Capital de
          parceiros de compra é passivo com remuneração fixa (<Link href="/app/parceiros" className="underline">ver contratos</Link>); venda de
          participação exige contrato e alteração contratual. Os riscos estão em <Link href="/app/riscos" className="underline">Riscos</Link>.
        </Aviso>
        <NotaRevisao conselho={conselho} itens={["Retiradas as frases \"retorno elevado sobre capital investido a cada ciclo\", \"sem perda financeira\", \"sem risco típico de apostas\" e a seção que compara o produto a plataformas de aposta (itens 38, 39, 57) — revisão jurídica pendente.", "\"Receita recorrente\" e \"conselho estratégico\" na lista \"o que existe\" passaram a etiqueta de dado da administração."]} />
      </Secao>

      <footer className="border-t border-border pt-6 text-xs text-muted">
        Memorando originalmente publicado em investmentmemorandumleilaonozap.com e valuationleilaonozap.com (Gamma). Esta versão: 17/10/2026,
        com os números do sistema na data. Documento confidencial — uso restrito a convidados com termo de sigilo aceito.
      </footer>
    </Pagina>
  );
}
