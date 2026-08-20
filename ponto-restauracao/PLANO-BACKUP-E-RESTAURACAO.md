# 🛟 Backup e ponto de restauração — antes de mexer no estoque

> **Nada foi alterado no sistema.** Este documento é o procedimento, e o que está na
> pasta `codigo-antes/` é a fotografia do código de hoje.
>
> Subordinado a `docs/VERDADE.md` do projeto Leilonozap.

---

## A regra que não pode ser esquecida

> ### Voltar o código NÃO desfaz mudança de dado.
>
> Se você reverter o deploy, o `catalog_active` que foi desligado continua desligado.
> A classificação que foi zerada continua zerada.

Por isso são **dois backups independentes**, e o segundo é o difícil.

| | O que protege | Como volta | Dificuldade |
|---|---|---|---|
| **Trilha 1 — Código** | os arquivos, o deploy | Vercel Instant Rollback | fácil, ~1 min |
| **Trilha 2 — Dados** | `products`, `store_inventory` | restauração dirigida por retrato | exige preparo |

---

## Situação de partida (medida em 20/08/2026)

| Item | Estado |
|---|---|
| Commit em produção | `8d4dddc684b4905ee7be12c370f068c95353f58a` |
| Data do commit | 20/08/2026 09:16 (-03) |
| Branch | `main` |
| Tags no repositório | **nenhuma** |
| Banco de produção | Supabase `gezvviyegtxytnwjkrjv` (sa-east-1) |
| Ambiente de homologação | **não existe** — um único banco |
| CI automático | **não existe** (`.github/workflows` ausente) |

### 🔴 Armadilha: preview do Vercel escreve em produção

Não existe segundo banco. Pior: `src/api/supabaseClient.js:8` traz a URL de produção
**fixa no código**, como valor padrão. Então um deploy de preview — aquele link que o
Vercel gera para cada Pull Request — vai falar com o **banco de produção**.

**Testar num preview não é teste. É produção com outra roupa.**
O teste seguro é com um produto-cobaia designado, descrito na seção 5.

---

## 1. Trilha 1 — Código

### 1.1 Marcar o ponto de retorno

```bash
git fetch origin
git tag -a restauracao/estoque-2026-08-21 8d4dddc6 \
  -m "Estado estavel antes das correcoes de estoque (baixa/vitrine/classificacao)"
git push origin restauracao/estoque-2026-08-21
```

A partir daí, voltar o código é sempre:

```bash
git checkout -b reverter/estoque restauracao/estoque-2026-08-21
```

### 1.2 Anotar o deploy atual do Vercel

No painel do Vercel, projeto do Leilão NoZap → **Deployments**. Anote aqui o ID do
deploy que está em produção **agora**:

```
Deploy em producao antes da mudanca: ______________________
```

Voltar = achar esse deploy na lista → **⋯ → Promote to Production**. Leva menos de um
minuto e não depende de build novo.

### 1.3 Um Pull Request por etapa

Não juntar as correções num PR só. Cada uma tem risco diferente e origem diferente:

| PR | O que muda | Risco |
|---|---|---|
| 1 | baixa manual desliga a vitrine (`catalog_active`) | baixo |
| 2 | campo de quantidade aceitar zero | baixo |
| 3 | venda baixar também a classificação | médio — caminho de venda |
| 4 | busca da Gestão de Estoque ir ao banco | médio — muda leitura |
| 5 | conferência de estoque no checkout | médio — caminho de pagamento |

Assim, se der problema, você reverte **um** PR — não a semana inteira.

### 1.4 Não existe CI — o portão é manual

Antes de cada merge, na sua máquina:

```bash
npm run lint
npm run build
```

Se qualquer um falhar, não sobe.

---

## 2. Trilha 2 — Dados (a que realmente importa)

Fazer **antes de qualquer escrita**, na mesma janela em que for mexer.

### 2.1 Tabela-espelho dentro do banco (restauração mais rápida)

No SQL Editor do Supabase:

```sql
CREATE TABLE bkp_products_20260821          AS SELECT * FROM public.products;
CREATE TABLE bkp_store_inventory_20260821   AS SELECT * FROM public.store_inventory;

-- conferir que copiou tudo
SELECT (SELECT count(*) FROM public.products)        AS produtos_agora,
       (SELECT count(*) FROM bkp_products_20260821)  AS produtos_backup,
       (SELECT count(*) FROM public.store_inventory) AS loja_agora,
       (SELECT count(*) FROM bkp_store_inventory_20260821) AS loja_backup;
```

Os dois pares têm que bater. **Se não bater, pare** e não siga para a mudança.

É instantâneo, não custa nada, e é o caminho mais rápido de volta.

### 2.2 Cópia fora do Supabase

A tabela-espelho protege contra erro na mudança. Ela **não** protege contra perder o
projeto inteiro. Então baixe também um arquivo, e guarde fora do Supabase:

```bash
curl -s "https://gezvviyegtxytnwjkrjv.supabase.co/rest/v1/products?select=*" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Accept: text/csv" > products-antes-20260821.csv

curl -s "https://gezvviyegtxytnwjkrjv.supabase.co/rest/v1/store_inventory?select=*" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Accept: text/csv" > store_inventory-antes-20260821.csv
```

> ⚠️ O PostgREST corta em 1000 linhas por padrão. Confira se o CSV tem as ~3.500+ linhas
> esperadas. Se vier com exatamente 1000, pagine com `Range: 0-999`, `1000-1999`… ou
> exporte pelo SQL Editor com `COPY (SELECT * FROM public.products) TO STDOUT WITH CSV HEADER;`

### 2.3 Point-in-Time Recovery — verificar se existe

No painel do Supabase → **Database → Backups**. Confirme qual é o caso de vocês:

- **Tem PITR:** anote o horário exato em UTC antes de começar. É a rede de segurança mais forte.
- **Só backup diário:** anote a hora do último backup — você perde o que aconteceu depois dele.
- **Nada:** os itens 2.1 e 2.2 **são** o seu backup. Não pule nenhum.

```
Modalidade de backup do plano: ______________________
Horario UTC antes de comecar:  ______________________
```

---

## 3. O retrato — o que torna a volta segura

Aqui está o ponto central do que você pediu: **voltar sem causar problema novo.**

### Por que um restore cego é perigoso

Se você restaurar a tabela inteira do backup, vai ressuscitar estoque de produtos que
foram **vendidos de verdade** depois do backup. Você conserta um problema e cria outro,
maior — produto vendido voltando a ter saldo e voltando à vitrine.

**Nunca faça isto:**

```sql
-- ☠️ NUNCA. Isso desfaz vendas legítimas junto.
UPDATE public.products p SET quantity = b.quantity
  FROM bkp_products_20260821 b WHERE p.id = b.id;
```

### A regra da restauração dirigida

> Restaure **só as colunas que você mexeu**, e **só nas linhas que o script tocou**.
> `quantity` só volta se foi você quem mexeu nela — nunca em lote.

Para isso, todo script retroativo tem que gravar o **retrato** (estado anterior, linha a
linha) antes de escrever. Vocês já fazem exatamente isso — `commissionReset.js:66` monta
um `retrato` com o `saldo_anterior` de cada conta, e o resultado virou o arquivo
`docs/retrato-comissao-antes-limpeza-2026-07-26.json`.

**Mesma prática aqui.** Cada correção de estoque gera:

`docs/retrato-estoque-antes-<assunto>-20260821.json`

Com, por produto: `id`, `descricao`, e o valor **anterior** de cada campo tocado
(`catalog_active`, `qty_perfeito`, `qty_bom`, `qty_oficina`, `qty_ruim`).

### E o padrão preview → executar

Também já existe no projeto e deve ser seguido. Todo script novo nasce em modo simulação:

```js
if (body.mode !== 'executar' || body.confirm !== 'PALAVRA') {
  return res.status(200).json({ ok: true, modo: 'preview', afetados: n, retrato });
}
```

Autenticação por `DIAG_KEY`, como em `commissionReset.js:50`.

**Fluxo obrigatório:** roda em preview → você lê os números e aprova → só então
`{ key, mode: 'executar', confirm: 'PALAVRA' }`.

Nenhum script retroativo roda direto. Nenhum.

---

## 4. Como voltar, na prática

### Caso A — deu ruim no código (tela quebrou, erro no deploy)

1. Vercel → deploy anotado em 1.2 → **Promote to Production**
2. Confirme a loja e a Gestão de Estoque abrindo
3. Só depois investigue

Tempo: ~1 minuto. Não mexe em dado.

### Caso B — o dado saiu errado (produtos indevidamente alterados)

Use o retrato do lote, não o backup inteiro:

```sql
-- exemplo: desfazer o catalog_active de UM lote de correcao
UPDATE public.products p
   SET catalog_active = b.catalog_active
  FROM bkp_products_20260821 b
 WHERE p.id = b.id
   AND p.id IN ( /* ids do retrato daquele lote */ );
```

Confira **antes** de executar, com o mesmo filtro:

```sql
SELECT p.id, p.description, p.catalog_active AS agora, b.catalog_active AS voltaria
  FROM public.products p JOIN bkp_products_20260821 b ON b.id = p.id
 WHERE p.id IN ( /* ids do retrato */ );
```

### Caso C — perdeu o controle (não sabe o que mudou)

1. Pare tudo. Não rode mais nenhum script.
2. Se tem PITR: restaure para o horário anotado em 2.3.
3. Se não tem: a tabela-espelho de 2.1 é a base — mas a restauração tem que ser dirigida,
   comparando linha a linha o que mudou desde o backup e separando o que foi venda real.

O Caso C é o que a gente está trabalhando para nunca acontecer. É por isso que existem
o retrato e o preview.

---

## 5. Teste antes de confiar

### 5.1 Produto-cobaia

Escolha **um** produto de baixo valor e sem movimento. Anote:

```
id do produto:        ______________________
descricao:            ______________________
quantity antes:       ____   catalog_active antes: ____
qty_perfeito antes:   ____   qty_bom antes:        ____
```

Rode a mudança só nele. Confira na loja. Só depois libere para o resto.

### 5.2 Ensaio de restauração — não pule

> **Backup que nunca foi testado não é backup.**

Antes de rodar qualquer correção em lote, faça o ensaio completo com o produto-cobaia:
altere → confirme que mudou → **restaure pelo retrato** → confirme que voltou ao valor
anotado em 5.1.

Se o ensaio funcionar, o procedimento é confiável. Se não funcionar, você descobriu
com um produto, e não com três mil.

---

## 6. Ordem de execução

```
[ ] 1. Tag no git (1.1)
[ ] 2. Anotar deploy do Vercel (1.2)
[ ] 3. Tabelas-espelho no Supabase (2.1) + conferir contagem
[ ] 4. CSV fora do Supabase (2.2) + conferir numero de linhas
[ ] 5. Verificar modalidade de backup do plano (2.3)
[ ] 6. Escolher e anotar o produto-cobaia (5.1)
[ ] 7. Ensaio de alteracao + restauracao no cobaia (5.2)
[ ] 8. So entao: primeiro PR
```

Os passos 1 a 7 não alteram nada em produção — são só preparação e uma cobaia.
A primeira alteração de verdade é o passo 8.

---

## 7. O que está guardado nesta pasta

| Arquivo | O que é |
|---|---|
| `codigo-antes/` | conteúdo exato dos 7 arquivos que serão tocados, hoje |
| `SHA256SUMS.txt` | impressão digital de cada um — prova de que é o mesmo conteúdo |

Serve para comparar depois: se houver dúvida sobre o que mudou num arquivo, é só
conferir contra esta cópia.

**Não substitui a tag do git** (item 1.1) — a tag é o ponto de retorno oficial, com
histórico. Esta pasta é a conferência rápida.
