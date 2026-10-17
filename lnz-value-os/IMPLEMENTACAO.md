# LNZ VALUE OS — Diário da implementação

> Aprovação do CEO para construir: **17/10/2026** ("aprovado, pode fazer"). Regra mantida: **nada muda no app, no banco do app, nos sites ou na produção** sem ordem explícita; o portal nasce separado.

## Onde cada peça mora

| Peça | Onde | Estado em 17/10/2026 |
|---|---|---|
| Código do portal | este repositório, pasta `valueos/` (Next.js 16) | **no ar**: login por e-mail + código (só com convite), termo de sigilo com hash/IP, registro de acesso. Telas: Visão geral (capa com os 4 tempos), **Memorando revisado** (12 capítulos do Gamma com cada número etiquetado), Números com prova, DRE, **Parceiros de compra**, **Riscos**, **Valuation** (metodologia, sem número), **Governança e time**, **Metas e simulação** (plano × realizado + simulador por alavancas), **Data room** (mapa do que existe/falta), Cargas, prova por métrica |
| Hospedagem | Vercel, equipe "Leilaapp's projects", projeto **`lnz-value-os`** (`prj_2ZMGeV9phCiKDkKpeWC6yfzJDb3D`), funções em São Paulo (gru1) | **publicado a partir do GitHub** (branch `claude/zen-albattani-uql6jy`, produção); proteção de login da Vercel desligada (o login é do portal) |
| Endereço do portal | **`investidor.leilaonozap.net`** | **no ar** — CNAME criado pelo CEO na IONOS em 17/10 (`investidor` → `cname.vercel-dns.com`), reconhecido pela Vercel |
| Banco do portal | Supabase, organização "Leilao Nozap 4.0" (plano Pro), projeto **`lnz-value-os`** em São Paulo | **usando o projeto já existente e vazio `leilaonozaplivooBasil's Project` (`hmldusqewfckxgzldqga`, Ohio)** — a criação de projeto novo trava numa tela de custo; tabelas com prefixo `vos_`; migrações em `valueos/supabase/migrations/`. Mudar para um projeto próprio em São Paulo depois é só reaplicar as migrações. |
| Banco do app (leitura) | Supabase `leilonozap` (`gezvviyegtxytnwjkrjv`) | intocado; as visões de leitura entram como arquivo de migração, aplicadas só com ordem |
| Vitrines públicas | Gamma: memorando → `investmentmemorandumleilaonozap.com`; valuation → `valuationleilaonozap.com` | intocadas; o memorando tem **alterações não publicadas** (última publicação há ~2 meses); o valuation foi republicado em 17/10 |

## Carga inicial (17/10/2026)

- **30 métricas** no dicionário (`vos_metricas`), 6 famílias.
- **57 evidências** com hash encadeado e **57 valores** (ago–16/out/2026), de duas cargas: consultas somente-leitura no app e extratos/contratos enviados pelo CEO.
- Etiquetas: a maioria `VERIFIED`; despesas e aportes como `MANAGEMENT_DATA`; nenhum `FORECAST` ainda; **nenhum número de valuation**.

## Conteúdo dos sites dentro do portal (17/10/2026, à noite)

- Os dois sites do Gamma foram lidos na origem e viraram as páginas `memorando`, `valuation`, `governanca`, `roadmap` do portal. **Regra:** narrativa da administração mantida; todo número ganhou etiqueta; o que a auditoria (Anexo A) marcou REMOVE saiu (Livoo, TikTok Shop, "99%", PHIZ, "valuation conservador", "retorno elevado", comparação com apostas); o que marcou VERIFY/RECALCULATE aparece com o valor medido ao lado do declarado.
- **Nota de revisão** em cada capítulo (o que mudou em relação ao site público) aparece **só para BOARD/ADMIN** (`NotaRevisao`); o investidor vê o conteúdo revisado com etiquetas.
- Páginas `riscos` e `valuation` têm uma seção extra só para o conselho (riscos legais/origem de recursos; números que já circulam).
- Nomes da diretoria vêm do site público; parceiros de compra e comprador do 1% continuam como A, B e iniciais.
- Componentes em `valueos/src/components/ui.tsx` (Etiqueta, Numero, Secao, Cartao, Aviso, Barras, Tabela, NotaRevisao, Legenda) e navegação em `nav.tsx`. Papel do usuário em `lib/papel.ts`; valores das métricas em `lib/metricas.ts`.

## Identidade visual dos sites dentro do portal (17/10/2026, noite)

- **Pedido do CEO:** o portal com a cara do memorando e do site de valuation (Gamma), só que mais profissional, com os dados de hoje. Fonte do desenho: os dois PDFs enviados (60 páginas do memorando + página do valuation) e a leitura dos documentos no Gamma.
- **Identidade:** fundo preto, verde da marca `#00B86B`, etiqueta de capítulo verde-menta, **Poppins** nos títulos e **Roboto** no texto (as mesmas fontes do PDF), barra superior com a logo do app. Tokens em `valueos/src/app/globals.css`; peças visuais em `valueos/src/components/marca.tsx` (Capitulo, Cartao, CartaoNumerado, LinhaDoTempo, Trajetoria, Setas, GraficoBarras, Ciclo, NumeroGrande, Hoje).
- **Imagens:** 25 artes tiradas dos próprios PDFs (foto do fundador, capa, mapas, abertura de cada capítulo, logo com transparência, logos do ecossistema) em `valueos/public/m/`, comprimidas (≈ 5 MB no total).
- **Memorando (`/app/memorando`):** refeito na ordem do original — carta do fundador na íntegra, trajetória, conquistas, convergência, linha do tempo (com jun/ago/set/out de 2026 acrescentados), resumo executivo, os 12 capítulos, 12 barreiras, capítulo 9 com **R$ 25.000.000 em destaque e selo de referência do fundador**, ciclo virtuoso e mensagem final (botões: reunião por WhatsApp e data room). Números trocados pelos do sistema, com etiqueta e link para a prova.
- **Valuation (`/app/valuation`):** capa no estilo do site de valuation; **“O que vale R$ 25.000.000”** com cada ativo ao lado do número de hoje; **painel vivo** (no lugar da planilha) com ago/set/out linha a linha; mercado, momento, ecossistema, roadmap; e a metodologia v1.0, a ponte e os comparáveis.
- **Início e login** no mesmo padrão. **Conferência visual** por fotos de tela (1280 px, 1024 px e celular 390 px), sem rolagem lateral e sem texto abaixo de 12 px; prévia local em `/previa/<página>` (só em modo de desenvolvimento, com dados de arquivo).
- **Remuneração paga aos parceiros no painel** (set R$ 1.600; out R$ 15.000) está escrita no código da página: virar métrica própria na próxima carga.

## Livro do capital — "A história do dinheiro" (17/10/2026, noite)

- **Pedido do CEO:** juntar o que está no Gamma, no Drive e no financeiro do app e contar a história verdadeira do dinheiro: aportes, custo fixo (sala R$ 10 mil/mês, galpão ~R$ 24 mil/mês e ~R$ 100 mil de obra, orçamento de equipe R$ 200–250 mil), vendas da fase anterior ao app e o saldo que fica na carteira do cliente.
- **Página nova `/app/capital`** (menu Números → "Capital e custos" e porta no Início): quatro números-resumo, linha do tempo do dinheiro (nov/2025 → out/2026), vendas mês a mês desde dez/2025 (cinza = registro da operação; verde = app), investimento dos fundadores separado entre dinheiro (R$ 439 mil) e não financeiro (R$ 792 mil), dinheiro que entrou em 2026, custo do capital de terceiros (R$ 340 mil a R$ 14.600/mês, 4,3% a.m.), carteira do cliente (51% do depositado ainda não gasto) e custo fixo (orçamento × cadastrado × pago). Seção **só para o conselho** com o que um analista do investidor vai achar e a lista de pendências do fundador.
- **Carga nova no banco do portal** (tipo manual, 15 valores, 8 métricas na família "7. Capital e história"): `SALES_HISTORY_MGMT`, `REVENUE_TAX_RBT12`, `CAPITAL_FOUNDERS_DECLARED`, `THIRD_PARTY_CAPITAL`, `CAPITAL_COST_M`, `FIXED_COST_BUDGET_M`, `FIXED_COST_REGISTERED_M`, `WALLET_UNSPENT_SHARE`. Cada valor com evidência (fonte + composição) na cadeia de hash. Terceiros aparecem como "Parceiro A/B" e "Investidor 1/2"; nenhum nome de pessoa física de fora da diretoria no repositório.
- **Fontes lidas:** Gamma (Resumo Executivo 17/12/2025; Resumo Executivo Integrado 11/09/2026; Documento Oficial 28/08/2026; Reorganização Societária 17/10/2026; proposta de entrada de mar/2026; deck "10 Milhões"), Drive (relatório consolidado NEXUS de 24/04/2026, planilha diária `vendas.xlsx`, "NEXUS — Espelho de Vendas"), banco do NEXUS no Base44 (123 vendas abr–jun/2026), app em **somente leitura** (`financial_expenses`, `financial_income`, `catalog_sales`, `app_users`, `lotes_recebidos`) e o código do app (`src/lib/operacaoNumeros.js`: PGDAS-D 06/2026, RBT12 R$ 714.458). O zip "NEXUS — App v2" enviado pelo CEO é só o esqueleto do Base44, sem dados.
- **Achados que vão para o CEO:** totais por pessoa trocados no documento dos fundadores (itens somam 713/481, títulos dizem 723/471); preço da participação mudou quatro vezes (R$ 6,9 mi → 25 → 50 → 90 mi); promessa de rendimento fixo em dois documentos (parecer jurídico); despesas a separar da empresa; aluguel do escritório lançado em dobro e título de capitalização com um zero a mais; parceiro A fora do financeiro do app; Simples (R$ 714 mil em 12 meses) × registros internos (R$ 188 mil de dez/25 a mai/26); "10 mil produtos" sem prova (o próprio app já tirou esse número da home).

### Correções com os extratos e a declaração do Simples (17/10/2026, madrugada)

- **Simples:** a declaração no Drive (PGDAS-D do PA 05/2026, transmitida em 15/05/2026) mostra **2025 zerado** e R$ 714.458 de **jan a mai/2026** — não é receita de 12 meses, como estava rotulado no código do app (`operacaoNumeros.js`, "RBT12"). Métrica antiga `REVENUE_TAX_RBT12` desativada; nova `REVENUE_TAX_DECLARED_M` mês a mês. Balancete 2025 do contador (R$ 1.186.031 de receita) em `ACCOUNTING_REVENUE_Y`. As três fontes (Simples, balancete, banco) não fecham entre si — pendência do contador.
- **Banco:** 30 páginas de extrato Santander enviadas pelo CEO, juntadas por script (dias partidos entre páginas somados, páginas repetidas descartadas): 164 dias de 15/01 a 05/10/2026. Pix de até R$ 5 mil por mês viraram `BANK_SMALL_PIX_IN` (prova bancária da venda pelo WhatsApp). Correções entram como **linha nova** no mesmo período (o banco do portal passa a ser só-acrescenta também em `vos_valores`): `lib/metricas.ts` ordena por período e, no empate, pela mais recente — a linha antiga fica como histórico na prova. Março corrigido para o mês inteiro (R$ 44.109,58).
- **Capital:** investidor 1 (familiar de um diretor) entrou com um carro de R$ 50 mil, que lastreia uma carta de crédito, e R$ 20 mil de limite de cartão — a empresa usa o cartão e paga a fatura (os ~R$ 23 mil mensais para ele são fatura, não galpão); rende ~5% ao mês. Investidor 2 ~R$ 20 mil. Posição em 17/10: R$ 340 mil a R$ 14.600/mês. Os R$ 200 mil do Itaú (24–30/09) são a compra de 1% por um diretor (`EQUITY_SUBSCRIPTION`), com origem a documentar: R$ 130 mil de três pagadores e R$ 70 mil em espécie em 43 depósitos no mesmo dia.
- **Galpão:** set e out pagos à imobiliária (`RENT_WAREHOUSE_PAID`, verificado); jun e jul por repasse, candidatos sem nome no extrato a confirmar.

## Próximos passos (ordem)

1. ~~Login, convite, termo, acesso~~ — feito.
2. ~~Esquema do banco do portal~~ — feito (0001, 0002).
3. ~~Carga das 30 métricas com prova~~ — feito (carga manual pela sessão; automatizar na Fase 2).
4. ~~Tela "clique para provar" e tela de Cargas~~ — feito.
5. ~~Conteúdo dos dois sites dentro do portal, com etiquetas~~ — feito (17/10). Falta: Fase 2 completa (modelo por alavancas com custo por venda, cenários salvos, XLSX) — hoje há um simulador simples em "Metas e simulação".
6. Visões de leitura sobre o app (arquivo, aplicado só com ordem) e rotina mensal de carga.
7. Botão no app e botão "Área do investidor" nos sites (com aprovação do texto).

## Pendências do CEO

- ~~Supabase → URL Configuration e template do Magic Link~~ — feito pelo CEO em 17/10 (login testado de ponta a ponta).
- ~~E-mail pelo remetente da empresa (Brevo)~~ — **feito pelo CEO em 17/10 à noite:** Supabase Auth com SMTP personalizado (`smtp-relay.brevo.com:587`, remetente `relacionamento@leilaonozap.com`, nome "Leilão NoZap"), usando a chave SMTP `supabase-portal` criada no Brevo (sem expiração fixa). Limite sobe para 30 e-mails/hora. **Alerta:** chave SMTP do Brevo **expira após 90 dias sem uso** — se o portal ficar 3 meses sem ninguém pedir código, gerar outra chave no Brevo e colar de novo no Supabase. A chave de API do app (`BREVO_API_KEY`) é outra coisa e não foi tocada.
- **Assunto do e-mail de código:** trocar `Your Magic Link` por "Seu código de acesso · Leilão NoZap" (Supabase → Authentication → Emails → Modelos → Magic link or OTP → Subject).
- Decidir o que fazer com as alterações não publicadas do memorando no Gamma.
- (Opcional) criar um projeto Supabase próprio em São Paulo e me avisar para migrar.
