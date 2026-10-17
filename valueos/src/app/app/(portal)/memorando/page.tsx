import Image from "next/image";
import Link from "next/link";
import {
  Award, BadgeCheck, Boxes, Brain, Building2, ChartLine, Check, CircleCheck, Cpu, Factory, Gauge, Gavel, Layers, Network,
  Package, Recycle, Rocket, Shield, ShieldCheck, ShoppingBag, ShoppingCart, Store, TrendingUp, User, UserCheck, Users,
  Droplet, Share2, Workflow,
} from "lucide-react";
import { valoresCarregados } from "@/lib/metricas";
import { papelAtual, eConselho } from "@/lib/papel";
import { mesCurto } from "@/lib/etiquetas";
import { Etiqueta, NotaRevisao, SeloReferencia, brl, brlMil, inteiro } from "@/components/ui";
import {
  Capitulo, Cartao, CartaoNumerado, Ciclo, Citacao, Conteiner, Faixa, GraficoBarras, Grade, Hoje, Imagem, LinhaDoTempo,
  Nota, NumeroGrande, Setas, Tag, Texto, Titulo, Trajetoria,
} from "@/components/marca";

export const dynamic = "force-dynamic";

const WHATSAPP = "https://wa.me/5521998753772";

// Série do memorando publicado (nov/25–mai/26): dado da administração, sem rastro no sistema.
const SERIE_DECLARADA = [
  ["nov/25", 16336], ["dez/25", 26358], ["jan/26", 27034], ["fev/26", 17191], ["mar/26", 23000], ["abr/26", 60374], ["mai/26", 181000],
] as const;

const CAPITULOS = [
  ["carta", "Carta do fundador"], ["resumo", "Resumo executivo"], ["tracao-hoje", "Tração hoje"], ["problema", "1 · Problema"],
  ["oportunidade", "2 · Oportunidade"], ["solucao", "3 · Solução"], ["tecnologia", "4 · Tecnologia"], ["modelo", "5 · Modelo"],
  ["tracao", "6 · Tração"], ["governanca", "7 · Governança"], ["barreiras", "8 · Barreiras"], ["valuation", "9 · Valuation"],
  ["roadmap", "10 · Roadmap"], ["visao", "11 · Visão 2035"], ["investimento", "12 · Investimento"],
];

export default async function Memorando() {
  const [{ ultimo, serie }, papel] = await Promise.all([valoresCarregados(), papelAtual()]);
  const conselho = eConselho(papel);
  const v = (id: string) => ultimo.get(id)?.valor ?? null;
  const s = (id: string) => serie.get(id) ?? [];
  const mes = (id: string, iso: string) => s(id).find((x) => x.periodo === iso)?.valor ?? null;

  const gmv = s("GMV_GOODS");
  const entradas = s("CASH_IN_GROSS");
  const arremates = s("GMV_AUCTION");
  const lances = s("BIDS_COUNT");
  const arrSet = mes("GMV_AUCTION", "2026-09-01");
  const arrOut = mes("GMV_AUCTION", "2026-10-01");
  const lancesSet = mes("BIDS_COUNT", "2026-09-01");
  const lancesOut = mes("BIDS_COUNT", "2026-10-01");
  const entAgo = mes("CASH_IN_GROSS", "2026-08-01");
  const entSet = mes("CASH_IN_GROSS", "2026-09-01");
  const loc = v("TECH_LOC");
  const licCargo = v("LICENSEES_TOTAL");
  const licRole = v("LICENSEES_ROLE");
  const licAtivo = v("LICENSEES_ACTIVE_30D");
  const contas = v("USERS_REGISTERED");
  const pagantes = v("CUSTOMERS_PAYING_90D");
  const recorrentes = v("BUYERS_REPEAT");
  const estoque = v("INVENTORY_AT_COST");
  const comissao = v("REVENUE_COMMISSION_RETAINED");
  const n = (x: number | null) => (x === null ? "—" : inteiro(x));
  const r = (x: number | null) => (x === null ? "—" : brl(x));
  const vezes = (a: number | null, b: number | null) => (a && b ? (a / b).toLocaleString("pt-BR", { maximumFractionDigits: 1 }) : "—");
  const kmil = (x: number) => (x >= 1000 ? `${Math.round(x / 1000)}k` : `${Math.round(x)}`);
  const ic = "h-6 w-6";

  return (
    <article className="bg-background">
      {/* CAPA */}
      <section className="relative isolate flex min-h-[92vh] items-center justify-center overflow-hidden text-center">
        <Image src="/m/capa.jpg" alt="" fill priority sizes="100vw" className="-z-10 object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-black/30 via-black/55 to-black" aria-hidden />
        <Conteiner className="py-28">
          <h1 className="font-display text-5xl font-semibold tracking-tight text-white sm:text-7xl">LEILÃO NOZAP</h1>
          <div className="mx-auto mt-8 h-px max-w-3xl bg-white/50" />
          <p className="mt-6 text-lg font-light text-white/90">Investment Memorandum · Memorando de Investimento · 2026</p>
          <p className="mt-3 text-sm font-light text-pill">Edição atualizada em 17/10/2026 — números do sistema, com prova</p>
        </Conteiner>
      </section>

      <nav aria-label="Capítulos" className="sticky top-[61px] z-20 border-y border-white/10 bg-black/90 backdrop-blur">
        <Conteiner className="flex gap-1 overflow-x-auto py-2">
          {CAPITULOS.map((c) => (
            <a key={c[0]} href={`#${c[0]}`} className="whitespace-nowrap rounded-md px-3 py-1.5 text-xs text-white/75 hover:bg-white/5 hover:text-white">
              {c[1]}
            </a>
          ))}
        </Conteiner>
      </nav>

      {/* CARTA DO FUNDADOR */}
      <Faixa id="carta">
        <Tag>
          <User className="h-3.5 w-3.5" aria-hidden /> Carta do fundador
        </Tag>
        <h2 className="mt-3 font-display text-3xl font-light leading-tight text-white sm:text-5xl">
          Não estamos construindo apenas uma empresa.
          <br />
          <span className="text-accent">Estamos construindo uma infraestrutura.</span>
        </h2>
        <p className="mt-6 font-light text-texto">
          Meu nome é <strong className="font-medium text-white">Luiz Sant’Anna</strong>.
        </p>
        <Imagem src="/m/fundador.jpg" alt="Luiz Sant’Anna, fundador e CEO da Leilão NoZap, em seu escritório" className="mt-6 aspect-[3/2] max-w-5xl" prioridade />
        <Texto className="mt-8">
          <p>Ao longo de mais de duas décadas empreendendo, tive a oportunidade de atuar em ambientes completamente diferentes entre si. Hoje percebo que cada um deles contribuiu para a construção da visão que deu origem à Leilão NoZap.</p>
          <p>Minha trajetória começou no <strong>Corpo de Fuzileiros Navais</strong>, onde aprendi disciplina, liderança, resiliência e execução sob pressão. Foi ali que tive meu primeiro contato com algo que se tornaria uma constante em toda a minha vida profissional: a construção de sistemas capazes de multiplicar pessoas, resultados e oportunidades.</p>
          <p>Após o período militar, atuei em operações de franquias, telecomunicações e varejo, passando por empresas como <strong>Sky</strong> e <strong>Nextel</strong>, onde desenvolvi experiência prática em expansão comercial, gestão de equipes, distribuição e crescimento operacional.</p>
          <p>Empreendi em diferentes segmentos, incluindo o varejo físico através de restaurante próprio, aprendendo na prática sobre margem, fluxo de caixa, atendimento, operação e gestão.</p>
          <p>Mas foi no desenvolvimento humano e na construção de comunidades de alta performance que encontrei um dos aprendizados mais importantes da minha trajetória.</p>
          <p>Durante aproximadamente oito anos, participei ativamente do setor de marketing de relacionamento, investindo mais de <strong>R$ 300 mil</strong> em mentorias, formações executivas, treinamentos, vendas, liderança, comportamento humano e desenvolvimento organizacional.</p>
          <p>Ao longo desse período alcancei a posição máxima de liderança em duas organizações já consolidadas nacionalmente.</p>
          <p>Em uma delas, do segmento de turismo, participei da construção, expansão e liderança de estruturas que alcançaram mais de <strong>30 mil pessoas</strong> ao longo da minha trajetória profissional, com presença em mais de vinte estados brasileiros e equipes distribuídas em seis países.</p>
          <p>Essa experiência me permitiu compreender profundamente temas como liderança, cultura organizacional, meritocracia, sistemas de incentivo, formação de líderes, retenção de talentos, escalabilidade comercial e construção de comunidades.</p>
          <p>O reconhecimento dessa trajetória resultou em homenagens institucionais e no recebimento de uma <strong>Moção de Reconhecimento</strong> concedida pelo Estado do Rio de Janeiro pelos serviços prestados ao setor.</p>
          <p>Foi também nesse período que participei do movimento que consolidou o reconhecimento oficial do Marketing de Relacionamento no estado do Rio de Janeiro.</p>
          <p>Após atingir os mais altos níveis de liderança nessas operações, decidi direcionar todo esse conhecimento para a construção de negócios próprios.</p>
          <p>Posteriormente mergulhei no mercado financeiro, tornando-me correspondente bancário certificado e atuando em operações estruturadas de crédito.</p>
          <p>Ao longo dessa fase atuei na originação e comercialização de mais de <strong>R$ 100 milhões</strong> em operações de crédito — principalmente Home Equity, crédito com garantia e operações estruturadas — com aproximadamente <strong>R$ 40 milhões</strong> efetivamente aprovados e formalizados.</p>
          <p>Essa experiência aprofundou meu conhecimento sobre análise de risco, estruturação financeira, vendas consultivas, indicadores de performance, gestão comercial e crescimento escalável.</p>
          <p>Mais tarde, em uma fase completamente diferente, construí uma operação de captação de investimentos utilizando metodologia própria, marketing digital e cultura organizacional. Com uma equipe enxuta de aproximadamente oito pessoas e atuação totalmente digital, essa operação captou mais de <strong>R$ 22 milhões</strong> em investimentos — valor independente e separado das operações de crédito anteriores.</p>
          <p>Todo o processo foi conduzido através de treinamento contínuo, aplicação de cultura, desenvolvimento de executivos e melhoria constante da metodologia operacional.</p>
          <p>Essa experiência consolidou uma das convicções que carrego até hoje:</p>
        </Texto>
        <Citacao verde className="mt-6 max-w-4xl">Escala não é consequência do tamanho da equipe. Escala é consequência da qualidade do sistema.</Citacao>
        <Texto className="mt-6">
          <p>Foi justamente dessa visão que nasceu a <strong>X-EOS</strong>, metodologia própria de desenvolvimento humano, formação de líderes e expansão organizacional. A X-EOS foi a primeira startup estruturada dentro desse ecossistema e alcançou valuation de aproximadamente <strong>R$ 4 milhões</strong> ainda em sua fase inicial de desenvolvimento.</p>
          <p>Ao longo dessa jornada percebi algo que se repetia em todos os mercados.</p>
          <p>Existem excelentes ideias. Existem excelentes tecnologias. Existem excelentes produtos.</p>
          <p>Mas o que normalmente falha não são as empresas.</p>
          <p>O que falha é a capacidade de transformar visão em execução.</p>
          <p>Foi então que comecei a estudar profundamente quais seriam os mercados mais resilientes das próximas décadas.</p>
          <p>E descobri uma verdade simples:</p>
          <p>Compra e venda existem desde que o mundo é mundo.</p>
          <p>Tecnologias mudam. Empresas surgem e desaparecem. Mas a troca de valor entre pessoas continua existindo.</p>
          <p>Ao mesmo tempo, uma transformação silenciosa estava acontecendo.</p>
          <p>O crescimento do e-commerce gerava milhões de devoluções. Milhões de produtos retornavam para estoques. Fabricantes produziam. Consumidores compravam.</p>
          <p>Mas faltava uma infraestrutura eficiente conectando todas as partes.</p>
          <p>Foi nesse momento que percebi uma oportunidade que poucos estavam enxergando.</p>
          <p>A <strong>Leilão NoZap</strong> nasceu para transformar riqueza parada em liquidez. Transformar estoques em receita. Transformar tecnologia em prosperidade. Transformar consumidores em empreendedores. Transformar oportunidade em distribuição.</p>
          <p>Mas existe algo ainda mais importante.</p>
          <p>Acreditamos que o principal ativo do mundo não é a tecnologia. Não é o capital. Não é a infraestrutura.</p>
          <p><strong>É o ser humano.</strong></p>
          <p>Por isso investimos tanto na formação de líderes.</p>
          <p>Por isso criamos a <strong>Mentalidade do Executivo</strong>, a <strong>Mentalidade do Diretor</strong> e a <strong>Mentalidade do CEO</strong>.</p>
          <p>Por isso acreditamos que toda empresa deveria funcionar também como uma escola.</p>
          <p>Porque empresas são construídas por pessoas. Mercados são transformados por pessoas. E o futuro continua sendo construído por pessoas.</p>
          <p>A Leilão NoZap representa a convergência de tudo o que aprendi ao longo dessa jornada:</p>
          <p className="!font-medium !text-accent">Militarismo. Empreendedorismo. Tecnologia. Mercado financeiro. Desenvolvimento humano. Escalabilidade comercial. Cultura organizacional. Distribuição inteligente.</p>
          <p>Não estamos construindo apenas um marketplace. Não estamos construindo apenas uma plataforma.</p>
          <p><strong>Estamos construindo algo que dura.</strong></p>
          <p>Uma plataforma capaz de conectar tecnologia, oportunidade, pessoas e prosperidade distribuída.</p>
          <p>Estamos apenas no começo.</p>
          <p>Mas acreditamos que as empresas que transformarão a próxima década serão aquelas capazes de desenvolver pessoas na mesma velocidade em que avançam tecnologicamente.</p>
          <p>Essa é a visão da Leilão NoZap.</p>
          <p>E este é apenas o primeiro capítulo de uma história muito maior.</p>
        </Texto>
        <div className="mt-8 max-w-4xl border-t border-white/15 pt-5">
          <p className="font-display text-lg text-accent">Luiz Sant’Anna</p>
          <p className="text-sm font-light text-texto">Fundador e CEO — Leilão NoZap</p>
        </div>
      </Faixa>

      {/* TRAJETÓRIA E CONQUISTAS */}
      <Faixa>
        <Titulo tag="Trajetória do fundador" verde>
          Uma Jornada de Duas Décadas
        </Titulo>
        <Trajetoria
          itens={[
            { titulo: "Fuzileiros Navais", texto: "Disciplina, liderança e execução sob pressão. Construção de sistemas que multiplicam pessoas e resultados." },
            { titulo: "Telecomunicações & Franquias", texto: "Sky e Nextel. Expansão comercial, gestão de equipes e crescimento operacional em larga escala." },
            { titulo: "Mercado Financeiro R$100M+", texto: "Correspondente bancário certificado. Mais de R$ 100 milhões originados em operações de crédito." },
            { titulo: "Leilão NoZap", texto: "Infraestrutura de leilões via WhatsApp. Uma nova categoria no mercado brasileiro." },
          ]}
        />
      </Faixa>

      <Faixa>
        <Titulo tag="Conquistas" verde>
          Captação de R$ 22 Milhões
        </Titulo>
        <div className="mt-12 grid gap-10 md:grid-cols-3">
          <NumeroGrande valor="R$22M" rotulo="em Investimentos Captados" sub="Operação 100% digital com equipe enxuta de ~8 pessoas, usando metodologia própria e marketing digital." cor="verde" />
          <NumeroGrande valor="~8" rotulo="Pessoas na Equipe" sub="Prova de que escala é consequência da qualidade do sistema, não do tamanho da equipe." cor="verde" />
          <NumeroGrande valor="R$4M" rotulo="Valuation Inicial X-EOS" sub="Primeira startup do ecossistema, nascida da metodologia de desenvolvimento humano e expansão organizacional." cor="verde" />
        </div>
        <Citacao className="mt-12">Escala não é consequência do tamanho da equipe. Escala é consequência da qualidade do sistema.</Citacao>
        <p className="mt-4 text-xs text-muted">
          Números da trajetória pessoal do fundador: <Etiqueta tipo="MANAGEMENT_DATA" pequena /> — documentação no data room.
        </p>
      </Faixa>

      <Faixa>
        <Titulo tag="Visão do fundador">A Convergência de Tudo</Titulo>
        <p className="mt-4 font-light text-texto">A Leilão NoZap representa a convergência de tudo o que foi aprendido ao longo dessa jornada:</p>
        <Grade colunas={2} className="mt-6">
          <Cartao tom="cinza" icone={<Shield className={ic} />} titulo="Militarismo">Disciplina e execução</Cartao>
          <Cartao tom="cinza" icone={<Rocket className={ic} />} titulo="Empreendedorismo">Visão e construção</Cartao>
          <Cartao tom="cinza" icone={<Cpu className={ic} />} titulo="Tecnologia">Infraestrutura própria</Cartao>
          <Cartao tom="cinza" icone={<ChartLine className={ic} />} titulo="Mercado Financeiro">Análise e estruturação</Cartao>
          <Cartao tom="cinza" icone={<Users className={ic} />} titulo="Desenvolvimento Humano">Formação de líderes</Cartao>
          <Cartao tom="cinza" icone={<Share2 className={ic} />} titulo="Distribuição Inteligente">Escala descentralizada</Cartao>
        </Grade>
        <p className="mx-auto mt-10 max-w-4xl text-center font-medium text-accent">
          Estamos apenas no começo. Mas acreditamos que as empresas que transformarão a próxima década serão aquelas capazes de desenvolver pessoas na mesma velocidade em que avançam tecnologicamente.
        </p>
        <p className="mt-4 text-center font-light text-muted">— Luiz Sant’Anna, Fundador e CEO — Leilão NoZap</p>
      </Faixa>

      {/* LINHA DO TEMPO */}
      <Faixa>
        <Titulo tag="Linha do tempo" verde>
          A Construção da Leilão NoZap
        </Titulo>
        <p className="mt-4 max-w-4xl font-light text-texto">
          A Leilão NoZap não nasceu de uma ideia isolada. Nasceu da combinação entre experiência prática, validação de mercado e execução contínua.
        </p>
        <LinhaDoTempo
          itens={[
            { quando: "Jul 2024", texto: "Encerramento do ciclo anterior. Início dos estudos sobre recommerce, devoluções e redistribuição inteligente." },
            { quando: "Ago 2024", texto: "Primeiro MVP. Mais de 600 produtos comercializados da residência do fundador via WhatsApp, Facebook e OLX. Mais de 60% vendidos rapidamente. Validação prática do modelo." },
            { quando: "Set 2024", texto: "Estruturação da operação. Criação do escritório. Desenvolvimento da tese de mercado. Início da construção da base tecnológica." },
            { quando: "Out 2024 – Mar 2025", texto: "Pesquisa de mercado. Metodologia. Formação da equipe inicial. Negociações com fornecedores e parceiros estratégicos." },
            { quando: "Abr 2025", texto: "Início efetivo da construção da plataforma. Primeiros módulos operacionais. Primeiras integrações e validações técnicas." },
            { quando: "Nov 2025", texto: "Primeira estrutura executiva formada. Operação comercial organizada. Primeiras vendas através da rede." },
            { quando: "Jun 2026", texto: "Aplicativo em produção: primeiras vendas pagas registradas no sistema (01/06/2026). Primeira turma em formação.", etiqueta: "VERIFIED", novo: true },
            { quando: "Ago 2026", texto: "Marco oficial do app: a série financeira auditável começa em 01/08/2026. Leilões com reserva de saldo por lance em operação.", etiqueta: "VERIFIED", novo: true },
            { quando: "Set 2026", texto: `Primeiro capital de parceiros de compra (R$ 250 mil, 2 contratos) e primeira venda de participação informada (1%). Mês de maior movimento no app: ${r(entSet)} em entradas.`, etiqueta: "VERIFIED", novo: true },
            { quando: "Out 2026", texto: `Leilão acelera: em 16 dias, ${r(arrOut)} em arremates e ${n(lancesOut)} lances — acima de setembro inteiro. Lançado este portal do investidor, com cada número rastreável.`, etiqueta: "VERIFIED", novo: true },
            { quando: "Dez 2026", texto: "Lançamento oficial. Meta: 300 licenciados ativos · 8 lojas físicas · Distribuidor Recreio · R$ 1M+/mês.", etiqueta: "FORECAST" },
          ]}
        />
      </Faixa>

      {/* RESUMO EXECUTIVO */}
      <section id="resumo" className="grid scroll-mt-20 lg:grid-cols-[minmax(0,38%)_minmax(0,62%)]">
        <div className="relative min-h-[50vh]">
          <Image src="/m/mapa-brasil.jpg" alt="" fill sizes="(min-width:1024px) 38vw, 100vw" className="object-cover" />
        </div>
        <div className="bg-[#070707] px-5 py-16 sm:px-12 lg:px-16">
          <Tag>Resumo executivo</Tag>
          <h2 className="mt-4 font-display text-3xl font-light leading-tight text-white sm:text-5xl">
            Infraestrutura Brasileira de Recommerce, Distribuição Inteligente e Desenvolvimento Humano
          </h2>
          <Texto className="mt-6">
            <p>A Leilão NoZap é uma empresa brasileira de tecnologia, recommerce e distribuição inteligente criada para transformar estoques parados, devoluções de e-commerce, excedentes industriais e oportunidades comerciais em <strong>liquidez distribuída</strong> através de uma infraestrutura proprietária que conecta fabricantes, distribuidores, vendedores, licenciados e consumidores finais.</p>
            <p>A companhia atua em um dos mercados de maior crescimento do mundo: a convergência entre e-commerce, recommerce, social commerce, live commerce e inteligência artificial aplicada ao varejo.</p>
            <p>Mais do que um marketplace, a Leilão NoZap está construindo uma <strong>infraestrutura nacional de comercialização</strong> baseada em tecnologia, distribuição descentralizada e desenvolvimento humano.</p>
          </Texto>
          <div className="my-8 h-px bg-white/20" />
          <p className="font-display text-2xl font-light text-accent">Nossa Tese</p>
          <Texto className="mt-3">
            <p>Acreditamos que o Brasil não sofre por falta de produtos. Não sofre por falta de consumidores. Não sofre por falta de empreendedores. O Brasil sofre por falta de <strong>conexão eficiente</strong> entre essas partes. A Leilão NoZap foi criada para resolver exatamente essa ineficiência.</p>
          </Texto>
          <div className="my-8 h-px bg-white/20" />
          <div className="grid gap-8 sm:grid-cols-2">
            <div>
              <p className="font-display text-2xl font-light text-white">Valuation</p>
              <p className="num mt-3 whitespace-nowrap font-display text-4xl font-bold leading-none text-accent xl:text-[2.6rem]">R$ 25.000.000</p>
              <div className="mt-3">
                <SeloReferencia />
              </div>
              <p className="mt-2 text-sm font-light text-muted">
                Valor de referência declarado pelo fundador. O valuation independente, com método e faixa, é calculado neste portal —{" "}
                <Link href="/app/valuation" className="text-pill underline underline-offset-2">ver metodologia</Link>.
              </p>
            </div>
            <div>
              <p className="font-display text-2xl font-light text-white">Roadmap</p>
              <ul className="mt-2 list-disc space-y-1 pl-5 font-light text-texto">
                <li>300 licenciados e vendedores ativos</li>
                <li>8 lojas físicas</li>
                <li>1 centro de distribuição</li>
                <li>Faturamento superior a R$ 1 milhão por mês</li>
                <li>Lançamento oficial da plataforma</li>
              </ul>
              <div className="mt-2"><Etiqueta tipo="FORECAST" pequena /></div>
            </div>
          </div>
        </div>
      </section>

      <Faixa>
        <Titulo tag="Nossa tese">O Brasil Não Sofre por Falta de Produtos</Titulo>
        <Grade colunas={2} className="mt-8">
          <Cartao tom="escuro" titulo="O Que Existe">
            <ul className="list-disc space-y-1 pl-5">
              <li>Produtos em abundância</li>
              <li>Consumidores prontos</li>
              <li>Empreendedores motivados</li>
              <li>Fabricantes produtivos</li>
            </ul>
          </Cartao>
          <Cartao tom="escuro" titulo="O Que Falta">
            <p>O Brasil sofre por falta de <strong className="font-medium text-white">conexão eficiente</strong> entre essas partes.</p>
            <p className="mt-3">A Leilão NoZap foi criada para resolver exatamente essa ineficiência — conectando toda a cadeia de valor através de tecnologia proprietária.</p>
          </Cartao>
        </Grade>
      </Faixa>

      {/* TRAÇÃO HOJE (substitui o "+1.000%" com a série do sistema) */}
      <Faixa id="tracao-hoje">
        <Titulo tag="Tração comprovada · atualizada" verde>
          O Motor de Leilão Já Está Acelerando
        </Titulo>
        <p className="mt-4 max-w-4xl font-light text-texto">
          A série oficial começa no marco do aplicativo (01/08/2026) e vem direto do banco de dados, sem planilha no meio. Outubro conta só até o dia 16 — e já passou setembro inteiro no leilão.
        </p>
        <div className="mt-12 grid gap-10 md:grid-cols-3">
          <NumeroGrande valor={`${vezes(entSet, entAgo)}×`} rotulo="Entradas no app" sub={`agosto ${r(entAgo)} → setembro ${r(entSet)}`} etiqueta="VERIFIED" href="/app/prova/CASH_IN_GROSS" />
          <NumeroGrande valor={arrOut !== null ? brlMil(arrOut).replace(" mil", "K").replace("R$ ", "R$") : "—"} rotulo="Arremates em 16 dias" sub={`outubro já supera setembro inteiro (${r(arrSet)})`} etiqueta="VERIFIED" href="/app/prova/GMV_AUCTION" />
          <NumeroGrande valor={n(lancesOut)} rotulo="Lances em outubro" sub={`contra ${n(lancesSet)} em setembro inteiro`} etiqueta="VERIFIED" href="/app/prova/BIDS_COUNT" />
        </div>
        <div className="mt-12 grid grid-cols-1 gap-8 lg:grid-cols-2">
          <GraficoBarras
            titulo="Arremates pagos no app (R$)"
            dados={arremates.map((x) => ({ rotulo: mesCurto(x.periodo), valor: x.valor, tom: "verificado" as const }))}
            formato={kmil}
            altura={300}
          />
          <GraficoBarras
            titulo="Lances registrados"
            dados={lances.map((x) => ({ rotulo: mesCurto(x.periodo), valor: x.valor, tom: "verificado" as const }))}
            formato={(x) => inteiro(Math.round(x))}
            altura={300}
          />
        </div>
        <p className="mt-6 text-sm font-light text-muted">
          Fonte: banco do app (tabela de vendas pagas e mensagens de lance), carga de 17/10/2026, com impressão digital.{" "}
          <Link href="/app/numeros" className="text-pill underline underline-offset-2">Ver os 30 números com prova</Link>.
        </p>
      </Faixa>

      <Faixa>
        <Titulo tag="Tecnologia">Infraestrutura Tecnológica Proprietária</Titulo>
        <div className="mt-12 grid gap-12 md:grid-cols-2">
          <NumeroGrande valor={loc ? `${Math.round(loc / 1000)}K+` : "—"} rotulo="Linhas de Código" sub="medidas no repositório em 17/10/2026, sem contar testes" etiqueta="VERIFIED" href="/app/prova/TECH_LOC" />
          <NumeroGrande valor="2.033" rotulo="Arquivos de código" sub="arquitetura integrada e modular" etiqueta="VERIFIED" />
          <NumeroGrande valor="R$25M" rotulo="Valuation de referência" sub="declarado pelo fundador; o independente é calculado no portal" etiqueta="MANAGEMENT_DATA" />
          <NumeroGrande valor="Próprio" rotulo="Código-fonte" sub="escrito pela equipe, sobre infraestrutura de mercado (Supabase, Vercel, Mercado Pago); titularidade documentada no data room" etiqueta="MANAGEMENT_DATA" />
        </div>
      </Faixa>

      {/* CAPÍTULO 1 */}
      <Capitulo id="problema" numero="Capítulo 1" titulo="O Problema" sub="A Maior Ineficiência Oculta do Comércio Brasileiro" imagem="/m/cap1-problema.jpg" lado="esquerda">
        <p>Durante décadas, o varejo foi construído para vender. Mas ninguém construiu uma infraestrutura eficiente para lidar com o que sobra. O resultado é um problema silencioso que movimenta bilhões de reais todos os anos. Produtos devolvidos. Estoques excedentes. Mercadorias paradas. Fabricantes sem distribuição. Consumidores sem acesso. Empreendedores sem oportunidade. Todos coexistindo dentro do mesmo sistema. Mas sem conexão.</p>
      </Capitulo>

      <Faixa>
        <Titulo tag="O problema">Um Problema Bilionário Crescendo em Silêncio</Titulo>
        <Grade colunas={3} className="mt-8">
          <Cartao titulo="Um problema bilionário crescendo em silêncio">O crescimento do e-commerce criou uma consequência inevitável. Quanto mais vendas acontecem, mais devoluções acontecem. Quanto mais devoluções acontecem, maior se torna o volume de produtos que precisam ser revendidos, redistribuídos ou reintegrados ao mercado. Milhões de produtos retornam todos os anos para marketplaces, varejistas, fabricantes, distribuidores e centros de distribuição. Grande parte desses produtos possui valor comercial. Mas não possui liquidez.</Cartao>
          <Cartao titulo="O custo invisível">Quando um produto para de girar, ele deixa de ser estoque. Ele passa a ser custo. Ocupa espaço. Consome capital. Gera despesas operacionais. Reduz margem. Diminui produtividade. Impacta fluxo de caixa. A cada dia parado, o produto perde valor. A empresa perde dinheiro.</Cartao>
          <Cartao titulo="O problema não está apenas nos grandes players">Embora grandes empresas convivam diariamente com esse desafio, o problema é ainda mais grave para pequenas e médias empresas. Porque elas normalmente possuem menos capital, menos tecnologia, menos canais de distribuição e menos acesso a liquidez.</Cartao>
        </Grade>
      </Faixa>

      <Faixa>
        <Titulo tag="O problema">O Fabricante Produz. Mas Nem Sempre Consegue Vender.</Titulo>
        <div className="mt-8 grid gap-10 md:grid-cols-2">
          <div>
            <p className="font-display text-2xl font-light text-accent">O fabricante produz. Mas nem sempre consegue vender.</p>
            <Texto className="mt-3">
              <p>A maioria dos fabricantes domina a produção. Mas poucos dominam a distribuição. Eles sabem fabricar. Mas não possuem estrutura comercial, tecnologia, tráfego, influência digital ou canais próprios de expansão.</p>
              <p>O resultado é previsível: Produtos excelentes. Distribuição limitada. Capital travado.</p>
            </Texto>
          </div>
          <div>
            <p className="font-display text-2xl font-light text-accent">Enquanto isso, do outro lado</p>
            <Texto className="mt-3">
              <p>Milhões de brasileiros procuram exatamente o que essas empresas possuem: Produtos. Oportunidades. Renda. Possibilidade de empreender. Liberdade financeira.</p>
              <p>Mas encontram barreiras como falta de estoque, falta de capital, falta de tecnologia, falta de marketing e falta de acesso.</p>
            </Texto>
          </div>
        </div>
        <div className="mt-8"><Nota>O produto existe. O consumidor existe. O empreendedor existe. Mas a conexão não.</Nota></div>
      </Faixa>

      <Faixa>
        <Tag>A pergunta fundadora</Tag>
        <blockquote className="mt-6 border-l-2 border-white/80 py-4 pl-6 text-center font-display text-3xl font-light italic leading-snug text-white sm:pl-12 sm:text-4xl">
          Se milhões de produtos são devolvidos todos os anos, para onde eles vão?
        </blockquote>
        <Texto className="mt-6">
          <p>A resposta revelou um dos mercados mais subexplorados da economia moderna. E revelou também uma oportunidade ainda maior. Não era apenas sobre vender produtos. Era sobre construir a infraestrutura capaz de conectar riqueza parada a pessoas que precisam de oportunidade.</p>
        </Texto>
        <p className="mt-8 font-display text-2xl font-light text-accent">Nossa Convicção</p>
        <Grade colunas={3} className="mt-4">
          <Cartao tom="escuro">A próxima grande transformação do varejo não acontecerá apenas na venda. Ela acontecerá na <strong className="font-medium text-white">redistribuição</strong>.</Cartao>
          <Cartao tom="escuro">Não acontecerá apenas na produção. Acontecerá na <strong className="font-medium text-white">liquidez</strong>.</Cartao>
          <Cartao tom="escuro">Não acontecerá apenas nos produtos. Acontecerá na <strong className="font-medium text-white">conexão</strong>.</Cartao>
        </Grade>
        <p className="mt-6 text-center font-light text-texto">E foi exatamente para resolver essa ineficiência que a <strong className="font-medium text-white">Leilão NoZap</strong> nasceu.</p>
      </Faixa>

      {/* CAPÍTULO 2 */}
      <Capitulo id="oportunidade" numero="Capítulo 2" titulo="A Oportunidade" sub="Estamos diante de uma transformação histórica" imagem="/m/cap2-oportunidade.jpg">
        <p>As maiores empresas da última década não criaram mercados. Elas identificaram mudanças de comportamento antes dos demais.</p>
        <p>O Uber não criou a mobilidade. Transformou a forma como ela era acessada. O Airbnb não criou hospedagem. Transformou a forma como ela era distribuída. O WhatsApp não criou comunicação. Transformou a forma como as pessoas se conectavam. O Mercado Livre não criou o comércio. Transformou a forma como o Brasil compra e vende.</p>
        <p>A Leilão NoZap acredita que a próxima grande transformação acontecerá na redistribuição inteligente de produtos, ativos e oportunidades.</p>
      </Capitulo>

      <Faixa>
        <Titulo tag="Analogias de mercado">Transformação Antes do Consenso</Titulo>
        <Grade colunas={2} className="mt-8">
          {[
            ["Uber", "Não criou a mobilidade. Transformou a forma como ela era acessada."],
            ["Airbnb", "Não criou hospedagem. Transformou a forma como ela era distribuída."],
            ["WhatsApp", "Não criou comunicação. Transformou a forma como as pessoas se conectavam."],
            ["Mercado Livre", "Não criou o comércio. Transformou a forma como o Brasil compra e vende."],
          ].map(([t, d]) => (
            <div key={t} className="overflow-hidden rounded-lg border-2 border-accent bg-black">
              <div className="h-12 bg-accent" aria-hidden />
              <div className="p-6">
                <p className="font-display text-xl font-light text-accent">{t}</p>
                <p className="mt-2 text-[15px] font-light text-texto">{d}</p>
              </div>
            </div>
          ))}
        </Grade>
        <p className="mt-6 text-center font-medium text-accent">A Leilão NoZap acredita que a próxima grande transformação acontecerá na redistribuição inteligente de produtos, ativos e oportunidades.</p>
      </Faixa>

      <Faixa className="text-center">
        <p className="font-display text-3xl font-light text-white sm:text-4xl">Uma nova economia está sendo construída</p>
        <p className="mx-auto mt-6 max-w-4xl font-light text-texto">Durante décadas o varejo foi baseado em três pilares: Produzir. Distribuir. Vender. Mas um quarto pilar começou a ganhar protagonismo:</p>
        <p className="mt-8 font-display text-6xl font-bold tracking-tight text-accent sm:text-8xl">Redistribuir.</p>
        <p className="mx-auto mt-8 max-w-4xl font-light text-texto">O crescimento do e-commerce criou uma nova camada econômica global. Uma camada formada por devoluções, excedentes, produtos de exposição, produtos de mostruário, excesso de estoque, ativos sem liquidez e oportunidades comerciais subutilizadas. Essa camada movimenta bilhões. E continua crescendo.</p>
      </Faixa>

      <Faixa>
        <Titulo tag="Múltiplas oportunidades">Oportunidades em Todos os Elos da Cadeia</Titulo>
        <div className="mt-8 grid gap-10 md:grid-cols-2">
          {[
            [<Factory key="f" className="h-9 w-9" />, "Para Fabricantes", "Grande parte dos pequenos e médios fabricantes possui capacidade produtiva. Mas não possui capacidade de distribuição. Produzem bem. Mas dependem de marketplaces, representantes, distribuidores e tráfego pago. O resultado é previsível: Margens reduzidas. Dependência crescente. Escala limitada. A Leilão NoZap surge como uma infraestrutura complementar de distribuição."],
            [<Store key="s" className="h-9 w-9" />, "Para Varejistas", "As grandes empresas enfrentam um desafio crescente. Quanto maior a operação, maior o volume de devoluções. Maior a necessidade de redistribuição. Maior o custo operacional. A tendência é clara. As empresas buscarão cada vez mais parceiros especializados em liquidez e redistribuição."],
            [<User key="u" className="h-9 w-9" />, "Para Empreendedores", "Milhões de brasileiros desejam empreender. Mas encontram os mesmos obstáculos: Falta de estoque. Falta de tecnologia. Falta de marketing. Falta de capital. A Leilão NoZap reduz essas barreiras. Transformando oportunidade em acesso."],
            [<Brain key="b" className="h-9 w-9" />, "Para a Tecnologia", "A Inteligência Artificial mudou a equação. Pela primeira vez pequenas operações podem operar com eficiência comparável a grandes organizações. A IA reduz custo operacional, tempo de resposta, necessidade de equipe e complexidade de gestão. A Leilão NoZap nasce dentro dessa nova realidade. Não como adaptação. Mas como arquitetura nativa."],
          ].map(([icone, t, d]) => (
            <div key={t as string} className="flex gap-5">
              <span className="shrink-0 text-accent">{icone}</span>
              <div>
                <p className="font-display text-xl font-light text-accent">{t}</p>
                <p className="mt-2 text-[15px] font-light leading-relaxed text-texto">{d}</p>
              </div>
            </div>
          ))}
        </div>
      </Faixa>

      <section className="grid lg:grid-cols-[minmax(0,62%)_minmax(0,38%)]">
        <div className="bg-[#070707] px-5 py-16 sm:px-12 lg:px-16">
          <Tag>Vantagem brasileira</Tag>
          <h2 className="mt-4 font-display text-3xl font-light text-white sm:text-5xl">O Brasil Como Ambiente Ideal</h2>
          <p className="mt-4 font-light text-texto">O Brasil reúne características únicas que criam um ambiente extremamente favorável para a expansão de modelos baseados em recommerce e distribuição inteligente:</p>
          <div className="mt-6 space-y-4">
            {[["Conectividade", "Forte presença do WhatsApp"], ["Cultura Comercial", "Espírito empreendedor e indicação"], ["E-commerce", "Crescimento constante no país"], ["Sensibilidade", "Alta busca por economia e oportunidade"]].map(([t, d]) => (
              <Cartao key={t} tom="cheio" titulo={t}>{d}</Cartao>
            ))}
          </div>
        </div>
        <div className="relative min-h-[50vh]">
          <Image src="/m/mapa-brasil-luz.jpg" alt="" fill sizes="(min-width:1024px) 38vw, 100vw" className="object-cover" />
        </div>
      </section>

      <Faixa>
        <Titulo tag="Por que agora?" verde>Por Que Esta Empresa Está Surgindo Agora?</Titulo>
        <p className="mt-4 max-w-4xl font-light text-texto">Todo investidor experiente faz a mesma pergunta: por que esta empresa está surgindo agora? Nossa resposta é simples. Porque agora é o primeiro momento em que todos os elementos necessários convergem simultaneamente.</p>
        <div className="mt-8 grid gap-10 md:grid-cols-2">
          {[
            [<Cpu key="1" className="h-8 w-8" />, "Inteligência Artificial", "A IA eliminou gargalos que antes tornavam esse modelo extremamente dependente de mão de obra. Automação. Classificação. Distribuição. Atendimento. Análise. Tudo se tornou exponencialmente mais eficiente."],
            [<ShoppingCart key="2" className="h-8 w-8" />, "Crescimento do E-commerce", "Quanto mais o e-commerce cresce, maior se torna o volume de devoluções. Quanto maior o volume de devoluções, maior se torna o mercado de recommerce."],
            [<UserCheck key="3" className="h-8 w-8" />, "Mudança de Comportamento", "Após a pandemia, milhões de consumidores passaram a comprar online de forma recorrente. Esse comportamento se consolidou."],
            [<Gauge key="4" className="h-8 w-8" />, "Pressão Econômica", "Consumidores buscam economia. Empresas buscam liquidez. Fabricantes buscam distribuição. A Leilão NoZap atua exatamente nessa convergência."],
          ].map(([icone, t, d]) => (
            <div key={t as string} className="flex gap-4">
              <span className="shrink-0 text-accent">{icone}</span>
              <div>
                <p className="font-display text-xl font-light text-accent">{t}</p>
                <p className="mt-2 text-[15px] font-light leading-relaxed text-texto">{d}</p>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-8"><Nota>Acreditamos que a próxima década será marcada pela profissionalização da redistribuição inteligente. Estamos construindo essa infraestrutura antes da consolidação definitiva desse mercado.</Nota></div>
        <div className="mt-12">
          <p className="font-display text-2xl font-light text-white">Mercados bilionários, uma única plataforma</p>
          <div className="mt-6 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            <NumeroGrande valor="R$185B+" rotulo="E-commerce Brasil" sub="volume anual" />
            <NumeroGrande valor="R$40B+" rotulo="Logística reversa" sub="devoluções anuais" />
            <NumeroGrande valor="R$25B+" rotulo="Estoques excedentes" sub="capital represado" />
            <NumeroGrande valor="147M" rotulo="Usuários de WhatsApp" sub="no Brasil" />
          </div>
          <p className="mt-6 text-center text-xs text-muted">
            Estimativas de mercado citadas pela administração <Etiqueta tipo="MANAGEMENT_DATA" pequena /> — fonte, ano e método serão anexados ao data room.
          </p>
        </div>
      </Faixa>

      {/* CAPÍTULO 3 */}
      <Capitulo id="solucao" numero="Capítulo 3" titulo="A Solução" sub={<>Não construímos um marketplace.<br />Construímos uma infraestrutura.</>} imagem="/m/cap3-solucao.jpg" lado="direita">
        <p>Quando começamos a estudar profundamente o mercado, percebemos algo importante. O problema não era falta de produto. O problema não era falta de consumidor. O problema não era falta de tecnologia. O problema era a ausência de uma infraestrutura capaz de conectar todas as partes de forma simples, escalável e inteligente.</p>
        <p>Foi por isso que a Leilão NoZap nunca foi pensada como uma loja. Nunca foi pensada como um aplicativo. Nunca foi pensada apenas como um leilão.</p>
        <p>Desde o primeiro dia, ela foi desenhada para se tornar uma infraestrutura.</p>
      </Capitulo>

      <Faixa>
        <Titulo tag="O modelo">A Infraestrutura que Faltava</Titulo>
        <p className="mt-4 max-w-5xl font-light text-texto">
          Enquanto a maioria das empresas tenta resolver apenas uma etapa do processo, a Leilão NoZap conecta toda a cadeia:{" "}
          <strong className="font-medium text-white">Fabricantes. Distribuidores. Estoques de oportunidade. Produtos de devolução. Arrematantes. Licenciados. Vendedores. Consumidores. Recompra. Nova redistribuição.</strong>{" "}
          O resultado é um sistema que transforma riqueza parada em liquidez distribuída.
        </p>
        <Setas itens={["Fabricante", "Sistema Inteligente de Análise de Lotes", "Marketplace", "Rede de Licenciados / Vendedores / Lojas / Leilão"]} />
        <p className="mt-8 text-center font-medium text-white/90">Mais canais. Mais velocidade. Mais liquidez. Mais distribuição.</p>
        <div className="mt-12 grid items-center gap-8 lg:grid-cols-2">
          <Imagem src="/m/canal-vs-rota.jpg" alt="Comparação entre o canal tradicional de liquidação, com muitos intermediários, e a rota direta da Leilão NoZap" className="aspect-[1440/732]" />
          <div>
            <p className="font-display text-2xl font-light text-accent">Do canal tradicional à rota direta</p>
            <p className="mt-3 text-[15px] font-light leading-relaxed text-texto">
              Hoje: marketplace → centro de distribuição → triagem → estoque → leilão → revendedor → consumidor. Alto custo e burocracia.
              Amanhã: marketplace → Leilão NoZap → consumidor. Menos etapas, mais velocidade, mais margem para fornecedores e licenciados.
            </p>
          </div>
        </div>
      </Faixa>

      <Faixa>
        <Titulo tag="Diferenciais" verde>WhatsApp First Commerce</Titulo>
        <div className="mt-8 grid items-center gap-10 lg:grid-cols-[1.4fr_1fr]">
          <Texto>
            <p>A maioria das empresas continua tentando obrigar o consumidor a mudar seu comportamento. Nós seguimos o comportamento do consumidor.</p>
            <p>O Brasil já escolheu sua principal plataforma de comunicação: o WhatsApp. As pessoas compram pelo WhatsApp, negociam pelo WhatsApp, indicam pelo WhatsApp e recomendam pelo WhatsApp.</p>
            <p>A Leilão NoZap foi construída respeitando essa realidade. Não dependemos do WhatsApp. Utilizamos o WhatsApp como <strong>canal estratégico de relacionamento e distribuição</strong>.</p>
          </Texto>
          <NumeroGrande valor="147M" rotulo="usuários" sub="O Brasil já escolheu" etiqueta="MANAGEMENT_DATA" />
        </div>
        <p className="mt-10 font-display text-2xl font-light text-accent">O poder da indicação</p>
        <Texto className="mt-3">
          <p>A indicação continua sendo a forma mais poderosa de aquisição de clientes do planeta. Antes da internet existia indicação. Depois da internet continua existindo indicação. A tecnologia mudou. O comportamento humano não. Por isso criamos uma infraestrutura capaz de transformar relacionamento em distribuição.</p>
        </Texto>
      </Faixa>

      <Faixa>
        <Titulo tag="Rede de distribuição">Rede de Licenciados e Vendedores</Titulo>
        <div className="mt-10 grid gap-8 md:grid-cols-3">
          <NumeroGrande valor={n(licCargo)} rotulo="Licenciados por cargo" sub="definição em revisão (DEC-3)" etiqueta="VERIFIED" href="/app/prova/LICENSEES_TOTAL" />
          <NumeroGrande valor={n(licRole)} rotulo="Contas com acesso de licenciado" sub="contagem alternativa no sistema" etiqueta="VERIFIED" href="/app/prova/LICENSEES_ROLE" />
          <NumeroGrande valor={n(licAtivo)} rotulo="Ativos nos últimos 30 dias" sub="entraram no app no período" etiqueta="VERIFIED" href="/app/prova/LICENSEES_ACTIVE_30D" />
        </div>
        <p className="mt-4 text-center text-sm font-light text-muted">A edição anterior dizia “80+ licenciados ativos”. Esta edição mostra as três contagens do sistema, com a regra de cada uma.</p>
        <Grade colunas={2} className="mt-10">
          <Cartao tom="lateral" titulo="Rede de Licenciados">A Leilão NoZap não cresce apenas através de mídia. Ela cresce através de pessoas. Cada licenciado se torna um ponto de expansão da companhia. Recebendo treinamento, tecnologia, produtos, suporte, metodologia e inteligência comercial. O resultado é uma expansão descentralizada e altamente escalável.</Cartao>
          <Cartao tom="lateral" titulo="Rede de Vendedores">Além dos licenciados, existe uma segunda camada: os vendedores. Uma estrutura desenhada para permitir que qualquer pessoa possa comercializar produtos utilizando a infraestrutura da companhia. Sem estoque. Sem estrutura própria. Sem necessidade de construir tecnologia.</Cartao>
        </Grade>
      </Faixa>

      <Faixa>
        <Titulo tag="ComparAI — inteligência de lotes" verde>Sistema Inteligente de Análise e Distribuição de Lotes</Titulo>
        <Imagem src="/m/comparai.jpg" alt="Tela do sistema de análise de lotes" className="mt-8 aspect-[16/9]" />
        <Texto className="mt-8">
          <p>A Leilão NoZap identificou um dos maiores gargalos do mercado de recommerce e arrematação. Após a compra de um lote, o operador normalmente precisa executar um processo manual de análise, classificação, precificação, busca de imagens, cadastro de produtos e publicação. Esse processo pode consumir dias ou semanas.</p>
          <p>Para resolver esse problema foi criado o Sistema Inteligente de Análise e Distribuição de Lotes. A solução permite leitura automática de planilhas, classificação de produtos, estimativa de valor de mercado, projeção de lucro, cálculo de margem, análise de viabilidade, importação automática de imagens, geração automática de anúncios e publicação integrada.</p>
          <p><strong>Mais importante do que analisar o lote, a plataforma transforma automaticamente o lote em oportunidade comercial.</strong></p>
        </Texto>
        <div className="mt-8 grid gap-8 md:grid-cols-2">
          {[["01", "Leitura Automática", "Leitura automática de planilhas e classificação de produtos"], ["02", "Análise Inteligente", "Estimativa de valor de mercado, projeção de lucro, cálculo de margem e análise de viabilidade"], ["03", "Importação Automática", "Importação automática de imagens e geração automática de anúncios"], ["04", "Publicação Integrada", "Publicação integrada no marketplace. Centenas de produtos em minutos."]].map(([num, t, d]) => (
            <div key={num}>
              <p className="font-display font-light text-white">{num}</p>
              <div className="mt-2 h-0.5 bg-accent" />
              <p className="mt-3 font-display text-xl font-light text-accent">{t}</p>
              <p className="mt-2 text-[15px] font-light text-texto">{d}</p>
            </div>
          ))}
        </div>
        <div className="mt-8"><Hoje>40 lotes recebidos e processados no sistema entre abril e outubro de 2026</Hoje></div>
      </Faixa>

      <Faixa>
        <Tag>Em operação</Tag>
        <h2 className="mt-3 font-display text-3xl font-light text-white sm:text-[2.6rem]">
          Leilão Inteligente — <span className="text-accent">O Principal Motor de Escala</span>
        </h2>
        <Texto className="mt-6">
          <p>O principal motor de escala da companhia, já em operação no aplicativo. O leilão inteligente transforma uma simples compra em experiência. Ele une economia, oportunidade, entretenimento e liquidez, criando um ambiente de alta participação e engajamento.</p>
          <p>Cada lance reserva o saldo do participante; quem não vence tem a reserva devolvida automaticamente. A experiência é desenhada para transformar expectativa em oportunidade real de compra.</p>
        </Texto>
        <Citacao verde className="mt-6">Nossa filosofia é simples: se vencer o leilão, compra abaixo do mercado. Se não vencer, o saldo reservado volta para a carteira.</Citacao>
        <div className="mt-8 grid overflow-hidden rounded-lg md:grid-cols-2">
          <div className="bg-accent p-6 text-accent-ink">
            <p className="font-display text-xl font-semibold">Se Vencer</p>
            <p className="mt-1 font-medium">Compra abaixo do mercado</p>
          </div>
          <div className="border-t border-black/20 bg-accent p-6 text-accent-ink md:border-l md:border-t-0">
            <p className="font-display text-xl font-semibold">Se Não Vencer</p>
            <p className="mt-1 font-medium">O saldo reservado volta para a carteira</p>
          </div>
        </div>
        <div className="mt-8 flex flex-col gap-2">
          <Hoje href="/app/prova/BIDS_COUNT">{`${n(lancesOut)} lances e ${r(arrOut)} em arremates em outubro (até o dia 16)`}</Hoje>
          <Hoje href="/app/prova/AUCTIONS_PRODUCT_ENDED">{`${n(mes("AUCTIONS_PRODUCT_ENDED", "2026-09-01"))} leilões encerrados em setembro, ${n(mes("AUCTIONS_WITH_WINNER", "2026-09-01"))} com vencedor`}</Hoje>
        </div>
      </Faixa>

      <Faixa>
        <Titulo tag="Múltiplos motores">Uma Empresa. Múltiplos Motores de Crescimento.</Titulo>
        <p className="mt-4 font-light text-texto">A Leilão NoZap não depende de uma única receita. A infraestrutura foi desenhada para gerar crescimento através de múltiplos canais simultâneos:</p>
        <Grade colunas={2} className="mt-8">
          {[
            [<ShoppingBag key="1" className="h-6 w-6" />, "Produtos", "Devoluções e oportunidades", "verde", "VERIFIED"],
            [<Award key="2" className="h-6 w-6" />, "Licenciamento", "Expansão territorial", "azul", "VERIFIED"],
            [<Store key="3" className="h-6 w-6" />, "Marketplace", "Receita sobre movimentação", "verde", "VERIFIED"],
            [<Building2 key="4" className="h-6 w-6" />, "Lojas Físicas", "Exposição e liquidez local", "azul", "MANAGEMENT_DATA"],
            [<Gavel key="5" className="h-6 w-6" />, "Leilão Inteligente", "Principal motor de escala — em operação", "verde", "VERIFIED"],
            [<Rocket key="6" className="h-6 w-6" />, "Live Commerce próprio", "Próximo canal de distribuição", "azul", "FORECAST"],
          ].map(([icone, t, d, tom, et]) => (
            <div key={t as string} className={`rounded-lg border bg-cinza/85 p-6 ${tom === "azul" ? "border-info" : "border-accent"}`}>
              <span className={`flex h-12 w-12 items-center justify-center rounded-full text-white ${tom === "azul" ? "bg-info" : "bg-accent"}`}>{icone}</span>
              <p className="mt-4 font-display text-xl font-light text-white">{t}</p>
              <p className="mt-1 text-[15px] font-light text-texto">{d}</p>
              <div className="mt-3"><Etiqueta tipo={et as string} pequena /></div>
            </div>
          ))}
        </Grade>
        <Citacao className="mt-8 !font-light">A maioria das empresas utiliza pessoas para escalar tecnologia. A Leilão NoZap utiliza tecnologia para escalar pessoas.</Citacao>
      </Faixa>

      {/* CAPÍTULO 4 */}
      <Capitulo id="tecnologia" numero="Capítulo 4" titulo="Arquitetura Tecnológica" verde sub="A Infraestrutura Invisível que Sustenta a Escala" imagem="/m/cap4-tecnologia.jpg">
        <p><strong>A maioria das empresas constrói tecnologia para vender. A Leilão NoZap constrói tecnologia para escalar. Desde o início entendemos que o maior gargalo de crescimento não seria a venda. Seria a operação.</strong></p>
      </Capitulo>

      <Faixa>
        <Titulo tag="Módulos tecnológicos" sub="A Infraestrutura Invisível que Sustenta a Escala">Ecossistema Tecnológico Integrado</Titulo>
        <p className="mt-4 max-w-5xl font-light text-texto">A maioria das empresas constrói tecnologia para vender. A Leilão NoZap constrói tecnologia para escalar. Desde o início entendemos que o maior gargalo de crescimento não seria a venda. Seria a operação. Empresas quebram porque vendem mais do que conseguem entregar. Nós decidimos construir primeiro a infraestrutura. Depois acelerar.</p>
        <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_auto]">
          <Grade colunas={2}>
            <Cartao titulo="Marketplace Proprietário">Centro da operação. Responsável pela distribuição dos produtos. Conecta fornecedores, licenciados, vendedores e consumidores. É o principal canal de liquidez da companhia.</Cartao>
            <Cartao titulo="Sistema de Licenciamento">Permite expansão descentralizada. Cada licenciado recebe tecnologia, treinamento, metodologia, produtos e suporte operacional. Aumentando escala sem necessidade de expansão tradicional.</Cartao>
            <Cartao titulo="CRM Comercial">Centraliza leads, clientes, licenciados, vendedores e histórico comercial. Transformando relacionamento em inteligência operacional.</Cartao>
            <Cartao titulo="Sistema Financeiro">Controla recebimentos, pagamentos, comissionamentos e indicadores. Pagamentos do app conciliados ao centavo com o gateway e os bancos.</Cartao>
            <Cartao titulo="Sistema de Comissionamento">Automatiza toda a lógica de distribuição financeira da companhia. Reduzindo erros. Reduzindo operação manual. Aumentando transparência.</Cartao>
            <Cartao titulo="Dashboard Executivo">Permite acompanhamento em tempo real: vendas, indicadores, licenciados, vendedores e operações.</Cartao>
          </Grade>
          <div className="relative mx-auto hidden aspect-[945/2048] w-56 lg:block">
            <Image src="/m/app-celular.jpg" alt="Tela do aplicativo Leilão NoZap no celular" fill sizes="224px" className="rounded-2xl object-cover" />
          </div>
        </div>
        <div className="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <NumeroGrande valor={loc ? `${Math.round(loc / 1000)}K+` : "—"} rotulo="Linhas de código" cor="verde" etiqueta="VERIFIED" href="/app/prova/TECH_LOC" />
          <NumeroGrande valor="2.033" rotulo="Arquivos" cor="verde" etiqueta="VERIFIED" />
          <NumeroGrande valor={n(contas)} rotulo="Contas de clientes" cor="verde" etiqueta="VERIFIED" href="/app/prova/USERS_REGISTERED" />
          <NumeroGrande valor="1" rotulo="Aplicação própria" cor="verde" etiqueta="VERIFIED" />
        </div>
        <Citacao className="mt-10">“Não usamos tecnologia para substituir pessoas. Usamos tecnologia para multiplicar pessoas.”</Citacao>
      </Faixa>

      <Faixa>
        <Titulo tag="Ecossistema" verde>O Ecossistema Tecnológico Leilão NoZap</Titulo>
        <p className="mt-4 font-medium text-white">A Leilão NoZap não está construindo apenas uma plataforma. Está construindo um ecossistema tecnológico.</p>
        <Grade colunas={2} className="mt-8">
          <Cartao titulo="Leilão NoZap">Infraestrutura principal. Marketplace. Licenciamento. Leilão Inteligente. Distribuição.</Cartao>
          <Cartao titulo="Sistema Inteligente de Análise de Lotes">Ferramenta responsável por transformar planilhas em oportunidades comerciais. Classificação. Precificação. Projeção de lucro. Importação. Publicação. Distribuição.</Cartao>
          <Cartao tom="azul" titulo="ComparAI">Infraestrutura de inteligência do ecossistema. Responsável por potencializar análise de dados, precificação, comparação de mercado e tomada de decisão.</Cartao>
          <Cartao tom="azul" titulo="Top College e X-EOS">Formação executiva e capacitação de licenciados (Top College — Faculty of Entrepreneurs) e a estrutura de operações e expansão que sustenta a rede (X-EOS).</Cartao>
        </Grade>
        <div className="mt-8 flex flex-wrap items-center gap-6">
          {[["/m/eco-comparai.jpg", "ComparAI"], ["/m/eco-topcollege.png", "Top College"], ["/m/eco-xeos.jpg", "X-EOS"]].map(([src, alt]) => (
            <div key={alt} className="relative h-20 w-20 overflow-hidden rounded-xl">
              <Image src={src} alt={alt} fill sizes="80px" className="object-cover" />
            </div>
          ))}
        </div>
      </Faixa>

      {/* CAPÍTULO 5 */}
      <section id="modelo" className="relative isolate scroll-mt-20 overflow-hidden">
        <Image src="/m/cap5-modelo.jpg" alt="" fill sizes="100vw" className="-z-10 object-cover" />
        <div className="absolute inset-0 -z-10 bg-black/85" aria-hidden />
        <Conteiner className="py-20 sm:py-28">
          <Tag>Capítulo 5</Tag>
          <h2 className="mt-4 font-display text-4xl font-light text-white sm:text-6xl">Modelo de Negócio</h2>
          <p className="mt-2 font-display text-2xl font-light text-accent sm:text-3xl">Uma Empresa. Múltiplos Motores de Receita.</p>
          <p className="mt-6 max-w-5xl font-medium text-white">Uma das maiores fragilidades das empresas tradicionais é depender de uma única fonte de faturamento. A Leilão NoZap foi desenhada para crescer através de múltiplos motores simultaneamente.</p>
          <div className="mt-8 overflow-x-auto rounded-lg border border-white/20">
            <table className="w-full min-w-[640px] text-left text-[15px]">
              <thead className="bg-accent text-accent-ink">
                <tr>
                  <th className="px-5 py-3 font-semibold">Motor</th>
                  <th className="px-5 py-3 font-semibold">Status hoje</th>
                  <th className="px-5 py-3 font-semibold">O que o sistema registra</th>
                </tr>
              </thead>
              <tbody className="bg-black/60 font-medium text-white">
                {[
                  ["01 Venda de Produtos", "ativo", `mercadoria vendida e paga: ${r(v("GMV_GOODS"))} em outubro (até 16)`],
                  ["02 Licenciamento", "ativo", "adesões e licenças registradas no app"],
                  ["03 Marketplace", "ativo", `comissão retida: ${r(comissao)} em outubro (até 16)`],
                  ["04 Leilão Inteligente", "ativo", `arremates: ${r(arrOut)} em outubro (até 16)`],
                  ["05 Lojas Físicas", "ativo", "operação informada pela administração"],
                  ["06 Análise de Lotes", "crescendo", "40 lotes processados (abr–out/26)"],
                  ["07 Serviços a Fornecedores", "crescendo", "infraestrutura para fabricantes parceiros"],
                  ["08 ComparAI", "ativo", "consultas de preço em uso"],
                  ["09 Live Commerce próprio", "planejado", "próximo canal"],
                  ["10 Novos canais", "planejado", "expansão para novos ambientes de comunicação"],
                ].map(([m, st, d]) => (
                  <tr key={m} className="border-t border-white/15">
                    <td className="px-5 py-3">{m}</td>
                    <td className={`px-5 py-3 font-semibold ${st === "ativo" ? "text-pill" : st === "crescendo" ? "text-info" : "text-muted"}`}>
                      {st === "ativo" ? "● ATIVO" : st === "crescendo" ? "◐ CRESCENDO" : "○ PLANEJADO"}
                    </td>
                    <td className="px-5 py-3 font-light text-texto">{d}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-6 text-center font-light text-texto">Empresas frágeis possuem uma receita. Empresas resilientes possuem múltiplas receitas.</p>
        </Conteiner>
      </section>

      {/* CAPÍTULO 6 */}
      <Capitulo id="tracao" numero="Capítulo 6" titulo="Tração e Validação" sub="A Empresa Foi Validada Antes da Tecnologia Estar Pronta" imagem="/m/cap6-tracao.jpg" lado="direita">
        <p>Uma das características mais importantes da Leilão NoZap é que a operação foi validada antes da automação completa. Primeiro validamos o mercado. Depois aceleramos a tecnologia.</p>
      </Capitulo>

      <Faixa>
        <Titulo tag="O case dos 600 produtos">O MVP que Validou Tudo</Titulo>
        <div className="mt-8 grid gap-6 md:grid-cols-2">
          <Cartao tom="lateral" titulo="O Experimento">
            <p>Antes de qualquer tecnologia. Antes de qualquer investimento. Antes de qualquer aplicativo. A Leilão NoZap foi validada na prática.</p>
            <p className="mt-3">Mais de 600 produtos foram comercializados a partir da residência do fundador utilizando apenas WhatsApp, Facebook e OLX.</p>
            <p className="mt-3">Sem automação. Sem marketplace próprio. Sem equipe estruturada.</p>
          </Cartao>
          <div>
            <Cartao tom="lateral" titulo="O Resultado">
              <p>O resultado demonstrou algo fundamental.</p>
              <p className="mt-3 font-medium text-white">O mercado já existia. Os consumidores já existiam. A demanda já existia.</p>
              <p className="mt-3">O que faltava era infraestrutura.</p>
            </Cartao>
            <div className="mt-8">
              <NumeroGrande valor="60%+" rotulo="dos produtos vendidos" etiqueta="MANAGEMENT_DATA" />
            </div>
          </div>
        </div>
      </Faixa>

      <Faixa>
        <Titulo tag="Evolução da receita">Da Operação Manual ao Aplicativo</Titulo>
        <p className="mt-4 max-w-5xl font-light text-texto">
          Antes do aplicativo, a operação vendia por WhatsApp e loja física, com lançamento manual. A partir de agosto de 2026 a venda passa a ser registrada pelo próprio sistema — e é essa série que vale como número oficial.
        </p>
        <div className="mt-10 grid grid-cols-1 gap-10 lg:grid-cols-[1.5fr_1fr]">
          <div>
            <GraficoBarras titulo="Receita declarada na edição anterior (R$) — nov/25 a mai/26" dados={SERIE_DECLARADA.map(([rot, val]) => ({ rotulo: rot, valor: val, tom: "gestao" as const }))} formato={kmil} />
            <p className="mt-2 text-xs text-muted">
              <Etiqueta tipo="MANAGEMENT_DATA" pequena /> Operação manual, antes do app; sem rastro no sistema. Crescimento de nov/25 a mai/26: +1.008%.
            </p>
          </div>
          <div>
            <GraficoBarras titulo="Entradas pagas no aplicativo (R$) — série oficial" dados={entradas.map((x) => ({ rotulo: mesCurto(x.periodo), valor: x.valor, tom: "verificado" as const }))} formato={kmil} />
            <p className="mt-2 text-xs text-muted">
              <Etiqueta tipo="VERIFIED" pequena /> Inclui depósitos de carteira (que são saldo do cliente, não receita). Mercadoria vendida e paga:{" "}
              {gmv.map((x) => `${mesCurto(x.periodo)} ${x.valor !== null ? brlMil(x.valor) : "—"}`).join(" · ")}. Outubro até o dia 16.
            </p>
          </div>
        </div>
        <Citacao verde className="mt-10">Não estamos validando uma hipótese. Estamos acelerando uma hipótese já validada.</Citacao>
        <div className="mt-8 grid gap-8 sm:grid-cols-3">
          <NumeroGrande valor={n(pagantes)} rotulo="Clientes pagantes" sub="últimos 90 dias" etiqueta="VERIFIED" href="/app/prova/CUSTOMERS_PAYING_90D" />
          <NumeroGrande valor={n(recorrentes)} rotulo="Compraram 2+ vezes" sub="desde junho de 2026" etiqueta="VERIFIED" href="/app/prova/BUYERS_REPEAT" />
          <NumeroGrande valor={estoque !== null ? brlMil(estoque) : "—"} rotulo="Estoque a custo" sub="posição de 17/10/2026" etiqueta="VERIFIED" href="/app/prova/INVENTORY_AT_COST" />
        </div>
      </Faixa>

      <Faixa>
        <Titulo tag="Infraestrutura física">Expansão Física em Andamento</Titulo>
        <Grade colunas={2} className="mt-8">
          <Cartao tom="escuro" titulo="Loja física em Senador Camará">Operação ativa com exposição de produtos e atendimento presencial</Cartao>
          <Cartao tom="escuro" titulo="Operação integrada em Bangu">Operação integrada com logística e distribuição em andamento</Cartao>
          <Cartao tom="escuro" titulo="Expansão em andamento">Novas unidades em processo de abertura e estruturação</Cartao>
          <Cartao tom="escuro" titulo="Centro de distribuição planejado">CD estruturado para suportar escala nacional</Cartao>
        </Grade>
        <p className="mt-3 text-xs text-muted"><Etiqueta tipo="MANAGEMENT_DATA" pequena /> Endereços, contratos e venda por loja entram no data room.</p>
        <Citacao className="mt-8 !font-light">
          <strong className="font-semibold">Meta Dezembro 2026:</strong> 300 licenciados ativos. 8 lojas físicas. Distribuidor Recreio. Faturamento superior a <span className="font-semibold text-accent">R$ 1 milhão por mês.</span>
        </Citacao>
      </Faixa>

      {/* CAPÍTULO 7 */}
      <Capitulo id="governanca" numero="Capítulo 7" titulo={<>Governança, Cultura e<br />Desenvolvimento Humano</>} verde sub="O Principal Produto da Companhia Não é a Tecnologia" imagem="/m/cap7-governanca.jpg">
        <p>Existe uma crença comum no mercado de startups: que tecnologia é o principal ativo. Nós discordamos. Tecnologia acelera. Pessoas constroem. Acreditamos que o principal produto do mundo continua sendo o ser humano.</p>
      </Capitulo>

      <Faixa>
        <Titulo tag="Governança executiva">Estrutura de Formação — Evolução por Desenvolvimento, Não Apenas por Cargo</Titulo>
        <p className="mt-4 font-light text-texto">A evolução dentro da companhia não acontece apenas por cargo. Acontece por desenvolvimento.</p>
        <ol className="mt-8 space-y-2">
          {[
            ["NÍVEL 8 — CONSELHO ESTRATÉGICO", "", "text-accent"],
            ["NÍVEL 7 — MENTALIDADE DO CEO", "Formação de novos fundadores", "text-accent"],
            ["NÍVEL 6 — DIRETORIA EXECUTIVA", "Convite · Resultado · Cultura", "text-info"],
            ["NÍVEL 5 — MENTALIDADE DO DIRETOR", "Gestão sistêmica · 3 meses", "text-info"],
            ["NÍVEL 4 — DIRETOR OPERACIONAL", "", "text-white"],
            ["NÍVEL 3 — MENTALIDADE DO EXECUTIVO", "Liderança · 6 meses", "text-white"],
            ["NÍVEL 2 — LICENCIADO", "Gestão comercial · Distribuição", "text-muted"],
            ["NÍVEL 1 — VENDEDOR", "Produto · Vendas · Relacionamento", "text-muted"],
          ].map(([t, d, cor], i, arr) => (
            <li key={t}>
              <div className="rounded-lg bg-surface px-5 py-4 text-center">
                <p className={`font-semibold ${cor}`}>{t}</p>
                {d && <p className="mt-1 font-light text-texto">{d}</p>}
              </div>
              {i < arr.length - 1 && <p className="py-1 text-center text-accent" aria-hidden>▲</p>}
            </li>
          ))}
        </ol>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[["Conselho", "Visão & Cultura", "bg-accent text-accent-ink"], ["Executivos", "Resultado & Gestão", "bg-info text-black"], ["Operacional", "Liderança em Formação", "bg-zinc-600 text-white"], ["Rede", "Comercial & Vendas", "bg-zinc-800 text-white"]].map(([t, d, c]) => (
            <div key={t} className={`rounded-lg p-5 ${c}`}>
              <p className="font-display text-xl font-semibold">{t}</p>
              <p className="mt-1 font-medium">{d}</p>
            </div>
          ))}
        </div>
        <p className="mt-4 text-xs text-muted"><Etiqueta tipo="VERIFIED" pequena /> A escala de oito níveis é a mesma gravada no cadastro de carreira do aplicativo.</p>
      </Faixa>

      <Faixa>
        <Titulo tag="Filosofia">Nossa Filosofia de Formação</Titulo>
        <Grade colunas={2} className="mt-8">
          <Cartao tom="escuro" titulo="A Escola da Leilão NoZap">A maioria das empresas possui treinamento. A Leilão NoZap foi construída para ser uma escola. Uma escola de vendas, liderança, gestão, tecnologia, empreendedorismo e desenvolvimento humano. Porque empresas crescem na velocidade dos seus líderes — não dos seus sistemas.</Cartao>
          <Cartao tom="escuro" titulo="Distribuição Global">
            <p>A companhia possui uma filosofia própria de reconhecimento.</p>
            <p className="mt-3 font-medium text-accent">1% do faturamento bruto global</p>
            <p className="mt-3">é destinado ao ecossistema de fundadores através da infraestrutura interna de distribuição. Essa política fortalece alinhamento de longo prazo entre crescimento da companhia e geração de valor para quem ajudou a construí-la.</p>
          </Cartao>
          <Cartao tom="escuro" titulo="Nossa Convicção">A maioria das startups tenta construir tecnologia. Nós tentamos construir líderes. Porque líderes constroem empresas. Empresas constroem mercados. E mercados transformam sociedades.</Cartao>
          <Cartao tom="escuro" titulo="Diretoria executiva e conselho">
            <ul className="space-y-1">
              <li><strong className="font-medium text-white">Luiz Sant’Anna</strong> — CEO, fundador e conselheiro</li>
              <li><strong className="font-medium text-white">Elohá Sant’Anna</strong> — co-fundadora e conselheira</li>
              <li><strong className="font-medium text-white">Diogo Archanjo</strong> — diretor de tecnologia</li>
              <li><strong className="font-medium text-white">Flávio Monteiro</strong> — diretor jurídico</li>
              <li><strong className="font-medium text-white">Luciano Pinheiro</strong> — diretor de captação</li>
              <li><strong className="font-medium text-white">José Amâncio</strong> — diretor de relacionamento</li>
              <li><strong className="font-medium text-white">Luciene Soares</strong> — fundadora e conselheira</li>
            </ul>
            <Link href="/app/governanca" className="mt-3 inline-block text-sm text-pill underline underline-offset-2">Ver governança completa</Link>
          </Cartao>
        </Grade>
      </Faixa>

      <Faixa>
        <Titulo tag="Estrutura de fundadores">Fundador vs. Sócio: Conceitos Diferentes</Titulo>
        <p className="mt-4 font-light text-texto">Uma das características mais singulares da Leilão NoZap é a diferenciação entre fundador e sócio.</p>
        <div className="mt-8 grid overflow-hidden rounded-lg border border-white/20 md:grid-cols-2">
          <div className="p-6">
            <p className="font-display text-xl font-light text-accent">Fundador</p>
            <p className="mt-2 text-[15px] font-light text-texto">Representa quem participou da construção da companhia em sua fase inicial. O título reconhece contribuição, construção e alinhamento com a visão.</p>
          </div>
          <div className="border-t border-white/20 p-6 md:border-l md:border-t-0">
            <p className="font-display text-xl font-light text-accent">Sócio</p>
            <p className="mt-2 text-[15px] font-light text-texto">Participação societária segue critérios tradicionais de mercado: Valuation. Investimento. Aquisição formal de participação.</p>
          </div>
        </div>
        <Grade colunas={2} className="mt-5">
          <Cartao tom="escuro" titulo="Filosofia">Nem todo fundador é sócio. Nem todo sócio é fundador. São conceitos diferentes.</Cartao>
          <Cartao tom="escuro" titulo="Reconhecimento">Executivos formados antes do lançamento oficial poderão receber reconhecimento como fundadores da companhia.</Cartao>
        </Grade>
      </Faixa>

      {/* CAPÍTULO 8 */}
      <Capitulo id="barreiras" numero="Capítulo 8" titulo="O Que Não Pode Ser Copiado" sub="As Verdadeiras Barreiras Competitivas" imagem="/m/cap8-barreiras.jpg" lado="direita">
        <p>Copiar tecnologia é relativamente fácil. Copiar cultura é extremamente difícil.</p>
      </Capitulo>

      <Faixa>
        <Titulo tag="Barreiras competitivas">12 Barreiras que Protegem a Companhia</Titulo>
        <p className="mt-4 max-w-5xl font-light text-texto">Muitos investidores perguntam: <em>“O que impede alguém de copiar a Leilão NoZap?”</em> Nossa resposta é simples. Copiar tecnologia é relativamente fácil. Copiar cultura é extremamente difícil.</p>
        <div className="mt-6 grid gap-x-5 gap-y-4 md:grid-cols-2">
          {[
            ["Capital Intelectual do Fundador", "A companhia não nasceu do zero. Ela nasceu da combinação de militarismo, telecomunicações, franquias, marketing de relacionamento, mercado financeiro, startups e desenvolvimento humano. Mais de duas décadas de experiência condensadas em um único modelo."],
            ["Cultura", "Cultura não se compra. Não se terceiriza. Não se programa. É construída diariamente."],
            ["X-EOS", "Metodologia própria de desenvolvimento humano, liderança e expansão. Base da formação executiva da companhia. Desenvolvida e refinada ao longo de mais de duas décadas."],
            ["Mentalidade do Executivo", "Trilha que forma o principal sistema de crescimento interno da companhia."],
            ["Mentalidade do Diretor", "Trilha que forma o principal sistema de crescimento interno da companhia."],
            ["Mentalidade do CEO", "Essas três trilhas formam o principal sistema de crescimento interno da companhia."],
            ["Rede de Licenciados", "A infraestrutura cresce de dentro para fora. Assim como grandes comunidades e movimentos. Essa expansão não depende exclusivamente de mídia paga."],
            ["Comunidade", "A Leilão NoZap não possui apenas clientes. Possui uma comunidade — que combina tecnologia, comércio e desenvolvimento humano em um modelo difícil de replicar."],
            ["Sistema Inteligente de Análise de Lotes", "Não é apenas uma ferramenta. É um motor de inteligência para todo o mercado de recommerce."],
            ["Integração Tecnológica", "Marketplace. CRM. Financeiro. Comissionamento. Leilão. Analisador. Tudo conectado."],
            ["Vale do Recreio", "A Leilão NoZap não é uma empresa isolada. É a primeira empresa operacional do Vale do Recreio."],
            ["Visão de Longo Prazo", "Estamos construindo olhando para 2035. Enquanto a maioria olha para o próximo trimestre."],
          ].map(([t, d], i) => (
            <CartaoNumerado key={t} n={i + 1} titulo={t}>{d}</CartaoNumerado>
          ))}
        </div>
        <Citacao className="mt-10 !font-light">Tecnologia pode ser copiada. Produtos podem ser copiados. Preços podem ser copiados. Mas <strong className="font-semibold">visão, cultura, liderança e execução</strong> são muito mais difíceis de replicar.</Citacao>
      </Faixa>

      {/* CAPÍTULO 9 */}
      <section id="valuation" className="relative isolate scroll-mt-20 overflow-hidden text-center">
        <Image src="/m/cap9-valuation.jpg" alt="" fill sizes="100vw" className="-z-10 object-cover" />
        <div className="absolute inset-0 -z-10 bg-black/80" aria-hidden />
        <Conteiner className="py-20 sm:py-28">
          <div className="text-left"><Tag>Capítulo 9 — Valuation</Tag></div>
          <div className="relative mx-auto mt-6 aspect-[610/900] w-52 sm:w-72">
            <Image src="/m/logo.png" alt="Leilão NoZap" fill sizes="288px" className="object-contain" />
          </div>
          <p className="mt-10 font-display text-4xl font-light text-white">Valuation</p>
          <p className="mt-2 font-display text-2xl font-light text-white/90">Por Que R$ 25 Milhões?</p>
          <p className="num mt-8 font-display text-5xl font-bold tracking-tight text-accent sm:text-8xl">R$ 25.000.000</p>
          <div className="mt-4"><SeloReferencia /></div>
          <p className="mx-auto mt-6 max-w-4xl font-light text-texto">
            Uma das perguntas mais importantes para qualquer investidor é: por que essa empresa vale R$ 25 milhões? A resposta não está em uma única variável. Ela está na combinação dos ativos — e, a partir desta edição, cada ativo traz ao lado o número que o sistema mede hoje.
          </p>
        </Conteiner>
      </section>

      <Faixa>
        <Titulo tag="Composição do valuation">Os Ativos que Compõem o Valuation</Titulo>
        <Grade colunas={2} className="mt-8">
          <Cartao tom="lateral" titulo="Ativo 01 — Tecnologia" rodape={<Hoje href="/app/prova/TECH_LOC">{`${n(loc)} linhas em 2.033 arquivos`}</Hoje>}>
            Código próprio sobre infraestrutura de mercado. Marketplace. Aplicativos. IA. Analisador. CRM. Comissionamento. Leilão Inteligente.
          </Cartao>
          <Cartao tom="lateral" titulo="Ativo 02 — Operação Validada" rodape={<Hoje href="/app/prova/CASH_IN_GROSS">{`${r(entSet)} em entradas no app em setembro; ${n(pagantes)} clientes pagantes em 90 dias`}</Hoje>}>
            Mercado validado. Clientes reais. Vendas reais, pagas e conciliadas com o gateway e os bancos.
          </Cartao>
          <Cartao tom="lateral" titulo="Ativo 03 — Capital Intelectual" rodape={<Hoje etiqueta="MANAGEMENT_DATA">trajetória do fundador e da diretoria; documentação no data room</Hoje>}>
            Mais de 20 anos de experiência aplicada em diferentes mercados e estruturas. Crédito: originação e comercialização de mais de R$ 100 milhões, com aproximadamente R$ 40 milhões aprovados. Investimentos: captação de mais de R$ 22 milhões com equipe enxuta e operação totalmente digital. Liderança: participação na formação e desenvolvimento de mais de 30 mil pessoas em mais de 20 estados.
          </Cartao>
          <Cartao tom="lateral" titulo="Ativo 04 — Rede Comercial" rodape={<Hoje href="/app/prova/LICENSEES_TOTAL">{`${n(licCargo)} licenciados por cargo · ${n(licAtivo)} ativos em 30 dias · ${n(contas)} contas de clientes`}</Hoje>}>
            Licenciados. Executivos. Vendedores. Parceiros.
          </Cartao>
          <Cartao tom="lateral" titulo="Ativo 05 — Metodologia" rodape={<Hoje etiqueta="MANAGEMENT_DATA">ativo qualitativo — entra no scorecard do valuation</Hoje>}>
            X-EOS. Mentalidade do Executivo. Mentalidade do Diretor. Mentalidade do CEO.
          </Cartao>
          <Cartao tom="lateral" titulo="Ativo 06 — Ecossistema" rodape={<Hoje href="/app/prova/INVENTORY_AT_COST">{`estoque a custo de ${r(estoque)}`}</Hoje>}>
            Leilão NoZap. ComparAI. Top College. X-EOS. Vale do Recreio.
          </Cartao>
          <Cartao tom="lateral" titulo="Ativo 07 — Potencial de Escala" rodape={<Hoje etiqueta="FORECAST">meta de dez/2026: R$ 1 milhão por mês</Hoje>}>
            O valuation atual considera principalmente o que já foi construído. Não o que poderá ser capturado integralmente.
          </Cartao>
          <Cartao tom="verde" titulo="Valuation independente">
            <p>Com os dados reais em mãos, este portal calcula o valor por nove métodos — múltiplos, transações, método VC, soma das partes, fluxo de caixa, custo de reposição — com pesos fixados antes de ver o resultado.</p>
            <Link href="/app/valuation" className="mt-4 inline-flex rounded-md bg-accent px-4 py-2 text-sm font-semibold text-accent-ink hover:brightness-110">Ver metodologia e ponte do valor</Link>
          </Cartao>
        </Grade>
      </Faixa>

      <Faixa>
        <Titulo tag="Potencial não precificado">O Que Ainda Não Está Precificado Integralmente</Titulo>
        <Grade colunas={2} className="mt-8">
          <Cartao titulo="Expansão Nacional">Escala para todo o território brasileiro ainda não capturada no valuation atual</Cartao>
          <Cartao titulo="Live Commerce próprio">Canal de vendas ao vivo integrado ao leilão e ao marketplace</Cartao>
          <Cartao titulo="Novos canais de distribuição">Expansão para novos ambientes de comunicação digital — a mesma tese, mais alcance</Cartao>
          <Cartao titulo="Aceleração do ComparAI">ComparAI como infraestrutura de inteligência central do ecossistema</Cartao>
          <Cartao titulo="Novos Módulos">Expansão tecnológica com novos módulos e funcionalidades em desenvolvimento</Cartao>
          <Cartao titulo="Internacionalização">Expansão para mercados internacionais com a infraestrutura já construída</Cartao>
        </Grade>
        <p className="mt-4 text-xs text-muted"><Etiqueta tipo="FORECAST" pequena /> Opções de crescimento: entram no valuation como cenário, nunca como valor atual.</p>
      </Faixa>

      <section className="relative isolate overflow-hidden text-center">
        <Image src="/m/verdade-atemporal.jpg" alt="" fill sizes="100vw" className="-z-10 object-cover" />
        <div className="absolute inset-0 -z-10 bg-black/75" aria-hidden />
        <Conteiner className="py-24">
          <Tag>Verdade atemporal</Tag>
          <p className="mt-6 font-display text-5xl font-light leading-tight text-accent sm:text-7xl">Compra e Venda Existem Desde que o Mundo é Mundo.</p>
          <p className="mx-auto mt-8 max-w-4xl font-medium text-white">Ao longo da história, tecnologias surgiram. Empresas nasceram e desapareceram. Mercados evoluíram. Mas existe uma atividade que permaneceu constante: compra e venda. O ser humano troca valor desde o início da civilização.</p>
          <Citacao className="mx-auto mt-8 max-w-4xl text-left">As ferramentas mudam. A necessidade de comercializar continua. Por isso acreditamos que a Leilão NoZap está posicionada em um comportamento permanente da humanidade.</Citacao>
        </Conteiner>
      </section>

      {/* CAPÍTULO 10 */}
      <section id="roadmap" className="relative isolate scroll-mt-20 overflow-hidden">
        <Image src="/m/textura.jpg" alt="" fill sizes="100vw" className="-z-10 object-cover" />
        <Conteiner className="py-20 sm:py-28">
          <Tag>Capítulo 10</Tag>
          <h2 className="mt-4 font-display text-4xl font-light text-accent sm:text-6xl">Roadmap 2026</h2>
          <p className="mt-2 font-display text-2xl font-light text-white sm:text-3xl">Objetivos Estratégicos até o Lançamento Oficial</p>
          <div className="mt-10 grid gap-5 md:grid-cols-2">
            <Cartao tom="cinza" titulo="Expansão Comercial" rodape={<Hoje href="/app/prova/LICENSEES_ACTIVE_30D">{`${n(licAtivo)} licenciados ativos em 30 dias`}</Hoje>}>300 licenciados ativos. Crescimento contínuo da rede de vendedores em todo o Brasil.</Cartao>
            <Cartao tom="cinza" titulo="Expansão Física" rodape={<Hoje etiqueta="MANAGEMENT_DATA">loja em Senador Camará e operação em Bangu</Hoje>}>8 lojas físicas. Distribuidor Recreio. Presença física consolidada.</Cartao>
            <Cartao tom="cinza" titulo="Expansão Tecnológica" rodape={<Hoje>aplicativo em produção; leilão inteligente em operação</Hoje>}>Lançamento oficial do aplicativo. Ativação plena do Leilão Inteligente. Automação dos processos internos.</Cartao>
            <div className="rounded-lg border border-accent/50 bg-cinza/85 p-6">
              <p className="font-display text-xl font-light text-accent">Meta Financeira</p>
              <p className="num mt-2 font-display text-5xl font-light text-accent">R$ 1.000.000+/mês</p>
              <div className="mt-4 h-2.5 overflow-hidden rounded-full bg-black/50">
                <div className="h-full rounded-full bg-accent" style={{ width: `${Math.max(1, Math.min(100, ((entSet ?? 0) / 1_000_000) * 100))}%` }} />
              </div>
              <p className="mt-2 text-sm font-light text-texto">Melhor mês no app até hoje: {r(entSet)} em entradas (set/26) — {(((entSet ?? 0) / 1_000_000) * 100).toLocaleString("pt-BR", { maximumFractionDigits: 1 })}% da meta.</p>
              <div className="mt-3 flex gap-2"><Etiqueta tipo="FORECAST" pequena /><Etiqueta tipo="VERIFIED" pequena /></div>
            </div>
          </div>
        </Conteiner>
      </section>

      <Faixa>
        <Titulo tag="Projeção financeira">Projeção de Receita 2026–2028</Titulo>
        <GraficoBarras titulo="Receita projetada pela administração (R$ milhões)" dados={[{ rotulo: "2026", valor: 12, tom: "projecao" }, { rotulo: "2027", valor: 36, tom: "projecao" }, { rotulo: "2028", valor: 96, tom: "projecao" }]} formato={(x) => `${Math.round(x)}`} className="max-w-3xl" />
        <p className="mt-4 font-light text-texto">Crescimento projetado com base na ativação progressiva dos múltiplos motores de receita: marketplace, licenciados, leilão inteligente, live commerce e expansão física.</p>
        <p className="mt-2 text-xs text-muted">
          <Etiqueta tipo="FORECAST" pequena /> Projeção da administração. A previsão por alavancas do sistema — licenciados × vendas × ticket × margem — está em{" "}
          <Link href="/app/roadmap" className="text-pill underline underline-offset-2">Metas e simulação</Link>.
        </p>
      </Faixa>

      {/* CAPÍTULO 11 */}
      <Capitulo id="visao" numero="Capítulo 11" titulo="Visão 2035" verde sub="O Futuro Que Estamos Construindo" imagem="/m/cap11-visao.jpg">
        <p>A maioria das empresas nasce para resolver um problema. A Leilão NoZap nasceu para participar de uma transformação.</p>
        <p>Acreditamos que estamos entrando em uma nova era. Uma era onde inteligência artificial, automação, conectividade, distribuição digital e <strong>desenvolvimento humano irão redefinir a forma como as pessoas trabalham, empreendem e geram riqueza.</strong></p>
        <p><strong>A pergunta não é se essa transformação acontecerá. Ela já começou.</strong></p>
        <p><strong>A pergunta é: quem será beneficiado por ela?</strong></p>
      </Capitulo>

      <Faixa>
        <Tag>Visão 2035</Tag>
        <h2 className="mt-3 font-display text-3xl font-semibold text-white sm:text-4xl">Tecnologia Para o Bem</h2>
        <p className="mt-4 max-w-5xl font-light text-texto">Existe uma preocupação crescente em todo o mundo. A ascensão da Inteligência Artificial. A automação de processos. A substituição de funções humanas. Milhões de pessoas perguntam: <em>“O que acontecerá comigo?”</em> Nossa visão é diferente. Acreditamos que a tecnologia não deve substituir pessoas. A tecnologia deve potencializar pessoas.</p>
        <Grade colunas={2} className="mt-8">
          <Cartao tom="escuro" titulo="O Principal Ativo do Mundo">
            <p>Ao longo da nossa trajetória chegamos a uma conclusão. O principal ativo do planeta não é petróleo, ouro, imóveis, tecnologia ou capital financeiro. O principal ativo do planeta é o ser humano.</p>
            <p className="mt-3">Por isso acreditamos que o futuro pertence às organizações capazes de desenvolver pessoas na mesma velocidade em que avançam tecnologicamente.</p>
          </Cartao>
          <Cartao tom="escuro" titulo="Uma Nova Categoria de Empresa">
            <p>A Leilão NoZap não quer ser apenas um marketplace, um aplicativo ou uma plataforma de leilão. Quer ser o sistema central de um novo mercado.</p>
            <p className="mt-3">Um sistema onde fabricantes prosperam. Distribuidores prosperam. Empreendedores prosperam. Consumidores prosperam. Pessoas prosperam.</p>
          </Cartao>
        </Grade>
      </Faixa>

      <Faixa>
        <Titulo tag="Futuro do recommerce">O Recommerce Será uma Categoria Dominante</Titulo>
        <div className="mt-8 grid gap-10 md:grid-cols-3">
          {[
            [<Recycle key="1" className="h-11 w-11" />, "Futuro da Distribuição", "Mais inteligente, automatizada e descentralizada. Empresas buscam liquidez, fabricantes buscam distribuição, consumidores buscam economia, empreendedores buscam oportunidade."],
            [<Package key="2" className="h-11 w-11" />, "Futuro do Recommerce", "Produtos devolvidos, open box, recondicionados e excedentes farão parte do consumo cotidiano, consolidando no Brasil a transformação já observada em mercados internacionais."],
            [<User key="3" className="h-11 w-11" />, "Futuro da Geração de Renda", "A próxima geração de empreendedores nascerá em plataformas inteligentes — pessoas comuns gerando renda e construindo negócios sem as barreiras tradicionais."],
          ].map(([icone, t, d]) => (
            <div key={t as string}>
              <span className="text-accent">{icone}</span>
              <p className="mt-4 font-display text-xl font-light text-accent">{t}</p>
              <p className="mt-2 text-[15px] font-light leading-relaxed text-texto">{d}</p>
            </div>
          ))}
        </div>
      </Faixa>

      <Faixa>
        <Titulo tag="Vale do Recreio">O Vale do Recreio: Onde a Escassez Será Escassa</Titulo>
        <Imagem src="/m/vale-recreio.jpg" alt="Vista noturna de uma cidade conectada por linhas de dados" className="mt-8 aspect-[16/9]" />
        <Texto className="mt-8">
          <p>A Leilão NoZap é a primeira empresa operacional de um projeto maior: o <strong>Vale do Recreio</strong>. Uma iniciativa criada para demonstrar que o Brasil pode criar empresas tecnológicas de classe mundial.</p>
          <p>Assim como o Vale do Silício se tornou referência global em inovação, acreditamos que o Brasil também pode se tornar referência em tecnologia aplicada ao desenvolvimento humano.</p>
          <p>O lema do Vale do Recreio resume nossa visão: <strong>onde a escassez será escassa.</strong></p>
        </Texto>
        <Citacao className="mt-6 !font-light">Não se trata apenas de riqueza financeira. Trata-se de acesso. Acesso à tecnologia. Acesso ao conhecimento. Acesso à oportunidade. Acesso ao desenvolvimento.</Citacao>
        <div className="my-10 h-px bg-white/20" />
        <p className="font-display text-2xl font-light text-accent">Live commerce e visão global</p>
        <Texto className="mt-3">
          <p>Acreditamos que uma das maiores transformações do varejo mundial continuará sendo a convergência entre entretenimento, relacionamento e comércio. Mercados asiáticos, especialmente a China, já demonstraram a força do live commerce como canal de distribuição. Nossa visão é antecipar essas tendências e adaptá-las à realidade brasileira, com operação própria de vendas ao vivo integrada ao leilão e ao marketplace.</p>
        </Texto>
      </Faixa>

      <Faixa>
        <Titulo tag="O Brasil como referência">O Brasil Pode Criar Empresas Tecnológicas Globais</Titulo>
        <p className="mt-4 max-w-5xl font-light text-texto">
          Acreditamos que o Brasil possui tudo o que é necessário para criar empresas tecnológicas globais. <span className="text-accent">Criatividade. Capacidade comercial. Mercado consumidor. Espírito empreendedor.</span> O que muitas vezes faltou foi <span className="text-accent">infraestrutura</span>. É exatamente isso que estamos construindo.
        </p>
        <p className="mt-8 font-display text-2xl font-light text-white">O Que Queremos Que Digam Sobre Nós</p>
        <p className="mt-3 max-w-5xl font-light text-texto">Esperamos que no futuro a Leilão NoZap seja lembrada não apenas pelos produtos que vendeu. Nem pela tecnologia que criou. Mas pelo impacto que gerou. Que seja reconhecida como uma empresa que demonstrou que tecnologia pode servir ao ser humano. Que criou oportunidades. Que formou líderes. Que desenvolveu pessoas. Que transformou riqueza parada em prosperidade distribuída.</p>
        <Citacao className="mt-6 !font-light">
          Assim como o <span className="text-accent">PIX</span> criou uma nova camada para pagamentos, e o <span className="text-accent">WhatsApp</span> redefiniu a comunicação no Brasil, a <span className="text-accent">Leilão NoZap</span> está construindo a espinha dorsal da redistribuição inteligente, da formação de líderes e da prosperidade distribuída.
        </Citacao>
      </Faixa>

      {/* CAPÍTULO 12 */}
      <section id="investimento" className="grid scroll-mt-20 lg:grid-cols-[minmax(0,62%)_minmax(0,38%)]">
        <div className="bg-[#070707] px-5 py-16 sm:px-12 lg:px-16">
          <Tag>Capítulo 12</Tag>
          <h2 className="mt-4 font-display text-4xl font-light text-white sm:text-5xl">Oportunidade de Investimento</h2>
          <p className="mt-2 font-display text-2xl font-light text-white sm:text-3xl">Algumas Janelas Não Permanecem Abertas Por Muito Tempo</p>
          <Texto className="mt-6">
            <p>Ao longo da história, os maiores retornos financeiros normalmente foram capturados por investidores que conseguiram identificar tendências antes de se tornarem consenso.</p>
            <p>Antes do <span className="text-accent">Uber</span> se tornar Uber. Antes do <span className="text-accent">Airbnb</span> se tornar Airbnb. Antes do <span className="text-accent">Mercado Livre</span> se tornar Mercado Livre. Antes do <span className="text-accent">Nubank</span> se tornar Nubank.</p>
            <p>O maior retorno raramente acontece quando todos já acreditam. O maior retorno acontece quando poucos conseguem enxergar.</p>
          </Texto>
          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            <div className="rounded-lg border-2 border-white/25 p-5">
              <p className="font-display text-xl font-light text-accent">A Assimetria</p>
              <p className="mt-2 text-[15px] font-light leading-relaxed text-texto">Todo investidor procura assimetria. Baixo risco relativo. Alto potencial de crescimento. Parte relevante dos riscos já foi reduzida através da validação prática. Mas grande parte da expansão ainda está à frente.</p>
            </div>
            <div className="rounded-lg border-2 border-white/25 p-5">
              <p className="font-display text-xl font-light text-accent">O Efeito de Rede</p>
              <p className="mt-2 text-[15px] font-medium leading-relaxed text-white">Mais vendedores → Mais produtos → Mais consumidores → Mais liquidez → Mais fornecedores → Mais oportunidades → Mais crescimento.</p>
              <p className="mt-2 text-[15px] font-light text-texto">Esse ciclo cria um efeito cumulativo difícil de interromper.</p>
            </div>
          </div>
        </div>
        <div className="relative min-h-[50vh]">
          <Image src="/m/cap12-investimento.jpg" alt="" fill sizes="(min-width:1024px) 38vw, 100vw" className="object-cover" />
        </div>
      </section>

      <Faixa>
        <Titulo tag="O que existe hoje">A Leilão NoZap Não é uma Ideia. É uma Realidade.</Titulo>
        <p className="mt-4 font-light text-texto">A Leilão NoZap não é uma ideia. Não é um PowerPoint. Não é uma projeção. A companhia já possui — e cada item diz se foi conferido no sistema:</p>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            [<CircleCheck key="1" className="h-6 w-6" />, "Operação Validada", "VERIFIED"],
            [<CircleCheck key="2" className="h-6 w-6" />, "Vendas Pagas no App", "VERIFIED"],
            [<Cpu key="3" className="h-6 w-6" />, "Tecnologia Própria", "VERIFIED"],
            [<Store key="4" className="h-6 w-6" />, "Marketplace Próprio", "VERIFIED"],
            [<Gavel key="5" className="h-6 w-6" />, "Leilão em Operação", "VERIFIED"],
            [<Check key="6" className="h-6 w-6" />, "Rede Comercial", "VERIFIED"],
            [<BadgeCheck key="7" className="h-6 w-6" />, "Licenciados", "VERIFIED"],
            [<Building2 key="8" className="h-6 w-6" />, "Lojas Físicas", "MANAGEMENT_DATA"],
            [<ShieldCheck key="9" className="h-6 w-6" />, "Diretoria Estruturada", "MANAGEMENT_DATA"],
            [<Network key="10" className="h-6 w-6" />, "Conselho Estratégico", "MANAGEMENT_DATA"],
            [<Layers key="11" className="h-6 w-6" />, "Metodologia Proprietária", "MANAGEMENT_DATA"],
            [<Workflow key="12" className="h-6 w-6" />, "Infraestrutura Tecnológica Avançada", "VERIFIED"],
          ].map(([icone, t, et]) => (
            <div key={t as string} className="flex flex-col rounded-lg bg-cinza/85 p-5">
              <span className="flex h-12 w-12 items-center justify-center rounded-full bg-black text-white">{icone}</span>
              <p className="mt-4 flex-1 font-display text-lg font-light text-accent">{t}</p>
              <div className="mt-3"><Etiqueta tipo={et as string} pequena /></div>
            </div>
          ))}
        </div>
      </Faixa>

      <Faixa>
        <Titulo tag="A assimetria">Baixo Risco Relativo. Alto Potencial de Crescimento.</Titulo>
        <p className="mt-4 font-light text-texto">Todo investidor procura assimetria. Baixo risco relativo. Alto potencial de crescimento.</p>
        <Grade colunas={2} className="mt-8">
          <Cartao tom="escuro" titulo="Riscos Já Reduzidos">
            <ul className="list-disc space-y-1 pl-5">
              <li>Mercado validado na prática</li>
              <li>Produto com demanda comprovada</li>
              <li>Distribuição testada e funcionando</li>
              <li>Operação com receita real, conciliada</li>
              <li>Cultura aplicada e funcionando</li>
            </ul>
          </Cartao>
          <Cartao tom="escuro" titulo="Expansão Ainda à Frente">
            <ul className="list-disc space-y-1 pl-5">
              <li>Expansão nacional ainda não iniciada</li>
              <li>Lançamento oficial da plataforma</li>
              <li>Escala do leilão inteligente</li>
              <li>Escalabilidade da rede de licenciados</li>
              <li>Massificação do marketplace</li>
              <li>Consolidação da infraestrutura de recommerce</li>
            </ul>
          </Cartao>
        </Grade>
        <div className="mt-10 grid gap-8 lg:grid-cols-2">
          <div>
            <p className="font-display text-2xl font-light text-white">O Papel do Capital</p>
            <p className="mt-4 font-light text-texto">Capital <strong className="font-medium text-white">não</strong> será utilizado para sustentar uma operação deficitária.</p>
            <p className="mt-3 font-light text-texto">Capital <strong className="font-medium text-white">será</strong> utilizado para acelerar uma operação validada.</p>
            <p className="mt-4 text-sm font-light text-muted">Os riscos que ainda existem — e o que reduz cada um — estão em <Link href="/app/riscos" className="text-pill underline underline-offset-2">Riscos</Link>.</p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {["Expansão Comercial", "Aceleração Tecnológica", "Aquisição de Estoque Estratégico", "Ampliação da Rede", "Crescimento das Operações Físicas", "Fortalecimento da Marca"].map((t) => (
              <div key={t} className="rounded-lg border border-white/20 bg-surface p-4 font-display text-lg font-light text-accent">{t}</div>
            ))}
            <div className="rounded-lg border border-white/20 bg-surface p-4 font-display text-lg font-light text-accent sm:col-span-2">Consolidação da Infraestrutura Nacional</div>
          </div>
        </div>
      </Faixa>

      <Faixa>
        <Titulo tag="Efeito de rede">O Ciclo Virtuoso de Crescimento</Titulo>
        <Ciclo
          itens={[
            { titulo: "Mais Produtos", texto: "Maior variedade e volume", icone: <Boxes className="h-6 w-6" /> },
            { titulo: "Mais Consumidores", texto: "Crescimento da base de clientes", icone: <Users className="h-6 w-6" /> },
            { titulo: "Mais Liquidez", texto: "Maior volume de transações", icone: <Droplet className="h-6 w-6" /> },
            { titulo: "Mais Fornecedores", texto: "Atração de novos parceiros", icone: <Factory className="h-6 w-6" /> },
            { titulo: "Mais Crescimento", texto: "Ciclo cumulativo e difícil de interromper", icone: <TrendingUp className="h-6 w-6" /> },
            { titulo: "Mais Vendedores", texto: "Expansão da rede comercial", icone: <UserCheck className="h-6 w-6" /> },
          ]}
        />
      </Faixa>

      {/* MENSAGEM FINAL */}
      <Faixa className="text-center">
        <Tag>Mensagem final</Tag>
        <div className="relative mx-auto mt-8 aspect-[610/900] w-48 sm:w-64">
          <Image src="/m/logo.png" alt="Leilão NoZap" fill sizes="256px" className="object-contain" />
        </div>
        <p className="mt-8 font-display text-3xl font-semibold text-accent">LEILÃO NOZAP</p>
        <p className="mt-3 font-light text-texto">Infraestrutura Brasileira de Recommerce, Distribuição Inteligente e Desenvolvimento Humano</p>
        <div className="mx-auto my-8 h-px max-w-5xl bg-white/25" />
        <div className="prosa mx-auto max-w-5xl border-l-2 border-white/60 pl-6 text-left">
          <p>Quando iniciamos essa jornada, não buscávamos criar apenas mais uma empresa. Buscávamos construir algo capaz de permanecer relevante pelas próximas décadas.</p>
          <p>Algo que gerasse prosperidade. Algo que desenvolvesse pessoas. Algo que criasse oportunidades. Algo que mostrasse que o Brasil pode criar empresas tecnológicas de classe mundial.</p>
          <p>Estamos apenas no começo.</p>
          <p>Mas acreditamos que o futuro pertence às organizações capazes de unir tecnologia, inteligência, execução e propósito em uma mesma direção.</p>
          <p>Essa é a nossa direção.</p>
        </div>
        <div className="mx-auto mt-8 grid max-w-5xl gap-4 text-left sm:grid-cols-2">
          {[["O Mercado", "Já existe."], ["Os Produtos", "Já existem."], ["Os Consumidores", "Já existem."], ["A Infraestrutura", "Está sendo construída — e já opera."]].map(([t, d]) => (
            <div key={t} className="rounded-lg bg-accent p-5 text-accent-ink">
              <p className="font-display text-xl font-semibold">{t}</p>
              <p className="mt-1 font-medium">{d}</p>
            </div>
          ))}
        </div>
        <div className="mx-auto my-8 h-px max-w-5xl bg-white/25" />
        <p className="font-semibold text-accent">Valuation de referência do fundador: R$ 25.000.000</p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <a href={WHATSAPP} target="_blank" rel="noopener noreferrer" className="rounded-md border border-accent px-5 py-3 font-semibold text-pill hover:bg-accent/10">
            Solicitar Reunião Estratégica
          </a>
          <Link href="/app/dataroom" className="rounded-md bg-accent px-5 py-3 font-semibold text-accent-ink hover:brightness-110">
            Acessar Data Room
          </Link>
        </div>
        <p className="mt-8 font-light text-texto">— Luiz Sant’Anna, Fundador e CEO — Leilão NoZap</p>
        <p className="mt-4 text-sm text-muted">Documento Confidencial | Uso Restrito para Investidores</p>
      </Faixa>

      {conselho && (
        <Conteiner className="pb-16">
          <NotaRevisao
            conselho
            itens={[
              "Esta edição substitui a de ~agosto publicada no Gamma. Mantida toda a narrativa; números trocados pelos do sistema com etiqueta.",
              "Retirados: Livoo/LivroLive (parceria encerrada em 17/10/2026), “TikTok Shop ativo”, “99% concluído”, “PHIZ em fase final”, “valuation conservador”, “sem perda financeira / sem risco típico de apostas” (revisão jurídica pendente), “receita recorrente” (não há cobrança periódica no sistema).",
              "Atualizados: linhas de código 178 mil → 331 mil (2.033 arquivos); “80+ licenciados ativos” → três contagens do sistema (15 · 23 · 8); série de receita: a declarada (nov/25–mai/26) aparece rotulada e separada da série oficial do app (ago–out/26).",
              "Mantido em destaque, com selo de referência do fundador: R$ 25.000.000. O valuation independente segue sem número até a metodologia v1.0 e o primeiro fechamento oficial.",
              "Fora do memorando, mas visível ao investidor em outras páginas: a queda do varejo físico na planilha (jun R$ 72 mil → ago R$ 3,4 mil) em Riscos; a dívida com parceiros de compra em Parceiros de compra. As divergências contábeis detalhadas ficam na seção do conselho em Riscos.",
            ]}
          />
        </Conteiner>
      )}
    </article>
  );
}
