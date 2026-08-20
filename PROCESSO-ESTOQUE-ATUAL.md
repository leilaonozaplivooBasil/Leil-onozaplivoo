# Como está HOJE o processo de entrada e saída do estoque

Levantamento feito em 20/08/2026 lendo o código de produção do repositório
`leilaonozaplivooBasil/Leilonozap`. **Nada foi alterado** — este documento e o CSV são
só leitura e retrato.

---

## 0. Onde o estoque mora

São **duas tabelas separadas**, e essa separação é a origem de boa parte da confusão:

| Tabela | O que é | Quem mexe |
|---|---|---|
| `products` | Estoque **central** da casa (Bangu, Oficina, Recreio) | Admin, PDV, importação de planilha |
| `store_inventory` | Estoque **próprio de cada lojista** da rede | Compra de estoque, consignado, PDV do lojista |

Em `store_inventory` cada linha tem uma `origem`:
- `comprado` — o lojista pagou, é dele;
- `consignado` — está com ele, mas a dívida (`divida_aberta`) continua em aberto.

---

## 1. ENTRADA (como produto entra)

São **seis portas de entrada** diferentes, e nenhuma delas gera documento de entrada.

### 1.1 Importação de planilha (Excel/CSV)
`src/components/catalog/PlanilhaImport.jsx` → `api/functions/bulkImportProducts.js`

- Aceita cabeçalhos em português: `Nome, Preço, Custo, De, Estoque, SKU, Imagem, Observação`.
- A coluna **Estoque** vira `quantity`. Se vier vazia, entra **1**.
- Cria sempre com `catalog_active: false` (`bulkImportProducts.js:70` — "NUNCA publica direto").

> ⚠️ **Divergência encontrada:** a tela manda `publish: true` e depois mostra
> *"X produto(s) publicados na loja!"*, mas o servidor **ignora esse parâmetro** e grava
> `catalog_active: false`. Ou seja: a tela diz que publicou, e não publicou. Alguém
> precisa ativar na mão depois.

### 1.2 Cadastro manual, um a um
`src/pages/ProductManagement.jsx` e `src/pages/CreateAuction.jsx`.
No CreateAuction (`:992`) o produto novo nasce com `quantity: 1` e `catalog_active: true`.

### 1.3 Lote recebido
`api/functions/loteRecebidoWrite.js` — registro do lote que chega.

### 1.4 Compra de estoque próprio pelo lojista
`api/_lib/supplySettle.js` → insere em `store_inventory` com `origem='comprado'` e
`custo_unitario`.

### 1.5 Consignado
`api/functions/manageConsignacao.js` → insere em `store_inventory` com
`origem='consignado'`, `divida_aberta` e `prazo_em`.

### 1.6 Ajuste manual do admin
`api/functions/manageStoreInventory.js` — ações `add | setQuantity | toggle | remove`.
Grava o número direto, sem histórico.

**Ponto comum a todas as entradas:** o número é **escrito por cima** do que estava lá.
Não existe nota de entrada, não existe linha de movimento, não existe "de quanto para
quanto". Se alguém digitar 500 em vez de 50, não há como descobrir depois.

---

## 2. SAÍDA (como produto sai)

Desde 08/08/2026 existe **uma função única** de baixa: `api/_lib/baixaEstoque.js`.
Isso foi um acerto — antes cada tela tinha a sua regra. A ordem de consumo é sempre:

```
1º  store_inventory  origem = 'comprado'    (é dele, já pagou)
2º  store_inventory  origem = 'consignado'  (é dele, com dívida aberta)
3º  products                                (estoque central da casa)
```

### Os canais de venda

| Canal | Arquivo | Quando o estoque baixa |
|---|---|---|
| Loja virtual online | `api/functions/createStoreOrder.js` | **só quando o pagamento confirma** (mpWebhook → `storeFulfill.js`) |
| PDV — PIX / cartão | `api/functions/createPdvOrder.js` | **só quando o pagamento confirma** |
| PDV — dinheiro / saldo | `api/functions/createPdvOrder.js` | na hora |
| Leilão / arremate | `finalizeAuctionCore.js` → `storeFulfill.js` | quando o vencedor paga |

---

## 3. POR QUE ESTÁ VENDENDO O QUE NÃO EXISTE

Seis mecanismos concretos, todos verificados no código:

### 3.1 Ninguém segura a peça entre o "comprar" e o "pagou" 🔴
`createStoreOrder.js:4` diz com todas as letras:
*"O estoque só é baixado e a comissão só é paga QUANDO o pagamento confirma."*

A conferência de estoque acontece no checkout, mas **nada reserva a peça**. Da última
unidade, dois (ou dez) compradores passam na mesma conferência, geram PIX, e **todos
pagam**. Só existe uma peça. É o caso clássico do PIX que fica 30 minutos aberto.

### 3.2 A baixa **nunca falha** — ela silencia 🔴
`baixaEstoque.js`, função `baixarCentral`:

```js
const novaQtd = Math.max(0, (Number(p.quantity) || 0) - qty);
```

Se tem 1 em estoque e vende 3, ele grava **0** e retorna `true` — sucesso.
As 2 peças que foram vendidas sem existir **somem sem aviso**. Em
`baixarItensDaVenda` o que sobra (`restante`) é simplesmente descartado.
Nenhum log, nenhum alerta, nenhuma pendência.

### 3.3 A vitrine mostra esgotado de propósito 🔴
`src/pages/Catalog.jsx:207`:

```js
// 🛒 Esgotados sempre por último (não some, mas não atrapalha quem quer comprar)
```

A consulta da vitrine filtra **só** `catalog_active: true` — **nunca** olha `quantity`.
O filtro "só em estoque" existe, mas é **opcional e o cliente é quem liga**. Quem não
liga, vê e compra peça zerada.

### 3.4 Produto é publicado sem olhar se tem peça 🔴
`CreateAuction.jsx:984` marca `catalog_active: true` num produto já existente **sem
conferir `quantity`**. Um produto zerado volta pra vitrine com um clique.
Só o `baixaEstoque` desliga a vitrine — e só quando ele mesmo leva a quantidade a zero.

### 3.5 O PDV da rede não confere estoque central 🔴
Em `createPdvOrder.js:95-107`: quando quem vende **é dono de loja**, confere
(`"Estoque insuficiente..."`). Quando é **vendedor da rede vendendo do estoque central**,
cai no `else` da linha 102 — que lê `p.quantity` na consulta e **nunca compara**.
Vende qualquer quantidade, de qualquer coisa, inclusive de item zerado.

### 3.6 Não existe livro-caixa do estoque 🔴
O **dinheiro** ganhou extrato em 18/08/2026 (`reserva_ledger`) justamente depois de uma
auditoria achar R$ 159,60 travados sem rastro. **O estoque não tem nada disso.**
Toda movimentação é `UPDATE` destrutivo. Quando a peça fantasma aparece, não há como
saber quando saiu, por qual venda, nem por qual caminho.

### 3.7 O `status` não é confiável como fonte de verdade
O campo declara 5 valores (`ESTOQUE`, `VENDIDO PIX`, `VENDIDO DINHEIRO`, `CONSERTO`,
`BRINDE VENDEDOR`), mas:
- `baixaEstoque.js` grava `'VENDIDO'` — que **não está na lista**;
- a base já tem `'VENDIDO CARTÃO CRÉDITO'` e `'VENDIDO BOLETO PARCELADO'`.

Quem filtrar por `status` para saber o que tem em casa vai errar.

---

## 4. O que já existe de remédio (e por que não resolve)

`api/functions/reconciliarEstoqueLoja.js` — endpoint de admin que varre a base,
acha `quantity <= 0 AND catalog_active = true` e desliga da vitrine.

É **vassoura, não é conserto**: roda **na mão**, depois do estrago, e não impede a
próxima venda fantasma. Entre uma varrida e outra o buraco continua aberto.

---

## 5. O que os números mostram

Contado sobre o retrato de 26/05/2026 (3.543 produtos):

| Achado | Número |
|---|---|
| Produtos ativos na vitrine (`catalog_active = true`) | **40** |
| **Desses, com `quantity <= 0` — vendável sem existir** | **13 (32,5%)** |
| Status `ESTOQUE` mas `quantity <= 0` (fantasma) | **171** |
| `qty_perfeito+bom+ruim+oficina` ≠ `quantity` | **84** |
| Status `VENDIDO*` mas ainda com `quantity > 0` | **4** |
| Status fora da lista declarada | **2** |

**Um terço da vitrine já estava vendendo o que não existia** — e isso num retrato de
três meses atrás, antes do volume atual.

Valor parado (status `ESTOQUE`, `quantity > 0`): **3.101 itens / 7.689 peças /
R$ 321.400,65 a custo**.

Depósitos: Bangu 3.135 · Recreio 6 · **sem depósito preenchido 131**.

---

## 6. Resumo em uma frase

> A entrada escreve número por cima sem deixar rastro; a saída nunca reclama quando
> falta; a vitrine mostra esgotado de propósito; e não existe extrato de estoque para
> conferir nada depois.
