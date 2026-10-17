# Anexo A — Auditoria dos dois sites (item 42)

**Base da análise:** as duas capturas em PDF que você enviou — `LEILAO-NOZAP.pdf` (Memorando de Investimento, 60 páginas) e `LEILAO-NOZAP_1.pdf` (página única com o valuation).
**Limite:** **não consegui abrir os sites ao vivo** (o ambiente não resolve os dois endereços). Não avaliei botões, links, scripts, SEO nem o que muda com o tempo. Pareei cada PDF ao site **pelo conteúdo**, não pelo endereço.
**Estado dos números:** todos os números dos sites são `MANAGEMENT DATA` (dado da administração, sem rastro) até aparecerem no Metrics Registry com origem no banco.

## Como ler as etiquetas

| Etiqueta | Significa |
|---|---|
| **KEEP** | Narrativa da administração. Fica como está. |
| **DYNAMIC** | Número que deve passar a vir do sistema (com data da última atualização). |
| **VERIFY** | Afirmação que precisa de prova antes de continuar publicada. |
| **RECALCULATE** | Número existe, mas a conta está errada, vem de janela diferente ou conflita com o banco. |
| **REMOVE** | Sai do ar (ou é reescrito) por risco ou por não ter base. |
| **DUPLICATE** | Mesma informação em dois lugares — deve haver uma só fonte. |
| **INCONSISTENT** | Dois lugares dizem coisas diferentes. |

Legenda de origem: **M** = Memorando · **V** = página do Valuation.

---

## 1. Valuation e números-chave

| # | Informação | Onde | Etiqueta | O que encontrei / o que fazer | Metric ID proposto |
|---|---|---|---|---|---|
| 1 | "Valuation R$ 25.000.000" | M, V (várias vezes) | **RECALCULATE** | Tratar como `FOUNDER_REFERENCE_VALUATION`. Nenhum método é mostrado: nem múltiplo, nem fluxo de caixa. Vira *comparação* contra o valuation independente, não manchete. | `VAL_FOUNDER_REFERENCE` |
| 2 | "Valuation conservador" | M, V | **REMOVE** | Palavra sem base. A mesma página diz "valor presente dos ativos — não projeções". Conservador **comparado a quê**? | — |
| 3 | "Valuation baseado em ativos reais e operação validada" | V | **REMOVE / reescrever** | Os "ativos" listados são quase todos intangíveis (código, rede, marca, metodologia, capital intelectual do fundador). Estoque e caixa **não aparecem**. Reescrever como "o que sustenta o valor" com peso e evidência de cada item. | — |
| 4 | Soma de 7 "ativos" que compõem o valuation (Tecnologia, Operação, Capital Intelectual, Rede, Metodologia, Ecossistema, Potencial) | M cap. 9 | **VERIFY** | Nenhum recebe valor em R$. "Capital intelectual do fundador" (R$ 100 mi de crédito originado, R$ 22 mi captados, 30 mil pessoas) **é currículo, não ativo da empresa** — comprador desconta. Mover para "Equipe/Governança". | — |
| 5 | "Potencial não precificado" (expansão nacional, live, PHIZ, ComparAI, internacionalização) | M | **VERIFY** | Contradiz "não é projeção" (item 3). Se está fora do valuation, dizer quanto vale cada opção ou tirar. | — |

## 2. Receita e crescimento

| # | Informação | Onde | Etiqueta | O que encontrei / o que fazer | Metric ID proposto |
|---|---|---|---|---|---|
| 6 | Receita mensal nov/25 16,3k · dez 26,4k · jan 27k · fev 17,2k · mar 23k · abr 60,4k · mai/26 181k | M gráfico, V gráfico (fev–mai) | **VERIFY** | **Não reproduzível no banco** (ver Anexo B1/B8): `catalog_sales` só começa em 01/06/2026; o histórico de produtos vendidos dá R$ 24,6 mil em maio, não 181 mil. Falta a fonte (planilha Nexus? extrato?). Sem definição de "receita": bruta? depósito? comissão? | `REVENUE_GROSS_M`, `REVENUE_NET_M` |
| 7 | "Pico mensal R$ 181K em maio/2026" | M, V | **VERIFY + RECALCULATE** | Mesma pendência do item 6. Também está **defasado**: hoje é 17/10 e não há jun–set no material. | `REVENUE_GROSS_M` (máx) |
| 8 | "+1.000% de crescimento" | M | **INCONSISTENT** com 9 | Base nov/25 (16,3k → 181k = +1.011%). | `GROWTH_REVENUE_WINDOW` |
| 9 | "960%" e "10x em 4 meses" e "R$ 17K a R$ 181K em 4 meses" | V | **INCONSISTENT** com 8 | Base fev/26 (17,2k → 181k = +952%). **Mesma série, duas janelas, duas manchetes.** O registry deve exigir a janela no nome da métrica (ex.: `GROWTH_3M`, `GROWTH_6M`). | `GROWTH_REVENUE_*` |
| 10 | "7 meses de validação comercial" | M | **VERIFY** | Nov/25–mai/26. Só vale se o item 6 for comprovado. | — |
| 11 | "Receita recorrente" | M (lista "o que existe hoje"), V ("licenciamento = receita recorrente") | **VERIFY** | O banco mostra 1 adesão paga (R$ 1.497) e nenhuma cobrança periódica. **Recorrente exige repetição contratada** — não vi. | `REVENUE_RECURRING` |
| 12 | "Meta R$ 1 milhão+/mês em dez/2026" | M, V | **KEEP como `MANAGEMENT PLAN`** | Meta não é fato. Versionar (Parte 7). Contexto: maior mês comprovado no banco = R$ 54 mil (jun, importação) / R$ 49 mil entrada bruta (set, 63% depósito). | `PLAN_REVENUE_DEC26` |
| 13 | Projeção R$ 12M (2026) · R$ 36M (2027) · R$ 96M (2028) | M | **RECALCULATE** | Jan–mai/26 somam R$ 308,6 mil pelo próprio gráfico; faltariam R$ 11,7 mi em jun–dez (média R$ 1,67 mi/mês), mas a meta de dezembro é R$ 1 mi/mês. **O 2026 projetado não fecha com a meta do próprio material.** Título diz "2026–2030"; só vi 3 anos. Trocar por previsão por drivers. | `FCST_REVENUE_Y*` |
| 14 | "Operação construída via processos manuais — aderência antes da automação" | M | **KEEP** | Narrativa. | — |

## 3. Tecnologia

| # | Informação | Onde | Etiqueta | O que encontrei / o que fazer | Metric ID proposto |
|---|---|---|---|---|---|
| 15 | "178 mil linhas de código, 883 arquivos" | M, V (4 vezes) | **RECALCULATE → DYNAMIC** | Medi no repositório do app: **≈ 331 mil linhas em 2.033 arquivos de código** (sem testes); com testes **≈ 421 mil linhas**. Só `src/` tem 231 mil. **Cuidado:** inclui ~37 mil linhas do legado Base44 e ~18 mil de SQL; linha não é valor. Ficar com um número definido e com a data (`TECH_LOC_V1`). | `TECH_LOC`, `TECH_FILES` |
| 16 | "Tecnologia 100% proprietária, desenvolvida internamente" | M, V | **VERIFY** | O app usa Supabase, Vercel, Mercado Pago, Melhor Envio, Z-API, provedores de IA e bibliotecas abertas. "100% própria" é imprecisa; "código-fonte próprio sobre infraestrutura de mercado" é verdadeira e mais forte diante de due diligence. Propriedade do código (contratos, quem escreveu) vai para o Data Room. | — |
| 17 | "ComparAI — IA proprietária de precificação, já em operação" | M, V | **VERIFY** | Banco: `comparai_cache` 117 linhas, `comparai_logs` 0, valores de mercado salvos em 02/09 e hoje só **1** produto em estoque tem `market_value`. *(frente de código confirma o que é — ver Parte 1)* | — |
| 18 | "Sistema Inteligente de Análise de Lotes" (planilha→classificação→preço→anúncio→publicação) | M | **VERIFY** | Banco: `lotes_recebidos` 40 lotes (abr–out/26) com `itens_json`/`produtos_gerados`: há uso real. "Centenas de produtos em minutos": medir tempo real. *(frente de código)* | — |
| 19 | "Leilão Inteligente 99% concluído" / "Live Commerce 99%" / "PHIZ Leilão 99%" / "Aplicativo 99% concluído (jun/26)" | M | **VERIFY** | "99%" é sensação, não métrica. Substituir por checklist com entrega verificável. *(frente de código)* | — |
| 20 | "Live Commerce — Livoo Live: integração 99%, collab ativa, **sociedade em fase final**" (também listada como um dos 5 negócios do grupo e como motor "Live Commerce 99%") | M, V | **REMOVE — urgente** | **FATO (registro do dono em 17/10/2026, `docs/DIRETIVA_ATUAL.md` DIR-258 e `docs/GUIA_DE_DESIGN.md:63`):** a Livoo "não é mais parceira" e foi retirada das telas do app **hoje**. Os dois sites continuam anunciando a sociedade. Banco: `livoo_lives` 0 e `livoo_webhook_deliveries` 0. O nome também aparece como "LivroLive" e "Livoo Live" no mesmo documento. Decidir o que o motor "Live Commerce" é agora ("o dono terá a própria live depois") e reescrever. | — |
| 20b | "TikTok Shop ativo e funcional" | M | **VERIFY** | Na leitura do código só achei um link de perfil numa tela (`LojaShopeeHeader.jsx:13`); **não há integração de TikTok Shop**. | — |

## 4. Rede e clientes

| # | Informação | Onde | Etiqueta | O que encontrei / o que fazer | Metric ID proposto |
|---|---|---|---|---|---|
| 21 | "80+ Licenciados **ativos**" | M, V (cabeçalho) | **INCONSISTENT** com 22 | Banco: `role='licensee'` = **23**; nível de carreira licenciado* = **15**; `licenciado_context` preenchido = **84**; licensees com acesso em 30 dias = **8**. | `LICENSEES_TOTAL`, `LICENSEES_ACTIVE_30D`, `LICENSEES_PAYING` |
| 22 | "80+ licenciados **totais**, 50% de ativação, ~40 ativos hoje" | V (seção Rede Comercial) | **INCONSISTENT** com 21 | A frase "50% de ativação" nunca aparece no memorando. **Exatamente o caso que você descreveu.** | idem |
| 23 | "2.000+ clientes — compradores ativos" | V | **RECALCULATE** | Banco: 1.132 contas "user"; 1.211 cadastros em `customers`; **65 contas distintas pagaram** (compra ou depósito) de jun a out/26; 160 contas entraram nos últimos 30 dias. "Cliente" sem definição. | `CUSTOMERS_REGISTERED`, `CUSTOMERS_PAYING_90D`, `USERS_ACTIVE_30D` |
| 24 | "Taxa de ativação 50%" | V | **VERIFY** | Sem fórmula. Ativação = fez o quê, em quantos dias? | `LICENSEES_ACTIVATED` |
| 25 | Metas: 300 licenciados (2026), 1.000 e 10 mil vendedores (2027), 8 lojas, CD no Recreio | M, V | **KEEP como `MANAGEMENT PLAN`** | Versionar e medir contra o realizado (Plan × Actual). | `PLAN_LICENSEES_*` |
| 26 | "Lojas físicas: Senador Camará e Bangu" | M | **VERIFY** | Banco: tabela `stores` 0 linhas; 1 conta com nível `loja_fisica`. Precisa de lista com endereço, contrato e venda por loja. | `STORES_ACTIVE` |
| 27 | "~8 pessoas na equipe" / diretoria de 8 fundadores | M, V | **KEEP** | Governança. Conferir com a folha. | — |

## 5. Modelo econômico

| # | Informação | Onde | Etiqueta | O que encontrei / o que fazer | Metric ID proposto |
|---|---|---|---|---|---|
| 28 | "Compra lotes a 20–25% do valor de mercado" | M, V | **RECALCULATE** | Banco (34 lotes): custo = **3,7% do "valor de mercado" cadastrado** (mediana 0,7%). O número do site não vem desses lotes. Antes de usar qualquer um dos dois, provar o preço de venda realizado. | `LOT_COST_TO_MARKET` |
| 29 | "Vende 20% abaixo do mercado" | M, V | **VERIFY** | Só 1 de 1.469 produtos em estoque tem valor de mercado. **Não verificável hoje.** | `SELL_VS_MARKET` |
| 30 | "Margem bruta estrutural elevada / ROI elevado por ciclo" | M, V | **RECALCULATE** | Margem aproximada medida: loja +6% a +15%; arremate **−63%** (42 pedidos com custo — a validar). | `GROSS_MARGIN_BY_CHANNEL` |
| 31 | "30% de comissão para licenciados + impostos" | V | **VERIFY** | No banco, comissão por papel é: licenciado ~3–6%, vendedor 10%, loja física ~11%, distribuidor até 20%, indicação de depósito 10%, leilão retido ~24,5%, indicador de leilão 5%. **A regra de 30% não aparece como número único.** *(frente de rede confirma)* | `COMMISSION_PAID_PCT` |
| 32 | "1% do faturamento bruto global é destinado ao ecossistema de fundadores" | M | **VERIFY — crítico** | É custo que reduz EBITDA e muda quem fica com o quê. Banco: registros de fundador/conselheiro/diretoria em fração de ponto percentual cada. Entra no modelo como **linha própria**, com base de cálculo definida e partes relacionadas identificadas. | `FOUNDERS_POOL_PCT` |
| 33 | 10 "motores de receita" (5 ativos, 2 crescendo, 3 "99%") | M | **VERIFY** | O banco só mostra receita real em: venda de produto, loja, arremate (comissão), passaporte, adesão. Sem linha de receita para análise de lotes, serviços a fornecedores, live ou PHIZ. **Cada motor deve ter métrica de receita própria; sem número = "planejado".** | `REVENUE_BY_ENGINE` |

## 6. Mercado

| # | Informação | Onde | Etiqueta | O que encontrei / o que fazer | Metric ID proposto |
|---|---|---|---|---|---|
| 34 | E-commerce Brasil R$ 185B+ · Logística reversa R$ 40B+ · Estoques excedentes R$ 25B+ · recommerce +35% a.a. · devolução 30% · 147M usuários de WhatsApp | M, V | **VERIFY** | Nenhuma fonte nem data. Todo número de mercado precisa de fonte, ano e metodologia. | `MKT_*` (tabela de fontes) |
| 35 | "R$ 40B+" rotulado de **dois jeitos**: "Logística reversa — devoluções anuais" (topo) e "Capital represado em estoques e devoluções por ano" (seção O Problema) | V | **INCONSISTENT** | Mesmo número, dois significados. | — |
| 36 | "9 mercados convergindo" | V | **KEEP** | Narrativa. | — |
| 37 | "A única plataforma brasileira que os conecta" / "o líder nacional ainda não existe" | V | **REMOVE** | Superlativo sem prova. Atrai pergunta de concorrência que o material não responde. | — |

## 7. Risco regulatório e de linguagem (alerta — não é parecer jurídico)

| # | Informação | Onde | Etiqueta | O que encontrei / o que fazer |
|---|---|---|---|---|
| 38 | "Se vencer compra abaixo do mercado; se não vencer continua com seu dinheiro" / "Sem perda financeira, sem risco típico de apostas" | M, V | **VERIFY (jurídico)** | O app trava saldo por lance e devolve ao perdedor — isso sustenta a frase. Mas há também bônus, roleta (LEILÃO20), passaporte e cupons. **Revisar com o jurídico** antes de manter a frase como promessa pública. |
| 39 | Seção "Transformando vidas": compara com plataformas de aposta ("Se é para apostar, aposte em oportunidades reais") | V | **VERIFY (jurídico)** | Comparar o produto a "aposta" convida a ser analisado como tal. Peça ao jurídico a leitura contra o Código de Defesa do Consumidor e a regulação de apostas. |

## 8. Acesso e coerência de publicação

| # | Informação | Onde | Etiqueta | O que encontrei / o que fazer |
|---|---|---|---|---|
| 40 | Rodapé do memorando: "Documento confidencial — uso restrito para investidores" | M | **INCONSISTENT** | Se o site é aberto sem login, o rótulo "confidencial" contradiz o acesso. A Parte 9 (Investor Experience) propõe acesso em 3 níveis. |
| 41 | Botão "Acessar Data Room" | M | **VERIFY** | Não consegui ver para onde leva. Se não existe data room, o botão promete algo que não há. |
| 42 | Botões "Baixar Memorando Completo", "Acessar a Plataforma", "Agendar Reunião Estratégica" | V | **KEEP** (a validar o destino) | — |

## 9. Narrativa e história

| # | Informação | Onde | Etiqueta | Observação |
|---|---|---|---|---|
| 43 | Carta do fundador, trajetória (Fuzileiros, Sky/Nextel, mercado financeiro, X-EOS) | M | **KEEP** | Narrativa da administração. Números dela (R$ 100 mi, R$ 40 mi, R$ 22 mi, R$ 4 mi, 30 mil pessoas) são `MANAGEMENT DATA` e vão para o Data Room com documento. |
| 44 | Linha do tempo (jul/2024 → dez/2026) | M | **KEEP / VERIFY** | "600 produtos vendidos da residência, 60%+ vendidos" (ago/24): histórico anterior ao sistema, sem rastro. Banco: atividade de leilão começa em set/2025. |
| 45 | "Vale do Recreio", Top College, X-EOS, Mentalidade do Executivo/Diretor/CEO | M, V | **KEEP** | Narrativa/ecossistema. Sem número verificável; não entram no valuation. |
| 46 | Nível de carreira 1–8 (Vendedor → Conselho) | M | **KEEP** | Bate com `primary_career_level` do banco (vendedor, licenciado, executivo, diretoria, ceo…). |

---

## Resumo da auditoria

| Etiqueta | Itens |
|---|---:|
| KEEP | 13 |
| DYNAMIC (via RECALCULATE→DYNAMIC) | 1 |
| VERIFY | 22 |
| RECALCULATE | 7 |
| REMOVE | 3 |
| INCONSISTENT | 6 |
| DUPLICATE | 0 (há 2 casos de *mesmo número, duas janelas* — itens 8/9 e 21/22 — tratados como INCONSISTENT) |

> Alguns itens recebem mais de uma etiqueta; a contagem acima considera a principal de cada linha.

**Os 5 que mais mudam a conversa com um investidor:**
1. Item 6/7 — a série de receita precisa de fonte rastreável (hoje não está no banco).
2. Item 21/22 — "80 ativos" × "80 totais, 40 ativos" × 23 no banco.
3. Item 28 — custo do lote 3,7% do "mercado" (não 20–25%) → provar com preço realizado.
4. Item 13 — o R$ 12 mi de 2026 não fecha com a meta de dezembro.
5. Item 32 — o 1% do faturamento bruto aos fundadores precisa entrar no modelo como custo.

---

## 10. Itens que o dossiê contábil e os extratos acrescentam (47–56)

> Estes itens **não estão nos dois sites com este nome**: nascem do **cruzamento** do que os sites dizem com os documentos do Drive e os extratos (Anexo C). Valores são `MANAGEMENT DATA — documento recebido`, **não autenticados** por mim.

| # | Informação do site | Onde | Etiqueta | O que o dossiê/os extratos mostram | Ver |
|---|---|---|---|---|---|
| 47 | Receita de **nov/25 R$ 16,3 mil** e **dez/25 R$ 26,4 mil** | M gráfico | **INCONSISTENT** | A **declaração de faturamento ao banco** e os **livros (ECF)** trazem, para os mesmos meses, **R$ 105,1 mil** e **R$ 106,0 mil** (≈ 6,4× e 4×) — a declaração e os livros coincidem entre si; o memorando é o que destoa. | C5 |
| 48 | "**7 meses de validação comercial**" (começa em nov/25) | M | **INCONSISTENT** | Os livros de 2025 registram receita **desde janeiro/2025** (R$ 90 mil no primeiro mês; **R$ 1,19 mi no ano**). Ou a operação é anterior ao que o memorando diz, ou a série dos livros precisa ser explicada. | C3 |
| 49 | Gráfico jan–mai/26 (soma **R$ 308,6 mil**) | M, V | **RECALCULATE** | Entradas de terceiros nas duas contas (Santander + Mercado Pago) em jan–mai: ≈ **R$ 622 mil** — mas **inclui aportes e empréstimos** e não inclui venda em dinheiro/outras contas. **Entrada de banco não é receita**; só vira número depois de classificada. | C4, C5 |
| 50 | "Diretoria de 8 fundadores" / equipe | M, V | **VERIFY** | No contrato social de 12/08/2025 as 500.000 cotas estão em nome de **uma única sócia**. Falta o quadro societário **atual**. | C2 |
| 51 | Porte e regime (não citado) | — | **VERIFY** | Cartão CNPJ: **ME**; receita escriturada 2025: R$ 1,19 mi. Regime 2025 **Lucro Presumido**; 2026 **Simples Nacional** (sem o documento de opção à vista). O laudo tributário de 22/07 foi emitido por agente de IA. | C2, C5 |
| 52 | Caixa e estoque (não aparecem nos sites) | V ("ativos reais") | **VERIFY** | Balanço 31/12/2025: caixa **R$ 705.958,47**; estoque R$ 79.108,28. Saldo bancário conhecido em 01/01/2026: **R$ 42,29**. Reconciliar antes de dizer que o valuation tem lastro em ativos. | C3, C4 |
| 53 | Consórcios (não aparecem nos sites) | — | **VERIFY** | 21 cartas no nome da empresa (2 contempladas, 19 a contemplar), 2 contempladas no nome de um sócio, 1 alienada; parcelas ≈ R$ 12–18 mil/mês. Entram como **ativo/passivo não operacional** na ponte (Parte 8). | C6 |
| 54 | Painel do Parceiro com Valuation/Memorando | app | **REMOVE do pacote público** | Valuation, **CNPJ, número do PGDAS e nome da contadora** estão no código entregue ao navegador (`operacaoNumeros.js`). | Parte 1 (segurança 5) |
| 55 | "Pico mensal" e crescimento | M, V | **VERIFY** | Setembro/2026 tem **≈ R$ 400 mil de entradas de terceiros** nas duas contas contra **R$ 49,2 mil de pagamentos do app**; nenhum "novo pico" pode ser publicado com base em entrada de banco sem classificar (origem dos recursos). | C9 |
| 56 | Série "até mai/26" sem jun–set | M | **RECALCULATE** | A planilha Nexus mostra **jun R$ 72,0 mil → jul R$ 11,8 mil → ago R$ 3,4 mil → nada de setembro em diante**; o dinheiro "real" do app: ago R$ 11,7 mil · set R$ 49,2 mil · out (até 15/10) R$ 40,5 mil. Memorando termina em maio e não mostra a queda do varejo. | Parte 1 (3, 4, 5) |

### Resumo acrescentado

| Etiqueta | Itens 47–56 |
|---|---:|
| INCONSISTENT | 2 (47, 48) |
| RECALCULATE | 2 (49, 56) |
| VERIFY | 5 (50, 51, 52, 53, 55) |
| REMOVE | 1 (54) |

> Total da auditoria com esta seção: **56 itens numerados** (46 dos sites + 10 do dossiê), mais o 20b.
