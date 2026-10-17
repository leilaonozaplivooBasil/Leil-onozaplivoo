# LNZ VALUE OS — Diário da implementação

> Aprovação do CEO para construir: **17/10/2026** ("aprovado, pode fazer"). Regra mantida: **nada muda no app, no banco do app, nos sites ou na produção** sem ordem explícita; o portal nasce separado.

## Onde cada peça mora

| Peça | Onde | Estado em 17/10/2026 |
|---|---|---|
| Código do portal | este repositório, pasta `valueos/` (Next.js) | esqueleto gerado e enviado; sem telas, sem banco |
| Hospedagem | Vercel, equipe "Leilaapp's projects", projeto **`lnz-value-os`** (`prj_2ZMGeV9phCiKDkKpeWC6yfzJDb3D`), funções em São Paulo (gru1) | criado; **sem ligação com o GitHub ainda** (ligar em Settings → Git, ou eu publico por upload) |
| Endereço do portal | **`investidor.leilaonozap.net`** | adicionado ao projeto e verificado; **DNS pendente**: o `leilaonozap.net` é gerido na **IONOS** (servidores `ui-dns`), precisa de **1 registro CNAME `investidor` → `cname.vercel-dns.com`** |
| Banco do portal | Supabase, organização "Leilao Nozap 4.0" (plano Pro), projeto **`lnz-value-os`** em São Paulo | **não criado**: a criação pela conexão pede confirmação de custo numa tela que não chega aqui (2 tentativas, nada criado); **o CEO cria no painel** |
| Banco do app (leitura) | Supabase `leilonozap` (`gezvviyegtxytnwjkrjv`) | intocado; as visões de leitura entram como arquivo de migração, aplicadas só com ordem |
| Vitrines públicas | Gamma: memorando → `investmentmemorandumleilaonozap.com`; valuation → `valuationleilaonozap.com` | intocadas; o memorando tem **alterações não publicadas** (última publicação há ~2 meses); o valuation foi republicado em 17/10 |

## Próximos passos (ordem)

1. Login (e-mail + código), convite, termo de sigilo, registro de acesso — `valueos/`.
2. Esquema do banco do portal (registry, valores, evidência, snapshots, cargas) — migrações em `valueos/supabase/`.
3. Visões de leitura sobre o app — arquivo em `valueos/supabase/app-readonly/` (não aplicado).
4. As 30 métricas com prova + DRE/EBITDA ago–out.
5. Botão no app e botão "Área do investidor" nos sites (com aprovação do texto).

## Pendências do CEO

- Criar o projeto Supabase `lnz-value-os` (São Paulo).
- Registro CNAME na IONOS: `investidor.leilaonozap.net` → `cname.vercel-dns.com`.
- Ligar o repositório ao projeto Vercel (ou autorizar publicação por upload).
- Decidir o que fazer com as alterações não publicadas do memorando no Gamma.
