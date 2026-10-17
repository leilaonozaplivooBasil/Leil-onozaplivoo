# Parte 10 — Roadmap de implementação

> **Nada disto começa sem a sua aprovação.** As durações são **estimativas grossas** (equipe pequena: 1 desenvolvedor sênior + 1 analista financeiro + apoio meu), e dependem das decisões da Parte 12 e dos dados que você ainda vai mandar. **Não são compromisso de prazo.**

---

## 10.1 Visão geral

```
 SEMANAS     0    2    4    6    8   10   12   14   16   18   20 ───────►
 FASE 0   ███░ Decisões, dados e limpeza dos documentos        (paralelo a tudo)
 FASE 1        ░████████ Fundação: acesso, registro de métricas, ingestão, evidência
 FASE 2              ░██████████ Modelo financeiro e conciliação
 FASE 3                    ░███████████ Motor de valuation v1.0 (+ modo cego)
 FASE 4                              ░████████████ Experiência: portal, data room, IA, portas
 FASE 5                                          ░░░░░░░░ Operar: fechamento mensal, backtest, laudo
```

---

## 10.2 Fase 0 — Decisões, dados e limpeza (semanas 0–2; **depende de você**)

| Entrega | Responsável | Critério de pronto |
|---|---|---|
| **Decisões da Parte 12** (perímetro, "receita", licenciado, hierarquia de fontes…) | CEO | documento com as respostas |
| **Dados que faltam:** extratos de 2025 e jul–out/2026 (todas as contas), contrato social atual, aportes, consórcios, balancete 2026, PGDAS/DAS 2026, CSV completo do Nexus (inclui nov/25–mai/26) | CEO / financeiro / contador | arquivos na pasta do Drive |
| **Classificar os 19 PIX ≥ R$ 5.000** (venda, aporte, empréstimo, parte relacionada) | financeiro | planilha com a natureza de cada um |
| **Revisão independente** das receitas (livros × PGDAS × declaração × banco) e da declaração ao banco | contador independente + advogado | parecer escrito |
| **Retirar do Drive compartilhado** os documentos pessoais de sócios | CEO | pasta 08/12/14 fora do compartilhamento |
| **Atualizar os dois sites** (retirar Livoo, "TikTok ativo", "99%", números sem fonte) **ou** levá-los atrás de login | CEO | texto aprovado |

---

## 10.3 Fase 1 — Fundação (semanas 2–6)

| Entrega | O que é | Reuso do app |
|---|---|---|
| Projeto novo (repo + Vercel + **Supabase novo**) | isolamento total da produção | copia o padrão de pastas e testes |
| **Login + 2º fator + convite**, papéis `PUBLIC/INVESTOR/BOARD/ADMIN`, **registro de acesso** | porta de entrada | ideia do `exigirPapel`, mas **sem** o crachá caseiro |
| **Metrics Registry v1** (≈ 30 métricas centrais, Parte 6) | dicionário versionado | aproveita o Dashboard da Diretoria (`dado/aproximação/sem_fonte`) |
| **Data Engine v1:** extração **somente leitura** do app (views) + **upload com hash** de extrato, PGDAS, balancete | cada carga vira um "lote" | |
| **Evidence Ledger v1** (só-acrescenta, hash encadeado, bloqueio de UPDATE/DELETE no banco) | prova de cada número | copia o padrão de `reserva_ledger` e `auction_auditoria`, **com o bloqueio que eles não têm** |
| **Snapshots** Live/Shadow/Oficial | séries imutáveis | evolui o `fechamento_diario` |
| **Data Quality Score v1** | placar 0–100 | |
| Testes com **Postgres real** (não banco falso) | confiança nos cálculos em SQL | **novo** (hoje os testes do app não executam SQL) |

**Critério de saída:** 30 métricas calculadas, cada uma com evidência, em dois snapshots seguidos que **batem entre si**.

---

## 10.4 Fase 2 — Modelo financeiro e conciliação (semanas 4–10)

| Entrega | Detalhe |
|---|---|
| **Plano de contas único** e mapa das despesas existentes | uma categoria por linha da DRE |
| **DRE e FCFF realizados** (mensal) | com semáforo por linha (Parte 7.2) |
| **Radar de discrepâncias** | banco × gateway × app × contabilidade × planilha, **diário** |
| **Livro de aportes e consórcios** | cada aporte/cota com contrato, saldo, parcelas, repasse |
| **Plan × Actual** | metas v1 do memorando (imutáveis) com progresso real |
| **Forecast por drivers** | árvores da Parte 7.6, calibradas no histórico |

**Critério de saída:** DRE de **3 meses** (ago–out/2026) com **pelo menos 70% das linhas 🟢/🟡** e as 4 ilhas conciliadas (ou com divergência **explicada**).

---

## 10.5 Fase 3 — Motor de valuation v1.0 (semanas 6–14)

| Entrega | Detalhe |
|---|---|
| Biblioteca de cálculo **pura e testada** | DCF/FCFF, múltiplos, transações, Método VC, soma das partes, economia por unidade, custo de reposição, NAV |
| Banco de **comparáveis e transações** | com fonte, data e justificativa (Parte 8.2) |
| **Metodologia v1.0** com pesos e premissas **pré-registrados** (hash) | aprovada pelo CEO (e idealmente por um terceiro) |
| **Faixa por simulação**, Sensibilidade, Scenario Lab | |
| **Modo cego** (referência do fundador lacrada) | a primeira rodada **oficial** só roda depois |
| **Value Bridge** e **Marco → Valor** | |
| **Casos de referência**: planilhas conhecidas de DCF/múltiplos que o motor **precisa reproduzir** | prova de que a conta está certa |

**Critério de saída:** o motor reproduz **100%** dos casos de referência; uma rodada completa gera faixa, ponte e relatório com **todas as premissas visíveis**.

---

## 10.6 Fase 4 — Experiência (semanas 10–18)

Cockpit do conselho · Portal do investidor · **memorando dinâmico** e **vitrine de valuation** nos dois domínios · **Data Room** (NDA, marca d'água, Q&A, ligação documento↔métrica) · **Ask LNZ AI** com filtro de permissão · exportações (XLSX/PDF/CSV) · **teste de invasão** e revisão de segurança.

**Critério de saída:** um investidor convidado cumpre a jornada de 30 minutos sem ajuda; teste de invasão **sem falha crítica**; **nenhum número público** sem fonte.

---

## 10.7 Fase 5 — Operar e provar (contínuo)

Fechamento **mensal oficial** (imutável) · **backtest** a cada evento real · revisão da metodologia (v1.1…) · **laudo de terceiro** quando houver transação · relatório trimestral do conselho.

---

## 10.8 Mudanças no app (produção) — **todas dependem da sua ordem**

O Value OS foi desenhado para **não precisar** mexer na produção para começar (lê views). Estas mudanças **melhoram a qualidade do dado** e **cada uma é decisão sua**; as da zona vermelha só mesclam com a **sua ordem** e na **janela 01h00–02h15**.

### A. Segurança (independentes do Value OS; recomendo fazer **de qualquer forma**)

| # | Mudança | Risco | Zona vermelha? |
|---|---|---|---|
| S1 | Ligar RLS nas 3 tabelas `gateway_*` (3 linhas; **arquivo de migração** no repositório) | baixo | não (mas toca tabela de pagamento) |
| S2 | **Trancar** `consultarAssinaturaSigilo` (entrar na lista de rotas trancadas) e **não devolver CPF/e-mail/IP** | baixo | não (dado pessoal) |
| S3 | Tirar valuation, **CNPJ, PGDAS e nome da contadora** do pacote público do site (`operacaoNumeros.js`) | baixo | não |
| S4 | Conferir na Vercel `SESSAO_MODO` e `CRON_SECRET` | nenhum (leitura) | — |
| S5 | **Esconder `cost_price`** da leitura pública (view de produtos sem custo — "lote 3" já pendente no app) | médio (precedente de 15/09) | sim |
| S6 | `commission_records` sem leitura pública | médio | sim |
| S7 | NDA validado **no servidor** (hoje só no navegador) | médio | não |

### B. Dados que o Value OS precisa (melhoram o app também)

| # | Mudança | Para quê | Zona vermelha? |
|---|---|---|---|
| D1 | **Custo congelado** por venda (e por leilão no martelo) | margem | **sim** |
| D2 | Colunas **canal** e **loja** em cada venda | unit economics | **sim** |
| D3 | **Frete real** e **taxa do gateway** por venda | margem de contribuição | **sim** |
| D4 | `lote_id` em `products` (chave real) | validar "compra a 20–25%" | não |
| D5 | **Evento de adesão** (`licensee_membership`) | LICENSEES_* | **sim** |
| D6 | **Histórico de login/atividade** (tabela de eventos) | ACTIVE_30D, retenção | não |
| D7 | Vincular **depósito → leilão/produto** | PCP | **sim** |
| D8 | Corrigir **semântica de `financial_income`** (separar comissão paga × retida) e **reverter em estorno** | receita correta | **sim** |
| D9 | Tabela de **gasto por canal** e **atribuição** por venda | CAC | não |
| D10 | Normalizar **status** (uma língua) | simplifica tudo | **sim** |

### C. O que posso fazer **sem tocar** na produção

Tudo da Fase 1 em diante (o Value OS lê, não escreve), **mais** normalizações nas views do Value OS (status, fuso, exclusões) — a ordem acima só é necessária para **melhorar a qualidade**, não para **começar**.

---

## 10.9 O que pode ser **reutilizado** do app (item 41)

| Item | Reuso |
|---|---|
| Padrão de **extrato só-acrescenta** (`reserva_ledger`, `financial_income`, `bonus_ledger`, `auction_auditoria`) | **copiar o padrão** (e acrescentar o bloqueio no banco) |
| `dinheiroReal`, `custoProduto`, `simplesNacional`, tags `dado/aproximação/sem_fonte` | **copiar a regra**; reimplementar com teste |
| **Conciliação com o Mercado Pago** (`painel_conciliacao`, `auditoriaGateway`) | **ler** como fonte do Radar |
| **Fechamento diário** (`fechamento_diario`) | **ler** até haver snapshot próprio |
| Guia de design, componentes de gráfico (recharts), padrão de pastas e de testes | **copiar** |
| Zona vermelha, skill "antes de mesclar", janela de deploy | **seguir** para qualquer mudança no app |
| Cofre de segredos (`app_segredos`), limite de uso (`rate_limit_hit`) | **copiar o padrão** (limite **falhando fechado**) |
| **Marco oficial de 01/08/2026** | **adotar** como início da série do app |

## 10.10 O que deve ser **refeito** (item 42)

| Item | Por quê |
|---|---|
| **Painel do Parceiro** com Valuation/Memorando e números no código | números fixos, públicos, com CNPJ e PGDAS; NDA no navegador → migrar para o Value OS |
| **Definições de "venda paga" e "faturamento"** | 4–6 versões → **uma**, no Registry |
| **Controle de acesso do investidor** | hoje cosmético → login, NDA no servidor, expiração |
| **Laudo tributário por IA** | substituir por laudo de contador com CRC |
| **Contadores mortos** (`indicated_clients_count`, `total_commissions_generated`) | apagar ou alimentar |
| **`InvokeLLM` aberto** | trancar; não servir de base para a IA do Value OS |
| **Telas mortas** (`pdv/DashboardTab`, `RentabilidadeOperacao`, `BalancoGeralTab`) | remover (dados fixos em `localStorage`) |
| **"Giro da força de venda"** simulado e **"espectadores" aleatórios (150–199)** | não podem alimentar nenhum número para investidor |

## 10.11 Arquivos, tabelas e componentes que **precisariam mudar** (item 40)

- **No Value OS (novos):** repositório e projeto Supabase novos; ~15 tabelas (registry, valores, evidência, snapshots, lotes de carga, plano, cenários, comparáveis, transações, metodologia, acessos, documentos, perguntas); biblioteca `valuation/`; `financeiro/`; `metricas/`; telas do portal.
- **No app (opcional, ver 10.8):** `supabase/migrations/` (RLS, views de leitura, colunas novas), `api/functions/` (rota do NDA; `createPdvOrder`, `storeFulfill`, `settleAuctionWithBalance`, `finalizeAuctionCore`, `mpWebhook` para gravar custo/canal/frete — **todos na zona vermelha**), `src/lib/operacaoNumeros.js` (tirar dados fiscais), `src/lib/rotasTrancadas.js`.
- **Nos dois sites:** conteúdo (retirar Livoo, números sem fonte), integração (consumir o Registry) e login.
