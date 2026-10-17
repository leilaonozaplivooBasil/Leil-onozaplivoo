# Partes 3 e 4 — Arquitetura futura e diagrama completo

> **Estado:** proposta para sua aprovação. Nada foi construído.
> **Linguagem:** os nomes dos módulos são os seus (Metrics Registry, Evidence Ledger…). Cada um vem com uma frase em português simples.

---

## 3.1 A pergunta que você fez: "dentro do app, com login e senha, ou fora?"

**Resposta curta:** **login e senha, sim — sempre, para qualquer número.**
**Dentro do app de clientes, não.** O certo é uma **área própria, com login próprio**, ligada ao app por um botão no painel de administração.

Em uma frase: **o motor mora fora do app; o botão de entrada mora dentro.**

### Por que não dentro do app (o que encontrei no código)

| # | O que eu vi | Por que importa |
|---|---|---|
| 1 | O app tem login próprio, e **128 das 209 rotas só anotam num registro** quando falta o crachá — não barram. | Dado de investidor não pode depender de uma trava que hoje só observa. |
| 2 | O navegador lê o banco com uma chave pública. **Qualquer pessoa com essa chave lê o custo dos produtos** (`products.cost_price`) e **as comissões** (`commission_records`). | Um investidor não pode morar num banco com essa porta. |
| 3 | **Já existe um "Valuation" e um "Memorando" dentro do app** (painel do Parceiro), com números **escritos no código** — **inclusive CNPJ e número do PGDAS no pacote público do site** — e o sigilo (NDA) é conferido só no navegador. | É exatamente o modelo que você quer deixar para trás. |
| 4 | Uma rota do NDA (`consultarAssinaturaSigilo`) devolve a linha inteira da assinatura (nome, CPF, e-mail, IP) de **qualquer** pessoa pelo número de usuário, sem trava ligada. | Misturar investidor externo ali amplia esse risco. |
| 5 | Deploy só entre **01h00 e 02h15** e mudança em dinheiro exige ordem sua. | Toda melhoria no painel de investidor esperaria essa janela e essa fila. |
| 6 | Quem avalia não deveria poder escrever no sistema que gera os números. | Credibilidade: o investidor pergunta "quem garante que o painel não foi ajustado?". Separar resolve. |

### Por que a área própria é mais profissional

Salas de dados de mercado (Datasite, Intralinks, DocSend) têm em comum: **convite por e-mail, aceite de confidencialidade, marca d'água com o nome de quem abriu, prazo de acesso, permissão por pasta e por arquivo, e registro de tudo que cada pessoa viu.** Foi o que as fontes que consultei apontam como o mínimo hoje (ver *Fontes*, abaixo). Nada disso faz sentido dentro de um app que também é loja e leilão.

### O que fica dentro do app

Só **um botão** "Abrir LNZ VALUE OS" para quem é super_admin/admin. Ele leva à área própria. Nada de dado de investidor passa pelo app.

### Os três lugares, resumidos

```
 ┌────────────────────────┐   ┌─────────────────────────────┐   ┌──────────────────────────┐
 │ APP DE CLIENTES         │   │ LNZ VALUE OS  (área própria)│   │ OS 2 SITES ATUAIS        │
 │ leilaonozap.net         │   │ login + 2º fator + convite  │   │ (portas de entrada)      │
 │ clientes, rede, leilão  │   │ cockpit CEO/Conselho        │   │ só narrativa, sem número │
 │                         │──►│ portal do investidor        │◄──│ vivo; botão "Entrar"     │
 │ [botão: Abrir Value OS] │   │ data room · Ask LNZ AI      │   │ leva ao login do Value OS│
 └────────────────────────┘   └─────────────────────────────┘   └──────────────────────────┘
        (só lê, nunca é escrito pelo Value OS)
```

**Recomendação para os dois domínios:** `valuationleilaonozap.com` vira a **vitrine** do Live Valuation (resumo + "Entrar"), e `investmentmemorandumleilaonozap.com` vira o **memorando dinâmico** (narrativa sua + números que só aparecem depois do login). Os dois consomem **o mesmo backend**, como você pediu.

---

## 3.2 Princípios da arquitetura

1. **Só leitura sobre a produção.** O Value OS **nunca escreve** nas tabelas do app. Ele lê, calcula e guarda o resultado **no seu próprio banco**.
2. **Banco separado.** Um projeto Supabase novo (só do Value OS). Assim, a falha de segurança de um não abre o outro, e o login do investidor não se mistura com 1.100 contas de cliente.
3. **Uma fonte da verdade.** Nenhuma tela escreve número à mão. Toda tela lê a **Camada de Métricas**.
4. **Todo número tem etiqueta de origem:** `VERIFIED`, `MANAGEMENT DATA`, `FORECAST`, `AI ASSUMPTION` — e carrega o caminho até o dado bruto.
5. **Nada se apaga.** Evidência e fechamento oficial são *só acrescentam*, com impressão digital (hash) encadeada e bloqueio no próprio banco contra alteração.
6. **A IA nunca vê o que o usuário não pode ver.** O filtro acontece **antes** da pergunta chegar ao modelo, não depois.
7. **Cálculo em código puro, testável.** Fórmulas de valuation são funções simples, testadas com casos conhecidos (planilhas de referência) — nada de fórmula só dentro de SQL.

---

## 3.3 As camadas

```
CAMADA 0 — FONTES (só leitura)
  App (Supabase prod)  ·  Mercado Pago  ·  Contabilidade/PGDAS  ·  Extrato bancário
  Planilha Nexus       ·  Dados de mercado (comparáveis)  ·  Documentos (Data Room)
                │
                ▼
CAMADA 1 — LNZ DATA ENGINE (extração)
  • perfil de banco SOMENTE LEITURA (views dedicadas)  • cargas por upload (PGDAS, extrato)
  • cada carga vira um "LOTE" com data, quem subiu, hash do arquivo
                │
                ▼
CAMADA 2 — SINGLE SOURCE OF TRUTH
  fatos brutos normalizados (status em um idioma só, datas em BRT, valor em centavos)
                │
                ▼
CAMADA 3 — METRICS REGISTRY + CAMADA CENTRAL DE MÉTRICAS
  definição oficial de cada KPI  →  valor por período  →  etiqueta de qualidade
                │
        ┌───────┴────────┐
        ▼                ▼
CAMADA 4 — MODELO FINANCEIRO     CAMADA 5 — QUALIDADE & EVIDÊNCIA
  Realizado · Forecast por         Evidence Ledger · Discrepancy Radar
  drivers · Cenários · DRE/FCFF    Data Quality · Confiança · Risco
        │                         ▲
        ▼                         │
CAMADA 6 — VALUATION ENGINE ──────┘
  DCF · Comparáveis · Transações · Método VC · Soma das partes · Custo de reposição
  → Triangulação → FAIXA  (+ Modo Cego)
        │
        ▼
CAMADA 7 — SNAPSHOTS
  Live (contínuo) · Shadow (diário) · Oficial (mensal, imutável)
        │
        ▼
CAMADA 8 — EXPERIÊNCIA
  Cockpit CEO/Conselho · Portal do Investidor · Memorando dinâmico · Data Room · Ask LNZ AI
```

### O que fica em cada pedaço

| Pedaço | O que é, em português simples | Onde mora |
|---|---|---|
| Data Engine | Robô que busca os dados e guarda cada busca com data, autor e impressão digital. | Funções de servidor do Value OS + perfil de leitura no banco do app |
| Metrics Registry | O "dicionário oficial": cada número tem uma definição só, um dono e uma fórmula. | Tabelas versionadas |
| Financial Model Engine | A conta de resultado (DRE) e caixa, do passado e do futuro. | Bibliotecas de cálculo + tabelas |
| Valuation Engine | Os métodos de avaliação e a mistura deles numa faixa. | Bibliotecas de cálculo + tabelas |
| Evidence Ledger | O "clique para provar": de onde veio cada número. | Tabela só-acrescenta com hash |
| Discrepancy Radar | Alarme quando duas fontes discordam. | Rotina diária |
| Snapshot | Foto fechada do valuation num dia. A oficial não muda mais. | Tabela só-acrescenta |
| Ask LNZ AI | Perguntas em português, respondidas só com o que a pessoa pode ver. | Função de servidor + modelo de IA |

---

## 3.4 Onde mora o código (o que eu recomendo)

| Opção | Prós | Contras |
|---|---|---|
| **A. Repositório novo + projeto Vercel novo + projeto Supabase novo** *(recomendada)* | Deploy fora da janela de 01h–02h15 do app; sem passar por "zona vermelha"; segurança isolada; fácil dar acesso só ao time de valuation. | Mais uma coisa para manter. Reaproveitar o padrão visual exige copiar o guia de design. |
| B. Pasta nova dentro do repositório do app (`src/pages/ValueOs*`, `api/functions/valueOs*`) | Reaproveita login, componentes e CI. | Herda janela de deploy, zona vermelha e a fragilidade de login. Mistura investidor com cliente. |
| C. Este repositório de análises (`Leil-onozaplivoo`) vira o projeto | Já existe, já é "o repositório de diagnósticos". | Hoje é só documentação; precisaria virar um app. |

**Recomendo A**, e que o repositório seja **privado**. Se preferir C, funciona do mesmo jeito (é só renomear o papel dele).

> Reaproveitar do app (cópia, não ligação): o **guia de design** (`docs/GUIA_DE_DESIGN.md` — o Value OS terá paleta própria, como o "PC" já tem), o padrão de **extrato só-acrescenta** (`reserva_ledger`, `financial_income`), o **cofre de segredos**, e as bibliotecas `dinheiroReal`, `custoProduto`, `simplesNacional`.

---

## 3.5 Segurança desde o primeiro dia

| Item | Como fica no Value OS |
|---|---|
| Login | Supabase Auth do **projeto novo**: convite por e-mail + **segundo fator obrigatório** para CEO/Conselho e investidores. |
| Papéis (RBAC) | `PUBLIC` · `INVESTOR` · `BOARD` · `ADMIN`. **Não** usar a palavra "investidor" do app (lá é quem aporta capital em lote de leilão) — usar `valueos_viewer`. |
| Permissão por linha | Toda tabela com RLS **ligada e sem política aberta**. Acesso só por funções do servidor ou por política explícita. |
| Auditoria | Toda leitura de dado sensível e todo download vira linha no registro de acesso. |
| Prazo | Convite de investidor tem validade; acesso expira sozinho. |
| NDA | Aceite **registrado no servidor** com versão do texto, IP e hora — antes de ver qualquer número. |
| Marca d'água | Documento do Data Room sai com nome e e-mail de quem abriu. |
| IA | O filtro de permissão vem **antes** do prompt. Sem dado autorizado → "DADO NÃO DISPONÍVEL". |
| Segredos | Cofre; nada no código nem no navegador. Nenhum endpoint de IA aberto (o do app, `InvokeLLM`, está aberto — **não reutilizar**). |
| Limite de uso | Limite por usuário e por IP; falha **fechada** (se o contador cair, nega — o do app falha aberto). |

---

## Parte 4 — Diagrama completo

```
╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                                   LNZ VALUE OS                                            ║
║                       Live Valuation & Investor Intelligence                              ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝

 FONTES (somente leitura)                                                       PORTAS DE ENTRADA
 ┌───────────────────────┐                                                      ┌───────────────────┐
 │ APP LEILÃO NOZAP      │  perfil só-leitura / views                           │ valuationleilao…  │─┐
 │  usuários · lances    │──┐                                                   │  (vitrine)        │ │
 │  vendas · carteiras   │  │                                                   ├───────────────────┤ │ "Entrar"
 │  estoque · comissões  │  │      ┌──────────────────────────┐                 │ investmentmemo…   │ │
 └───────────────────────┘  │      │     LNZ DATA ENGINE      │                 │  (memorando       │ │
 ┌───────────────────────┐  ├─────►│  extrai · guarda LOTE    │                 │   dinâmico)       │─┤
 │ MERCADO PAGO          │  │      │  (data, autor, hash)     │                 ├───────────────────┤ │
 │  pagamentos · taxas   │──┤      └────────────┬─────────────┘                 │ botão no app      │ │
 └───────────────────────┘  │                   ▼                               │ (admin → Value OS)│─┘
 ┌───────────────────────┐  │      ┌──────────────────────────┐                 └─────────┬─────────┘
 │ CONTABILIDADE / PGDAS │──┤      │  SINGLE SOURCE OF TRUTH  │                           │
 │ EXTRATOS BANCÁRIOS    │  │      │ fatos normalizados       │                           ▼
 │ (upload com hash)     │  │      └────────────┬─────────────┘                 ┌───────────────────┐
 └───────────────────────┘  │                   ▼                               │  LOGIN + 2º FATOR │
 ┌───────────────────────┐  │      ┌──────────────────────────┐                 │  convite · NDA    │
 │ DADOS DE MERCADO      │──┤      │ METRICS REGISTRY         │                 └─────────┬─────────┘
 │ comparáveis, juros,   │  │      │ definição · fórmula ·    │                           │
 │ transações            │  │      │ dono · qualidade         │                           ▼
 └───────────────────────┘  │      └────────────┬─────────────┘            ┌────────────────────────────┐
 ┌───────────────────────┐  │                   │                          │ PAPÉIS                     │
 │ DOCUMENTOS            │──┘                   ▼                          │ PUBLIC  · INVESTOR · BOARD │
 │ contratos, balanços   │          ┌──────────────────────────┐           │ · ADMIN                    │
 └───────────────────────┘          │ FINANCIAL MODEL ENGINE   │           └────────────┬───────────────┘
                                    │ Realizado │ Forecast │   │                        │
                                    │ (drivers) │ Cenários │   │                        │
                                    │ DRE · Caixa · FCFF      │                        │
                                    └────────────┬─────────────┘                        │
                                                 ▼                                      │
              ┌─────────────────────────────────────────────────────────────┐          │
              │                    VALUATION ENGINE                         │          │
              │  DCF │ Comparáveis │ Transações │ Método VC │ Soma das      │          │
              │      │             │            │           │ partes │ Custo │          │
              │      │             │            │           │ de reposição  │          │
              │                  ▼  TRIANGULAÇÃO (pesos justificados) ▼     │          │
              │                  FAIXA: BAIXO · CENTRAL · ALTO              │          │
              │        MODO CEGO ◄── referência do fundador lacrada (hash)  │          │
              └─────────────────────────────┬───────────────────────────────┘          │
                                            ▼                                          │
   ┌────────────────────────────────────────────────────────────────────────┐          │
   │ QUALIDADE & EVIDÊNCIA                                                  │          │
   │ Data Quality · Confiança · Risco · Evidence Ledger · Discrepancy Radar │          │
   └─────────────────────────────┬──────────────────────────────────────────┘          │
                                 ▼                                                     │
   ┌────────────────────────────────────────────────────────────────────────┐          │
   │ SNAPSHOTS                                                              │          │
   │ LIVE (contínuo) ─► SHADOW (diário) ─► OFICIAL (mensal, IMUTÁVEL, hash) │          │
   └─────────────────────────────┬──────────────────────────────────────────┘          │
                                 ▼                                                     │
   ┌──────────────────────────────────────────────────────────────────────────────────▼────┐
   │ EXPERIÊNCIA (o que cada papel enxerga)                                                  │
   │  Cockpit CEO/Conselho │ Portal do Investidor │ Memorando dinâmico │ Data Room │ ASK LNZ AI │
   │  Scenario Lab │ Value Bridge │ Milestone-to-Value │ Exportações (XLSX / PDF / CSV)      │
   └───────────────────────────────────────────────────────────────────────────────────────┘

 TRANSVERSAL:  RBAC · Auditoria de acesso · Versão da metodologia · Backtest · Cofre de segredos
```

---

## Fontes consultadas para o padrão de mercado

Resumo do que as pesquisas encontraram (fontes de fornecedores; tratar como visão deles):
- **Salas de dados (VDR):** permissões por pasta e arquivo, marca d'água dinâmica por sessão, NDA obrigatório, registro só-acrescenta de acessos e certificação SOC 2 Type II são descritos como mínimo em [Papermark — virtual data room features](https://www.papermark.com/blog/virtual-data-room-features.md) e [Digify — comparação de provedores](https://digify.com/top-10-best-virtual-data-room-providers-2025-comparison.html). Datasite tem preço sob consulta; Intralinks é descrito como caro.
- **Valuation de startup:** a [Equidam combina cinco métodos](https://www.equidam.com/five-startup-valuation-methods/) (Scorecard, Checklist, dois DCF e Método VC) e pondera pelo estágio da empresa; o argumento dela é que "quem escolhe os métodos escolhe a resposta" — que é exatamente o motivo de **fixar pesos antes de calcular** no seu Modo Cego.
- **Painéis abertos de métricas:** o [Baremetrics Open Startups](https://venturebeat.com/ai/watch-what-open-startups-earn-in-real-time-with-this-handy-tool) mostra receita recorrente, clientes e fluxo ao vivo para empresas que escolhem se abrir — referência para a ideia de transparência; no seu caso, **atrás de login**.
- **Calculadora da Buyco:** não consegui abri-la (o ambiente não resolve o endereço). Pela imprensa ([Folha Vitória](https://www.folhavitoria.com.br/geral/buyco-oferece-ferramenta-gratuita-para-valuation-de-pmes)), é uma ferramenta gratuita de valuation para PMEs com mais de 100 mil avaliações — **uma calculadora de captação de contatos por múltiplos**, que é o oposto do que você quer construir (dados reais, evidência, rastro). **Se quiser que eu estude a tela dela, mande prints.**
