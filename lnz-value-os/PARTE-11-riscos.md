# Parte 11 — Riscos

> **Como ler:** cada risco tem **probabilidade** (P) e **impacto** (I) em 3 níveis — **A**lto, **M**édio, **B**aixo — a **origem** do risco (FATO observado ou INFERÊNCIA) e o que **reduz** o risco.
> Esta parte **não é parecer jurídico nem contábil.** Onde digo "falar com advogado/contador", é porque o assunto é deles.

---

## 11.1 Mapa de calor (resumo)

```
   IMPACTO ▲
      ALTO │  R-D1 R-D2   R-F1 R-F2   R-L1 R-L2   R-S1     R-V1
           │  R-D3        R-F3        R-L3                 R-V2
     MÉDIO │  R-D4 R-D5   R-F4        R-L4        R-S2 R-S3  R-T1 R-T2
           │              R-F5                    R-S4       R-T3
     BAIXO │  R-O1        R-O2        R-R1                   R-T4
           └──────────────────────────────────────────────────────────►
                 BAIXA            MÉDIA               ALTA     PROBABILIDADE
```

(D = dados · F = financeiro/valuation · L = legal/regulatório/conformidade · S = segurança · V = valor/credibilidade · T = técnico · O = operacional · R = reputação)

---

## 11.2 Riscos de **dados** (a base do número)

| ID | Risco | P | I | Origem | O que reduz |
|---|---|:-:|:-:|---|---|
| **R-D1** | **Quatro/cinco "receitas" diferentes** para o mesmo negócio (memorando, declaração ao banco, livros, PGDAS, banco). O valuation herda a confusão. | A | A | FATO (Anexo C5) | Decisão **DEC-2** (uma definição de receita, Parte 12) + Registry + Radar de discrepâncias. |
| **R-D2** | **Série de nov/25–mai/26 sem rastro** (não está no banco do app; vem do Nexus antigo, inacessível). Se não for recuperada, a "tração" mais forte do material fica sem prova. | A | A | FATO (Anexo B1, C8) | Exportar o Nexus antigo; ou assumir que a série oficial começa em 01/08/2026 (marco do próprio app). |
| **R-D3** | **Caixa de R$ 705,9 mil (balanço 2025) × R$ 42 nas contas conhecidas** em 01/01/2026. Ou há outras contas, ou o caixa contábil não existe como dinheiro. | M | A | FATO (Anexo C4) | Extratos de **2025** e de **todas** as contas; conciliação feita por contador independente. |
| **R-D4** | **Depósito de carteira contado como venda** (63–65% das entradas do app em set/out). Se alguém somar `catalog_sales` sem filtro, superestima receita ≈ 3×. | A | M | FATO | Regra global "depósito ≠ receita" no Registry; view `valueos_*` já exclui. |
| **R-D5** | **Histórico curto**: o dinheiro "real" do app tem ≈ 2,5 meses. DCF e previsão por tendência terão **incerteza alta**. | A | M | FATO | Faixa larga declarada; peso baixo do DCF (10% na proposta); crescer o histórico com fechamento mensal oficial. |
| **R-D6** | **Custo e margem não gravados por venda**; `market_value` apagado em 02/09. Unit economics fica "sem fonte". | A | M | FATO | Mudanças D1–D4 (Parte 10) — ordem sua, zona vermelha. Até lá: margem marcada `AI ASSUMPTION`. |
| **R-D7** | **Definições conflitantes** (licenciado: 6 sentidos / 4 contagens; venda paga: 3 listas de status). | A | M | FATO | Registry com definição única + **DEC-3** e **DEC-4** (Parte 12). |
| **R-D8** | **Planilha Nexus** é lançamento manual por 6 executivos (queda jun→ago; total do cabeçalho de julho não bate com o corpo). Dado `MANAGEMENT DATA` fraco. | M | M | FATO | Tratar como fonte de menor precedência; amostrar contra o banco. |

---

## 11.3 Riscos **financeiros e de valuation**

| ID | Risco | P | I | Origem | O que reduz |
|---|---|:-:|:-:|---|---|
| **R-F1** | **Distância entre os três valores que já circulam** (R$ 25 mi × R$ 0,37–0,75 mi × R$ 8–16 mi): a referência do fundador é **33× a 67×** o que o lucro apurado sustenta. Um investidor vai ver. | A | A | FATO (código do app + sites) | Narrativa única; mostrar o **valuation independente com a ponte**, sem defender R$ 25 mi; modo cego. |
| **R-F2** | **Perímetro indefinido** — qual CNPJ é dono do app, da marca e dos domínios; 100% das cotas do contrato social que li estão com uma só sócia. O valuation pode avaliar o ativo errado. | A | A | FATO (contrato 12/08/2025) + dado faltante | Decisão **DEC-1** (Parte 12): contrato social atual + quem detém a propriedade intelectual. |
| **R-F3** | **Dois negócios misturados:** varejo físico/WhatsApp (Nexus) × plataforma de leilão (app). Comparáveis e múltiplos são diferentes para cada um. | A | A | INFERÊNCIA (forte) | Valuation por **soma das partes** (SOTP), mostrando cada negócio. |
| **R-F4** | **Passivos fora do balanço do app:** carteira de clientes ≈ R$ 45,1 mil (dívida disfarçada), aportes de "parceiro" com repasse prometido (≈ R$ 3,07 mi em intenções canceladas; o que foi pago precisa ser medido), tributos a pagar (R$ 83 mil em 2025), parcelas de consórcio (R$ 12–18 mil/mês), contas vencidas (≈ R$ 167 mil). | A | M | FATO + dado faltante | Ponte do EV para o patrimônio com todos os itens "tipo dívida"; Livro de aportes e consórcios. |
| **R-F5** | **1% do faturamento bruto aos fundadores** e **cota Livoo 2%** ainda no motor: custo que muda margem e EBITDA. | M | M | FATO | Linha própria no modelo + **DEC-10** (Parte 12). |
| **R-F6** | **Viés de confirmação:** a referência de R$ 25 mi já foi vista; a primeira rodada **não pode ser cega**. | A | M | FATO | Dizer isso na tela; pré-registrar pesos e premissas (hash) **antes** de rodar; revisão por terceiro. |
| **R-F7** | **Comparáveis difíceis:** o modelo (leilão de excedentes + rede de licenciados + varejo) não tem par exato; os candidatos que listei (Liquidity Services, Enjoei, ThredUp, RealReal, eBay…) são **a validar**. | M | M | INFERÊNCIA | Mostrar o conjunto de comparáveis, a justificativa e a sensibilidade ao conjunto escolhido. |

---

## 11.4 Riscos **legais, regulatórios e de conformidade** (conversar com advogado e contador)

| ID | Risco | P | I | Origem | O que reduz |
|---|---|:-:|:-:|---|---|
| **R-L1** | **Origem dos recursos.** Créditos de valor redondo (os 20 mais recentes ≥ R$ 5 mil são múltiplos exatos de R$ 1.000), **43 depósitos em dinheiro fracionados no mesmo dia** (24/09, R$ 70 mil) e saldo de R$ 0 → R$ 130 mil em um dia. **Pode ter explicação legítima** (por exemplo, aportes), mas é o tipo de padrão que banco, auditor e investidor tratam como alerta (prevenção à lavagem de dinheiro). | M | A | FATO (extratos, Anexo C9) | Para cada lançamento: **contrato/recibo e quem pagou**. **Advogado + contador antes do Data Room.** O Value OS **não classifica** isso por conta própria: mostra o lançamento, a natureza **informada** e o documento anexado. |
| **R-L2** | **Documento de crédito com total que não confere:** a Declaração de Faturamento soma 16 meses no total impresso (R$ 1.725.558,81 × R$ 1.352.881,81 das 12 linhas) e traz no campo "uso exclusivo do banco" um nome igual ao da administradora (a confirmar). Se foi apresentada ao banco, pode ter consequência; se circular a investidores, é ponto de *due diligence*. | M | A | FATO (conferência por script) | **Levar ao contador e ao advogado antes de circular o dossiê.** Corrigir/retirar e documentar. |
| **R-L3** | **Receitas diferentes para Receita Federal, livros e banco** (PGDAS RBT12 R$ 0,71 mi × livros 2025 R$ 1,19 mi × declaração R$ 1,35–1,73 mi); mudança de **Lucro Presumido para Simples Nacional** sem documento de opção à vista; porte **ME** com receita escriturada acima do limite; **tributo a pagar R$ 83 mil** e só R$ 367 de DARF nas contas conhecidas. | M | A | FATO (dossiê) | Revisão independente (parecer escrito); medir o passivo fiscal potencial e colocá-lo na ponte do valuation. |
| **R-L4** | **Linguagem de oferta pública / promessa:** "sem perda financeira, sem risco típico de apostas"; comparação com apostas; bônus, roleta, passaporte e cupons. Material com projeção de retorno ou captação pode cair em regras de **oferta de valores mobiliários** (CVM) ou de **defesa do consumidor** e de **apostas**. | M | M | FATO (texto dos sites) | Revisão jurídica do texto dos sites e do memorando; o Value OS usa as etiquetas **FORECAST / AI ASSUMPTION** e a frase "não é oferta" em toda tela. |
| **R-L5** | **Aportes de "parceiro" com repasse prometido** podem ter natureza de **captação**; precisam de contrato e enquadramento. | M | A | FATO (plano de capital no app) + dado faltante | Livro de aportes com contrato; advogado define o enquadramento antes de qualquer número ir ao Data Room. |
| **R-L6** | **Dados pessoais (LGPD):** o app guarda CPF, endereços, IP; o dossiê tem documentos pessoais de sócios em pasta compartilhada. | M | M | FATO | Tirar as pastas 08/12/14 do compartilhamento; o Value OS recebe **só agregados**; registro de acesso; retenção definida. |
| **R-L7** | **Sigilo do dossiê:** foi compartilhado "em caráter confidencial". Um repositório de código **não** é o lugar de dados pessoais ou de números sensíveis por pessoa. | B | A | FATO | Nos arquivos que gerei só há **agregados** (sem CPF, conta ou nome de pessoa). Manter o Data Room real num cofre com acesso controlado, não em repositório. |
| **R-L8** | **Propriedade intelectual:** quem escreveu o código (contratos de trabalho/prestação), titularidade da marca e dos domínios. | M | M | dado faltante | Contratos de cessão no Data Room. |
| **R-L9** | **Venda de participação sem contrato.** Informada: **1% por R$ 250 mil** (R$ 200 mil já no Itaú em 24 e 30/09, **incluindo R$ 70 mil em 43 depósitos de dinheiro**; R$ 50 mil a receber). **O CEO informa que o contrato só será assinado depois que o restante de R$ 50 mil entrar** → hoje **R$ 200 mil estão recebidos sem contrato**. No contrato social que li, as cotas estão com uma só sócia: se foi cota dela, o dinheiro não é da empresa; se foi aumento de capital, falta alteração contratual; a **origem do dinheiro do comprador** precisa estar documentada. | M | A | MANAGEMENT DATA + extratos (C14) | Contrato de compra, alteração na Junta, identificação do investidor e do pagador; **advogado antes de nova captação** (DEC-21). |
| **R-L10** | **"Parceiro de compra" com juros fixos e captação.** Contrato A (assinado): **4,5% ao mês fixos + devolução do principal**, com "fee" de 1,5% para quem traz novos parceiros; contrato B: 3% do capital ao mês. O texto do painel diz "sem retorno garantido, não é investimento"; o memorando público fala em "retorno elevado sobre capital investido"; o Mapa Jurídico de 23/09 trata o modelo como "a definir". Enquadramento possível como **empréstimo** ou **captação de investimento coletivo**; testemunhas ligadas à empresa; contrato B com **data impressa em branco** (assinado em 11/08, segundo o CEO; confirmar pelo certificado DocuSign); **pagador do aporte A diferente do parceiro**. | A | A | FATO (contratos, painel, sites, extratos) | **Advogado antes de qualquer nova captação e antes de divulgar o memorando**; confirmar a data de assinatura do contrato B pelo certificado DocuSign; alinhar texto; documentar origem do dinheiro (DEC-22). |
| **R-F8** | **Resultado "apurado" superestimado:** a linha de 5% dos parceiros de compra saiu dos cenários em 02/10/2026 (resultado anual de R$ 88.884 para R$ 124.596). O "valuation" de R$ 0,37–0,75 mi (3–6×) herda a diferença. | A | M | FATO (código + ramo de restauração) | Reincluir o custo real; mostrar as duas versões; **DEC-23**. |
| **R-F9** | **Serviço da dívida com parceiros maior que a receita reconhecida.** Só os contratos A e B exigem **R$ 10,5 mil/mês** (setembro: receita contabilizada R$ 6,1 mil); os repasses saem do dinheiro dos **novos aportes** — risco de **dependência de captação** para pagar os antigos. Além dos contratos, há **R$ 35,6 mil (15/09) e R$ 30,6 mil (15/10)** pagos como **cartão de crédito da empresa** (ver R-F10). | A | A | FATO (contratos + extratos) | Cronograma por contrato; classificação dos pagamentos redondos fora dos contratos; teste de "pagaria sem novos aportes?" no Value OS (DEC-22, DEC-24). |
| **R-F10** | **Despesas do cartão empresa só por informação.** **Pagamentos** de **R$ 18,8 mil (ago), R$ 23,0 mil (set) e R$ 18,4 mil (5/10)** lançados no app como "Cartão de Crédito" + **R$ 35,6 mil (15/09) e R$ 30,6 mil (15/10)**: o CEO informa **aluguel de R$ 10 mil (o "hotel"), tecnologia e marketing** e **não enviará as faturas**; informa também que **não há fatura em aberto (tudo pago)**. O app lança **o pagamento**, não **o que foi comprado**: **sem fatura, não há prova por categoria**. | M | B | MANAGEMENT DATA (sem fatura) + extratos | Usar a composição informada (confiança baixa); **fatura em aberto = R$ 0** na ponte; amostra de **uma fatura** se um investidor pedir (DEC-25). |

---

## 11.5 Riscos de **segurança** (nada foi alterado; cada item depende da sua ordem)

| ID | Risco | P | I | Origem | Correção sugerida (Parte 10, S1–S7) |
|---|---|:-:|:-:|---|---|
| **R-S1** | **Rota do termo de sigilo** devolve a linha inteira (nome, CPF, e-mail, IP) de qualquer `user_id` e **não está na lista de rotas trancadas**. Depende do modo da trava (`SESSAO_MODO`) na Vercel. | M | A | FATO (código); modo a confirmar | S2 + S4 |
| **R-S2** | **`cost_price` e comissões legíveis com a chave pública** do navegador. Um concorrente ou investidor curioso lê o custo real de cada produto. | M | M | FATO (privilégio e política verificados) | S5, S6 (zona vermelha) |
| **R-S3** | **128 de 209 rotas** do servidor só anotam no registro quando falta o crachá — **não barram**. | M | M | FATO | Subir rotas para "trancada" em lotes, com teste |
| **R-S4** | **3 tabelas de pagamento sem RLS** (`gateway_*`); acesso público revogado hoje — "uma trava só". | B | M | FATO | S1 |
| **R-S5** | **Valuation, CNPJ, PGDAS e contadora no pacote público do site**; NDA conferido só no navegador. | A | M | FATO | S3, S7 |
| **R-S6** | **`InvokeLLM` aberto**: um chat de IA sem filtro de permissão sobre dados de investidor seria vazamento. | M | A | FATO | A IA do Value OS (Ask LNZ AI) responde **só** do que o papel do usuário pode ver (filtro antes do modelo). |
| **R-S7** | **Segredos** (tokens de Mercado Pago, etc.) ficam na Vercel; **eu não os li nem devo**. Se o Value OS pedir token de gateway, isso cria um segundo lugar com segredo. | B | A | FATO | Value OS **não guarda** token de gateway; consome arquivos exportados e views somente leitura. |
| **R-S8** | **Login caseiro do app** (crachá HMAC) não deve ser reaproveitado para investidores. | — | A | FATO | Login separado, 2º fator, convite, papéis `valueos_viewer`, expiração. |

---

## 11.6 Riscos de **valor e credibilidade** (o que o investidor percebe)

| ID | Risco | P | I | O que reduz |
|---|---|:-:|:-:|---|
| **R-V1** | **Os sites afirmam coisas que o código não confirma** (TikTok Shop ativo, "99%", "PHIZ", "IA proprietária de preço", "Livoo: sociedade em fase final" — a Livoo saiu hoje). Um item falso derruba a confiança no resto. | A | A | Retirar/reescrever **antes** de qualquer divulgação nova; itens em `anexos/A`. |
| **R-V2** | **Material inconsistente entre si** (80 ativos × 40 ativos × 23 no banco; 960% × 1.000%; "R$ 40B" com dois significados). | A | A | Números vindos do Registry, com a janela e a definição no nome da métrica. |
| **R-V3** | **"Mais preciso que humanos"** ou "valuation final" como promessa. | B | A | Nunca afirmar; mostrar faixa, incerteza e método. |

---

## 11.7 Riscos **técnicos** e de projeto

| ID | Risco | P | I | O que reduz |
|---|---|:-:|:-:|---|
| **R-T1** | **Testes do app não executam SQL** (banco falso): 6 erros plantados, 4.479 testes passaram nos 6. Se o Value OS herdar fórmulas do app sem teste real, herda os erros. | A | M | Testes com **Postgres real** e **casos de referência** (Parte 10, Fase 1/3). |
| **R-T2** | **Escopo muito grande** (46 itens, 6 camadas): risco de entregar tudo pela metade. | A | M | Fases com critério de saída; fase 1–2 já entregam valor (DRE + radar). |
| **R-T3** | **Dependência de dados que só você tem** (extratos, contratos, aportes, Nexus antigo, Mercado Pago). | A | M | Lista objetiva em 12.3; o motor roda com o que houver e **mostra o que falta**. |
| **R-T4** | **Fuso e datas** (UTC × BRT; `pago_em` só desde 08/10/2026). | M | B | Regra global do Registry (BRT; `pago_em` quando existir). |
| **R-T5** | **Mudar produção** para melhorar dados (D1–D10) mexe em zona vermelha. | M | A | Só com sua ordem, na janela 01h00–02h15, com migração em arquivo. O Value OS **começa sem isso**. |

---

## 11.8 Riscos **operacionais** e de **reputação**

| ID | Risco | P | I | O que reduz |
|---|---|:-:|:-:|---|
| **R-O1** | Depender de planilha manual (Nexus) para o varejo. | M | B | Lançamento no app ou integração; amostragem. |
| **R-O2** | Fechamento mensal oficial exige rotina (extratos, conciliação, aprovação). | M | M | Calendário e responsável; checklist no Value OS. |
| **R-R1** | Se o valuation independente vier **muito abaixo** de R$ 25 mi, o fundador fica exposto se já divulgou o valor. | M | M | Decidir **antes** (**DEC-6**, Parte 12) como o resultado será comunicado; a primeira rodada é **sombra** (não pública). |

---

## 11.9 Os 10 riscos que eu trataria **primeiro** (ordem)

1. **R-L1** — origem dos recursos (advogado + contador, antes de qualquer Data Room).
2. **R-L2 / R-L3** — declaração ao banco e receitas diferentes (contador independente).
3. **R-F2** — perímetro: quem é dono do app, da marca, dos domínios; cap table atual.
4. **R-V1** — retirar dos sites o que não é verdade hoje (Livoo, TikTok, 99%).
5. **R-S1 / R-S5** — rota do termo de sigilo e dados fiscais no pacote público.
6. **R-D1** — uma só definição de receita.
7. **R-D3** — extratos de 2025 e de todas as contas (reconciliar o caixa).
8. **R-D2** — recuperar a série do Nexus antigo.
9. **R-L6 / R-L7** — documentos pessoais fora do compartilhamento.
10. **R-F4 / R-L5** — livro de aportes e consórcios com contrato.

> **O que eu não fiz:** não corrigi nada. Nenhuma linha do app, do banco, dos sites ou da produção foi alterada.
