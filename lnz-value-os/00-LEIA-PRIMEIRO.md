# LNZ VALUE OS — Live Valuation & Investor Intelligence
## Primeira entrega: análise e proposta (17/10/2026)

> **Status: PROPOSTA PARA A SUA APROVAÇÃO. Nada foi construído.**
> Nenhum código do Value OS foi escrito. **Nenhuma linha do app, do banco, dos dois sites ou da produção foi alterada** — o que fiz no banco e no código do app foi **só leitura**.
> Também **não apresento nenhum número de valuation** nesta entrega: a referência de R$ 25 mi já foi vista (então a primeira rodada não pode ser cega) e o dado ainda não fecha (ver abaixo).

---

## Em 10 linhas (o que a análise mostra)

1. **Os dados estão em 4 "ilhas" que não conversam:** o app, a planilha Nexus (vendas lançadas à mão), a contabilidade e os bancos. Por isso o mesmo negócio tem **4–5 "receitas" diferentes** (Parte 1 e Anexo C5).
2. **O app só tem "dinheiro real" desde 01/08/2026** (marco oficial do próprio app). Antes disso, o app chama tudo de teste. A série do memorando (nov/25–mai/26) **não está no banco do app**.
3. **Há 3 "valuations" circulando** (R$ 25 mi nos sites · R$ 0,37–0,75 mi no código do painel do Parceiro · R$ 8–16 mi no cenário de R$ 1 mi/mês). Precisa de uma narrativa única.
4. **Não está definido o que está sendo avaliado:** a empresa com contas formais (Compras Full Comércio Ltda) tem, no contrato que li, 100% das cotas com uma só sócia; falta saber de qual CNPJ são o app, a marca e os domínios.
5. **63–65% do que entrou no app em set/out foi depósito de carteira** — não é receita; é dívida com o cliente.
6. **Não existe margem por venda, leilão ou produto** (custo não é gravado). Sem isso o fluxo de caixa descontado não é defensável hoje.
7. **Recomendo uma área separada, com login próprio** (não dentro do app) e o app só com um botão; os dois sites viram "portas" do mesmo sistema (Partes 3 e 9).
8. **5 pontos de segurança** foram encontrados no app (nenhum foi alterado) — Parte 1, Parte 10 (S1–S7).
9. **Os extratos mostram um padrão de entradas que precisa de documentação** (valores redondos, 43 depósitos em dinheiro no mesmo dia). Pode ter explicação legítima; **recomendo advogado e contador antes de montar o Data Room** (Parte 11, R-L1; Anexo C9).
10. **Mercado Pago:** recebi os extratos de jul, set e out (fecham ao centavo; Anexo C13). **Só falta agosto.** Em set e out toda entrada de terceiros dele é venda do app (≈ R$ 33 mil e R$ 27 mil/mês); os R$ 400 mil de setembro entraram por Santander e Itaú e **ainda não têm origem documentada**.

---

## Como navegar (as 12 partes que você pediu)

| Parte | Arquivo | Em uma linha |
|---|---|---|
| 1 · Diagnóstico | `PARTE-01-diagnostico.md` | 23 achados, segurança, os 2 sites e o app por área |
| 2 · Arquitetura atual | `PARTE-02-arquitetura-atual.md` | as 4 ilhas, camadas do app, mapa do dinheiro, 6 "faturamentos" |
| 3 · Arquitetura futura **e** 4 · Diagrama completo | `PARTE-03-04-arquitetura-futura-e-diagrama.md` | "dentro do app ou separado?", camadas 0–8, diagrama ASCII |
| 5 · Database map | `PARTE-05-database-map.md` | tabela a tabela: confiável × não, dados que faltam, camada de leitura |
| 6 · Metrics Registry | `PARTE-06-metrics-registry.md` | regras globais e famílias de métricas |
| 7 · Financial model | `PARTE-07-financial-model.md` | DRE, caixa (FCFF), balanço, forecast por drivers, Plan × Actual |
| 8 · Valuation engine | `PARTE-08-valuation-engine.md` | métodos, pesos pré-registrados, faixa, ponte, modo cego |
| 9 · Investor experience | `PARTE-09-investor-experience.md` | papéis, telas, Evidence Ledger, Data Room, Ask LNZ AI |
| 10 · Roadmap | `PARTE-10-roadmap.md` | fases 0–5, mudanças no app (S1–S7, D1–D10), reuso/refazer |
| 11 · Riscos | `PARTE-11-riscos.md` | dados, financeiro, legal/conformidade, segurança, credibilidade, técnico |
| 12 · Decisões | `PARTE-12-decisoes.md` | **25 decisões suas (DEC-1…25)** e os **10 dados que faltam** |

**Anexos:** `anexos/A-auditoria-dos-dois-sites.md` (59 itens) · `anexos/B-evidencias-do-banco.md` (números do banco e as consultas) · `anexos/C-dossie-contabil-e-bancario.md` (dossiê do Drive e extratos).

---

## Onde está cada um dos 46 itens da sua lista

| # | Item | Onde |
|---|---|---|
| 1 | Diagnóstico dos dois sites | Parte 1 (1.2) · Anexo A |
| 2 | Diagnóstico do app | Parte 1 (1.3) |
| 3 | Mapa das fontes de dados | Parte 2 (2.1) |
| 4 | Mapa das tabelas relevantes | Parte 5 · Anexo B |
| 5 | Inventário de KPIs | Parte 6 (6.3–6.8) · Parte 2 (6 "faturamentos") |
| 6 | Divergências existentes | Parte 1 (1.4) · Parte 2 · Anexo C5 |
| 7 | Dados faltantes | Parte 5 (5.5) · Parte 1 (1.5) · Parte 12 (12.3) |
| 8 | Metrics Registry proposto | Parte 6 |
| 9 | Arquitetura do Data Engine | Parte 3 (3.3, camadas 1–3) |
| 10 | Arquitetura do Financial Model | Parte 7 (7.1) |
| 11 | DRE conceitual | Parte 7 (7.2) |
| 12 | Cash flow conceitual | Parte 7 (7.4) |
| 13 | Balance sheet relevante | Parte 7 (7.5) |
| 14 | Forecast model | Parte 7 (7.6, 7.8) |
| 15 | Valuation Engine | Parte 8 |
| 16 | DCF Engine | Parte 8 (8.2, método 1) |
| 17 | Comparables Engine | Parte 8 (8.2, candidatos a validar) |
| 18 | Precedent Transaction Engine | Parte 8 (8.2) |
| 19 | Triangulation Engine | Parte 8 (8.3, 8.4) |
| 20 | Sensitivity Engine | Parte 8 (8.7) |
| 21 | Scenario Lab | Parte 8 (8.7) · Parte 7 (7.8) |
| 22 | Value Bridge | Parte 8 (8.5, 8.7) |
| 23 | Milestone-to-Value | Parte 8 (8.7) · Parte 7 (7.7) |
| 24 | Data Quality Score | Parte 6 (6.9) · Parte 3 (camada 5) — *fórmula fixada na metodologia v1.0* |
| 25 | Valuation Confidence Score | Parte 8 (8.4) |
| 26 | Risk Score | Parte 8 (8.4) |
| 27 | Evidence Ledger | Parte 9 (9.4) · Parte 3 (3.3) |
| 28 | Discrepancy Radar | Parte 3 (3.3) · Parte 10 (Fase 2) · Anexo C5 |
| 29 | Snapshot system | Parte 3 (camada 7) · Parte 7 (7.1) |
| 30 | Valuation history | Parte 8 (8.8) · Parte 9 (9.8, "viagem no tempo") |
| 31 | Investor Dashboard | Parte 9 (9.2, 9.3) |
| 32 | Investment Memorandum dinâmico | Parte 9 (9.5) |
| 33 | Data Room | Parte 9 (9.6) |
| 34 | Ask LNZ AI | Parte 9 (9.7) |
| 35 | Export XLSX / PDF | Parte 9 (9.10) |
| 36 | Security | Parte 3 (3.5) · Parte 11 (11.5) · Parte 10 (S1–S7) |
| 37 | Backtest | Parte 8 (8.8) |
| 38 | Versioning | Parte 8 (8.8) · Parte 6 (6.1) |
| 39 | Roadmap de implementação | Parte 10 |
| 40 | Tabelas/arquivos/componentes a alterar | Parte 10 (10.8, 10.11) |
| 41 | O que pode ser reutilizado | Parte 10 (10.9) · Parte 2 (2.3) |
| 42 | O que deve ser refeito | Parte 10 (10.10) · Parte 2 (2.4) |
| 43 | Riscos técnicos | Parte 11 (11.7) |
| 44 | Riscos financeiros | Parte 11 (11.3) |
| 45 | Riscos de integridade de dados | Parte 11 (11.2) |
| 46 | Perguntas que exigem decisão do CEO | Parte 12 |

---

## O que está **fora** desta entrega (limites)

- **Não vi os dois sites ao vivo** (o ambiente não os abre); trabalhei com as capturas em PDF.
- **Não vi o Mercado Pago de jul–out/2026**, nem os extratos de 2025, nem outras contas.
- **Não autentiquei** os documentos do Drive (não consultei banco, Receita nem Junta): tudo é `MANAGEMENT DATA — documento recebido`.
- **Não vi** o contrato social atual, o PGDAS em si, os aportes, os contratos de consórcio, nem o app Nexus antigo (o zip tinha só o esqueleto).
- Os **comparáveis** da Parte 8 são **candidatos a validar** — não são números finais.
- Durações do roadmap são **estimativas**, não prazo.

## Avisos

- **Confidencialidade:** os arquivos desta pasta têm **só valores agregados** — sem CPF, número de conta, endereço ou nome de pessoa. Não abri as pastas de documentos pessoais (08, 12, 14) do Drive. Recomendo tirá-las do compartilhamento (DEC-20).
- **Segurança:** os 5 pontos da Parte 1 **não foram corrigidos**; cada um depende da sua ordem e do processo do app.
- **Conformidade:** nada aqui é parecer jurídico ou contábil. Onde indico "advogado/contador", é porque a decisão é deles.

## Próximo passo

Responda a Parte 12 (pode ser só "ok" / "ajustar" em cada linha) e mande os arquivos de 12.3 na ordem que conseguir — **começando pelo CSV do Mercado Pago (jul–out) e pela lista de aportes**. Com a sua aprovação do desenho, começa a Fase 0 (sem tocar em produção).
