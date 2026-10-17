# Parte 9 — Investor Experience

> **Meta que você pediu:** quem abrir o sistema entende **quanto vale em 30 segundos**, **por que vale em 1 minuto**, **tração, financeiro, futuro, risco e dados em 5 minutos**, e consegue fazer a **análise inicial inteira em 30 minutos**.
> Os valores nos desenhos abaixo são **marcadores** (`R$ XX,X M`), não números reais.

---

## 9.1 Quem vê o quê

| | **PUBLIC** (os 2 sites) | **INVESTOR** (convidado, NDA aceito) | **BOARD** (CEO, conselho, auditor) | **ADMIN** (operação do Value OS) |
|---|---|---|---|---|
| Narrativa institucional | ✅ | ✅ | ✅ | ✅ |
| KPIs autorizados (com "última atualização") | só os marcados como públicos | ✅ | ✅ | ✅ |
| Valuation (faixa), EV, equity | ❌ | ✅ **oficial** (não "ao vivo") | ✅ + Shadow | ✅ |
| Modelo financeiro, projeções autorizadas | ❌ | ✅ | ✅ | ✅ |
| Evidence Ledger (ver a prova) | ❌ | **resumo** (fonte, período, snapshot) | **completo** (consulta, fórmula, bruto, ajustes) | ✅ |
| Data Room | ❌ | só **pastas e arquivos liberados** a ele | tudo | gerencia |
| Metodologia, premissas, **discrepâncias**, auditoria | ❌ | metodologia | ✅ tudo | ✅ |
| Scenario Lab | ❌ | ✅ (simulação) | ✅ | ✅ |
| Ask LNZ AI | ❌ | só dados do nível dele | só dados do nível dele | ✅ |

**Regra de ouro:** nenhum número **ao vivo** (Live) aparece para o investidor. Ele vê **o último fechamento oficial** e, quando permitido, o **Shadow** com a etiqueta *indicativo*. Isso evita "valuation piscando como criptomoeda".

**Público: só narrativa.** Hoje os sites mostram "R$ 25 milhões" e "80+ licenciados". No novo desenho, **número nenhum** vai para a vitrine pública enquanto não houver definição e prova — a vitrine leva ao **login**.

---

## 9.2 Os quatro tempos

### 30 segundos — a tela "Overview"

```
 ┌────────────────────────────────────────────────────────────────────────────┐
 │ LNZ VALUE OS                                  Leilão NoZap · Compras Full   │
 │                                                                             │
 │              VALUATION INDICATIVO                (snapshot oficial 30/09)   │
 │                                                                             │
 │                      R$ XX,X M                                              │
 │          faixa defensável:  R$ XX,X M ──────●────── R$ XX,X M              │
 │                                                                             │
 │   Enterprise value R$ XX,X M     Equity value R$ XX,X M     Δ 30 dias +X%   │
 │                                                                             │
 │   Qualidade do dado 41/100   Confiança 38/100   Risco 62/100                │
 │   ▲ baixa qualidade alarga a faixa — veja "Por quê" ▼                       │
 │                                                                             │
 │   Receita mensal   GMV   EBITDA   Margem   FCFF   CAC   LTV   LTV/CAC      │
 │   R$ X mil       R$ X    R$ X      X%       R$ X   —     —      —           │
 │   Clientes pagantes  Retenção  Churn   Licenciados ATIVOS (definição ⓘ)     │
 │                                                                             │
 │   [ Por que vale? ]  [ Ver evidência ]  [ Cenários ]  [ Perguntar à IA ]    │
 └────────────────────────────────────────────────────────────────────────────┘
```

Quando o dado **não existe**, a caixa **não mostra zero**:

```
   EBITDA        DADO NÃO DISPONÍVEL     ⓘ falta: custo congelado por venda e
                                            classificação das despesas  → ver plano
```

### 1 minuto — "Por que vale"

Uma tela única com **a ponte** (waterfall) da **referência do fundador** até o **valor independente**, mostrando **que parte da diferença vem de quê** (receita, margem, passivos, riscos…), **e o que precisa acontecer para a faixa subir** (Marco → Valor).

### 5 minutos — as abas

`Tração` · `Financeiro` · `Futuro` · `Risco` · `Dados` — cada uma com **3 gráficos no máximo** e um quadro "o que isto prova / o que isto **não** prova".

### 30 minutos — análise completa

`Métodos de valuation` · `Comparáveis` · `Transações` · `Sensibilidade` · `Scenario Lab` · `Memorando` · `Data Room` · `Evidence Ledger` · `Ask LNZ AI` · exportações.

---

## 9.3 Navegação (os seus 20 itens, por papel)

| # | Item | Investor | Board | Observação |
|---|---|:-:|:-:|---|
| 01 | Overview | ✅ | ✅ | |
| 02 | Live Valuation | oficial | ✅ + shadow | |
| 03 | Actual × Forecast | ✅ | ✅ | |
| 04 | Financials | ✅ | ✅ | |
| 05 | EBITDA | ✅ | ✅ | "DADO NÃO DISPONÍVEL" até haver custo por venda |
| 06 | Cash Flow | ✅ | ✅ | |
| 07 | Business Drivers | ✅ | ✅ | árvores da Parte 7.6 |
| 08 | Unit Economics | ✅ | ✅ | |
| 09 | Valuation Methods | ✅ | ✅ | |
| 10 | Comparables | ✅ | ✅ | |
| 11 | Transactions | ✅ | ✅ | |
| 12 | Sensitivity | ✅ | ✅ | |
| 13 | Scenario Lab | ✅ | ✅ | |
| 14 | Value Bridge | ✅ | ✅ | |
| 15 | Milestone to Value | ✅ | ✅ | |
| 16 | Investment Memorandum | ✅ | ✅ | dinâmico (9.5) |
| 17 | Data Quality | resumo | ✅ completo + Radar | |
| 18 | Evidence Ledger | resumo | ✅ | |
| 19 | Data Room | liberado | ✅ | |
| 20 | Ask LNZ AI | ✅ | ✅ | |

---

## 9.4 Evidence Ledger — o "clique para provar"

```
 RECEITA SETEMBRO (GMV de mercadoria)                R$ 16.915,06      [ VER EVIDÊNCIA ]
 ─────────────────────────────────────────────────────────────────────────────────────
 metric_id        GMV_GOODS v1.0           período     01/09–30/09/2026 (BRT)
 fonte            banco do app · catalog_sales        snapshot   2026-10-01 · hash a3f…9c
 filtro           status PAGA · kind ∈ {loja, arremate, produto} · sem depósito/adesão
 consulta         [ver SQL]  → resultado bruto 17 linhas-grupo
 bruto            R$ 16.915,06   ajustes: 0,00   final: R$ 16.915,06
 conciliação      gateway: 34 de 36 pagamentos conferidos · 2 sem rastro  → ver Radar
 extraído em      17/10/2026 15:07       confiança 78/100       rótulo VERIFIED*
 *VERIFIED = recalculado do banco; "conferido com o banco real" exige extrato (Open Finance)
```

*(No desenho acima, o valor de R$ 16.915,06 é o GMV real de setembro (Anexo B3); o **hash, o nº de pagamentos conferidos, a confiança e o horário são ilustrativos**.)*

Objetivo: **um terceiro autorizado reconstrói o número sozinho**. Para o investidor, a visão é a **primeira metade** (fonte, período, snapshot, rótulo). Para o conselho, **tudo**, incluindo a consulta.

---

## 9.5 Memorando dinâmico e vitrine de valuation (as duas "portas")

**Regra de edição:** a **narrativa estratégica é da administração** — a IA **nunca** a altera. Os **números** vêm do Registry.

| Trecho do memorando | Hoje | No novo desenho |
|---|---|---|
| Carta do fundador, tese, problema, visão 2035, cultura, X-EOS, Vale do Recreio | texto fixo | **permanece** (controle da administração, com histórico de versões) |
| "R$ 181K de receita em maio", gráfico nov/25–mai/26 | texto fixo | **sai** da vitrine pública; vira bloco **com fonte, "última atualização" e etiqueta**; a série só volta quando houver prova (Anexo C) |
| "80+ licenciados ativos" | texto fixo | **dinâmico**: `LICENSEES_ACTIVE_30D` (+ as outras 3 definições visíveis) |
| "178K linhas / 883 arquivos" | texto fixo | **dinâmico**: `TECH_LOC` com data e definição |
| "R$ 25 milhões" | texto fixo | **dinâmico**: aparece como **"Referência do fundador"** ao lado do **valuation independente** (quando autorizado), nunca como "valor atual" |
| "Compra a 20–25% do mercado" | texto fixo | `LOT_COST_TO_MARKET` com a base (valor da planilha do fornecedor) |
| Metas 2026/2027 | texto fixo | `MANAGEMENT PLAN v1` com **progresso real** |
| "Livoo — sociedade em fase final" | texto fixo | **sai** (parceria encerrada em 17/10/2026) |
| "TikTok Shop ativo", "Leilão Inteligente 99%", "PHIZ" | texto fixo | **só voltam com evidência** |

Cada número do memorando mostra **"atualizado em dd/mm/aaaa hh:mm"** e o nível de confiança.

**Rodapé "Documento confidencial — uso restrito para investidores":** passa a ser **verdadeiro** (porque o memorando completo só abre depois de login + NDA).

---

## 9.6 Data Room

```
 DATA ROOM
 ├── 01 Corporativo      contrato social ATUAL · quadro de sócios · atas · organograma · CNPJ
 ├── 02 Financeiro       balanço · DRE · balancete · extratos (por conta) · conciliações
 ├── 03 Jurídico         contratos de aporte · parcerias · consórcios · litígios
 ├── 04 Fiscal           ECD · ECF · PGDAS · DAS pagos · certidões · opção de regime
 ├── 05 Tecnologia       titularidade do código · contratos de desenvolvimento · licenças · arquitetura
 ├── 06 Contratos        fornecedores · leiloeiros · licenciados · gateway
 ├── 07 Propriedade intelectual   marca · domínios · INPI · software
 ├── 08 Governança       regimento · política de comissões · acordo de sócios
 └── 09 Materiais        memorando · apresentações · FAQ (alimentado pelas perguntas)
```

| Recurso | Padrão de mercado | Como fica |
|---|---|---|
| Convite por e-mail + 2º fator | sim | obrigatório |
| **NDA com aceite registrado** (versão do texto, IP, data) | sim | obrigatório **antes** de qualquer número |
| Permissão **por pasta e por arquivo** | sim | por pessoa e por grupo |
| **Marca d'água** com nome e e-mail | sim | em todo arquivo aberto/baixado |
| Prazo de acesso e revogação | sim | com data de expiração |
| Registro de **cada abertura** (quem, quando, quanto tempo, quais páginas) | sim | só-acrescenta |
| **Perguntas e respostas** (Q&A) | sim | respostas viram FAQ e alimentam a Ask LNZ AI **só depois de aprovadas** |
| **Ligação documento ↔ métrica** | **diferencial** | cada KPI aponta para o documento que o sustenta (extrato, balanço, contrato) |

**O que não vai ao Data Room:** documentos pessoais de sócios (RG, comprovante de residência, informe de rendimentos pessoal) — **não são necessários** e aumentam o risco com a LGPD. (O dossiê atual os contém; **recomendo retirá-los** das pastas compartilhadas.)

**Checklist antes de abrir o Data Room a qualquer investidor** (decorre do Anexo C):
1. contador independente explica as 4–5 receitas e o total da declaração ao banco;
2. extratos de **2025** e **todas as contas**;
3. contrato social **atual**;
4. aportes, consórcios e contratos em pasta própria;
5. tributos: situação de 2025 e do Simples 2026;
6. remover dados pessoais.

---

## 9.7 Ask LNZ AI

**Regras:**
1. Responde **só** com dado que **o papel de quem pergunta** pode ver — o filtro vem **antes** de a pergunta chegar ao modelo, não depois.
2. Toda resposta traz **fonte, período e snapshot**.
3. Sem dado: **"DADO NÃO DISPONÍVEL"**. **Nunca inventa.**
4. Não altera narrativa, metodologia nem número.
5. Registra pergunta, resposta e dado usado (auditoria).
6. Nenhum endpoint de IA aberto (o `InvokeLLM` do app hoje é aberto — **não reutilizar**).

**Como ela responderia hoje às suas perguntas de exemplo:**

| Pergunta | Resposta honesta com os dados de hoje |
|---|---|
| "Qual foi o crescimento nos últimos 90 dias?" | "Entradas pagas no app: ago R$ 11,7 mil → set R$ 49,2 mil → out (até 15) R$ 40,5 mil. **63–65% dessas entradas são depósitos de carteira (não são receita).** Mercadoria vendida: set R$ 16,9 mil, out (15 dias) R$ 14,3 mil. **A série oficial começa em 01/08/2026.** *(fonte: `catalog_sales`, snapshot…)*" |
| "Quantos licenciados estão realmente ativos?" | "**Depende da definição.** Cargo licenciado: 15 · papel `licensee`: 23 · com acesso em 30 dias: 8. **Nenhuma conta tem hoje 'venda real paga' associada de forma auditável**; a métrica `LICENSEES_ACTIVE_30D` aguarda definição." |
| "Qual é a margem atual?" | "**DADO NÃO DISPONÍVEL.** O custo não é gravado por venda. *Aproximação não oficial:* loja +6% a +15% sobre custo atual." |
| "Qual o EBITDA?" | "**DADO NÃO DISPONÍVEL.** Despesas sem classificação confiável." |
| "Por que o valuation mudou?" | "Ainda não há dois snapshots oficiais para comparar." |
| "Qual seria o valuation com R$ 1 milhão/mês?" | "Posso rodar como **cenário** (Marco → Valor). **Hoje o maior mês comprovado no app tem entradas de R$ 49 mil; a meta exige 20× — a conta mostra o que precisa ser verdade.** *Simulação, não valuation.*" |
| "Quais os maiores riscos?" | lista os 13 fatores com a **nota de cada um** e a evidência |

---

## 9.8 Onde dá para **inovar** (o que mercado ainda não faz junto)

| # | Ideia | Referência de mercado | O que é diferente aqui |
|---|---|---|---|
| 1 | **Valuation cego com selo (commit-reveal)** | método único por estágio, como a [Equidam](https://www.equidam.com/five-startup-valuation-methods/) | pesos fixados **antes**, referência do fundador **lacrada com hash** e aberta só depois |
| 2 | **"Ver evidência"** em todo número, com consulta reproduzível | salas de dados mostram o documento; **não** o cálculo | **o número carrega a própria prova** |
| 3 | **Pacote de reconstrução** | auditoria pede planilha e extratos | arquivo único com consulta + hash que **um terceiro roda e confere** |
| 4 | **Discrepancy Radar contínuo** | conciliação mensal | banco × gateway × app × contabilidade **todo dia**, com causa provável |
| 5 | **Viagem no tempo ("como era em…")** | — | qualquer snapshot oficial reabre **exatamente como foi mostrado** |
| 6 | **Painel de transparência atrás de login** | [Baremetrics Open Startups](https://venturebeat.com/ai/watch-what-open-startups-earn-in-real-time-with-this-handy-tool) expõe métricas ao vivo **publicamente** | aqui é **seletivo, auditado e por papel** |
| 7 | **Q&A que vira FAQ aprovada** | salas de dados têm Q&A | resposta **aprovada** alimenta a IA — a IA nunca "aprende" sozinha |
| 8 | **Marco → Valor** com "o que precisa ser verdade" | análise de sensibilidade | ranqueia metas por **impacto × confiança** e mostra a **distância** do realizado |

**O que a calculadora da Buyco é, e por que o Value OS não é isso:** pela imprensa ([Folha Vitória](https://www.folhavitoria.com.br/geral/buyco-oferece-ferramenta-gratuita-para-valuation-de-pmes)), é uma ferramenta **gratuita** de valuation para PMEs, usada para captar contatos, com mais de 100 mil avaliações — **perguntas de formulário × múltiplos**. O Value OS usa **dado real, evidência e rastro**. *(Não consegui abrir a página dela; se quiser que eu estude a tela, mande prints.)*

---

## 9.9 Visual

**Referência:** *investment bank + fintech + private equity + Bloomberg + Apple* — **limpo, premium, simples, institucional**. **Não** pode parecer cassino, bet, dashboard genérico nem ERP antigo.

| Princípio | Como |
|---|---|
| Espaço | muito respiro; uma ideia por tela |
| Tipografia | forte; **números grandes**; hierarquia perfeita |
| Cor | **poucas**: neutros + **1** cor de destaque; **vermelho/âmbar só para alerta de dado** (nunca para decorar) |
| Gráficos | claros; **3 por aba, no máximo**; eixos honestos (zero real); incerteza **sempre desenhada** (faixa, não linha única) |
| Estados de dado | `VERIFIED` · `MANAGEMENT` · `FORECAST` · `ASSUMPTION` com **ícone e legenda fixos** |
| **Evitar** | rosa da Livoo (saiu em 17/10); verde-neon "vitória"; roleta; confete; contagem regressiva |
| Acessibilidade | mínimo 12 px; contraste; foco visível (segue o espírito do `GUIA_DE_DESIGN` do app) |

> A paleta do Value OS será **própria** (como a sub-marca "PC" tem a dela no app) — **não** herda a identidade de consumo "verde/leilão".

---

## 9.10 Exportações

`Modelo financeiro (XLSX)` · `Valuation (PDF)` · `Investment Memorandum (PDF)` · `CSV dos KPIs` · `Relatório do Conselho (PDF)` — todos com **marca d'água** e **registro de quem exportou**. O painel substitui a planilha **visualmente**, mas o padrão financeiro (abas DRE/FCFF/WACC/sensibilidade) continua existindo.
