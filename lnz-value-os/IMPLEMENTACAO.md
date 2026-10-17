# LNZ VALUE OS — Diário da implementação

> Aprovação do CEO para construir: **17/10/2026** ("aprovado, pode fazer"). Regra mantida: **nada muda no app, no banco do app, nos sites ou na produção** sem ordem explícita; o portal nasce separado.

## Onde cada peça mora

| Peça | Onde | Estado em 17/10/2026 |
|---|---|---|
| Código do portal | este repositório, pasta `valueos/` (Next.js 16) | **no ar**: login por e-mail + código (só com convite), termo de sigilo com hash/IP, registro de acesso, visão geral com etiquetas e qualidade do dado |
| Hospedagem | Vercel, equipe "Leilaapp's projects", projeto **`lnz-value-os`** (`prj_2ZMGeV9phCiKDkKpeWC6yfzJDb3D`), funções em São Paulo (gru1) | **publicado a partir do GitHub** (branch `claude/zen-albattani-uql6jy`, produção); proteção de login da Vercel desligada (o login é do portal) |
| Endereço do portal | **`investidor.leilaonozap.net`** | **no ar** — CNAME criado pelo CEO na IONOS em 17/10 (`investidor` → `cname.vercel-dns.com`), reconhecido pela Vercel |
| Banco do portal | Supabase, organização "Leilao Nozap 4.0" (plano Pro), projeto **`lnz-value-os`** em São Paulo | **usando o projeto já existente e vazio `leilaonozaplivooBasil's Project` (`hmldusqewfckxgzldqga`, Ohio)** — a criação de projeto novo trava numa tela de custo; tabelas com prefixo `vos_`; migrações em `valueos/supabase/migrations/`. Mudar para um projeto próprio em São Paulo depois é só reaplicar as migrações. |
| Banco do app (leitura) | Supabase `leilonozap` (`gezvviyegtxytnwjkrjv`) | intocado; as visões de leitura entram como arquivo de migração, aplicadas só com ordem |
| Vitrines públicas | Gamma: memorando → `investmentmemorandumleilaonozap.com`; valuation → `valuationleilaonozap.com` | intocadas; o memorando tem **alterações não publicadas** (última publicação há ~2 meses); o valuation foi republicado em 17/10 |

## Carga inicial (17/10/2026)

- **30 métricas** no dicionário (`vos_metricas`), 6 famílias.
- **57 evidências** com hash encadeado e **57 valores** (ago–16/out/2026), de duas cargas: consultas somente-leitura no app e extratos/contratos enviados pelo CEO.
- Etiquetas: a maioria `VERIFIED`; despesas e aportes como `MANAGEMENT_DATA`; nenhum `FORECAST` ainda; **nenhum número de valuation**.

## Próximos passos (ordem)

1. ~~Login, convite, termo, acesso~~ — feito.
2. ~~Esquema do banco do portal~~ — feito (0001, 0002).
3. ~~Carga das 30 métricas com prova~~ — feito (carga manual pela sessão; automatizar na Fase 2).
4. Tela "clique para provar" (evidência por número) e tela de Cargas.
5. DRE/EBITDA ago–out e modelo por alavancas (Fase 2).
6. Visões de leitura sobre o app (arquivo, aplicado só com ordem) e rotina mensal de carga.
7. Botão no app e botão "Área do investidor" nos sites (com aprovação do texto).

## Pendências do CEO

- **Supabase → Authentication → URL Configuration:** Site URL `https://investidor.leilaonozap.net`; Redirect URLs `https://investidor.leilaonozap.net/**` e `https://lnz-value-os.vercel.app/**`.
- **Supabase → Authentication → Email Templates → Magic Link:** incluir `{{ .Token }}` (o código de 6 dígitos) no corpo do e-mail.
- Decidir o que fazer com as alterações não publicadas do memorando no Gamma.
- (Opcional) criar um projeto Supabase próprio em São Paulo e me avisar para migrar.
