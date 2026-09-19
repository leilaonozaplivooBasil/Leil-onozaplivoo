# Conexão Sexta (app "ConexÃ" / repositório `Conex_sa`) — o que veio do Base44 e o que falta para desligar

Levantamento feito em 19/09/2026, logo depois de o app ser conectado ao GitHub.
Somente leitura: nada foi alterado no app, no Base44 nem no repositório `Conex_sa`.

## Resposta curta

1. **A conexão funcionou.** O Base44 criou o repositório privado
   `leilaonozaplivooBasil/Conex_sa` às 18:33 com o código completo do app: 145 arquivos.
   Clonei, instalei as dependências e compilei aqui. O código está íntegro.
2. **O que veio pelo Git é só o CÓDIGO.** Os **dados** (eventos, confirmações de presença,
   palavras do dia, módulos de aprendizado, reflexões e a lista de usuários) **não vêm pelo
   Git**. Continuam no banco do Base44 e só saem de lá por exportação.
3. **Daqui eu não consigo exportar os dados.** A conta Base44 conectada nesta sessão não
   enxerga nenhum app (0 apps) e recusa o ID deste (`68e6d0880d7bcce09547f963`:
   "Unable to access this app"). A rede desta sessão também bloqueia `base44.app`.
   Para exportar, é preciso a conta que abre o app no site base44.com (seção "O que preciso de você").
4. **Desligar totalmente do Base44 é uma migração**, não um botão. O app usa o Base44 para
   sete coisas (banco, login, funções de servidor, a IA ConnectYou, geração de texto e imagem,
   arquivos e hospedagem). O plano está abaixo. É o mesmo caminho já feito no Leilão NoZap:
   Supabase + Vercel.
5. **Não desconecte o GitHub e não apague o app no Base44 antes de exportar os dados.**
   Enquanto a conexão existir, o que se envia para a branch `main` do `Conex_sa` entra no app do
   Base44, e o que se edita no Base44 volta para o GitHub. Isso é bom agora (nada se perde) e
   só deve ser desfeito no último passo.

---

## 1. O que chegou no Git (`Conex_sa`, branch `main`, commit `38119ac`)

| Parte | Quantidade | Onde |
|---|---|---|
| Telas | 10 + o layout | `src/pages/`, `src/Layout.jsx` |
| Componentes do app | 27 | `src/components/{admin,connectyou,events,home,invite,learning,reflection}` |
| Componentes de interface (shadcn/ui) | 49 | `src/components/ui/` |
| Entidades (modelos de dados) | 5 | `base44/entities/` |
| Funções de servidor (Deno) | 17 | `base44/functions/` |
| Agente de IA (ConnectYou) | 1 | `base44/agents/conexao_friday.jsonc` |
| Configuração | Vite, Tailwind, ESLint, `package.json` | raiz |

As telas: Home (palavra do dia), WeeklyInvite (convite da sexta + confirmação de presença),
Events, EventDetail, EventHistory, LearningModules, ModuleDetail, ReflectionJournal,
AdminDashboard, RecoveryPanel. Mais a página OAuthConsent, que é do editor do Base44.

As 5 entidades e seus campos estão em `base44/entities/*.jsonc`:
**Event** (título, data, hora, local, tema, descrição, imagem, status, fotos, resumo, conteúdo),
**Attendance** (evento, nome, telefone, e-mail, confirmado em, origem, chegou, chegou em),
**DailyWord** (data, palavra, mensagem, autor, imagem, enviada ao WhatsApp),
**LearningModule** (semana, título, subtítulo, imagem, badge, conteúdo, ordem),
**ReflectionEntry** (e-mail do usuário, data, conteúdo, prompt, evento, palavra).

### Compila?

Sim, mas só com uma variável ligada. Sete importações em seis arquivos usam o formato antigo do
SDK (`@/entities/Event`, `@/functions/setSelfAdminIfSuper`). Sem `BASE44_LEGACY_SDK_IMPORTS=true`
o build quebra na hora. Com a variável, compila em ~3 s e gera 1,1 MB em `dist/`.
O lint aponta 45 erros, todos de importação não usada, nada que afete o funcionamento.

Arquivos com importação antiga: `src/Layout.jsx`, `src/components/learning/EditModuleModal.jsx`,
`src/pages/EventDetail.jsx`, `src/pages/Events.jsx`, `src/pages/LearningModules.jsx`,
`src/pages/ModuleDetail.jsx`.

---

## 2. O que NÃO chegou (e continua no Base44)

| O que | Onde está hoje | Como sai de lá |
|---|---|---|
| **Registros** das 5 entidades | Banco do Base44 | Exportar com a conta dona (CSV pelo painel, ou eu, via MCP, se a conta for reconectada) |
| **Usuários** e senhas/logins | Base44 Auth | A lista de usuários exporta; as senhas não. Todo mundo faz login de novo no destino |
| **Segredos** (`BASE44_SERVICE_ROLE_KEY`, `BASE44_APP_ID`) | Painel do Base44 | Não precisam sair: o destino terá as suas próprias chaves |
| **ID do app** (`base44/.app.jsonc`) | Ignorado pelo `.gitignore` | Já sei o ID pela URL do logo: `68e6d0880d7bcce09547f963` |
| **Logo** (`LOGOCONEXSADEFINITIVA.png`) | `media.base44.com` (13 referências no código) | Baixar e hospedar no destino |
| **Motor da IA ConnectYou** (conversas, streaming, ferramentas) | Serviço de agentes do Base44 | Reescrever com uma API de IA (as instruções do agente já estão no repositório) |
| **URL publicada** e domínio | Base44 | Descobrir com a conta dona; apontar para o Vercel no final |

---

## 3. Os cordões: tudo que o código pede ao Base44

26 dos 145 arquivos falam com o Base44. Este é o mapa do que cada um usa e pelo que trocar.

| # | O que o Base44 faz hoje | Usado em | Substituto proposto |
|---|---|---|---|
| 1 | **Banco de dados** — `entities.Event/Attendance/DailyWord/LearningModule/ReflectionEntry` (list, filter, create, update, delete) | 14 arquivos | Supabase Postgres: 5 tabelas com os mesmos campos, políticas de acesso (RLS) |
| 2 | **Login** — `auth.me`, `auth.isAuthenticated`, `auth.redirectToLogin`, `auth.logout` | 11 arquivos | Supabase Auth (e-mail/senha ou Google) |
| 3 | **Funções de servidor** — `functions.invoke('closeEvent' \| 'createAnonymousConversation' \| 'fixDatesAndMoveConfirmations')` + `setSelfAdminIfSuper` | 3 arquivos | Rotas de API no Vercel (ou Edge Functions do Supabase, que também são Deno) |
| 4 | **Agente ConnectYou** — `agents.createConversation`, `addMessage`, `subscribeToConversation` | 3 componentes (`ConnectYouChat`, `AuthenticatedConnectYou`, `ReflectionJournal`) | Endpoint próprio que chama a API da Anthropic com as instruções de `conexao_friday.jsonc`; conversas gravadas no Supabase |
| 5 | **Geração de texto e imagem** — `integrations.Core.InvokeLLM` (2 lugares) e `GenerateImage` (1 lugar) | `AnonymousConnectYou`, `EditEventModal` | A mesma API de IA para texto; para a imagem do convite, uma API de imagem ou upload manual |
| 6 | **Arquivos** — `UploadFile` (exportado, não usado nas telas) e o logo em `media.base44.com` | 6 arquivos (logo) | Supabase Storage ou a pasta `public/` do próprio site |
| 7 | **Ferramentas do editor** — `@base44/vite-plugin`, `appLogs.logUserInApp`, `VisualEditAgent`, `NavigationTracker`, `OAuthConsent`, `app-params` | 6 arquivos | Remover. São do editor do Base44, não do app |

`SendEmail`, `SendSMS` e `ExtractDataFromUploadedFile` aparecem só como exportação em
`src/api/integrations.js`; nenhuma tela usa. Não precisam de substituto.

### As 17 funções de servidor: 6 vivas, 11 para arquivar

| Vivas (precisam migrar) | Para quê |
|---|---|
| `closeEvent` | Botão do admin que encerra o evento e conta presenças |
| `createAnonymousConversation` | Abre a conversa com a ConnectYou para quem não fez login |
| `fixDatesAndMoveConfirmations` | Botão de manutenção no painel admin |
| `setSelfAdminIfSuper` | Promove o super admin ao entrar |
| `inviteLanding` | Link do convite com prévia (imagem, título) no WhatsApp; redireciona para `/WeeklyInvite` |
| `dailyWordPreview` | O mesmo para a palavra do dia; redireciona para `/Home` |

As outras 11 (`analyzeAttendances`, `cleanupAndOrganize`, `fixAllEventsAndAttendances`,
`fixEventStatus`, `listAllEvents`, `organizeAllConfirmations`, `organizeEventsNow`,
`recoverAttendances`, `separateEvents`, `inviteFirstAdmin`, `generateStoryInvite`) são scripts
de conserto de dados de outubro e novembro de 2024, com datas fixas no código, ou não são chamadas
por nenhuma tela. Ficam no histórico do Git; não vão para o destino.

---

## 4. Dois problemas de segurança que já existem hoje (independem da migração)

1. **A senha do painel administrativo está escrita no código do site**
   (`src/components/admin/AdminLoginModal.jsx`). Qualquer pessoa que abra o site e olhe o
   código-fonte no navegador lê o e-mail e a senha. Não reproduzo a senha aqui porque este
   repositório é público.
2. **O "modo admin" é só uma marca no navegador.** O login acima grava
   `conexao_admin_authenticated = true` no `localStorage`; quem souber disso liga o modo admin
   sem senha nenhuma. O que segura de verdade são as permissões das entidades no Base44,
   se estiverem configuradas.

Na migração isso se resolve de graça: o admin passa a ser um usuário com papel `admin` no
Supabase Auth, e as políticas do banco (RLS) é que barram escrita de quem não é admin.
Recomendo trocar a senha no Base44 hoje mesmo, por precaução.

---

## 5. Plano de migração (mesmo caminho do Leilão NoZap)

| Fase | O que | Depende de |
|---|---|---|
| **0. Exportar os dados** | Registros das 5 entidades + lista de usuários, guardados no Git como CSV/JSON | **Da conta Base44 dona do app** (bloqueio atual) |
| **1. Infraestrutura** | Projeto Supabase novo (região `sa-east-1`, como os outros): 5 tabelas, RLS, bucket de arquivos, logo re-hospedado. Projeto Vercel ligado ao `Conex_sa` | Sua confirmação (o projeto Supabase pode gerar custo na organização "Leilao Nozap 4.0", que já tem 7 projetos) |
| **2. Código** | Tirar `@base44/sdk` e o plugin; cliente Supabase; reescrever as chamadas dos 26 arquivos; 6 funções viram rotas de API; remover as ferramentas do editor; corrigir as 7 importações antigas | Nada. Pode começar já, numa branch do `Conex_sa` |
| **3. ConnectYou** | Endpoint com a API da Anthropic usando as instruções de `conexao_friday.jsonc`; conversa anônima e autenticada; histórico no Supabase | Uma chave de API da Anthropic |
| **4. Dados e testes** | Importar o export da fase 0; testar convite, confirmação, palavra do dia, admin, ConnectYou | Fases 0 a 3 |
| **5. Virar a chave** | Apontar o domínio para o Vercel; só então desconectar o GitHub no Base44 e encerrar o app | Fase 4 aprovada |

O que **não** muda: as telas, o visual, os textos, os componentes, os modelos de dados.
A migração troca o encanamento, não a casa.

---

## 6. O que preciso de você

1. **Acesso aos dados.** Uma destas opções:
   - reconectar o Base44 nesta ferramenta com o e-mail que abre o "ConexÃ" no site base44.com
     (aí eu exporto tudo por aqui); ou
   - exportar no painel do Base44 (Dados → cada entidade → exportar) e me mandar os arquivos;
     e também a lista de usuários.
2. **Confirmar o destino**: Supabase (banco, login, arquivos) + Vercel (site e funções), como
   no Leilão NoZap. Se preferir outro, me diga antes da fase 1.
3. **Chave de API de IA** para a ConnectYou (Anthropic), e decidir se a geração de imagem do
   convite continua automática ou vira upload manual.
4. **Qual é a URL pública atual** do app, para eu planejar o domínio.

Enquanto isso, a fase 2 (código) não depende de nada e é onde eu começaria.

---

## 7. Onde estão as coisas nesta sessão

```
/home/user/conex_sa          clone do Conex_sa (main, 38119ac), dependências instaladas, dist/ compilado
/home/user/Leil-onozaplivoo  este repositório (documentação)
```

A sessão é temporária; o clone some ao encerrar. Este arquivo é o que fica.
Complementa o `INVENTARIO-PROJETOS-2026-09-19.md` da branch `claude/eager-pasteur-b3a1yp`,
que listou os 11 repositórios anteriores (o `Conex_sa` é o 12º).
