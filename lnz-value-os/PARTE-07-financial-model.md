# Parte 7 — Financial Model

> **Em português simples:** é a "conta de resultado" (DRE), o caixa e o balanço da empresa — do **passado** (realizado) e do **futuro** (previsão por drivers) — montados **a partir do Registry**, linha por linha, com a origem de cada número.
> **Semáforo:** 🟢 dá para preencher hoje com dado do banco · 🟡 dá, com ressalva ou aproximação · 🔴 falta dado.

---

## 7.1 Camadas (nunca misturar)

```
 ACTUAL (realizado)        ← vem do Registry; nunca digitado
 MANAGEMENT PLAN (meta)    ← aprovada pela administração; VERSIONADA, nunca editada em silêncio
 AI FORECAST               ← calculada por drivers (7.6)
 SCENARIO                  ← simulação (Scenario Lab) — nunca vira "oficial"
 OFFICIAL SNAPSHOT         ← fechamento mensal imutável (hash)
```

Visão de 6 anos que você pediu (2026 realizado parcial → 2031):

```
                  REALIZADO         PROJETADO ─────────────────────────────►
                  2026*   2027   2028   2029   2030   2031      (* jan–out, com ressalvas)
 RECEITA          R$X     R$X    R$X    R$X    R$X    R$X
 CRESCIMENTO       —      XX%    XX%    XX%    XX%    XX%
 LUCRO BRUTO      R$X ...
 EBITDA / FCFF    ...
```
A tela só mostra o valor quando a linha for 🟢/🟡. Linha 🔴 aparece como **"DADO NÃO DISPONÍVEL"**, nunca como zero.

---

## 7.2 DRE conceitual — o que cada linha precisa

**Decisão de base (a confirmar — Parte 12):** o modelo trata a empresa como **principal** (compra o lote, vende a mercadoria): **receita = valor da venda**; a comissão da rede e a taxa do gateway são **custo/despesa de venda**. O app hoje registra **só a comissão retida** como "receita" (visão de agente). Os dois pontos de vista aparecem lado a lado até o CEO escolher.

| Linha | Fonte / fórmula | Hoje | O que falta |
|---|---|---|---|
| **Receita bruta** (por canal: Leilão · Arremate Agora · Loja virtual · PDV/Nexus · Licenciamento · Live · Outras) | `GMV_GOODS` + `REVENUE_FEES` (principal) | 🟡 | canal não é coluna; `pago_em` só desde 08/10; Nexus parcial |
| (−) Impostos sobre venda | DAS pago (ou estimativa pelo regime) | 🔴 | regime em transição; sem lançamento; tributos pagos quase inexistentes nos extratos |
| **= Receita líquida** | | 🔴 | |
| (−) Custo do produto (CMV) | custo **congelado** na venda × quantidade | 🔴 | custo hoje é recalculado e **igual por peça** |
| (−) Logística variável | frete **real** pago ao Melhor Envio | 🔴 | não é gravado (só protocolo/etiqueta) |
| (−) Comissões | `commission_records` pagas + `FOUNDERS_POOL` (1%) | 🟡 | base de cálculo do 1%; comissões de executivos pagas por PIX sem vínculo |
| (−) Taxa de gateway | `gateway.taxa` (desde 03/10) | 🟡 | histórico sem taxa |
| **= Lucro bruto / margem bruta** | | 🔴 | depende do CMV |
| (−) Marketing | anúncios, **prêmios do Rank, bônus LEILÃO20/100, cupom do Passaporte** | 🔴 | bônus e cupom **não viram despesa** |
| (−) Pessoal | pró-labore, salários, **comissões de executivos** | 🟡 | `financial_expenses` inconsistente |
| (−) Tecnologia | servidor, software, IA, desenvolvimento | 🟡 | desenvolvimento de código é pago por quem? |
| (−) Administrativo / G&A | aluguel, contador, tarifas | 🟡 | atraso de mar a ago; classificação |
| **= EBITDA / margem EBITDA** | | 🔴 | |
| (−) D&A | depreciação; código capitalizado? | 🔴 | nada capitalizado |
| **= EBIT** | | 🔴 | |
| (±) Resultado financeiro | juros de consórcio, "custo do aporte", rendimento CDB | 🟡 | "custo do aporte" é lançado como despesa genérica |
| (−) Imposto sobre o lucro | regime | 🔴 | |
| **= Lucro líquido** | | 🔴 | |

---

> **Linha obrigatória (17/10/2026): cronograma fixo de obrigações com parceiros de compra** (principal, remuneração mensal e datas **por contrato**), **não** "5% da receita". Só os contratos A e B somam **R$ 10.500/mês** e **R$ 502 mil nominais** em 24 meses; o CEO informa que **só existem estes 2 contratos**; os pagamentos redondos que não são deles estão **por classificar** (Anexo C15). A linha de 5% foi **retirada do painel em 02/10/2026**; o Value OS **não a retira**.

## 7.3 O "mostrador de lacunas": o que o app deixa ver de **setembro/2026**

> Não é a DRE. É um retrato para mostrar **a distância entre o que entra, o que é receita e o que sai**, com os números que já temos.

| Setembro/2026 | R$ | Como ler |
|---|---:|---|
| Pedidos pagos no app (tudo) | 49.185 | Anexo B3 — **inclui R$ 15.937 pagos com saldo da carteira** (dinheiro que já tinha sido contado como depósito; ver Anexo C10) |
| ↳ **Depósito de carteira** (obrigação com cliente) | 30.773 | **não é receita** |
| ↳ Venda de mercadoria (arremate 11.454 + loja 5.461) | 16.915 | `GMV_GOODS` |
| ↳ Adesão paga | 1.497 | 1 adesão |
| **Receita contabilizada pelo app** (comissão retida + taxa) | **6.060** | `financial_income` |
| **Despesas efetivamente pagas** (`financial_expenses`) | **103.127** | aluguel 37,5 mil · cartão 23 mil · salários 19 mil · escritório 10 mil · "custo do aporte" 5,6 mil… |
| Despesas vencidas em aberto (acumulado fev–set) | **166.923** | ou estão vencidas, ou foram pagas e **não baixadas** |
| Despesas pendentes outubro | 119.768 | inclui salários R$ 53 mil |

**Correção de leitura (Anexo C10):** o **dinheiro novo** que entrou pelo Mercado Pago em setembro foi **≈ R$ 33 mil, 93% depósito de carteira**; os outros R$ 16 mil de "pedidos pagos" são compra com saldo (dupla contagem se somados ao depósito).

**Leitura (preliminar, a validar):** o **app sozinho** gera, em ordem de grandeza, **R$ 6–17 mil/mês** de resultado reconhecido contra **~R$ 100 mil/mês** de despesas pagas. Há outras fontes de caixa fora do app (varejo Nexus, vendas no Mercado Livre pela conta do Mercado Pago, aportes). **O Value OS precisa juntar tudo** — e a primeira pergunta de um investidor será: *"quem financia a diferença?"*. As evidências apontam para **aportes e parceiros** (19 PIX ≥ R$ 5 mil nos extratos; despesa "custo do aporte"), que **não são receita**.

---

## 7.4 Fluxo de caixa livre (FCFF)

```
 EBIT
 (+) D&A
 (−) imposto sobre o resultado operacional
 (−) CAPEX              → desenvolvimento de tecnologia, lojas, equipamentos
 (−) Δ capital de giro  → estoque (R$ 64 mil a custo), contas a pagar vencidas, float da carteira
 = FCFF
```

**Dois pontos em que o seu princípio "depósito ≠ receita" vira regra de cálculo:**
1. **Float de carteira (R$ 45,1 mil):** o dinheiro do cliente em carteira **não é caixa livre**. Na ponte do valor da empresa para o valor do sócio, entra como **dívida** (`WALLET_LIABILITY_TOTAL`). No fluxo de caixa, a variação do float aparece **separada** da operação.
2. **Aportes com repasse prometido:** **passivo**, não receita (ver 7.5).

---

## 7.5 Balanço relevante (o que precisa existir)

| Ativo | Fonte | Hoje |
|---|---|---|
| Caixa e equivalentes (Santander, Mercado Pago, **outras contas**) | extrato / Open Finance | 🔴 só jan–jun; balanço 2025 mostra R$ 705.958 que **não bate** com os bancos (Anexo C) |
| Estoque | `products` a custo | 🟡 ≈ R$ 63,9 mil (era R$ 321,4 mil em 26/05) |
| A receber (consignado) | `app_users.divida_consignado` | 🟢 R$ 10,44 |
| **Cotas de consórcio** (não operacional) | contratos | 🔴 informado: 21 cartas na empresa |
| Tecnologia (código) | custo de reposição | 🔴 não está no balanço |
| Passivo | | |
| **Float de carteira** (clientes, comissões, bônus, crédito de vendedor) | Registry | 🟢 ≈ R$ 45,1 mil |
| Contas a pagar vencidas / pendentes | `financial_expenses` | 🟡 R$ 166,9 mil vencido · R$ 119,8 mil pendente (qualidade baixa) |
| Tributos a pagar | balanço 2025 | 🔴 R$ 83,2 mil em 31/12/2025; situação atual desconhecida |
| Pró-labore / INSS a pagar | balanço 2025 | 🔴 R$ 85,0 mil em 31/12/2025 |
| **Aportes de parceiros / investidores** (repasse prometido) | contratos (15 assinaturas) + extratos | 🔴 **a medir (CEO)** |
| Parcelas de consórcio a vencer | contratos | 🔴 |
| Patrimônio líquido | contabilidade | R$ 616,8 mil em 31/12/2025 (capital R$ 500 mil integralizado) |

---

## 7.6 Forecast por drivers (nada digitado)

Cada fluxo de receita tem **uma árvore de drivers**; cada driver é uma métrica do Registry (ou uma premissa marcada `AI ASSUMPTION`).

```
 LEILÃO
   leilões de produto/mês × % com vencedor × % pago × preço final médio = GMV_AUCTION
   GMV_AUCTION − custo do produto − comissões (5% + 10% + retida…) − frete − gateway = margem de leilão
   baseline set/out:  24 leilões/mês · 88% com vencedor · preço final médio R$ 640
   (a calibrar)       custo do produto ← **hoje não existe por leilão**

 ARREMATE AGORA
   n de arremates imediatos × preço de compra imediata ... (hoje conta junto com lance)

 LOJA VIRTUAL
   pagantes ativos × frequência de compra × ticket médio = GMV_LOJA
   baseline set:  20 compras · R$ 273 de ticket

 CARTEIRA / DEPÓSITO  (alimenta leilão e loja — não é receita)
   pagantes × depósito médio × recorrência = WALLET_DEPOSITS
   baseline set:  36 pagantes · 71 depósitos · R$ 433 por depósito

 LICENCIAMENTO
   licenciados ativos × vendas médias por licenciado × (comissão da empresa − comissão paga)
   + novas adesões × preço da adesão (R$ 1.497 / R$ 5.000)
   baseline: 1 adesão paga em 4,5 meses

 VAREJO NEXUS (showroom + WhatsApp)
   executivos × vendas/dia × ticket  (jun: 453 vendas · ticket R$ 159)   ← **em queda desde junho**

 LIVE COMMERCE
   não existe integração; a Livoo saiu em 17/10 → **0 até haver dado**
```

> **Regra de honestidade:** previsão acima do que a **série histórica (curta, ~2,5 meses de dinheiro real)** sustenta fica etiquetada `AI ASSUMPTION` e **o painel mostra o que precisa ser verdade** para o número acontecer (Parte 8: *Milestone to Value*).

---

## 7.7 Plan × Actual — metas do memorando, hoje

Metas entram como `MANAGEMENT PLAN v1` (imutável; qualquer mudança vira v2 com data, autor e motivo).

| Meta (fonte: memorando) | Meta | Realizado hoje | Progresso | Obs. |
|---|---:|---:|---:|---|
| Receita mensal (dez/26) | R$ 1.000.000 | `GMV_GOODS` out (até 15): R$ 14.264 · entradas brutas out: R$ 40.458 | 1,4% – 4,0% | definir qual "receita" |
| Licenciados ativos (dez/26) | 300 | 15 (cargo) / 23 (`role`) / ~8 ativos em 30 d | 3% – 8% | aguarda definição |
| Lojas físicas (dez/26) | 8 | 1 conta `loja_fisica`; tabela `stores` vazia | — | |
| Licenciados (2027) | 1.000 | — | — | |
| Vendedores ativos (2027) | 10.000 | 31 com cargo vendedor | 0,3% | |
| Receita 2026 | R$ 12 mi | jan–mai memorando R$ 308,6 mil | 2,6% | **não fecha com a meta de dez/26** (Anexo A item 13) |
| Receita 2027 / 2028 | R$ 36 mi / R$ 96 mi | — | — | |

---

## 7.8 Cenários

Três cenários **gerados dos drivers**, não de metas:

| Cenário | Regra |
|---|---|
| **Conservador** | drivers no **pior quartil** do histórico (set/out) e sem nenhum marco futuro |
| **Base** | drivers na **mediana** recente + marcos de **alta** confiança (ex.: crescimento orgânico de pagantes) |
| **Otimista** | drivers no **melhor quartil** + marcos de **média** confiança (ex.: R$ 1 mi/mês) |

Aviso fixo em toda tela de cenário: **"SIMULAÇÃO — NÃO É VALUATION OFICIAL"**.

---

## 7.9 O que preciso que você decida para fechar o modelo (resumo; detalhe na Parte 12)

1. **Principal × agente** (receita = venda ou = comissão).
2. **Plano de contas** único (hoje as despesas têm categorias soltas).
3. **Data de corte** da série oficial (01/08/2026) e **como tratar nov/25–mai/26**.
4. **Tratamento do consórcio** (ativo não operacional) e do **que está no nome do sócio**.
5. **Float de carteira como dívida** no valor do sócio (recomendado).
6. **Base de cálculo do 1% dos fundadores.**
7. **Quais aportes são capital, quais são passivo com repasse** (você vai me passar).
