# Parte 5 — Database Map

> Projeto Supabase `leilonozap`: **154 tabelas** em `public`, 151 com RLS ligada. Contagens de 17/10/2026.
> **Legenda de confiança:** 🟢 usar como fonte primária · 🟡 usar com ressalva · 🔴 não usar · ⚫ nunca ler (dado pessoal/segredo).

---

## 5.1 Mapa em uma imagem

```
                         ┌──────────── PESSOAS E REDE ────────────┐
                         │ app_users 1.173 ⚫  customers 1.211 🟡 │
                         │ career_levels 4   contrato_assinaturas │
                         │ kyc_data 7 ⚫      concurso_* (Rank)    │
                         └───────────────┬────────────────────────┘
                                         │ user_id / buyer_id / seller_id
   ┌──────────── LEILÃO ───────────┐     │      ┌──────────── LOJA / DINHEIRO ───────────┐
   │ auctions 195 🟡               │     │      │ catalog_sales 897 🟡  (vendas + depósitos│
   │ auction_messages 2.064 🟢     │◄────┼─────►│   misturados — separar por kind/status)  │
   │   (lances: message_type='bid')│     │      │ gateway_eventos 155 🟢  (desde 03/10)    │
   │ auction_auditoria 527 🟢      │     │      │ reserva_ledger 611 🟢  (desde 18/08)     │
   └───────────────┬───────────────┘     │      │ wallet_ledger 10 🔴    bonus_ledger 53   │
                   │ product_id          │      │ commission_records 1.775 🟡              │
   ┌──────── PRODUTO / ESTOQUE ────────┐ │      │ commission_ledger 547 🔴 (escrow antigo) │
   │ products 2.927 🟡 (custo do lote)  │ │      │ withdrawal_requests 3                    │
   │ store_inventory 13.470 🟡          │ │      └───────────────┬──────────────────────────┘
   │ lotes_recebidos 40 🟡              │ │                      │
   │ estoque_reservas 73                │ │      ┌──────── CONTABILIDADE INTERNA ───────────┐
   └────────────────────────────────────┘ │      │ financial_income 125 🟡 (só comissões)   │
                                          │      │ financial_expenses 440 🟡 (qualidade     │
                                          │      │   baixa; manual)                         │
                                          │      └──────────────────────────────────────────┘
          ILHAS FORA DO BANCO: planilha Nexus · contabilidade (SPED/PGDAS) · extratos bancários
```

---

## 5.2 Tabelas relevantes ao Value OS

### Pessoas e rede

| Tabela | Linhas | Desde | Uso no Value OS | Conf. | Ressalvas |
|---|---:|---|---|---|---|
| `app_users` | 1.173 | 29/09/2025 | contagens de usuários, papéis, atividade, saldos (agregados) | 🟡 | 89 colunas; **contém `password`, `access_token`, `cpf`, `email`, `phone`, `pix_key`** ⚫ — só views agregadas. `last_login` é **um carimbo sobrescrito** (sem histórico). `referred_by_id` cai no "Site Oficial" quando não há indicação real. `indicated_clients_count` nunca é gravado. |
| `customers` | 1.211 | 11/02/2026 | funil/CRM manual | 🟡 | Não é a mesma população de `app_users`. `source` tem padrão "site". |
| `career_levels` | 4 | — | percentuais por cargo | 🟡 | O código espera 8 níveis; o banco tem 4. Sem DDL no repositório. |
| `contrato_assinaturas` | 15 | — | aportes de parceiro (valor do aporte) | ⚫ | Nome, CPF, e-mail, IP, imagem da assinatura. |
| `concurso_*` (Rank Premiado) | 104 / 51 / 2 | — | custo de aquisição embutido | 🟡 | Prêmio é texto; sem custo no banco. |
| `passaporte_coupons`, `leilao20_*`, `bonus_*` | 124 / 105 / 53 | — | custo de campanha | 🟡 | Custo do bônus não vira despesa. |

### Leilão

| Tabela | Linhas | Uso | Conf. | Ressalvas |
|---|---:|---|---|---|
| `auctions` | 195 | contagem, preço final, vencedor, status | 🟡 | **Excluir `is_investment_plan = true`** (37 leilões, R$ 210.467,46) e `is_test_auction`. `status='sold'` **não prova venda**. Reativação **reusa o mesmo id**. Sem custo nem tipo. |
| `auction_messages` | 2.064 | **lances** (`message_type='bid'`) | 🟢 | A tabela `bids` é herança vazia — **não consultar**. Arremate Agora também grava `bid`. |
| `auction_auditoria` | 527 | trilha de mudança de vencedor/preço | 🟢 | Só-acrescenta (gatilho). |
| `reserva_ledger` | 611 | movimentos de saldo reservado | 🟢 | Desde 18/08/2026. Só cobre `saldo_reservado`. |

### Vendas, dinheiro e conciliação

| Tabela | Linhas | Uso | Conf. | Ressalvas |
|---|---:|---|---|---|
| `catalog_sales` | 897 | vendas, depósitos, arremates, adesões | 🟡 | **Mistura depósito (`kind='wallet_deposit'`) com venda.** Status em **2 idiomas** (cancelado/canceled/cancelled; entregue/delivered). Começa em **01/06/2026**. `pago_em` só preenchido desde 08/10. Cancelados com R$ 3 mi em `partner_plan`. Importação Nexus (`source='nexus'`) sem `product_id` nem custo. |
| `gateway_eventos` | 155 | caixa conciliado (Mercado Pago) | 🟢 | Só de 03 a 16/10/2026. **Sem RLS** (acesso público revogado). |
| `gateway_acoes`, `gateway_classificacoes` | 8 / 4 | ações sobre divergências | 🟢 | **Sem RLS**. |
| `commission_records` | 1.775 | comissão gerada/paga/estornada | 🟡 | Comissão **desde 01/08/2026**; **legível pela chave pública**; status `confirmed/paid/reversed/pending`; linhas **negativas** (`compra_com_saldo`). |
| `commission_ledger` | 547 | espera de 7 dias de indicação | 🔴 | 494 linhas são **escrow cancelado** (R$ 73.444,26) — **não somar**. |
| `comissao_pagamentos_manuais` | 24 | pagamentos por PIX fora do app (R$ 4.503,10) | 🟢 | |
| `withdrawal_requests` | 3 | saques (R$ 240) | 🟢 | PIX pago à mão. |
| `wallet_ledger` | 10 | estornos/bloqueios de carteira | 🔴 | **Não é extrato geral**; depósito e compra com saldo não deixam linha. |
| `bonus_saldos`, `bonus_ledger` | 17 / 53 | passivo de bônus (R$ 428,00) | 🟢 | Em centavos. |

### Contabilidade interna

| Tabela | Linhas | Uso | Conf. | Ressalvas |
|---|---:|---|---|---|
| `financial_income` | 125 | comissão retida/adesão (R$ 10.992,38 desde jul) | 🟡 | Dupla semântica; sem reversão em estorno; gravação "melhor esforço". Tela limita a 500 linhas. |
| `financial_expenses` | 440 | despesas | 🟡 | Categorias inconsistentes; `pago_integral` com valor 0; atrasos desde março; **inclui parcelas futuras até abr/2027**. |

### Produto, estoque, lotes

| Tabela | Linhas | Uso | Conf. | Ressalvas |
|---|---:|---|---|---|
| `products` | 2.927 | estoque a custo, preço, status | 🟡 | `cost_price` = custo do lote ÷ unidades, **igual por peça**; custo **recalculado**, não congelado; `market_value` **zerado em 02/09/2026** (1 de 1.469); **legível pela chave pública (inclui custo)**. |
| `store_inventory` | 13.470 | estoque do lojista (origem comprado/consignado/central) | 🟡 | Maioria deve ser "central". Repasse desligado. |
| `lotes_recebidos` | 40 | **custo do lote × valor de mercado × frete × taxa** | 🟡 | Melhor base para validar "compra a 20–25%". Valor de mercado vem da planilha do fornecedor. Vínculo com `products` é **por texto**, sem chave. |
| `stock_operations` | 1.699 | — | 🔴 | Só registra "zerar estoque"; não é movimento. |
| `comparai_cache` | 117 | preço de mercado (SerpApi/Zoom) | 🟡 | Cache de 7 dias, sem histórico. |

### Atribuição e atividade

| Tabela / campo | Uso | Conf. |
|---|---|---|
| `app_users.origem_trafego` (JSON) | origem do cadastro | 🟡 — só desde 25/09/2026; preenchido em 5,5% |
| `zeca_base_whatsapp` (3.229), `zeca_clientes` (100) | funil WhatsApp → conta → depósito | 🟡 — desde 16/10 |
| `system_logs` (2,9 mi) | **não usar para atividade** | 🔴 — log de diagnóstico, mutável, com PII |
| `live_sessions` (13.028) | presença de navegador | 🔴 — não é live commerce |

---

## 5.3 O que **não** usar

- **Herança Base44 vazia (0 linhas):** `bids`, `sales`, `payments`, `wallets`, `wallet_transactions`, `digital_wallets`, `digital_wallet_transactions`, `sale_commissions`, `tax_settings`, `payment_settings`, `sellers`, `stores`, `arrematantes`, `asaas_payments`, `cash_registers`, `price_history`, `pricing_formulas`, `deposit_packages`, `product_operations`, `influencer_*`, `licensee_leads`, `partner_plan_purchases`, `adesao_orders`, `retiradas`, `metas`, `shipping_carriers`, `suppliers`, `frete_settings`.
- **Cópias de segurança:** `bkp_products_20260820`, `bkp_store_inventory_20260820`, `market_value_backup_20260902`, `customers_backup_20260925`, `auctions_backup_reativacao_20260906`, `auction_messages_data_backup_20260903`, `financeiro_rotulos_backup_20260905`.
- **Operação interna do time (não é negócio de leilão):** `xgame_*`, `xperf_*`, `metodo_*`, `mapas_mentais`, `diario_bolso_*`, `xmusic_cache`, `reunioes_empresa`, `suporte_chamados`, `heloim_*`, `zeca_atendimentos`.

## 5.4 Colunas e tabelas que **nunca** entram no Value OS

`app_users.password`, `access_token`, `password_reset_token`, `cpf`, `email`, `phone`, `pix_key`, endereço · `app_users_auth` · `kyc_data` · `contrato_assinaturas` (dado pessoal) · `app_segredos` · `emails_enviados` · `email_codes` · `celular_confirmacoes`.
O Data Engine lê **só views agregadas**, sem identificador de pessoa (ou com identificador pseudonimizado).

## 5.5 O que **falta** no banco para o Value OS (dados faltantes)

| Dado | Por que importa | Onde nasceria |
|---|---|---|
| **Hora do pagamento confiável** para toda venda | reconhecimento correto da receita | `pago_em` (já existe; só vale desde 08/10) |
| **Custo congelado na venda** | margem por venda e por canal | coluna em `catalog_sales` ou tabela de itens |
| **Frete real pago** (Melhor Envio) e **taxa do gateway** por venda | margem de contribuição | hoje só em JSON ou não gravado |
| **Canal e loja** por venda | unit economics por canal | coluna `canal`/`loja_id` |
| **Chave produto → lote → compra** | validar a promessa de compra a 20–25% | `lote_id` em `products` |
| **Valor de mercado auditável** (fonte, data, snapshot) | validar "vende 20% abaixo" | tabela de preços com histórico |
| **Evento de adesão de licenciado** (data, valor, pago × concedido) | LICENSEES_* | `licensee_membership` |
| **Histórico de login/atividade** | ACTIVE_30D, retenção | tabela de eventos (não `system_logs`) |
| **Atribuição de origem por venda** e **gasto por canal** | CAC/LTV por canal | tabela de gasto + origem |
| **Depósito → leilão/produto** | PCP | vínculo na reserva |
| **Snapshots diários de KPI** | série histórica reconstruível | tabela de snapshot (no Value OS) |

> Todas as mudanças acima são **mudanças em produção** (várias em zona vermelha). Ficam como **proposta**, na Parte 10 e na Parte 12; **nada foi alterado.**

## 5.6 Camada de leitura proposta (read-only)

```
 papel do banco:  valueos_reader  (somente SELECT, sem acesso a tabela de pessoas)
 views dedicadas: vw_vo_vendas_pagas      (status normalizado, kind, valor, data BRT, pago_em)
                  vw_vo_depositos         (separa obrigação de receita)
                  vw_vo_lances            (message_type='bid', sem nome)
                  vw_vo_leiloes_produto   (sem is_investment_plan nem teste)
                  vw_vo_comissoes         (confirmed/paid/reversed, sem escrow)
                  vw_vo_passivos_carteira (soma das colunas de saldo)
                  vw_vo_estoque_custo     (por status)
                  vw_vo_lotes             (custo × mercado × frete)
                  vw_vo_receita_contabil  (financial_income)
                  vw_vo_despesas          (financial_expenses, categoria normalizada)
 regra do app:    criar por arquivo de migração (nunca SQL solto) e revisar privilégios
                  (precedente: 15/09 — mexer em privilégio derrubou o login)
```
