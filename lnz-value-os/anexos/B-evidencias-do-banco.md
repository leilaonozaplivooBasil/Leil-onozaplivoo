# Anexo B — Evidências lidas no banco de produção

**Extraído em:** 17/10/2026 · **Projeto Supabase:** `leilonozap` (`gezvviyegtxytnwjkrjv`)
**Como:** somente leitura (`SELECT`). Nenhuma linha foi alterada. Só somas e contagens — nenhum nome, e-mail, CPF ou telefone foi lido.
**Classificação de todos os números deste anexo:** `VERIFIED` quanto à *leitura* (saiu do banco) e `NÃO AUDITADO` quanto ao *significado* (ninguém conferiu com extrato do banco/gateway nem com a contabilidade). Para o valuation, trate como **dado primário ainda sem conciliação**.

> Regra de leitura: onde está escrito **INFERÊNCIA**, é hipótese minha, não fato lido.

---

## B1. Tamanho do banco — o que existe e o que está vazio

| Grupo | Tabela | Linhas | Observação |
|---|---|---:|---|
| Pessoas | `app_users` | 1.173 | contas do app (clientes, rede, time) |
| | `customers` | 1.211 | cadastro tipo CRM — **não é** a mesma coisa que `app_users` |
| Leilão | `auctions` | 195 | |
| | `auction_messages` | 2.064 | **é aqui que moram os lances** (`message_type='bid'`) |
| | `bids` | 0 | herança vazia do Base44 — **não usar** |
| Vendas | `catalog_sales` | 897 | mistura vendas **e depósitos** (ver B3) |
| | `sales`, `payments`, `wallets`, `wallet_transactions`, `digital_wallets` | 0 | herança vazia do Base44 |
| Dinheiro | `reserva_ledger` | 611 | extrato da reserva de lance (desde 18/08/2026) |
| | `wallet_ledger` | 10 | extrato de carteira (desde 20/08/2026) — quase vazio |
| | `bonus_ledger` / `bonus_saldos` | 53 / 17 | bônus LEILÃO20 |
| | `financial_income` | 125 | "receitas" contábeis — só comissões da plataforma (ver B4) |
| | `financial_expenses` | 440 | despesas — lançadas à mão, qualidade baixa (ver B5) |
| | `withdrawal_requests` | 3 | saques (todos em 26/09/2026) |
| | `gateway_eventos` | 155 | avisos do Mercado Pago (só de 03 a 16/10/2026) |
| Rede | `commission_records` | 1.775 | comissões (desde 01/08/2026) |
| | `commission_ledger` | 547 | outro extrato de comissões (desde 28/08/2026) |
| | `comissao_pagamentos_manuais` | 24 | comissões pagas à mão por PIX |
| Estoque | `products` | 2.927 | |
| | `store_inventory` | 13.470 | |
| | `lotes_recebidos` | 40 | lotes comprados (desde 18/04/2026) |
| Logs | `system_logs` | 2.896.956 | desde 11/06/2026 |

**Datas de início dos dados (ponto crítico para o histórico):**

| Tabela | Primeiro registro | Último |
|---|---|---|
| `app_users` | 29/09/2025 | 17/10/2026 |
| `auction_messages` | 25/09/2025 | 17/10/2026 |
| `customers` | 11/02/2026 | 06/10/2026 |
| `auctions` | 03/01/2026 | 14/10/2026 |
| `catalog_sales` | **01/06/2026** | 15/10/2026 |
| `financial_income` | **04/07/2026** | 14/10/2026 |
| `commission_records` | 01/08/2026 | 14/10/2026 |
| `commission_ledger` | 28/08/2026 | 15/10/2026 |
| `reserva_ledger` | 18/08/2026 | 17/10/2026 |
| `gateway_eventos` | 03/10/2026 | 16/10/2026 |
| `withdrawal_requests` | 26/09/2026 | 26/09/2026 |

**Conclusão B1:** não há histórico de vendas no banco antes de **junho/2026**. O memorando mostra faturamento de **nov/2025 a mai/2026** — esse período **não está em `catalog_sales`**.

---

## B2. Pessoas — o que o banco diz sobre "licenciados" e "clientes"

### Por papel (`app_users.role`)

| role | contas | entraram nos últimos 30 dias (`last_login`) |
|---|---:|---:|
| user | 1.132 | 160 |
| licensee | **23** | **8** |
| admin | 10 | 7 |
| (vazio) | 6 | 1 |
| leiloeiro | 1 | 0 |
| super_admin | 1 | 1 |

### Por nível de carreira (`primary_career_level`)

usuario 1.081 · vendedor 31 · influenciador 15 · **licenciado_aplicativo 13 + licenciado 2** · fundador 6 · parceiro 5 · diretoria_operacao 5 · ponto_retirada 2 · executivo_conta 2 · livoo_live 1 · distribuidor 1 · loja_fisica 1 · embaixador 1 · ceo 1 · (vazio) 6

### Outros marcadores

- `licenciado_context` preenchido em **84** contas (contém `executive_owner_id`) — **INFERÊNCIA:** é o número que mais se aproxima dos "80+ licenciados" do material.
- `active_partner_plan` preenchido em **1** conta ("Plano Visionário"). `partner_plan_activated_at` preenchido em 1 conta (admin).
- `origem_trafego` preenchido em **65 de 1.173** contas (5,5%) → **CAC por canal é impossível para 94,5% da base**.
- `referred_by_id` preenchido em 1.172 de 1.173; `recruited_by_id` em 1. **INFERÊNCIA:** `referred_by_id` recebe um valor padrão (raiz) — não serve para medir indicação real até confirmar no código.
- KYC aprovado: 8 contas.

### Quem de fato paga (de `catalog_sales`, só pedidos pagos)

| Medida | Valor |
|---|---:|
| Contas distintas que **compraram** (exclui depósito) | 46 |
| Contas distintas que **depositaram** | 49 |
| Contas distintas que compraram **ou** depositaram | **65** |
| Compradores com 2+ compras | 17 |
| Depositantes com 2+ depósitos | 25 |

Pagantes distintos por mês: jun/26 **1** · jul **9** · ago **30** · set **36** · out (até 15) **22**

### Lances (`auction_messages`, `message_type='bid'`)

| Mês | Lances | Licitantes distintos | Leilões com lance |
|---|---:|---:|---:|
| 2025-09 | 218 | 6 | 27 |
| 2025-10 | 153 | 12 | 14 |
| 2025-11 | 21 | 5 | 4 |
| 2025-12 | 76 | 8 | 42 |
| 2026-01 | 44 | 7 | 34 |
| 2026-02 | 8 | 3 | 4 |
| 2026-03 | 7 | 1 | 5 |
| 2026-04 | 4 | 1 | 3 |
| 2026-05 | 2 | 1 | 1 |
| 2026-06 | — (nenhum) | — | — |
| 2026-07 | 42 | 4 | 9 |
| 2026-08 | 45 | 14 | 26 |
| 2026-09 | 103 | 25 | 40 |
| 2026-10 (até 17) | 119 | 24 | 14 |

**Leitura:** a atividade de lance caiu a quase zero de fev a jun/2026 e voltou a crescer de jul a out/2026 (25 e 24 licitantes distintos em set e out).

**Conclusão B2:** "80+ licenciados ativos", "~40 ativos" e "2.000+ clientes" **não têm definição única nem batem com uma contagem simples do banco**. Depende de qual regra se escolhe (23, 15, 84…). Isto é exatamente o que o *Metrics Registry* precisa resolver.

---

## B3. Vendas e entradas de dinheiro (`catalog_sales`)

### Achado central: depósito e venda moram na mesma tabela

Valores de pedidos **pagos** (status pago/entregue/enviado/preparando), por mês e tipo (`kind`):

| Mês | Produto (estoque) | Loja | Arremate (leilão) | **Depósito de carteira** | Depósito operação | Adesão | Outros | **Total** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| jun/26 | 54.149,29 | 72,54 | — | — | — | — | — | **54.221,83** |
| jul/26 | 7.716,91 | 80,54 | — | 885,00 | — | — | — | **8.682,45** |
| ago/26 | 4.783,40 | 2.351,63 | 220,04 | 3.600,00 | 457,00 | — | 326,61 | **11.738,68** |
| set/26 | — | 5.461,46 | 11.453,60 | **30.773,00** | — | 1.497,00 | — | **49.185,06** |
| out/26 (até 15) | — | 850,04 | 13.413,60 | **26.194,00** | — | — | — | **40.457,64** |

(`Outros` ago/26 = passaporte R$ 300,00 + frete de vendedor R$ 26,61.)

- Em **set e out/2026, 63% e 65% do que entrou foi depósito de carteira** — dinheiro do cliente que ainda **não é receita** (é obrigação com o cliente até virar compra).
- **Jun/2026 (R$ 54 mil)** é quase todo `kind='produto'` com `source='nexus'`, `linha='BANGU'`: 449 pedidos, R$ 61.140,68 no total. **INFERÊNCIA:** importação histórica da planilha *Nexus* (o app tem um cron `syncNexusSheet`), não venda nova do app.

### Status escritos de jeitos diferentes (o mesmo estado, 3 grafias)

`cancelado` / `canceled` / `cancelled` · `entregue` / `delivered` · além de `paid`, `shipped`, `preparando`.
Quem somar com `status = 'cancelled'` perde 2/3 dos cancelamentos.

### Cancelados que contaminam qualquer soma ingênua

| Tipo | Status | Pedidos | Soma |
|---|---|---:|---:|
| `partner_plan` | canceled | 6 | **R$ 3.040.000,00** (um deles R$ 1.000.000) |
| `partner_plan` | cancelado | 1 | R$ 30.000,00 |
| `seller_adhesion` | canceled/cancelado | 26 | R$ 42.425,00 |
| `wallet_deposit` | cancelado/canceled/cancelled | 92 | R$ 65.829,55 |

**Leitura:** em agosto/2026, somar `total_amount` sem filtrar status daria **> R$ 3 milhões** — são tentativas de comprar plano de parceiro nunca pagas. O filtro de status é obrigatório.

### Só 1 adesão paga de verdade

Em `catalog_sales`, pedidos pagos de `seller_adhesion`: **1** (R$ 1.497,00, set/26). Nenhuma `partner_plan` paga. Isso **não** contradiz ter licenciados antigos (podem ter entrado pelo Base44 ou por fora do app), mas significa que **o banco atual não prova receita de licenciamento**.

---

## B4. Receita contabilizada (`financial_income`)

| Mês | Comissão de leilão | Comissão de loja | Taxa de adesão | Total |
|---|---:|---:|---:|---:|
| jul/26 | — | 462,35 | — | 462,35 |
| ago/26 | 49,61 | 1.126,12 | — | 1.175,73 |
| set/26 | 2.924,90 | 1.638,36 | 1.497,00 | 6.060,26 |
| out/26 (até 14) | 3.175,10 | 118,94 | — | 3.294,04 |
| **Total** | | | | **R$ 10.992,38** |

**Leitura:** o que o app registra como *receita da plataforma* é a **comissão** (taxa de 3% nos leilões e comissão de loja), não o valor total movimentado. Nada de venda de estoque próprio entra aqui. **Isso precisa de definição oficial:** "receita" = valor vendido (GMV) ou = comissão retida?

---

## B5. Despesas (`financial_expenses`)

440 lançamentos, de 10/02/2026 a 30/04/2027 (inclui parcelas e recorrências **futuras**).

Problemas de qualidade encontrados:
- **Categorias com grafias diferentes para a mesma coisa:** `Aluguel` / `Aluguel Escritório`; `Salario` / `Funcionários/Salários`; `alimentação`; `informatica`; e linhas com categoria **em branco**.
- **Status que não bate com o valor pago:** ao menos 4 lançamentos `pago_integral` com `amount_paid = 0` (ex.: Aluguel Escritório ago/26, R$ 10.000; Tecnologia set/26, R$ 1.185,41).
- **Atrasado há meses:** de mar a ago/2026, aluguel (R$ 15.787,49/mês), salários (R$ 3.900/mês) e servidor (R$ 2.680/mês) aparecem como `vencido` com pago = 0.
- **Out/2026 pendente:** salários R$ 53.000, alimentação R$ 24.629, aluguel R$ 14.500 + R$ 10.000.
- Linha única de **"Cartão de Crédito"** (R$ 18–23 mil/mês) sem abertura por item.
- Categorias ambíguas: `custo do aporte`, `investimento`, `Consorcio`.

**Conclusão B5:** **não dá para calcular EBITDA real com esta base.** Falta classificação (custo × despesa × investimento × retirada de sócio) e confirmação do que foi de fato pago.

---

## B6. Passivo com clientes e rede (o que a empresa "deve" hoje)

Soma das colunas de saldo em `app_users` (R$):

| Coluna | Contas com saldo | Soma |
|---|---:|---:|
| `saldo_disponivel` | 47 | 26.979,35 |
| `saldo_reservado` (lances em andamento) | 3 | 198,47 |
| `seller_credit_balance` | 3 | 7.994,00 |
| `commission_balance` | 22 | 9.239,44 |
| `catalog_commission_balance` | 17 | 252,14 |
| `saldo_operacao` | 1 | 7,00 |
| Bônus (`bonus_saldos`, 42.800 centavos) | 17 | 428,00 |
| `divida_consignado` (a receber, não é passivo) | 1 | 10,44 |

**Indicativo ≈ R$ 45,1 mil de obrigações** com clientes e rede (soma das 7 linhas de passivo). **Atenção:** só somar depois de confirmar no código se `saldo_reservado` está dentro ou fora de `saldo_disponivel`.

Comissões:
- `commission_records`: status `confirmed` / `paid` / `reversed`, com ~25 papéis diferentes. `leilao_retido` (61 registros, média 24,5%, R$ 6.088,11) é o maior. Fundadores/conselheiros/diretoria têm registros de ~0,08–0,15% cada.
- `commission_ledger`: **494 linhas "venda" `cancelado`** com `pct = 100` somando R$ 73.444,26. **FATO (lido no código):** é o antigo "escrow" de venda — dinheiro que ficava retido por 7 dias antes de liberar. Foi cancelado e desligado em 28/09/2026 (migração `20260928152855_grupo_c_escrow_cancelado.sql` cita 479 linhas / R$ 71.812,19; hoje há 494 / R$ 73.444,26, ou seja, 15 linhas a mais nasceram depois). **Não é comissão paga nem receita — não somar.**
- Pagas por fora: 24 pagamentos manuais = **R$ 4.503,10**. Saques pelo app: 3 = **R$ 240,00**.

---

## B7. Leilões (`auctions`)

- 195 leilões. **37 são `is_investment_plan = true`**, com preço final somado de **R$ 210.467,46** — **precisam ser excluídos** de qualquer GMV de produto (em jan/2026 eles inflam a soma para ~R$ 255 mil).
- `platform_commission_percentual`: **3,0%** em todos.
- Valor de mercado preenchido (`market_price` ou `manual_market_price`) em **6 de 195** leilões → **margem por leilão não é calculável** com este campo.
- Ligação com produto (`product_id`) em 136 de 195.

Leilões de produto finalizados com vencedor (preço final somado):

| Mês de criação | Leilões com vencedor | Preço final somado |
|---|---:|---:|
| jul/26 | 14 | R$ 1.849,04 |
| ago/26 | 22 | R$ 961,20 |
| set/26 | 21 | R$ 13.406,00 |
| out/26 | 5 | R$ 8.871,00 |

---

## B8. Estoque e lotes — testando "compra a 20–25% do mercado"

### Lotes comprados (`lotes_recebidos`, 18/04 a 06/10/2026)

40 lotes; 34 com custo **e** valor de mercado preenchidos:

| Medida | Valor |
|---|---:|
| Custo total (34 lotes) | R$ 276.675,97 |
| "Valor de mercado" cadastrado (mesmos lotes) | R$ 7.521.208,88 |
| **Custo ÷ mercado — ponderado** | **3,68%** |
| Custo ÷ mercado — mediana | **0,72%** |
| Custo ÷ mercado — P25 / P75 | 0,35% / 9,69% |

**Leitura:** o memorando diz comprar a **20–25%** do mercado. O banco mostra **3,7%** (mediana 0,7%). Duas explicações possíveis, e **só o dado de venda real decide**:
(a) a compra é de fato muito mais barata do que o prometido; ou
(b) o "valor de mercado" do lote é preço de tabela inflado (lote de devolução com valor cheio). **Um comprador de empresa vai assumir (b) até ver preço de venda realizado.**

### Estoque hoje (`products`)

| Status | Produtos | Peças | **A custo** | Com valor de mercado |
|---|---:|---:|---:|---:|
| ESTOQUE | 1.469 | 1.856 | R$ 51.914,15 | **1** |
| A_PRECIFICAR | 456 | 434 | R$ 7.021,71 | 0 |
| (sem status) | 44 | 80 | R$ 2.550,05 | 0 |
| BLOQUEADO_PRECO | 536 | 181 | R$ 2.479,35 | 0 |
| **Total a custo** | | | **≈ R$ 63.965** | |

- Em 26/05/2026 (retrato do outro repositório): status ESTOQUE com qtd > 0 = **3.101 itens / 7.689 peças / R$ 321.400,65 a custo**. Hoje: **R$ 51.914,15** — queda de ~84%. **Precisa de explicação** (vendas, baixa, reclassificação?) antes de usar estoque como ativo.
- **Só 1 produto em estoque tem `market_value`.** A tabela `market_value_backup_20260902` (2.616 linhas) mostra que os valores foram guardados em 02/09/2026 — **INFERÊNCIA:** foram zerados naquela data. Sem valor de mercado por produto, "vende 20% abaixo do mercado" **não é verificável**.
- Vitrine: 272 produtos ativos, **12 deles sem estoque**.

### Margem realizada (aproximada — junção pedido × `products.cost_price`)

| Canal | Pedidos pagos | Com custo | Receita (dos com custo) | Custo | **Margem aprox.** |
|---|---:|---:|---:|---:|---:|
| Arremate (leilão) | 62 | 42 | R$ 15.815,44 | R$ 25.844,27 | **−63,4%** |
| Loja (pagto por saldo) | 18 | 16 | R$ 4.691,49 | R$ 3.994,97 | +14,8% |
| Loja (outros) | 35 | 28 | R$ 3.310,28 | R$ 3.106,05 | +6,2% |
| Produto — Nexus/Bangu | 449 | 0 | — | — | sem custo |
| Produto — PDV | 6 | 0 | — | — | sem custo |

**CUIDADO (limite desta conta):** junta pedido a produto por `product_id`, usa `cost_price` atual do produto e quantidade do pedido; não inclui frete, imposto nem comissão. **INFERÊNCIA:** arremates a −63% podem ser *isca de aquisição* intencional (leilão como marketing) ou erro de custo cadastrado — **precisa validação linha a linha** antes de qualquer afirmação externa.

### Vendas de estoque pelo histórico de produtos (`products.sold_amount`, status VENDIDO*)

dez/25 R$ 37.875,55 · jan/26 R$ 476,82 · fev R$ 6.958,60 · mar R$ 9.747,89 · abr R$ 14.012,59 · **mai R$ 24.586,76** · jul R$ 4.668,37 · ago R$ 2.438,90 · set R$ 11.421,00 · out R$ 8.871,00

**Leitura:** nenhuma tabela que consultei reproduz a série do memorando (**nov/25 16,3k · dez 26,4k · jan 27k · fev 17,2k · mar 23k · abr 60,4k · mai 181k**). O mais próximo para mai/26 é R$ 24,6 mil (contra R$ 181 mil). **Não conclui que o memorando está errado** — a fonte pode estar fora do banco (planilha Nexus, extratos do gateway/banco, entidades do Base44 não migradas). **Conclui que hoje esse número não tem rastro.**

---

## B9. Gateway (Mercado Pago) — a conciliação que já existe

`gateway_eventos` (03 a 16/10/2026), só `mercado_pago`:

| Situação | Resultado | Eventos |
|---|---|---:|
| cancelado | estornado | 38 |
| pendente | ok:pending | 27 |
| liberado | already_paid | 21 |
| liberado | credited | 18 |
| devolvido | estornado | 8 |
| devolvido | already_paid | 8 |
| **conciliação** | **divergência** | **9** |

**Leitura:** já existe um mecanismo de conciliação gateway × app e ele **já achou 9 divergências em 2 semanas**. É a base natural do *Discrepancy Radar*. Só nasceu em 03/10/2026 — **não há conciliação do passado**.

---

## B10. Alerta de segurança que encontrei

O scanner do Supabase marcou **3 tabelas sem RLS (proteção por linha)**: `gateway_eventos`, `gateway_acoes`, `gateway_classificacoes`. Os comentários dizem "só o servidor lê e grava", mas **sem RLS ligada, qualquer pessoa com a chave pública do app consegue ler e alterar essas tabelas**. Elas guardam o corpo dos avisos de pagamento (`corpo` em JSON).
**Não apliquei nada.** SQL sugerido pelo scanner (para você decidir, e que precisa de arquivo de migração no repositório, pela regra do projeto):

```sql
ALTER TABLE public.gateway_eventos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gateway_acoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gateway_classificacoes ENABLE ROW LEVEL SECURITY;
```

Também: `app_users` tem colunas `password`, `access_token`, `password_reset_token` — **não consultei**; a frente de segurança verifica se estão protegidas (ver Parte 11).

---

## B11. Consultas usadas (para refazer)

> Todas `SELECT`. Rodadas em 17/10/2026. Para refazer, use o mesmo projeto, perfil somente-leitura.

```sql
-- B2: papéis
select coalesce(role,'(null)') role, count(*) total,
  count(*) filter (where last_login >= now() - interval '30 days') login_30d
from app_users group by 1 order by 2 desc;

-- B3: entradas pagas por mês e tipo
select to_char(date_trunc('month', coalesce(pago_em, created_date)),'YYYY-MM') mes,
  coalesce(kind,'(null)') kind, count(*) pedidos, round(sum(coalesce(total_amount,0))::numeric,2) total
from catalog_sales
where lower(status) in ('paid','entregue','delivered','shipped','preparando')
group by 1,2 order by 1,3 desc;

-- B3: cancelados (soma contaminadora)
select coalesce(kind,'(null)') kind, lower(status) status, count(*) n, round(sum(total_amount)::numeric,2) soma
from catalog_sales where lower(status) like 'cancel%' group by 1,2 order by soma desc;

-- B4: receita contabilizada
select to_char(date_trunc('month', received_date),'YYYY-MM') mes, category, count(*), round(sum(amount)::numeric,2)
from financial_income group by 1,2 order by 1;

-- B6: passivos em carteira (exemplo de uma coluna)
select count(*) filter (where saldo_disponivel>0), round(sum(saldo_disponivel)::numeric,2) from app_users;

-- B7: leilões que não são de produto
select count(*), round(sum(current_price)::numeric,2) from auctions where is_investment_plan is true;

-- B8: custo do lote ÷ valor de mercado
select round((sum(custo_total)/sum(valor_mercado_total))::numeric,4) razao_ponderada,
  round((percentile_cont(0.5) within group (order by custo_total/valor_mercado_total))::numeric,4) mediana
from lotes_recebidos where coalesce(custo_total,0)>0 and coalesce(valor_mercado_total,0)>0;

-- B8: estoque a custo
select status, count(*), round(sum(coalesce(quantity,0))::numeric,0) pecas,
  round(sum(coalesce(cost_price,0)*greatest(coalesce(quantity,0),0))::numeric,2) a_custo
from products group by 1 order by a_custo desc;

-- B8: margem aproximada por canal
select cs.kind, cs.source, count(*), sum(cs.total_amount), sum(p.cost_price*coalesce(cs.quantity,1))
from catalog_sales cs left join products p on p.id = cs.product_id
where lower(cs.status) in ('paid','entregue','delivered','shipped','preparando') and p.cost_price>0
group by 1,2;
```
