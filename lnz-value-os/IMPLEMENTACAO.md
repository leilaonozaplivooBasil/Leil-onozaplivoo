# LNZ VALUE OS — Diário da implementação

> Aprovação do CEO para construir: **17/10/2026** ("aprovado, pode fazer"). Regra mantida: **nada muda no app, no banco do app, nos sites ou na produção** sem ordem explícita; o portal nasce separado.

## Onde cada peça mora

| Peça | Onde | Estado em 17/10/2026 |
|---|---|---|
| Código do portal | este repositório, pasta `valueos/` (Next.js 16) | **no ar**: login por e-mail + código (só com convite), termo de sigilo com hash/IP, registro de acesso. Telas: Visão geral (capa com os 4 tempos), **Memorando revisado** (12 capítulos do Gamma com cada número etiquetado), Números com prova, DRE, **Parceiros de compra**, **Riscos**, **Valuation** (metodologia, sem número), **Governança e time**, **Metas e simulação** (plano × realizado + simulador por alavancas), **Data room** (mapa do que existe/falta), Cargas, prova por métrica |
| Hospedagem | Vercel, equipe "Leilaapp's projects", projeto **`lnz-value-os`** (`prj_2ZMGeV9phCiKDkKpeWC6yfzJDb3D`), funções em São Paulo (gru1) | **publicado a partir do GitHub** (branch `claude/zen-albattani-uql6jy`, produção); proteção de login da Vercel desligada (o login é do portal) |
| Endereço do portal | **`investidor.leilaonozap.net`** | **no ar** — CNAME criado pelo CEO na IONOS em 17/10 (`investidor` → `cname.vercel-dns.com`), reconhecido pela Vercel |
| Banco do portal | Supabase, organização "Leilao Nozap 4.0" (plano Pro), projeto **`lnz-value-os`** em São Paulo | **usando o projeto já existente e vazio `leilaonozaplivooBasil's Project` (`hmldusqewfckxgzldqga`, Ohio)** — a criação de projeto novo trava numa tela de custo; tabelas com prefixo `vos_`; migrações em `valueos/supabase/migrations/`. Mudar para um projeto próprio em São Paulo depois é só reaplicar as migrações. |
| Banco do app (leitura) | Supabase `leilonozap` (`gezvviyegtxytnwjkrjv`) | intocado; as visões de leitura entram como arquivo de migração, aplicadas só com ordem |
| Vitrines públicas | Gamma: memorando → `investmentmemorandumleilaonozap.com`; valuation → `valuationleilaonozap.com` | intocadas; o memorando tem **alterações não publicadas** (última publicação há ~2 meses); o valuation foi republicado em 17/10 |

## Carga inicial (17/10/2026)

- **30 métricas** no dicionário (`vos_metricas`), 6 famílias.
- **57 evidências** com hash encadeado e **57 valores** (ago–16/out/2026), de duas cargas: consultas somente-leitura no app e extratos/contratos enviados pelo CEO.
- Etiquetas: a maioria `VERIFIED`; despesas e aportes como `MANAGEMENT_DATA`; nenhum `FORECAST` ainda; **nenhum número de valuation**.

## Conteúdo dos sites dentro do portal (17/10/2026, à noite)

- Os dois sites do Gamma foram lidos na origem e viraram as páginas `memorando`, `valuation`, `governanca`, `roadmap` do portal. **Regra:** narrativa da administração mantida; todo número ganhou etiqueta; o que a auditoria (Anexo A) marcou REMOVE saiu (Livoo, TikTok Shop, "99%", PHIZ, "valuation conservador", "retorno elevado", comparação com apostas); o que marcou VERIFY/RECALCULATE aparece com o valor medido ao lado do declarado.
- **Nota de revisão** em cada capítulo (o que mudou em relação ao site público) aparece **só para BOARD/ADMIN** (`NotaRevisao`); o investidor vê o conteúdo revisado com etiquetas.
- Páginas `riscos` e `valuation` têm uma seção extra só para o conselho (riscos legais/origem de recursos; números que já circulam).
- Nomes da diretoria vêm do site público; parceiros de compra e comprador do 1% continuam como A, B e iniciais.
- Componentes em `valueos/src/components/ui.tsx` (Etiqueta, Numero, Secao, Cartao, Aviso, Barras, Tabela, NotaRevisao, Legenda) e navegação em `nav.tsx`. Papel do usuário em `lib/papel.ts`; valores das métricas em `lib/metricas.ts`.

## Identidade visual dos sites dentro do portal (17/10/2026, noite)

- **Pedido do CEO:** o portal com a cara do memorando e do site de valuation (Gamma), só que mais profissional, com os dados de hoje. Fonte do desenho: os dois PDFs enviados (60 páginas do memorando + página do valuation) e a leitura dos documentos no Gamma.
- **Identidade:** fundo preto, verde da marca `#00B86B`, etiqueta de capítulo verde-menta, **Poppins** nos títulos e **Roboto** no texto (as mesmas fontes do PDF), barra superior com a logo do app. Tokens em `valueos/src/app/globals.css`; peças visuais em `valueos/src/components/marca.tsx` (Capitulo, Cartao, CartaoNumerado, LinhaDoTempo, Trajetoria, Setas, GraficoBarras, Ciclo, NumeroGrande, Hoje).
- **Imagens:** 25 artes tiradas dos próprios PDFs (foto do fundador, capa, mapas, abertura de cada capítulo, logo com transparência, logos do ecossistema) em `valueos/public/m/`, comprimidas (≈ 5 MB no total).
- **Memorando (`/app/memorando`):** refeito na ordem do original — carta do fundador na íntegra, trajetória, conquistas, convergência, linha do tempo (com jun/ago/set/out de 2026 acrescentados), resumo executivo, os 12 capítulos, 12 barreiras, capítulo 9 com **R$ 25.000.000 em destaque e selo de referência do fundador**, ciclo virtuoso e mensagem final (botões: reunião por WhatsApp e data room). Números trocados pelos do sistema, com etiqueta e link para a prova.
- **Valuation (`/app/valuation`):** capa no estilo do site de valuation; **“O que vale R$ 25.000.000”** com cada ativo ao lado do número de hoje; **painel vivo** (no lugar da planilha) com ago/set/out linha a linha; mercado, momento, ecossistema, roadmap; e a metodologia v1.0, a ponte e os comparáveis.
- **Início e login** no mesmo padrão. **Conferência visual** por fotos de tela (1280 px, 1024 px e celular 390 px), sem rolagem lateral e sem texto abaixo de 12 px; prévia local em `/previa/<página>` (só em modo de desenvolvimento, com dados de arquivo).
- **Remuneração paga aos parceiros no painel** (set R$ 1.600; out R$ 15.000) está escrita no código da página: virar métrica própria na próxima carga.

## Próximos passos (ordem)

1. ~~Login, convite, termo, acesso~~ — feito.
2. ~~Esquema do banco do portal~~ — feito (0001, 0002).
3. ~~Carga das 30 métricas com prova~~ — feito (carga manual pela sessão; automatizar na Fase 2).
4. ~~Tela "clique para provar" e tela de Cargas~~ — feito.
5. ~~Conteúdo dos dois sites dentro do portal, com etiquetas~~ — feito (17/10). Falta: Fase 2 completa (modelo por alavancas com custo por venda, cenários salvos, XLSX) — hoje há um simulador simples em "Metas e simulação".
6. Visões de leitura sobre o app (arquivo, aplicado só com ordem) e rotina mensal de carga.
7. Botão no app e botão "Área do investidor" nos sites (com aprovação do texto).

## Pendências do CEO

- ~~Supabase → URL Configuration e template do Magic Link~~ — feito pelo CEO em 17/10 (login testado de ponta a ponta).
- ~~E-mail pelo remetente da empresa (Brevo)~~ — **feito pelo CEO em 17/10 à noite:** Supabase Auth com SMTP personalizado (`smtp-relay.brevo.com:587`, remetente `relacionamento@leilaonozap.com`, nome "Leilão NoZap"), usando a chave SMTP `supabase-portal` criada no Brevo (sem expiração fixa). Limite sobe para 30 e-mails/hora. **Alerta:** chave SMTP do Brevo **expira após 90 dias sem uso** — se o portal ficar 3 meses sem ninguém pedir código, gerar outra chave no Brevo e colar de novo no Supabase. A chave de API do app (`BREVO_API_KEY`) é outra coisa e não foi tocada.
- **Assunto do e-mail de código:** trocar `Your Magic Link` por "Seu código de acesso · Leilão NoZap" (Supabase → Authentication → Emails → Modelos → Magic link or OTP → Subject).
- Decidir o que fazer com as alterações não publicadas do memorando no Gamma.
- (Opcional) criar um projeto Supabase próprio em São Paulo e me avisar para migrar.
