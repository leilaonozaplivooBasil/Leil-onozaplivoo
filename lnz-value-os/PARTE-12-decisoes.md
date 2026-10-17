# Parte 12 — Decisões necessárias (e dados que faltam)

> **Em português simples:** nada do que está nas Partes 1–11 vira código, banco ou mudança de site sem a sua resposta. Esta parte junta **tudo o que só você pode decidir**, com a **minha recomendação** e o **porquê**. Você pode responder só "ok" ou "ajustar" em cada linha.
> **Três níveis de aprovação, separados:**
> 1. **Desenho** — aprovar as Partes 1–11 como direção (ou pedir ajuste).
> 2. **Decisões** — as 20 linhas de 12.1 e 12.2.
> 3. **Mudança em produção** — cada item S1–S7 e D1–D10 da Parte 10 é aprovado **um a um**, na zona vermelha só com a sua ordem e na janela 01h00–02h15.

---

## 12.1 Decisões que definem **o que** é medido (bloqueiam o modelo)

| # | Decisão | Opções | **Minha recomendação** | Por quê | Efeito se não decidir |
|---|---|---|---|---|---|
| **DEC-1** | **Perímetro:** o que será avaliado? | A. Compras Full Comércio Ltda · B. Ecossistema (empresa + app + marca + rede) · C. Só a plataforma/tecnologia | **Primeiro responder: de qual CNPJ (ou contrato) são o app, a marca e os domínios, e quem são os sócios hoje.** Depois escolher **B** se um CNPJ reunir os ativos; senão **A** + um quadro de "ativos de outro dono". | No contrato social que li (12/08/2025) as 500.000 cotas estão com **uma só sócia**; o CEO e os outros "fundadores" não aparecem. Avaliar o perímetro errado invalida tudo. | O motor não roda "oficial"; fica só em simulação. |
| **DEC-2** | **O que é "receita"** | Agente (a comissão que a empresa retém) · Principal (o valor da venda; comissão e taxa viram custo) | **Principal para o varejo/loja (a empresa compra o lote e vende); agente para o leilão entre terceiros, se houver**; mostrar as duas visões lado a lado. | O app grava só a comissão retida (R$ 10,99 mil desde julho). Investidor compara com margem de e-commerce, que usa venda. | Cada tela do investidor mostra um "faturamento" diferente. |
| **DEC-3** | **O que é "licenciado" e "ativo"** | 15 (cargo) · 23 (`role`) · 84 (contexto) · **pagante** (comprou adesão) | **Licenciado = pagou adesão ou comprou o kit (evento registrado); ativo = comprou ou indicou nos últimos 30 dias.** Mostrar também "total concedido". | Hoje não dá para separar pagante de concedido; os "80" dos sites não têm definição. | `LICENSEES_*` fica `sem fonte`. |
| **DEC-4** | **O que é "venda paga" e "cliente"** | 4 status (`dinheiroReal.js`) · 9–10 status (CRM) · só `paid` | **A lista do `dinheiroReal.js`**, sem depósito, sem teste, sem `is_investment_plan`; cliente = conta que pagou ≥ 1 vez nos últimos 90 dias. | É a única já usada como "dinheiro real" no marco oficial. | Três totais diferentes para o mesmo mês. |
| **DEC-5** | **Quem ganha quando as fontes discordam** | Sua ordem (contabilidade > app > planilha > gerencial > banco…) · **Banco/gateway > app > contabilidade > planilha > gerencial** | **Banco/gateway primeiro.** | Dinheiro que entrou na conta é mais difícil de "ajustar" do que lançamento. **Diverge da hierarquia que você escreveu** — por isso é decisão sua. | Sem regra, o Radar só mostra a divergência e não resolve. |
| **DEC-6** | **Como comunicar o resultado** | Mostrar já ao investidor · **Rodada sombra privada primeiro (só CEO/conselho)** · Nunca mostrar | **Sombra privada**, depois decidir. | A referência de R$ 25 mi já foi vista, então a primeira rodada **não pode ser cega**. Se o independente vier muito abaixo, você escolhe como contar — com a ponte pronta. | Risco de divulgar número que você não consegue defender. |
| **DEC-7** | **Data de corte e série antiga** | Série oficial a partir de **01/08/2026** (marco do app) · incluir nov/25–mai/26 se houver prova | **Oficial a partir de 01/08/2026; nov/25–mai/26 entra como `MANAGEMENT DATA` (rotulado) enquanto não houver exportação do Nexus antigo ou extrato que prove.** | O próprio app diz que antes de 01/08 é "teste, sem valor financeiro". | Contradição entre memorando e app continua visível. |
| **DEC-8** | **Consórcio** | Ativo não operacional da empresa (com passivo) · Fora do valuation | **Cartas no nome da empresa entram na ponte como ativo líquido (valor da carta − saldo devedor, com desconto de liquidez); cartas no nome do sócio ficam fora**, a menos que exista contrato de cessão. | O valor do equity muda, mas **não** o valor da operação. | O equity fica incompleto. |
| **DEC-9** | **Carteira dos clientes e aportes** | Carteira como patrimônio · **Carteira como dívida** · Aportes como capital · **Aportes com repasse como passivo** | **Carteira = dívida (≈ R$ 45,1 mil hoje).** **Aportes com repasse prometido = passivo; sem repasse = capital** — você vai me passar a lista. | Dinheiro de carteira pode ser sacado; aporte com repasse tem que ser devolvido. | Equity superestimado. |
| **DEC-10** | **1% do faturamento bruto aos fundadores e cota Livoo de 2%** | Custo na linha própria · fora do modelo | **Custo na linha própria**, com a base de cálculo que você definir (receita bruta global? só app?). **Livoo 2%: confirmar se o motor deve parar de pagar** (ela deixou de ser parceira em 17/10/2026). | Mexe em EBITDA e em quem fica com o quê. | Margem superestimada. |

---

## 12.2 Decisões de **método, produto e segurança**

| # | Decisão | **Minha recomendação** | Observação |
|---|---|---|---|
| **DEC-11** | **Metodologia v1.0 e pesos** (comps 25 · VC 20 · transações 15 · soma das partes 15 · DCF 10 · piso 10 · unit economics 5) | **Aprovar como proposta**, ou ajustar **antes** de rodar. | Depois da primeira rodada, mudar peso = versão nova (v1.1), nunca silenciosa. |
| **DEC-12** | **Fonte e orçamento dos comparáveis/transações** | Começar com fontes públicas (balanços de Liquidity Services, Enjoei, ThredUp, RealReal, eBay…) e **contratar uma base paga só se necessário**. | Lista da Parte 8 é "a validar". |
| **DEC-13** | **Onde mora o Value OS** | **Opção A:** repositório novo + Vercel novo + Supabase novo; o app só ganha um botão. | Isolamento total da produção; é o que um investidor espera ver. |
| **DEC-14** | **Login/NDA do investidor** | Login próprio + 2º fator + convite + NDA **no servidor** + papéis (`PUBLIC / INVESTOR / BOARD / ADMIN`) + expiração + marca d'água. | **Não** reaproveitar o crachá do app. |
| **DEC-15** | **Os dois sites** | Virar "portas" do Value OS (conteúdo vindo do sistema) **ou** ficar atrás de login até a revisão. **Em qualquer caso: retirar já a Livoo, "TikTok Shop ativo", "99%" e números sem fonte.** | Onde estão hospedados e quem controla o DNS? (não estão na sua conta Vercel.) |
| **DEC-16** | **Política de números públicos** | Nenhum número no site público sem fonte e data; investidores só dentro do portal. | Evita nova divergência. |
| **DEC-17** | **Segurança (S1–S7, Parte 10)** | **Fazer de qualquer forma**, em lotes pequenos, pelo processo do app (migração em arquivo, janela 01h00–02h15). Começar por S4 (só leitura), S2 e S3. | Cada item aprovado **um a um**. |
| **DEC-18** | **Melhorias de dado no app (D1–D10, Parte 10)** | Aprovar **só depois** da Fase 1; começar por D4, D6, D9 (fora da zona vermelha) e depois D1–D3 (custo, canal, frete). | O Value OS começa **sem** tocar produção. |
| **DEC-19** | **Revisão externa** | Contador independente (CRC) + advogado revisam: declaração de faturamento, PGDAS × livros × banco, regime tributário, **classificação dos créditos grandes e dos depósitos em dinheiro**, enquadramento dos aportes. **Antes** do Data Room. | Não é parecer meu; é de quem assina. |
| **DEC-20** | **Dossiê no Drive** | Tirar as pastas de documentos pessoais (08, 12, 14) do compartilhamento; manter o dossiê só com quem precisa. | Não abri essas pastas. |

---

## 12.3 **Dados que faltam** (peço, em ordem de importância)

| # | O que mandar | Para quê | Quem tem |
|---|---|---|---|
| 1 | **Relatórios do Mercado Pago em CSV**: *Liberações de dinheiro* e *Movimentações*, de **jul a out/2026** (e nov–dez/2025, se existirem). *Painel → Atividade → Relatórios.* | Eu **não consigo puxar** o Mercado Pago (o token fica na Vercel e não deve passar por mim). Sem isso, setembro e outubro ficam incompletos. | financeiro |
| 2 | **Lista dos aportes e investimentos** (quem, quando, quanto, contrato, repasse prometido) | Classificar os 19 + 20 créditos grandes e montar a ponte | CEO |
| 3 | **Extratos de 2025 e de todas as outras contas** (Nubank? outras do Santander/Itaú; contas dos sócios usadas pela empresa) | Reconciliar o caixa de R$ 705,9 mil do balanço de 2025 | financeiro |
| 4 | **Contrato social atual** e quadro de sócios | DEC-1 (perímetro) | contador / jurídico |
| 5 | **Quem é o dono do app, marca e domínios** (contratos de cessão) | DEC-1 | jurídico |
| 6 | **Exportação do Nexus antigo** (CSV das vendas nov/25–mai/26) ou acesso ao app antigo | Provar a série do memorando | quem desenvolveu |
| 7 | **Contratos e extratos dos consórcios** (valor da carta, parcelas pagas/a pagar, saldo devedor, contemplação, alienação) | DEC-8 | CEO |
| 8 | **Balancete/DRE 2026**, **PGDAS-D e DAS pagos 2026**, documento de **opção pelo Simples** | Receita e passivo fiscal | contador |
| 9 | **Folha/pró-labore, aluguel, dívidas e parcelamentos** | Passivos fora do app | financeiro |
| 10 | **Comprovantes dos 39 créditos ≥ R$ 5.000** (quem pagou e por quê) | Origem dos recursos | financeiro / CEO |

---

## 12.4 O que acontece depois da sua resposta

```
 Sua resposta (12.1 + 12.2)
        │
        ├─ Desenho aprovado ───► Fase 0 (semanas 0–2): dados e limpeza dos documentos
        │                              │
        │                              ▼
        │                        Fase 1 (semanas 2–6): projeto novo, login, Registry, ingestão, Evidence Ledger
        │                              │
        │                              ▼
        │                        Fases 2–3: DRE/FCFF conciliados → motor de valuation v1.0 (pesos pré-registrados)
        │                              │
        │                              ▼
        │                        Fase 4: portal, Data Room, Ask LNZ AI, as duas "portas"
        │
        └─ Mudanças em produção (S1–S7, D1–D10): uma a uma, na janela, com migração em arquivo
```

**Primeira entrega depois da aprovação** (Fase 1, ≈ semana 6): 30 métricas calculadas, cada uma com origem e prova, e **nenhum número de valuation mostrado**.
**Primeira rodada de valuation** (≈ semana 14): privada (DEC-6), com pesos e premissas travados antes.

---

## 12.5 O que eu **não** fiz (para ficar claro)

- Não escrevi código do Value OS.
- Não alterei o banco (só leitura: 154 tabelas, consultas listadas no Anexo B).
- Não alterei os dois sites, nem o app, nem a produção.
- Não abri as pastas de documentos pessoais do Drive.
- Não li valores de segredo (tokens, chaves).
- Não classifiquei nenhum crédito bancário como "irregular" — apenas mostrei o padrão e pedi a documentação.
- Não calculei nem apresentei um número de valuation.

> **Se você aprovar o desenho**, a próxima mensagem deve trazer: (a) respostas de 12.1 e 12.2; (b) os arquivos de 12.3, na ordem que conseguir. Dá para começar com o que já tem — o motor mostra o que falta.
