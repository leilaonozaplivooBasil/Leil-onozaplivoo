# Parte 6 — Metrics Registry (proposto)

> **O que é, em português simples:** o "dicionário oficial" de números. Cada número do Value OS (e dos dois sites) tem **uma** definição, **uma** fórmula, **uma** fonte e **um** dono. Nenhuma tela escreve número à mão — todas leem daqui.

---

## 6.1 Ficha de cada métrica

Todos os campos que você pediu, mais os que a investigação mostrou serem necessários:

| Campo | Para quê |
|---|---|
| `metric_id`, `name`, `description`, `business_definition`, `formula` | identidade e definição |
| `source`, `database`, `table`, `field` | de onde vem |
| `period` (e **fuso: sempre Brasília**), `refresh_frequency` | quando |
| `owner`, `unit`, `type`, `last_update` | quem responde |
| `quality_score`, `verification_status` | `VERIFIED` · `MANAGEMENT DATA` · `FORECAST` · `AI ASSUMPTION` |
| **`version`, `valid_from`, `valid_to`** | definição **muda sem apagar a anterior** |
| **`entity_scope`** | **qual CNPJ/empresa** (ex.: Compras Full; ecossistema) |
| **`exclusions`** | o que sai da conta (teste, plano de investimento, contas internas…) |
| **`series_start`** | a série oficial começa quando (ex.: 01/08/2026 para dinheiro do app) |
| **`conflict_rule`** | o que fazer se duas fontes divergirem |

Exemplo preenchido:

```
metric_id:          LICENSEES_ACTIVE_30D
version:            1.0   (válida a partir de 2026-11-01)
business_definition:Licenciado que, nos últimos 30 dias, gerou ao menos 1 venda real paga
                    (dinheiro real = paga + rastro de gateway ou saldo, data ≥ 01/08/2026)
formula:            count(distinct u.id)
                    where u.cargo_normalizado = 'licenciado' and u.active <> false
                      and exists (venda real paga com seller_id = u.id
                                  OR comissão gerada com anchor_user_id = u.id
                                  em [hoje−30d, hoje])
source / table:     app_users, catalog_sales, commission_records
exclusions:         contas da empresa/equipe/QA, e-mail .invalid, is_sample
entity_scope:       ecossistema Leilão NoZap
verification_status:VERIFIED  (calculado direto do banco, com evidência)
conflict_rule:      se divergir do painel do app, o Registry prevalece e o Radar abre alerta
```

---

## 6.2 Regras que valem para **todas** as métricas

| # | Regra | Por quê (o que o diagnóstico mostrou) |
|---|---|---|
| 1 | **Status em um idioma só.** `PAGA = {paid, preparando, saiu_entrega, shipped, delivered, entregue}`; `CANCELADA = {cancelado, canceled, cancelled}`. | Hoje há 4 listas diferentes de "paga" e 3 grafias de "cancelada"; filtrar `status='cancelled'` perde 2/3 dos cancelamentos. |
| 2 | **Mês e dia em Brasília**, nunca em UTC. | O navegador calcula em UTC, o SQL em BRT. |
| 3 | **Data da receita = hora do pagamento** (`pago_em`). Antes de 08/10/2026, usa-se a data de criação e a métrica leva a etiqueta `APROXIMAÇÃO`. | `pago_em` só é confiável desde 08/10. |
| 4 | **Valor em centavos** (inteiro). | Evita erro de arredondamento; o bônus já usa centavos. |
| 5 | **Séries do app começam em 01/08/2026** (`series_start`). O que veio antes é `LEGADO` e **só entra com documento**. | O documento oficial do app (`MARCO-OFICIAL-AGOSTO-2026`) já trata o que veio antes como teste. |
| 6 | **Exclusões padrão:** `is_sample`, `is_test_auction`, `is_investment_plan`, contas da empresa/equipe/QA, e-mails `.invalid`, pedidos cancelados. | R$ 3 mi de cancelados e R$ 210 mil de "planos" contaminam qualquer soma. |
| 7 | **Depósito não é receita.** Vai para `WALLET_LIABILITY`, não para `REVENUE_*`. | Em set/out, 63–65% do que entrou foi depósito. |
| 8 | **Fonte conflitante nunca é escolhida em silêncio.** O Radar mostra as duas e a diferença. | Seu princípio 26. |
| 9 | **Precedência para conflito:** *extrato bancário/gateway* **>** *app* **>** *contabilidade* **>** *planilha* **>** *gerencial*. | Dinheiro em conta é mais difícil de "ajustar" do que lançamento contábil. **Diverge da hierarquia que você escreveu** (item 5 do seu comando) — está na Parte 12 para sua decisão. |
| 10 | **Entidade explícita.** Toda métrica diz a que CNPJ pertence. | O ecossistema tem várias empresas e o app, a marca e a receita podem estar em CNPJs diferentes. |

---

## 6.3 Família "receita" — a mais importante (substitui os 6 "faturamentos")

| metric_id | Definição oficial (proposta) | Fonte | Hoje |
|---|---|---|---|
| `CASH_IN_GROSS` | Todo dinheiro que **entrou** em conta (PIX, cartão liberado), **qualquer natureza**, sem transferência entre contas da empresa | extrato + gateway | ✅ Jan–jun/26: ver Anexo C. Out/26: gateway |
| `WALLET_DEPOSITS` | Depósitos de carteira pagos | `catalog_sales` kind `wallet_deposit`, `operacao_deposit` | ✅ set R$ 30.773 · out (até 15) R$ 26.194 |
| `CAPITAL_INFLOWS` | **Aportes de sócios, investidores e parceiros, e empréstimos** — **não é receita** | extrato + contratos de aporte | ❌ **a classificar pelo CEO** (19 PIX ≥ R$ 5 mil) |
| `GMV_GOODS` | Valor de **mercadoria** vendida e paga (loja, arremate, PDV, Nexus), **sem frete, sem depósito, sem adesão** | `catalog_sales` kinds de produto | ✅ set R$ 16,9 mil · out (até 15) R$ 14,3 mil (app); Nexus à parte |
| `REVENUE_GOODS_GROSS` | Receita bruta da **venda de estoque próprio** = `GMV_GOODS` quando a empresa é a vendedora | idem | ⚠️ depende de definir quando o estoque é da empresa × do lojista |
| `REVENUE_COMMISSION_RETAINED` | Comissão **retida pela empresa** (leilão e loja) | `financial_income` corrigido | ⚠️ R$ 10.992 desde jul; **dupla semântica a separar** |
| `REVENUE_FEES` | Taxas e adesões pagas | `catalog_sales` kinds adesão | ⚠️ 1 adesão paga (R$ 1.497) |
| `REVENUE_NET` | Receita bruta − impostos sobre venda − devoluções | contabilidade + app | ❌ sem imposto gravado |
| `REVENUE_RECURRING` | Receita **contratada e repetida** (assinatura/mensalidade) | — | ❌ **hoje = 0** (não há mensalidade) |

> **Para qualquer investidor, a primeira pergunta será:** *"qual dessas é a 'receita' do memorando?"* — hoje não há resposta única.

### O que cada número do memorando seria em cada definição (para ele escolher)

| Mês | Memorando | `CASH_IN_GROSS` (banco) | `GMV_GOODS` (app/Nexus) | Declaração ao banco |
|---|---:|---:|---:|---:|
| Mai/26 | 181,0 mil | 205,6 mil (inclui aportes) | desconhecido (Nexus: falta CSV) | — |

---

## 6.4 Família "pessoas e rede"

**Nenhuma dessas existe hoje como número único.** As contagens abaixo são **só para mostrar a distância entre definições** (17/10/2026):

| metric_id | Definição oficial (proposta) | Contagem hoje | Observação |
|---|---|---:|---|
| `USERS_REGISTERED` | contas `role=user`, ativas, excluindo equipe/QA/teste | **1.132** | `app_users` tem 1.173 no total |
| `CUSTOMERS_PAYING_90D` | contas com ≥ 1 compra **ou** depósito pago nos últimos 90 dias | **65** (jun–out) | separar `BUYERS` (46) e `DEPOSITORS` (49) |
| `USERS_ACTIVE_30D` | login **ou** compra real em 30 dias | ~160 (só login) | `last_login` é um carimbo sobrescrito → **não dá histórico** |
| `BUYERS_REPEAT` | ≥ 2 compras pagas | 17 de 46 | |
| `LICENSEES_TOTAL` | **cargo normalizado = licenciado** (inclui `licenciado_aplicativo` e `licenciado_catalogo` legados), ativo ≠ lixeira | **15** (cargo) · 23 (`role=licensee`) · 84 (`licenciado_context`) | **o CEO decide qual é a regra** (Parte 12) |
| `LICENSEES_PAID` | adesão **paga** (R$ 5.000) e não estornada | ≈ 0–1 no banco atual | só o caminho "primeira compra" deixa rastro |
| `LICENSEES_GRANTED` | cargo concedido pelo admin **sem** pagamento | desconhecido | admin não grava valor |
| `LICENSEES_ACTIVATED` | pagantes que já fizeram a 1ª venda indicada | — | |
| `LICENSEES_ACTIVE_30D` | definição do exemplo (6.1) | ≈ 8 (só por login, 23 `role=licensee`) | recalcular por venda |
| `SELLERS_ACTIVE_30D` | cargo `vendedor` com venda real em 30 dias | — | |
| `NETWORK_DEPTH`, `NETWORK_SALES_SHARE` | profundidade da rede e % da venda vinda da rede | — | `referred_by_id` não separa indicação real de padrão |

**Para os sites:** "80+ licenciados" **não pode** ser exibido enquanto `LICENSEES_*` não estiver definido. Duas frases diferentes de hoje ("80+ ativos" × "80 totais, ~40 ativos") passam a ser **duas métricas com nome diferente**.

---

## 6.5 Família "carteira e passivo" (a regra "depósito ≠ receita")

| metric_id | Definição | Hoje |
|---|---|---:|
| `WALLET_LIABILITY_SPENDABLE` | soma de `saldo_disponivel` | R$ 26.979,35 (47 contas) |
| `WALLET_LIABILITY_RESERVED` | `saldo_reservado` (lances em andamento) | R$ 198,47 |
| `WALLET_LIABILITY_COMMISSION` | `commission_balance` + `catalog_commission_balance` | R$ 9.491,58 |
| `WALLET_LIABILITY_SELLER_CREDIT` | `seller_credit_balance` | R$ 7.994,00 |
| `PROMO_CREDIT_OUTSTANDING` | bônus LEILÃO20 em aberto | R$ 428,00 |
| `WALLET_LIABILITY_TOTAL` | soma das cinco acima **(após confirmar se `reservado` já está em `disponivel`)** | **≈ R$ 45,1 mil** |
| `OPERATING_CASH` | saldo bancário da empresa | ❌ falta extrato recente |
| `FREE_CASH` | `OPERATING_CASH` − `WALLET_LIABILITY_TOTAL` − tributos e contas vencidas | ❌ |
| `PARTNER_CAPITAL_LIABILITY` | aportes de parceiros com repasse prometido | ❌ **a medir (CEO)** |

---

## 6.6 Família "leilão"

| metric_id | Definição | Hoje |
|---|---|---:|
| `AUCTIONS_PRODUCT_ENDED` | leilões de produto encerrados (sem `is_investment_plan`/teste) | jul 24 · ago 33 · set 24 · out 5 |
| `AUCTIONS_WITH_WINNER` | …com vencedor | jul 14 · ago 22 · set 21 · out 5 |
| `AUCTIONS_PAID` | …com `order_status = paid` **e** venda `kind=arremate` | a calcular |
| `BIDS_COUNT` | `auction_messages` `message_type='bid'` | set 103 · out (até 17) 119 |
| `BIDDERS_DISTINCT` | licitantes distintos no período | set 25 · out 24 |
| `AUCTION_CONVERSION` | `AUCTIONS_PAID` ÷ `AUCTIONS_PRODUCT_ENDED` | a calcular |
| `GMV_AUCTION` | preço final de arremates pagos (sem frete) | set R$ 11.454 · out (até 15) R$ 13.414 |
| `AUCTION_TAKE_RATE` | comissão retida ÷ `GMV_AUCTION` | a calcular (`platform_commission_percentual` = 3,0%) |
| **`PCP`** (seu) | **total de depósitos associados ao produto ÷ custo do produto** | ❌ **não existe**: depósito **não fica marcado com o leilão**; aproximação possível por "depósitos de quem deu lance na janela do leilão" |
| `AUCTION_MARGIN` | preço final − custo congelado − comissões − frete − taxa | ❌ sem custo por leilão; `market_price` só em 6 de 195 |

---

## 6.7 Família "produto e estoque"

| metric_id | Definição | Hoje |
|---|---|---:|
| `INVENTORY_AT_COST` | Σ `cost_price × quantity` (status ESTOQUE + A_PRECIFICAR + BLOQUEADO_PRECO + sem status) | **≈ R$ 63,9 mil** (era R$ 321,4 mil em 26/05) |
| `LOT_COST_TO_MARKET` | `custo_total ÷ valor_mercado_total` por lote | 3,7% ponderado · 0,7% mediana (34 lotes) — **mercado = planilha do fornecedor** |
| `SELL_VS_MARKET` | preço de venda ÷ valor de mercado | ❌ `market_value` zerado em 02/09 |
| `GROSS_MARGIN_BY_CHANNEL` | (receita − custo congelado) ÷ receita | aprox.: loja +6% a +15% · arremate −63% (42 pedidos; **a validar**) |
| `STOCKOUT_SALES_RISK` | % da vitrine ativa com `quantity ≤ 0` | 12 de 272 |
| `TECH_LOC`, `TECH_FILES` | linhas e arquivos de código **com data e definição** | ≈ 331 mil linhas / 2.033 arquivos (sem testes) |

---

## 6.8 Família "financeiro e passivo fiscal"

| metric_id | Hoje |
|---|---|
| `EXPENSES_PAID` / `_OVERDUE` / `_PENDING` (por **categoria normalizada**) | ❌ categorias inconsistentes; requer mapa de plano de contas |
| `TAXES_PAYABLE` | R$ 83.232,71 (balanço 31/12/2025) — situação atual desconhecida |
| `PAYROLL_PAYABLE` | R$ 84.987,84 (balanço 31/12/2025) |
| `CONSORTIUM_PAYMENTS_M` | ≈ R$ 12 mil/mês (extratos jan–jun) |
| `FOUNDERS_POOL` | 1% do faturamento bruto aos fundadores — **base de cálculo a definir** |
| `COMMISSION_PAID_PCT` | comissão paga ÷ `GMV_GOODS` |
| `GATEWAY_FEE_PCT` | taxa do gateway ÷ valor — só no JSON `gateway` desde 03/10 |

---

## 6.9 Qualidade inicial do Registry (estimativa de 17/10/2026)

| Família | Métricas (≈) | Calculáveis hoje (≈) | Com evidência `VERIFIED` (≈) |
|---|---:|---:|---:|
| Receita | 9 | 4 | 2 |
| Pessoas e rede | 11 | 4 | 1 |
| Carteira e passivo | 9 | 6 | 5 |
| Leilão | 10 | 6 | 5 |
| Produto e estoque | 6 | 3 | 2 |
| Financeiro e fiscal | 7 | 1 | 0 |
| **Total** | **52** | **≈ 24 (46%)** | **≈ 15 (29%)** |

> Número esperado do **Data Quality Score** logo no início: **baixo** (~35–45/100). **Isso é o diagnóstico — não é defeito do Value OS**: o placar existe justamente para subir à medida que os dados faltantes (Parte 5.5) são corrigidos.
