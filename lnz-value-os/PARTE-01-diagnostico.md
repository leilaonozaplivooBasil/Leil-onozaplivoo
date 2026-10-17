# Parte 1 — Diagnóstico

> **Como ler:** cada afirmação tem uma etiqueta.
> **FATO** = li no código ou no banco. **INFERÊNCIA** = dedução minha, a confirmar. **MANAGEMENT DATA** = vem do material da administração, sem rastro.
> Os números do banco estão em `anexos/B-evidencias-do-banco.md` (com as consultas). A auditoria dos dois sites está em `anexos/A-auditoria-dos-dois-sites.md`.

---

## 1.1 Em uma página: o que o diagnóstico mostra

### O que está sólido

1. **O motor do leilão é maduro.** Lance atômico com versão, reserva de saldo com livro-caixa, fechamento do leilão, liquidação a cada 10 minutos, cancelamento em 48 h, trilha de auditoria do leilão. **FATO** (agentes de código; `reserva_ledger` 611 linhas, `auction_auditoria` 527).
2. **Existe uma conciliação com o Mercado Pago** (pagamento × venda do app) que já achou **9 divergências em duas semanas**. É a melhor âncora de caixa que o app tem. **FATO** (Anexo B9).
3. **A zona vermelha, a janela de deploy e a skill "antes de mesclar" existem** e têm testes. Cultura de controle de mudança já está pronta para receber um módulo novo. **FATO** (`CLAUDE.md` do app).
4. **O código é grande e real:** ≈ **331 mil linhas em 2.033 arquivos** de código (sem testes; ≈ 421 mil com testes), contra os "178 mil / 883" dos sites. **FATO** (medido no repositório; ver ressalva no Anexo A, item 15).

### O que o diagnóstico encontrou de mais sério

| # | Achado | Tipo | Por que importa para o valuation |
|---|---|---|---|
| 1 | **A série de receita dos sites (nov/25–mai/26) não está no banco do app.** A tabela de vendas só começa em 01/06/2026. | FATO | O número mais forte do material (R$ 181 mil em maio) hoje **não tem rastro**. |
| 2 | **Provável origem da série: a planilha "Nexus"** — vendas do showroom Bangu e do WhatsApp **lançadas à mão** por 6 executivos, importadas por um cron. O documento do banco Nexus de 28/04/2026 mostra R$ 49.450,91 de faturamento do mês (107 registros) — mesma ordem de grandeza dos R$ 60,4 mil de abril do memorando. | **INFERÊNCIA** (forte) | É um **negócio diferente** do app de leilão (varejo físico/WhatsApp, sem custo nem produto ligado à venda). O valuation precisa dizer **o que está sendo avaliado**. |
| 3 | **O documento oficial do próprio app diz que tudo antes de 01/08/2026 é "TESTE — sem valor financeiro, não é receita".** (`docs/MARCO-OFICIAL-AGOSTO-2026.md`, 04/08/2026; o código usa essa data como corte em `dinheiroReal.js`.) O memorando apresenta nov/25–mai/26 como "tração comprovada". | **FATO** | **Contradição interna.** Um investidor que ler os dois (o que um bom analista faz) vai perguntar. |
| 4 | **A própria planilha Nexus mostra a queda das vendas do varejo:** jun **R$ 72.048** (453 vendas) → jul **R$ 11.835** (83) → ago **R$ 3.381** (16) → **nenhum registro de set em diante.** (O app importou R$ 54.149 / 3.610 / 3.381: o importador ignora executivos fora de uma lista de 6 nomes — **INFERÊNCIA**.) | FATO (planilha lida pelo Drive) | O varejo físico/WhatsApp, que parece ser a origem da série do memorando, **perdeu volume depois de junho** (ou deixou de ser lançado). O memorando termina em maio e **não mostra jun–set**. O **total do mês no cabeçalho da planilha (R$ 70.269,22 "julho") não bate com a soma de julho no corpo (R$ 11.835,49)**. |
| 5 | **Dinheiro "real" no app tem ~2,5 meses.** Entradas pagas: ago R$ 11,7 mil · set **R$ 49,2 mil** · out (até 15/10) **R$ 40,5 mil**. | FATO | Histórico muito curto para fluxo de caixa descontado. |
| 6 | **63% (set) e 65% (out) do que entrou foi depósito de carteira** — dinheiro do cliente que ainda **não é receita**. A tabela de vendas mistura os dois. | FATO | Somar `catalog_sales` sem separar **superestima receita em quase 3×**. |
| 7 | **Receita contabilizada pelo app (comissões + taxa) = R$ 10,99 mil desde julho.** | FATO | É o que o app chama de receita: **a comissão retida**, não o valor movimentado. Definição oficial de "receita" não existe. |
| 8 | **Há três "valuations" circulando:** R$ 25 mi (sites; também em `documentoOficial.js`), **R$ 0,37–0,75 mi** (3–6× o lucro anual apurado de R$ 124.596, **escrito no código** do painel do Parceiro) e **R$ 8–16 mi** (cenário de R$ 1 mi/mês). | FATO | A referência do fundador é **33× a 67×** o valor que a conta fiscal da própria empresa sustenta. Precisa de uma narrativa única antes de qualquer investidor ver. |
| 9 | **A empresa que tem todas as contas formais é a COMPRAS FULL COMÉRCIO LTDA** (nome fantasia "LEILÃO NOZAP", ex-TOP HOUSE, **ME**, aberta em 25/07/2023). No contrato social de 12/08/2025 as **500.000 cotas estão em nome de uma única sócia**; o CEO não aparece como quotista nesse instrumento. | FATO (dossiê do Drive) | **Quem são os sócios hoje e qual CNPJ é dono do app, da marca e dos domínios?** Sem isso, não se sabe **o que** está sendo avaliado nem **quem** vende. |
| 10 | **"Compra a 20–25% do mercado, vende 20% abaixo" é premissa digitada** (`operacaoNumeros.js`), não medida. Nos 34 lotes com dado: custo = **3,7%** do "valor de mercado" cadastrado (mediana **0,7%**) — mas esse valor é o da planilha do fornecedor, e **o valor de mercado dos produtos foi apagado em 02/09/2026** por não ser confiável. | FATO | A promessa central de margem **não é verificável hoje**. Margem aproximada medida: loja +6% a +15%; arremate **−63%** (42 pedidos; a validar). |
| 11 | **Não existe margem por leilão, produto ou SKU.** O custo nunca é lido no fechamento nem na liquidação. | FATO | Sem isso não há unit economics, e sem unit economics não há DCF defensável. |
| 12 | **"Licenciado" tem 6 significados no código** e **ao menos 4 contagens diferentes no banco** (23 / 15 / 84 / 8 com acesso em 30 dias). A regra de **30% de comissão** é o **pool total da rede por venda**, não o ganho do licenciado (13% direto, 3% de rebate). | FATO | Os "80 ativos" dos sites não têm definição. O app mesmo diz "1.000+ parceiros reunidos, nenhum ativado". |
| 13 | **Despesas:** categorias inconsistentes, itens `pago_integral` com valor pago zero, aluguel/salários `vencido` desde março, uma linha de cartão sem abertura. | FATO | **EBITDA real não é calculável** com esta base. |
| 14 | **Obrigações com clientes e rede ≈ R$ 45,1 mil** (saldos, comissões a pagar, bônus). **Aportes de "parceiro" (plano de capital com repasse prometido) entram como receita de valor cheio.** | FATO | No valuation, dinheiro de carteira é **dívida disfarçada**; aporte com repasse é **passivo**, não venda. |
| 15 | **Afirmações dos sites que o código não confirma:** "TikTok Shop ativo" (só há link de perfil), "Leilão Inteligente 99%" e "PHIZ Leilão" (zero ocorrências), "ComparAI IA proprietária" (é busca em SerpApi/SearchApi/Zoom, sem histórico), "Livoo: sociedade em fase final" (**a Livoo deixou de ser parceira hoje, 17/10/2026**). | FATO | Risco de credibilidade e jurídico se um investidor checar. |
| 16 | **O dossiê contábil mostra receitas diferentes para cada destinatário.** Jan–abr/2026: memorando **R$ 127,6 mil**; declaração ao banco **R$ 539,5 mil**; entradas reais nas duas contas bancárias **R$ 416,9 mil** (que **incluem aportes e empréstimos**). 2025: livros **R$ 1,19 mi**; PGDAS (RBT12 até jun/26) **R$ 0,71 mi**. | FATO (ver Anexo C5) | **O mesmo negócio tem 4–5 receitas diferentes.** Antes de qualquer valuation, uma só receita, com origem, precisa ser definida. |
| 17 | **Na declaração de faturamento ao banco, o total impresso (R$ 1.725.558,81) não é a soma das suas 12 linhas (R$ 1.352.881,81).** A diferença (R$ 372.677,00) é exatamente jan–abr/2025 dos livros: **o total soma 16 meses.** | FATO (conferido por script) | Documento para fim de crédito com total que não confere é o tipo de ponto que uma *due diligence* acha em minutos. **Levar ao contador e ao advogado antes de circular.** |
| 18 | **65% de tudo que entrou de terceiros no Santander (jan–jun) veio de 19 PIX acima de R$ 5.000** (R$ 428,6 mil de R$ 659,9 mil; um único PIX de R$ 100 mil em abril). A natureza (venda, **aporte**, empréstimo, parte relacionada) é desconhecida. | FATO + dado faltante | A **qualidade da receita** depende disso. O CEO vai me passar os aportes. |
| 19 | **Caixa de R$ 705.958,47 no balanço de 31/12/2025 × R$ 42,29 nas contas Santander + Mercado Pago em 01/01/2026.** | FATO (balanço × extratos) | Ou há outras contas, ou o "caixa" contábil não existe como dinheiro. **Sem extratos de 2025 e de todas as contas não dá para reconciliar.** |
| 20 | **A série de receita 2025 dos livros cresce todos os meses (11 de 11), começa em exatamente R$ 90.000,00 e a mesma série está na declaração ao banco.** A DRE 2025 não tem aluguel, equipe, marketing, frete nem comissão. | FATO | Margem líquida escriturada de 52% **não representa** a operação real (que paga aluguel, equipe e comissões). **EBITDA histórico não serve de base.** |
| 21 | **Tributos:** R$ 83 mil a pagar no balanço de 2025, e **só R$ 367 de DARF** pagos pelo Santander em jan–jun/2026. Regime muda de **Lucro Presumido (2025)** para **Simples Nacional (2026)**; o laudo tributário de 22/07 é de **agente de IA**, com RBT12 de **R$ 1,19 mi** (alíquota 9,02%), enquanto o painel do app usa **R$ 0,71 mi** (7,56%) no mesmo dia. | FATO | Passivo fiscal potencial a medir; laudo precisa de contador com CRC. |
| 22 | **Consórcios (informação do CEO, `MANAGEMENT DATA`):** 21 cartas na empresa (2 contempladas ≈ R$ 150 mil, 19 a contemplar), mais 2 contempladas no nome de um sócio (≈ R$ 270 mil líquidos) e uma carta alienada em um veículo (R$ 55 mil, em dia). Nos extratos: **≈ R$ 72 mil de parcelas em jan–jun** (~R$ 12 mil/mês). | FATO (extratos) + informado | Ativo e passivo **não operacionais** na ponte do EV para o equity; **o que está no nome do sócio fica fora** da empresa. Preciso dos contratos. |
| 23 | **Entradas bancárias de valor redondo e em lote.** ≈ R$ 0,88 mi em 39 créditos de terceiros ≥ R$ 5.000 (jan–out); **os 20 mais recentes são todos múltiplos exatos de R$ 1.000**. Em **24/09/2026** a conta do Itaú foi de R$ 0 a **R$ 130.000** num dia: 4 PIX (R$ 80.000, 3 pagadores) + **43 depósitos em dinheiro de R$ 100 a R$ 2.000 (R$ 70.000)**. Setembro teve ≈ R$ 400 mil de entradas de terceiros nas duas contas contra **R$ 49,2 mil de pagamentos do app**. | FATO (extratos) | **Origem dos recursos.** Pode haver explicação legítima (aportes), mas exige contrato/recibo e quem pagou. **Falar com advogado e contador antes do Data Room** (Anexo C9). |
| 24 | **Mercado Pago pelo app (jul–16/10): 192 pagamentos aprovados, R$ 69,5 mil brutos; custo do gateway ≈ 1,6% (PIX ≈ 1,0%).** O **dinheiro novo** de setembro foi ≈ **R$ 33 mil (93% depósito)**; dos R$ 49,2 mil de "pedidos pagos", **R$ 15,9 mil foram pagos com saldo** (dupla contagem). O relatório de consórcio de 30/06 **bate ao centavo** com dois lotes dos extratos (25 boletos Itaú = R$ 45.572,58; 24 pagamentos MP = R$ 44.653,49) e mostra **compromisso de ≈ R$ 51 mil/mês**, muito acima do que as contas conhecidas pagam. | FATO (banco do app + extratos + relatório) | O app **explica ≈ R$ 33 mil** dos ≈ **R$ 400 mil** de entradas de setembro; o **consórcio é passivo financeiro relevante** e existem **outras contas**. (Anexo C10–C11) |
| 25 | **Os extratos do Mercado Pago (jul, set, out) fecham ao centavo e batem com o app e com os bancos.** Em set e out **toda entrada de terceiros do Mercado Pago é venda do app** (80/80 em set e 34/35 em out casadas pelo número da operação: R$ 33,0 mil e R$ 26,8 mil). As transferências da empresa para ele **batem exatamente com saídas do Santander e do Itaú** (set R$ 81.247,68; out R$ 57.178,30). **Entraram R$ 400.000,00 exatos em lotes redondos em setembro** (Santander R$ 200 mil · Itaú R$ 120 mil + R$ 80 mil) **contra R$ 33,5 mil de venda do app.** Faltam: **agosto** do Mercado Pago e a origem dos R$ 400 mil. | FATO (extratos + banco do app) | Prova que a **venda real do app é pequena** (≈ R$ 27–33 mil/mês) e que o resto do dinheiro que entra **precisa de documento** (Anexo C13). |
| 26 | **Aportes informados pelo CEO (17/10):** **R$ 200 mil no Itaú (24 e 30/09) = compra de 1% da empresa** (R$ 250 mil por 1% = **R$ 25 mi**; +R$ 50 mil a receber) e **R$ 50 mil (11/08) + R$ 200 mil (01/09) no Santander = "parceiro de compra"**, que **recebe rentabilidade**. **Tudo bate com os extratos, valor e data** (o equity soma R$ 200.000,00 exatos, incluindo **43 depósitos em dinheiro = R$ 70 mil**). **Nenhum aporte está registrado no app.** | MANAGEMENT DATA + extratos | **R$ 450 mil explicados (sem contrato).** Parceiro de compra = **passivo com remuneração**; 1% = **capital ou dinheiro de sócio** (peso zero como preço até haver documento). Anexo C14. |
| 27 | **A linha "Parceiros de compra (5%)" foi retirada dos cenários do painel do Parceiro em 02/10/2026** (decisão da diretoria registrada no código, na véspera da apresentação). Com ela: resultado do lote **R$ 4.952**, "hoje" **R$ 88.884/ano**; sem ela: **R$ 8.952** e **R$ 124.596/ano**. | FATO (código + ramo de restauração) | Se os parceiros **recebem rentabilidade**, **o resultado apurado e o "valuation de 3–6×" ficam superestimados** sem esse custo. Anexo C14. |
| 28 | **Contratos de parceiro de compra (recebidos 17/10):** **parceiro A (R$ 200 mil, assinado em 01/09)** = **R$ 9.000 fixos por mês (4,5% ao mês) por 24 meses + devolução integral do principal**; **parceiro B (R$ 50 mil)** = **R$ 1.500 por mês (3% do capital)**, **sem data e sem assinatura**. **Os pagamentos de 15/09 e 15/10 batem com os contratos ao centavo.** O CEO informa que **só existem estes 2 contratos**; mesmo assim **R$ 35,6 mil (15/09) e R$ 30,6 mil (15/10) em pagamentos redondos não são dos contratos** (segundo o CEO, **pagamento de cartão de crédito da empresa**, por PIX a **pessoas físicas**; o app só lança parte). O pagador dos R$ 200 mil **não é** o parceiro A. | FATO (contratos + extratos) | **É dívida com juros fixos, não participação no lucro.** Só estes 2 contratos: **R$ 10,5 mil/mês** e **R$ 502 mil nominais** em 24 meses. **Cartões de crédito em nome de pessoas = despesa sem fatura e dívida fora do balanço; pedir as faturas.** Anexo C15. |

### Segurança — 5 itens que você precisa conhecer (nada foi alterado)

1. **3 tabelas sem proteção por linha (RLS):** `gateway_eventos`, `gateway_acoes`, `gateway_classificacoes`. O acesso público está **revogado hoje** (risco baixo), mas é uma trava só; qualquer permissão futura abriria. Conserto barato (3 linhas), mas exige arquivo de migração no repositório. **FATO.**
2. **O custo dos produtos (`cost_price`) e as comissões (`commission_records`) são legíveis com a chave pública do navegador.** **FATO** (verifiquei privilégio e política no banco).
3. **A rota do termo de sigilo (`consultarAssinaturaSigilo`) devolve a linha inteira da assinatura** — nome, CPF, e-mail, IP — de qualquer `user_id`, e a rota **não está na lista de rotas trancadas**. Se a trava de sessão está só em modo "anotar", ela responde a qualquer um. **FATO** (código); **a confirmar** o modo da trava na Vercel.
4. **128 das 209 rotas do servidor só anotam no registro quando falta o crachá** — não barram. **FATO** (agente de segurança; `rotasTrancadas.js`).
5. **O "Valuation" e o "Memorando" que já existem dentro do app** (painel do Parceiro) têm **números, CNPJ, número do PGDAS e nome da contadora no pacote público do site**, e o NDA é conferido só no navegador. **FATO.**

> **Nada disso foi corrigido.** São mudanças em zona vermelha ou em segurança de produção; só avançam com a sua ordem e pelo processo do app (arquivo de migração, janela 01h–02h15). Estão listadas na Parte 12 como decisão sua.

---

## 1.2 Os dois sites — diagnóstico

**O que são:** vitrines de narrativa. **Nenhum número vem do sistema**, e nenhum dos dois endereços aparece no código do app (nem em redirecionamentos nem em CORS). **FATO** (busca no repositório).
**Onde estão hospedados:** **não estão na sua conta Vercel** (a conta só tem `leilaonozap.net`). **FATO** (Vercel). **Pergunta aberta:** em qual plataforma e quem controla o DNS? (Parte 12.)
**Limite da minha análise:** trabalhei com as **capturas em PDF**; não consegui abrir os sites ao vivo.

Resumo da auditoria (46 itens, Anexo A): **KEEP 13 · VERIFY 22 · RECALCULATE 7 · REMOVE 3 · INCONSISTENT 6.**
O dossiê, os extratos e o app acrescentaram **12 itens** (47–58, Anexo A seção 10): 3 INCONSISTENT · 3 RECALCULATE · 5 VERIFY · 1 REMOVE.

Os 5 itens que mais mexem numa conversa com investidor:
1. Série de receita sem fonte rastreável (itens 6/7).
2. "80 ativos" × "80 totais, 40 ativos" × 23 no banco (itens 21/22).
3. Custo do lote 3,7% do "mercado", não 20–25% (item 28).
4. R$ 12 mi projetado para 2026 não fecha com a meta de R$ 1 mi/mês em dezembro (item 13).
5. O 1% do faturamento bruto aos fundadores precisa entrar no modelo como custo (item 32).

E um sexto, urgente: **a Livoo saiu hoje e os dois sites ainda a anunciam** (item 20).

---

## 1.3 O app — diagnóstico por área

### Dinheiro (fluxo de ponta a ponta)

- **Depósito** só pelo **Mercado Pago** (PIX e cartão). Depósito **não grava extrato próprio**; fica como linha em `catalog_sales` com `kind='wallet_deposit'`. Não existe "total depositado" — soma-se por tipo. **FATO.**
- **Saldos** em `app_users`: `saldo_disponivel`, `saldo_reservado`, `saldo_alocado`, `commission_balance`, `saldo_operacao`, `seller_credit_balance`, `credito_estoque`, `divida_consignado`, `test_wallet_balance`; bônus à parte em `bonus_saldos`. **Não existe livro-razão único de saldo.** Cada extrato cobre um pedaço. **FATO.**
- **Lance:** reserva o saldo, grava em `auction_messages`, devolve a reserva do líder anterior.
- **Martelo:** **não cria venda e não é receita.** Vira dívida do arrematante, comissões pagas a pessoas e a fatia retida (única receita de leilão no livro de receita). A venda nasce na **liquidação** (cron de 10 min ou "Meus Arremates") e **só então baixa estoque**. **FATO.**
- **Arremate pago direto por PIX/cartão:** o webhook marca a venda como paga, mas **não achei código que atualize o status do leilão**. **INFERÊNCIA** — possível caminho morto.
- **Saque:** exige KYC e chave PIX = CPF; o **pagamento do PIX é feito à mão, fora do app**. 3 saques (R$ 240) e 24 pagamentos manuais de comissão (R$ 4.503,10). Nenhuma das duas saídas vira despesa. **FATO.**
- **Hora do pagamento:** o campo `pago_em` **só passou a ser preenchido a partir de 08/10/2026**. Antes disso a "data de receita" é a de criação do pedido. **FATO.**

### Receita e custo

- **Não há** receita bruta, custo, frete real, taxa do gateway, imposto ou margem **gravados por venda**. **FATO.**
- O **custo do produto** vem de `products.cost_price`, calculado **no estado atual do estoque** (não congelado na venda) — o mesmo produto pode mudar de custo depois. **FATO.**
- `products.cost_price` é **custo do lote ÷ unidades, igual por peça** (não por valor de mercado). O próprio código se contradiz sobre ser "unitário" ou "do lote" — já gerou "R$ 50 milhões investidos" numa tela. **FATO.**
- **Imposto** é só estimativa em tela (Simples Anexo I). A tabela de impostos está vazia. **FATO.**
- **`financial_income` tem duas semânticas opostas sob o nome "comissão":** na loja = o que foi **pago a pessoas**; no leilão = a fatia **retida pela empresa**. Nada reverte esses lançamentos em cancelamento/estorno. **FATO.**
- **Pelo menos 6 definições de "faturamento"** em telas diferentes (Visão Geral, Lucro do Dia, Painel de Alavancagem, CRM, Diretoria, Painel do Investidor), com listas diferentes de "venda paga", datas diferentes (UTC × BRT; criação × pagamento) e dupla contagem possível (depósito + compra com saldo). **FATO.**

### Rede comercial

- **Papel** em `app_users.role` (user, licensee, admin, super_admin, admin_financeiro…) e **cargo** em `career_levels`/`primary_career_level` (influenciador, vendedor, licenciado, parceiro, ponto_retirada, loja_fisica, distribuidor… + topo + legados). **Não existe campo "licenciado desde / valor pago / status da adesão".** **FATO.**
- **Como vira licenciado:** (A) primeira compra de **R$ 5.000** na loja (vendedor **R$ 1.497**) → o webhook concede o cargo; (B) cadastro com `?cargo=licenciado` (tabela `adesao_orders` está **vazia**, então **INFERÊNCIA:** caminho sem uso); (C) admin promove (**não guarda valor pago**); (D) legado. **Hoje não dá para separar licenciado pagante de licenciado concedido.**
- **Comissões:** venda direta influenciador 5% · vendedor 10% · licenciado 13% · parceiro 15% · ponto de retirada 16% · loja física 19% · distribuidor 20% (cadeia telescópica com teto de 20%) + topo 10% (CEO 3, Livoo 2, Embaixador 1, Conselheiro 1, Fundador 1, Dir. Exec. 0,5, Dir. Oper. 0,5, Executivo 1). Leilão: 5% indicador + 10% executivo + resto retido. **Base de cálculo = valor da venda, nunca lucro.** **FATO.**
- **Contadores mortos:** `indicated_clients_count` nunca é gravado; `total_commissions_generated` vazio em 100% das contas (o Marco de Agosto já listava). **FATO.**
- **Cota Livoo Live (2% de toda venda da loja)** continua no motor, embora a Livoo não seja mais parceira. **FATO** (decisão pendente do dono).
- **Origem do cliente:** `origem_trafego` só existe desde 25/09/2026 e só com UTM/click-id (preenchido em 5,5% da base). `referred_by_id` cai no "Site Oficial" quando não há indicação — **não distingue indicação real de indicação padrão**. **CAC por canal é impossível hoje**; LTV só "bruto" (sem margem). **FATO.**

### Produtos, lotes, ComparAI

- **Produto → lote é por texto** (`products.lot = nome do arquivo`), não por chave; nome não é único. **FATO.**
- O custo do lote (arremate + taxa + frete + outros) só vira colunas se publicado como "oportunidade"; no outro caminho fica em texto livre, e a tela do parceiro **assume** frete R$ 2.500, outros R$ 600 e taxa 7% quando falta. **FATO.**
- **ComparAI** = busca em **SerpApi, SearchApi e Zoom** (raspagem), mediana com faixa de 0,4×–2,2×; **não guarda histórico**; cache de 7 dias; **sem cota** em alguns períodos (SearchApi desde 20/08; SerpApi 4.005 de 5.000 e cartão recusado em 10/09). **Nenhum modelo de IA entra no preço.** **FATO.**
- **Analisador de Lotes** existe (`/AnaliseDeLotes`): lê planilha de fornecedor, calcula lucro projetado; **a classificação (grade A–E) e o valor vêm da planilha do fornecedor, não de IA**. **FATO.** O uso é real: 40 lotes (18/04 a 06/10).
- **Live commerce:** `live_sessions` (13.028 linhas) é **batimento de presença do site**, não transmissão; o número de espectadores exibido é **aleatório (150–199)**. **FATO.**
- **"Giro da força de venda"** mostrado ao parceiro é **simulado** (lista determinística) com aviso "demonstrativo". **FATO.**

### Qualidade e testes

- ≈ **6,2 mil casos de teste**; dinheiro de lance, reserva, webhook e liquidação têm teste real razoável. **Mas o banco falso dos testes não executa SQL:** as fórmulas dos KPIs em SQL **nunca rodam em teste**. Em 13/10, uma auditoria plantou 6 erros de dinheiro e **4.479 testes passaram nos 6**. **FATO.**
- **Confiança nos números de KPI e valuation: baixa.** Confiança no motor de leilão e saldo: razoável.

### Legado Base44

- Banco antigo **apagado em 05/08/2026**; `raw_base44` em 49 arquivos e `base44_id` em 50; **213 das 246 funções legadas não têm equivalente**; ponte ainda ativa (`base44Runtime.js`) usada por 3 funções de busca. **FATO.**
- **Duas línguas de status** (`entregue`/`delivered`, `cancelado`/`canceled`/`cancelled`) e **duas carteiras** (legada vazia + atual). **FATO.**

---

## 1.4 Divergências internas — resumo (inventário completo na Parte 6)

| Tema | Fontes que discordam |
|---|---|
| "Venda paga" | 4 status (`dinheiroReal.js`) × 9–10 status (CRM, SQL) × só `paid` (alguns SQL) |
| Faturamento | 6 telas, 6 fórmulas |
| Licenciado | 6 significados; 4 contagens |
| Valuation | R$ 25 mi × R$ 0,37–0,75 mi × R$ 8–16 mi |
| Clientes ativos | 250 mil (texto do painel do Parceiro; **meta** de KPI) × 1.167–1.173 contas × 65 pagantes |
| Comissão | "30%" (pool da rede) × 13% (licenciado direto) × `platform_commission_percentual` 3% |
| Mês/dia | UTC (navegador) × BRT (SQL); data de criação × data de pagamento |
| Saque | doc de auditoria diz "3 saques pagos em 26/09"; migração diz que foram marcados à mão em 28/09 e que R$ 240 ficaram presos em `saldo_alocado` |

---

## 1.5 O que eu **não** consegui verificar (honestidade)

- **Os dois sites ao vivo** (só as capturas em PDF).
- **A planilha Nexus completa** — li as primeiras linhas de cada aba (total de julho: R$ 70.269,22). Falta o CSV para calcular a série mensal nov/25–out/26.
- **Extratos de 2025 e de jul–out/2026**, e **outras contas** além de Santander e Mercado Pago. Sem eles o caixa não reconcilia (achado 19) e a série de receita 2025 não tem prova bancária.
- **Se os arquivos do dossiê são autênticos:** li PDFs entregues pela empresa; **não consultei o banco, a Receita nem a Junta**.
- **O PGDAS-D em si** (só vi a citação no código do app).
- **Contrato social atual**, quadro de sócios e **quem é dono do app, da marca e dos domínios**.
- **Os aportes e investimentos** nas empresas (o CEO vai informar) e os **contratos dos consórcios**.
- **O estado real de variáveis da Vercel** (ex.: `SESSAO_MODO`, `CRON_SECRET`) — não li valores de segredo.
- **Passivos fora do app** (empréstimos, tributos em atraso, parcelamentos).
- **Por que o estoque a custo caiu de R$ 321 mil (26/05) para R$ 64 mil (hoje)** — precisa de explicação.

**Nenhum arquivo do app, do banco ou dos sites foi alterado.** Tudo o que fiz em produção foi leitura.
