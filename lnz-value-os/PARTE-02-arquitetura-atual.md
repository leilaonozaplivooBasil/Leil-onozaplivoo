# Parte 2 — Arquitetura atual

> **Resumo em uma frase:** hoje a empresa tem **quatro ilhas de dados** que não se conversam — o app, a planilha Nexus, a contabilidade do contador e os bancos — e **cada uma conta uma receita diferente**.

---

## 2.1 As quatro ilhas

```
 ILHA 1 — O APP (Supabase + Vercel)         ILHA 2 — NEXUS (Google Sheets)
 ──────────────────────────────────         ───────────────────────────────
 leilão, loja, carteira, comissões          vendas do showroom e WhatsApp
 dinheiro "real" só desde 01/08/2026        lançadas à mão por 6 executivos
 receita = comissão retida + loja           importada p/ o app por cron diário
 R$ 40–49 mil/mês entrando (set/out)        sem produto nem custo na venda
        │                                          │
        │  (nenhuma ponte automática)              │
        ▼                                          ▼
 ILHA 3 — CONTABILIDADE (contador externo)  ILHA 4 — BANCOS (Santander + Mercado Pago)
 ─────────────────────────────────────────   ──────────────────────────────────────────
 ECD/ECF 2025, balancete, DRE                extratos mensais em PDF
 PGDAS-D 2026 (Simples)                      PIX, liberações, consórcios, tributos
 declaração de faturamento p/ banco          aportes, retiradas, transferências internas
 receita 2025: R$ 1,19 mi                    entradas jan–jun: R$ 0,66 mi (terceiros)
        └─────────────  4 receitas diferentes, 0 conciliações automáticas  ─────────────┘
```

| Ilha | Dono | Frequência | Prova do número |
|---|---|---|---|
| App | time de tecnologia | tempo real | banco de dados (rastreável) |
| Nexus | executivos | diária (à mão) | planilha + comprovantes PIX em pasta do Drive |
| Contabilidade | contador | anual/mensal | SPED (ECD/ECF), PGDAS |
| Bancos | financeiro | mensal (PDF) | extrato do banco |

**Consequência para o Value OS:** o motor precisa **ligar as quatro ilhas** (Parte 3) e **mostrar onde elas discordam** (Discrepancy Radar), em vez de escolher uma em silêncio.

---

## 2.2 A ilha do app — como é por dentro

### Camadas

```
 NAVEGADOR / APLICATIVO (Vite + React, PWA, Capacitor iOS/Android)
   154 telas · 690 componentes · 293 arquivos em src/lib
          │  chave pública do Supabase (leitura direta de várias tabelas)
          │  crachá de sessão 30 dias (cabeçalho x-sessao)
          ▼
 SERVIDOR (Vercel, 209 rotas em api/functions + ~100 auxiliares em api/_lib)
   login próprio (não é Supabase Auth) · regras de papel no servidor
   81 rotas barram sem crachá · 128 só registram
          │  chave de serviço (service role)
          ▼
 BANCO (Supabase, sa-east-1) — 154 tabelas, 151 com RLS
   funções SQL (RPC), gatilhos, 5 tarefas agendadas (pg_cron)
          ▲
 CRONS DA VERCEL (23) — leilão a cada minuto, liquidação a cada 10 min,
   conciliação com Mercado Pago a cada 30 min, fechamento diário, vigias…
          ▲
 1 EDGE FUNCTION (whatsapp-router): atendimento por WhatsApp (Zeca/Heloim) com IA
```

### Integrações externas (só nomes)

| Área | Quem |
|---|---|
| Pagamento | **Mercado Pago** (PIX e cartão). Asaas = legado, proibido pela zona vermelha |
| Frete | Melhor Envio |
| WhatsApp | Z-API (ativo), Evolution API (legado) |
| E-mail / push | Brevo e Resend / FCM e APNs |
| IA | Anthropic (Claude), Vercel AI Gateway, OpenAI (Whisper) |
| Busca de preço (ComparAI) | SerpApi, SearchApi.io, Zoom.com.br |
| Outros | Google (login, Drive, planilha Nexus), Slack, Sentry, PostHog, Meta Pixel/GA4 |
| **Não existe** | TikTok Shop (só link de perfil). **Livoo: deixou de ser parceira em 17/10/2026** |

### Onde o dinheiro entra e sai (mapa)

```
 CLIENTE ─► Mercado Pago (PIX/cartão) ─► webhook ─► catalog_sales (paga)
                                             │            │
                                             │            ├─ kind=wallet_deposit ─► saldo_disponivel   (OBRIGAÇÃO, não é receita)
                                             │            ├─ kind=loja/produto   ─► baixa estoque + comissões
                                             │            └─ kind=arremate       ─► (só na liquidação)
                                             ▼
                                   gateway_eventos (registro bruto) ─► conciliação (a cada 30 min)

 LANCE ─► reserva (reserva_ledger) ─► MARTELO ─► status=awaiting_payment + comissões + fatia retida (financial_income)
                                         └──► LIQUIDAÇÃO (cron 10 min) ─► catalog_sales kind=arremate + baixa estoque

 COMISSÃO ─► commission_records ─► commission_balance ─► SAQUE (PIX manual) ou compra na loja
 DESPESA  ─► financial_expenses (manual / IA em boleto / gastos fixos recorrentes)
 IMPOSTO  ─► só estimativa em tela (Simples) — nenhum lançamento contábil
```

### Quem calcula "faturamento" hoje (6 respostas diferentes)

| Tela / função | Conta o quê |
|---|---|
| Financeiro › Visão Geral | soma de `financial_income` (comissões/taxas), sem período, máx. 500 linhas |
| Financeiro › Lucro do Dia | `total_amount` de hoje − custo atual − comissão (30% loja / 5% leilão) − Simples |
| Painel de Alavancagem | depósitos + compras reais |
| CRM / Diretoria | loja + produto + arremate pagos (lista de "pago" diferente em cada uma) |
| Painel do Investidor (SQL) | pagos via gateway, por área |
| Fechamento diário (SQL) | depósitos + loja + arremates por dia (fuso de Brasília) |

---

## 2.3 O que já existe e **ajuda** o Value OS

| Item | Por que ajuda |
|---|---|
| **Conciliação Mercado Pago × app** (`painel_conciliacao`, `auditoriaGateway`) | Já classifica: bate, dinheiro saiu, pago lá/não aqui, valor diferente, venda fora do app, movimentação entre contas. **Embrião do Discrepancy Radar.** |
| **Fechamento diário** salvo em `system_logs` (desde ~08/10) | Embrião de snapshot — precisa virar tabela imutável. |
| **Dashboard da Diretoria** com etiqueta `dado / aproximação / sem fonte` por KPI | Embrião do Metrics Registry. |
| **Extratos só-acrescenta** (`reserva_ledger`, `commission_records`, `bonus_ledger`, `auction_auditoria`) | Padrão a copiar para o Evidence Ledger. |
| **Zona vermelha** (`docs/ZONA_VERMELHA.json`), skill "antes de mesclar", janela de deploy | Cultura de controle de mudança. |
| **Marco oficial de 01/08/2026** (`docs/MARCO-OFICIAL-AGOSTO-2026.md`) | Já define o que é "dinheiro real" — base para o corte da série oficial. |
| Libs `dinheiroReal`, `custoProduto`, `simplesNacional` | Regras de negócio já escritas. |

## 2.4 O que **atrapalha**

| Problema | Efeito |
|---|---|
| Sem livro-razão único de saldo | Provar "depósitos − gastos = saldo" exige cruzar 4 tabelas. |
| `financial_income` com dupla semântica | Receita do app mistura comissão paga com comissão retida. |
| Sem hora do pagamento (`pago_em` só desde 08/10) | Receita reconhecida na data errada. |
| Custo recalculado, não congelado | Margem de uma venda muda depois. |
| Sem margem por leilão/SKU | Não há unit economics. |
| `system_logs` mutável, 2,9 mi de linhas | Não serve como trilha de auditoria. |
| Ledgers "só-acrescenta" por convenção (sem gatilho que bloqueie UPDATE/DELETE) | Evidência pode ser alterada. |
| Chave pública lê custo de produtos e comissões | Não pode hospedar dado de investidor. |
| Testes que não executam SQL | KPIs em SQL nunca foram testados de verdade. |
| Legado Base44 (`raw_base44` em 49 arquivos; status em 2 idiomas) | Contamina séries históricas. |

## 2.5 Os dois sites e o dossiê, no mapa

```
 valuationleilaonozap.com ─┐      (hospedagem desconhecida — não está na Vercel da conta)
 investmentmemorandum…     ┘──►  narrativa estática · nenhum número vem do sistema
                                  nenhum dos dois aparece no código do app

 Drive "Dossiê 2025-2026" ──►  PDFs entregues a investidores (balanço, DRE, extratos, contrato)
                                  → ver Anexo C: receitas diferentes entre si
```
