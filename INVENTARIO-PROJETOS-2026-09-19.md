# Inventário dos projetos — Base44 e GitHub

Levantamento feito em 19/09/2026. Somente leitura: nenhum projeto foi alterado.

## Resposta curta

- **Base44 (conta conectada nesta sessão): 0 apps.** A conta Base44 ligada aqui não
  enxerga nenhum app. Pedi diretamente pelo ID do Leilão NoZap
  (`68d536db3c26ff51f79c4137`, que está gravado em `base44/.app.jsonc` do código) e a
  resposta foi "App not found". Ou seja: o app existe, mas pertence a **outra conta ou
  outro workspace** do Base44, não à conta que foi conectada aqui.
- **GitHub: 11 repositórios**, todos acessíveis e clonados nesta sessão (o 11º, Super APP Vale do Recreio, foi criado em 19/09 e trazido no mesmo dia). O código
  completo do app Base44 (telas, entidades, funções) já está no GitHub. Nada foi
  perdido.

## Os 11 repositórios

| # | Repositório | O que é | Veio do Base44? | Último commit | Tamanho |
|---|---|---|---|---|---|
| 1 | `Leilonozap` (público) | **Sistema em produção** do Leilão NoZap (leilaonozap.net). React + Vite, Capacitor (Android/iOS), Vercel, Supabase. Tem CI e migrations versionadas. | Sim — nasceu no Base44 (app "Leilão NoZap"). Em 21/08/2026 o plugin do Base44 foi removido do `vite.config.js`; hoje roda sem o builder. Ainda carrega 64 entidades e 246 funções na pasta `base44/`. | 19/09/2026 (#407) | 2.445 arquivos, 144 telas |
| 2 | `Leil-onozaplivoo` (público, este repo) | Diagnóstico do estoque (planilha de 26/05/2026, processo atual, ponto de restauração). Só documentação e dados. | Não (analisa o app, não é o app) | 21/08/2026 | 16 arquivos |
| 3 | `leilaonozap-frontend` (privado) | Tentativa de separar o Leilão NoZap em dois repositórios: só as telas. | Sim — cópia do export Base44 (`package.json` ainda se chama `base44-app`) | 27/07/2026 | 606 arquivos |
| 4 | `leilaonozap-backend` (privado) | A outra metade da separação: 85 endpoints Vercel, 193 funções Base44, migrations Supabase. | Sim — mesma origem (`base44/.app.jsonc` = 68d536db…) | 27/07/2026 | 339 arquivos |
| 5 | `Leil-o-Nozap-Final` (privado) | **Fotografia antiga** do Leilão NoZap, do jeito que o Base44 exportou. Ficou parada. | Sim — export direto do Base44 | 15/06/2026 | 824 arquivos, 118 telas |
| 6 | `Leilaapp-5.0` (privado) | Reescrita do zero ("v4.0") para rodar em leilaapp.com **sem Base44**: Supabase + Hetzner. Ficou na Fase 0/1 (7 telas). | Não — é a migração *para fora* do Base44 | 05/05/2026 | 304 arquivos |
| 7 | `AGA-Digital` (privado) | Projeto Next.js + Supabase de credenciamento (formulário blocos A–F). | Não | 14/06/2026 | 137 arquivos |
| 8 | `f3x-vox` (privado) | Projeto Next.js pequeno com seletor de IAs. | Não | 10/06/2026 | 72 arquivos |
| 9 | `Isabela-Dias` (privado) | Site institucional da Dra. Isabela Dias (HTML estático) + landing para Google Ads. Painel admin e app Capacitor "em construção". | Não | 06/06/2026 | 72 arquivos |
| 10 | `Painel-de-Controle-Admin-` (privado) | **Vazio.** Repositório criado, nenhum commit. | — | — | 0 arquivos |
| 11 | `Super_APP_Vale_Do_Recreio` (privado) | Super app do ecossistema **TTT Corporate / Vale do Recreio**: pilares (X-EOS, Top Tech Digital, Top College), rede social, Human Token, HumanBank, marketplace, metaverso, painel executivo. Nome no Base44: **"Vale Conecta"**. 30 telas, 21 entidades, 2 funções. **Desvinculado do Base44 em 19/09/2026**: roda em Vercel (`vale-conecta-beta.vercel.app`) + Supabase (projeto `rmhoaxbkvakqssifyoky`, sa-east-1). Dados antigos ainda no Base44. | Era — export do Base44, app ID `69934f1fbcc24e80ad99a2bb`; hoje independente | 19/09/2026 | 190 arquivos |

## O que isso significa

1. **Existem dois apps Base44 de verdade.** O "Leilão NoZap" (ID `68d536db3c26ff51f79c4137`),
   que aparece em quatro cópias (repositórios 1, 3, 4 e 5: o 1 é o vivo, o 5 o mais antigo,
   3 e 4 o mesmo código partido ao meio). E o "Vale Conecta" (ID `69934f1fbcc24e80ad99a2bb`),
   repositório 11, desvinculado do Base44 em 19/09/2026 (código, login, banco e
   funções próprios). Só os dados e as imagens antigas continuam lá.
2. **O Base44 não é mais a casa do projeto.** O código do repositório 1 já roda
   direto no Vercel + Supabase. O banco de produção é o Supabase
   `gezvviyegtxytnwjkrjv`. O Base44 ficou como histórico.
3. **A conta Base44 conectada nesta sessão não é a dona de nenhum dos dois apps.** Testei os
   dois IDs pela API e a resposta foi "App not found" para ambos. Para eu conseguir
   ver e mexer no app pelo Base44, é preciso reconectar o Base44 com o e-mail que
   abre o "Leilão NoZap" no site base44.com, ou me passar o ID do workspace onde
   ele mora.

## O emoji de cada aplicativo

Definido em 19/09/2026, depois de levantar o costume do Leilão NoZap (100% dos últimos
50 commits começam com emoji, mas sempre do **assunto**, nunca do aplicativo).

| Aplicativo | Emoji | Repositório |
|---|---|---|
| Leilão NoZap | 🔨 | `Leilonozap` (e `Leilaapp-5.0`, mesma marca) |
| Vale Conecta | 🏞️ | `Super_APP_Vale_Do_Recreio` |
| AGA Digital | 🌉 | `AGA-Digital` |
| Dra. Isabela Dias | ✨ | `Isabela-Dias` |
| VOX GEO | 🎙️ | `f3x-vox` |
| Estoque Leilão NoZap | 📦 | `Leil-onozaplivoo` (este) |

Como escrever o título da PR, o commit e o nome do chat:

```
🔨 Leilão NoZap — 🏷️ O selo "NOVO - Com Garantia" sai de trás dos botões
🏞️ Vale Conecta — 🧱 O app sai do Base44 e roda em Vercel + Supabase
```

O aplicativo vem na frente porque a Vercel corta o texto na lista de implantações: o
nome precisa caber no comecinho. O emoji do assunto continua depois, como já era.

**Cuidado:** a DIR-76.1 do Leilão NoZap ("está muito aparecendo emoji") e o "zero emoji
no super admin" valem para a **tela do aplicativo**, não para commit. São coisas
diferentes. O texto completo da regra está em `CLAUDE.md` do Vale Conecta.

O 🔨 não foi inventado: é o emoji que o próprio Leilão NoZap já usa para "Leilões" em
`docs/HANDOFF-SKILLS.md`.

## Onde os clones ficaram nesta sessão

```
/home/user/leilaonozaplivoobasil/leilonozap   (produção)
/home/user/leilaonozap-frontend
/home/user/leilaonozap-backend
/home/user/leil-o-nozap-final
/home/user/leilaapp-5.0
/home/user/aga-digital
/home/user/f3x-vox
/home/user/isabela-dias
/home/user/painel-de-controle-admin-           (vazio)
/home/user/super_app_vale_do_recreio           (Vale Conecta)
```

Clones rasos (`--depth 1`), somente leitura. A sessão é temporária: ao encerrar, eles
somem. Este arquivo é o que fica.
