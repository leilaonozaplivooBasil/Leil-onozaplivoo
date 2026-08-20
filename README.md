# Diagnóstico do estoque — Leilão NoZap

Levantamento **somente leitura** feito em 20/08/2026. Nenhuma linha do sistema de
produção (`leilaonozaplivooBasil/Leilonozap`) foi alterada.

## Arquivos

| Arquivo | O que é |
|---|---|
| `estoque_snapshot_2026-05-26.csv` | A planilha do estoque — 3.543 produtos, 40 colunas |
| `PROCESSO-ESTOQUE-ATUAL.md` | Como funciona hoje a entrada e a saída de produtos |
| `converter_dump_para_csv.py` | Script que gerou o CSV a partir do dump SQL |

## ⚠️ Sobre a data do CSV

Este CSV **não é o estoque de hoje**. É o retrato de **26/05/2026**.

O estoque de verdade vive no banco Supabase de produção
(projeto `gezvviyegtxytnwjkrjv`). Este ambiente **não tem acesso a ele**: a política de
rede bloqueia o endereço `supabase.co` e não há credencial de serviço disponível aqui.

A única base de produtos versionada no repositório é
`scripts/import-sql/insert_products.sql` — o backup do Base44 de 26/05/2026, usado na
migração para o Supabase. Foi ele que virou este CSV, **sem nenhuma alteração de dado**:
mesmas colunas, mesmos valores.

### Para gerar o CSV com os dados de hoje

Com acesso ao banco, um destes caminhos:

```bash
# 1) via PostgREST (precisa da service role key)
curl -s "$SUPABASE_URL/rest/v1/products?select=*" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Accept: text/csv" > estoque_hoje.csv
```

```sql
-- 2) direto no SQL Editor do Supabase
COPY (SELECT * FROM public.products) TO STDOUT WITH CSV HEADER;
```

## Como o CSV foi gerado (fidelidade)

`converter_dump_para_csv.py` lê os 36 blocos `INSERT` do dump e separa os valores
respeitando aspas escapadas (`''`), JSON embutido e quebras de linha dentro dos textos.

Conferência: **3.543 linhas lidas, 0 falhas** — bate exatamente com o cabeçalho do dump
(`-- Product → products (3543 registros)`).

Única coluna deixada de fora: `raw_base44` — um blob JSON que só repete, em formato
antigo, o que já está nas outras 40 colunas.
