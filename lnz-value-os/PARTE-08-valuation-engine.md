# Parte 8 — Valuation Engine

> **Em português simples:** é o conjunto de **métodos de avaliação** que transforma os números do modelo financeiro numa **faixa de valor**, mostrando como chegou lá. A regra: **o resultado nasce dos dados**, os métodos e pesos são fixados **antes** de olhar o resultado, e **nada é escolhido porque dá valor maior**.

> **Importante, para você não esperar o que eu não posso entregar:** o Value OS produz um valuation **defensável e rastreável**, não um **laudo de avaliação** assinado. Para uma transação real (rodada, venda, entrada de sócio), um laudo de terceiro continua sendo o padrão — o Value OS prepara tudo para esse terceiro conseguir refazer a conta em horas.

---

## 8.1 Primeiro: o que está sendo avaliado

O motor avalia **um perímetro** por vez. Hoje há três candidatos, e **a escolha é sua** (Parte 12):

| Perímetro | O que inclui | Observação |
|---|---|---|
| **A. Compras Full Comércio Ltda** | a empresa que tem CNPJ, contas bancárias, contabilidade e o nome fantasia "Leilão NoZap" | é a que o dossiê descreve; **as cotas estão em nome de uma sócia** (contrato de 08/2025) |
| **B. Ecossistema Leilão NoZap** | A + app/tecnologia + marca + rede + ComparAI + parcerias | só faz sentido se **um CNPJ** (ou um contrato) reúne esses ativos |
| **C. Só a plataforma/tecnologia** | código, marca, domínios, rede de licenciados | exige saber **quem é o dono** |

O valor da empresa se divide em duas partes que **nunca se misturam**:

```
 VALOR DA OPERAÇÃO (EV)        ← o negócio funcionando (leilão, loja, rede, varejo)
 + ATIVOS NÃO OPERACIONAIS     ← cotas de consórcio (da empresa), caixa em excesso
 − DÍVIDAS "DISFARÇADAS"       ← carteira de clientes, aportes com repasse, contas vencidas, tributos
 = VALOR DO EQUITY (do sócio)
```

---

## 8.2 Os métodos

| # | Método | O que faz | Serve hoje? | Peso inicial (ver 8.3) |
|---|---|---|---|---|
| 1 | **Fluxo de caixa descontado (DCF / FCFF)** | desconta o caixa futuro a uma taxa de risco (WACC) | **Fraco.** ~2,5 meses de dinheiro real, resultado operacional provavelmente negativo, valor final (terminal) domina. Vira útil com ≥ 12 meses de série. | baixo |
| 2 | **Múltiplos de empresas listadas** (EV/Receita, EV/GMV, EV/EBITDA) | compara com empresas parecidas na bolsa | **Sim, com desconto de tamanho e liquidez.** Precisa de definição única de receita. | médio |
| 3 | **Transações precedentes** | compara com compras/vendas reais de empresas parecidas | **Sim, como referência.** Dado difícil de achar no Brasil. | médio |
| 4 | **Método VC** | valor de saída esperado ÷ retorno exigido pelo investidor | **Sim**, dá o "tamanho do prêmio" se o plano acontecer. Sensível ao cenário de saída. | médio |
| 5 | **Soma das partes** | avalia cada negócio separado e soma | **Sim:** varejo Nexus · leilão · loja virtual · licenciamento · tecnologia · consórcio | médio |
| 6 | **Economia por unidade** (LTV/CAC em regime estável) | vale quanto a base de clientes gera de margem | **Ainda não:** sem CAC e sem margem por venda | baixo → alto com dado |
| 7 | **Custo de reposição da tecnologia** | quanto custaria **reconstruir** o código | **Sim, como piso**, não como valor de mercado | piso |
| 8 | **Patrimônio ajustado (NAV)** | ativos a valor realizável − passivos | **Sim, como piso** (estoque, caixa, consórcio líquido) | piso |
| 9 | **Qualitativos** (Scorecard / Berkus / Checklist) | notas por critério sobre uma média de mercado | **Sim, como conferência** para fase inicial | conferência |

### Candidatos a comparáveis e a transações (**a validar — nada aqui é número final**)

> Cada comparável entra no motor com: empresa, país, setor, modelo, receita, crescimento, margem, valor da empresa, múltiplos, **fonte e data**, e uma frase explicando **por que é comparável**. A lista abaixo é só **ponto de partida de pesquisa**.

| Tipo | Candidato | Por quê é parecido | O que a pesquisa já mostra |
|---|---|---|---|
| Listada (EUA) | **Liquidity Services (LQDT)** | marketplaces de leilão de excedente e devolução; "Retail Supply Chain Group" trata excesso/devolução de consumo | descrição do negócio em [seus documentos na SEC](https://www.sec.gov/Archives/edgar/data/1235468/000119312525289159/R13.htm); **faltam receita e múltiplos** (puxar do 10-K) |
| Listada (Brasil) | **Enjoei (ENJU3)** | recommerce brasileiro de pequeno porte | **cotação abaixo de R$ 1,00** e prazo da B3 para reenquadrar, segundo [esta reportagem](https://acionista.com.br/enjoei-enju3-estabelece-novo-prazo-ate-agosto-de-2026/) — **o par nacional mais próximo está sob pressão**; é informação, não resultado final |
| Listada (EUA) | ThredUp · The RealReal · eBay · Copart · RB Global | recommerce / leilões | a coletar |
| Listada (Brasil) | Mercado Livre (MELI) · Magazine Luiza | grande porte — referência de teto, não de comparação direta | a coletar |
| Transação | **Naver × Poshmark** | recommerce de moda; anunciado em out/2022, ~US$ 1,2 bi (US$ 17,90 por ação), receita 2021 de US$ 326 mi e prejuízo de US$ 98,3 mi ([fonte](https://www.retailtouchpoints.com/news/naver-acquires-poshmark-for-1-2-billion/118675/)) | ≈ **3,7× a receita 2021** sobre o valor de *equity* (o valor da empresa exige descontar o caixa). **Grande porte, outro mercado, outro momento.** |
| Transações no Brasil | recommerce, liquidação de estoque, leilão online | **buscar** (rodadas e vendas de empresas de recommerce, logística reversa, marketplaces de nicho) | a coletar |

**Fontes de parâmetros (a registrar com data):** taxa livre de risco (títulos públicos / Selic), prêmio de risco de mercado e de país, múltiplos por setor (por exemplo, os dados abertos de Aswath Damodaran, atualizados todo ano), prêmio de tamanho e de liquidez para empresa fechada.

**Aviso de realidade:** a média de múltiplos de grandes empresas **não** se aplica direto a uma empresa com R$ 5–50 mil/mês de receita reconhecida. O motor aplica **desconto de tamanho, liquidez e concentração**, com a **fonte do desconto** registrada — e mostra o valor **antes** e **depois** do desconto.

---

## 8.3 Triangulação — os pesos (pré-registrados)

**Regra:** os pesos são **escolhidos pelo estágio da empresa e pela qualidade do dado**, **registrados na metodologia v1.0 antes da primeira rodada** e guardados com impressão digital. Um método sem dado suficiente tem peso **zero e aparece como "não calculado"** — nunca como "valor baixo".

**Proposta de pesos para o estágio atual** (empresa operando há poucos meses com dado de dinheiro real, sem lucro comprovado), **para sua aprovação:**

| Método | Peso | Justificativa |
|---|---:|---|
| Múltiplos de listadas (com desconto) | 25% | só referência externa observável, mas de porte muito diferente |
| Transações precedentes | 15% | referência real de preço pago, mas escassa e distante |
| Método VC | 20% | alinha com o que um investidor de risco faz; depende do plano |
| Soma das partes | 15% | respeita que o varejo Nexus, o leilão e a rede têm perfis diferentes |
| DCF (cenários ponderados) | 10% | baixo até haver série ≥ 12 meses |
| Economia por unidade | 5% | sobe para 15–20% quando houver CAC e margem por venda |
| **Piso:** custo de reposição + NAV | 10% | o valor **não pode** ficar abaixo do que se reconstrói/liquida, a menos que justificado |
| **Total** | **100%** | |
| *Conferência (peso 0):* Scorecard/Berkus | — | só para o painel mostrar se o resultado destoa de um padrão de mercado |

Os pesos **mudam com o estágio** (tabela de transição fica na metodologia) — mas **nunca** depois de ver o resultado. Mudança de peso = nova versão da metodologia (8.9).

---

## 8.4 Como sai a **faixa** (não um número só)

```
 para cada método:  premissas = distribuição (não um ponto)   ← baseada no histórico real
        │
        ▼  simulação (milhares de sorteios)
 distribuição de valor por método
        │
        ▼  mistura com os pesos de 8.3  (+ piso de 8.3)
 distribuição final do valor da empresa
        │
        ├─ BAIXO     = percentil 25
        ├─ CENTRAL   = mediana (percentil 50)
        ├─ ALTO      = percentil 75
        └─ extremos  = percentis 10 e 90 (mostrados à parte)
```

- **Qualidade de dado baixa → faixa mais larga** (as distribuições das premissas se alargam por regra).
- **Confiança (0–100)** mede a **robustez** da análise (dado, reconciliação, aderência dos comparáveis, estabilidade do resultado a variações) — **não** a probabilidade de "acertar".
- **Score de risco (0–100)** soma 13 fatores que você listou (concentração de receita/cliente/fornecedor, dependência do fundador, regulatório, jurídico, tecnologia, margem, liquidez, dívida, governança, qualidade do dado, concorrência).

**Fatores de risco já visíveis nos dados de hoje:** 65% da entrada bancária de terceiros em 19 pagamentos; 100% dos pagamentos do app passando por um único gateway (Mercado Pago); varejo físico em queda desde junho; dependência de aportes; passivo fiscal e de contas vencidas; quadro societário e propriedade de ativos sem esclarecimento; regulatório sobre "leilão com saldo/bônus" (precisa do jurídico).

---

## 8.5 Da empresa ao sócio — a ponte (o que entra e sai)

| Item | Sinal | Origem | Hoje |
|---|---|---|---|
| Valor da operação (EV) | + | triangulação | — |
| Caixa operacional **verificado** | + | extrato/Open Finance | 🔴 só jan–jun |
| Estoque a valor realizável (se não estiver dentro do EV) | + | estoque × desconto | ≈ R$ 64 mil a custo |
| **Cotas de consórcio da empresa**, líquidas (valor da carta/crédito − saldo devedor), com desconto de liquidez | + | contratos | 🔴 CEO vai informar |
| **Float de carteira** (clientes, comissões, bônus, crédito de vendedor) | − | Registry | ≈ R$ 45,1 mil |
| **Aportes com repasse prometido** (parceiros/investidores) | − | contratos + extratos | 🔴 **CEO vai informar** |
| Contas vencidas e a pagar (aluguel, salários, fornecedores) | − | `financial_expenses` + balancete | R$ 166,9 mil vencido · R$ 119,8 mil pendente (**qualidade baixa**) |
| Tributos e encargos a pagar | − | balanço/contador | R$ 83,2 mil + R$ 85,0 mil em 31/12/2025 (situação atual desconhecida) |
| Contingências fiscais/jurídicas (divergência PGDAS × livros × declaração) | − | contador + jurídico | 🔴 a estimar |
| Obrigação do 1% aos fundadores | − | regra + base | 🔴 |
| = **Valor do equity** | | | |
| × participação de cada sócio | | contrato social **atual** | 🔴 |

> **Consórcio — duas regras claras:** (1) o que está **no nome da empresa** entra na ponte como ativo não operacional **líquido do passivo**, com desconto; (2) o que está **no nome de sócio** **fica de fora** (é patrimônio pessoal), a menos que exista contrato de cessão.

---

## 8.6 Modo Cego (Blind Valuation)

Para reduzir o viés de ancoragem:

1. **Antes de rodar**, o "valor de referência do fundador" (R$ 25 mi) e qualquer expectativa são **lacrados**: o sistema guarda só o **hash** (impressão digital) deles, com data.
2. O motor roda com **três coisas congeladas e com hash**: o **snapshot de dados**, a **versão da metodologia** e os **parâmetros**. Nenhum deles contém a referência.
3. O resultado é gravado.
4. **Só depois** a referência é aberta e comparada: *"referência do fundador × AI Independent Valuation"*, com a diferença e **o que explicaria cada parte da diferença** (Value Bridge).

> **Limite honesto:** **esta primeira rodada não pode ser cega** — o número de R$ 25 mi já circulou e eu já o li. O modo cego vale **para as próximas rodadas** e para **qualquer terceiro** que rode o motor. Por isso **eu não apresento nenhum valuation nesta primeira entrega** (nem "a faixa provável"): faria justamente o que você quer evitar.

**Inventário do que já existe (não são valuations do motor):**

| Número | Onde | Método | Observação |
|---|---|---|---|
| R$ 25.000.000 | sites, `documentoOficial.js` | nenhum visível | **Referência do fundador** |
| R$ 373.788 – R$ 747.576 | painel do Parceiro (código) | 3× a 6× o lucro anual "apurado" (R$ 124.596 — base fiscal de **outra** receita, RBT12 de R$ 714 mil) | **ilustrativo, o próprio código diz "não é laudo"** |
| R$ 7,97 mi – R$ 15,9 mi | painel do Parceiro (código) | mesmos múltiplos sobre lucro **projetado** com R$ 1 mi/mês | **cenário, não valor atual** |

---

## 8.7 Sensibilidade, Cenários, Ponte de valor e "Marco → Valor"

| Módulo | Como funciona | Regra de honestidade |
|---|---|---|
| **Matrizes de sensibilidade** | WACC × crescimento final · crescimento de receita × margem EBITDA · múltiplo × receita | todas as premissas visíveis e editáveis, **só na simulação** |
| **Scenario Lab** | você altera receita, crescimento, usuários, licenciados, margem, CAC, LTV, WACC, múltiplo e vê DCF, comparáveis, EV e equity | faixa **"SIMULAÇÃO — NÃO É VALUATION OFICIAL"** sempre visível; salva com rótulo |
| **Value Bridge** (por que mudou) | recalcula mudando **um grupo de entradas por vez** (receita, retenção, margem, CAC, risco, contrato…) e **tira a média sobre todas as ordens** para a atribuição não depender da ordem | **não inventa causalidade**: só mostra o que a conta prova; o resto aparece como "efeito combinado" |
| **Marco → Valor** | para cada marco (R$ 1 mi/mês, 300 licenciados, margem, CAC, retenção, novo contrato) recalcula o valor **se o marco acontecer**, e mostra **o que precisa ser verdade** | sempre **cenário**, nunca promessa; ordena por **impacto × confiança** |

---

## 8.8 Backtest e versionamento

- **Cada rodada é guardada** (dados, parâmetros, métodos, resultado, faixa).
- Quando houver **rodada de investimento, venda de cotas, aquisição, proposta vinculante ou transação verificada**, compara-se **AI × transação real**: erro absoluto mediano, MAPE, % de eventos reais dentro da faixa.
- **Proibido declarar** "mais preciso que humanos" antes de haver **evidência estatística suficiente** (algumas dezenas de eventos).
- **Metodologia versionada (v1.0, v1.1…)**: toda mudança registra **data, autor, mudança, motivo e impacto esperado**; **não há mudança silenciosa**; as rodadas antigas continuam valendo com a **versão em que foram feitas**.

---

## 8.9 Ordem de grandeza do que dá para dizer **hoje** (sem número)

- **Qualidade de dado:** baixa (~35–45/100 no início). **Confiança:** baixa. **Faixa:** muito larga.
- O que **sustenta** valor: motor de leilão maduro e testado; conciliação de pagamentos; código próprio de porte; rede em formação; ecossistema de formação (narrativa).
- O que **tira** valor: sem margem por venda comprovada; receita sem fonte única; dependência de aportes; passivos fiscais e a pagar; varejo físico em queda; propriedade de ativos e quadro societário não esclarecidos; documentos com divergências internas.
- O caminho para **subir** o valor defensável é **o mesmo caminho do Data Quality**: corrigir as lacunas da Parte 5.5 e reconciliar as quatro ilhas (Parte 2).
