# DataPovo — urna de pesquisa

Urna simples no formato da urna eletrônica (teclado, BRANCO / CORRIGE / CONFIRMA) para pesquisas de opinião.
Sem instalação: abra `index.html` no navegador. Funciona em celular e tablet.

| Arquivo | Para quê |
|---|---|
| `index.html` | A urna (quem vota) |
| `resultado.html` | Placar público, atualiza sozinho |
| `config.js` | **O único arquivo que você edita**: pergunta, opções, servidor |
| `dados.js` | Grava e lê os votos |
| `schema.sql` | Banco (Supabase) — só necessário para juntar votos de várias pessoas |

## Como usar

1. Edite a pergunta e as opções em `config.js`.
2. Abra `index.html`. Sem servidor configurado ele roda em **modo teste**: os votos ficam só no aparelho.
3. Para juntar os votos de todo mundo: crie um projeto no Supabase, rode `schema.sql`, e preencha
   `SUPABASE_URL` e `SUPABASE_KEY` (a chave pública/anon) em `config.js`. Publique a pasta em qualquer hospedagem estática.
4. Tablet num evento, várias pessoas em sequência: abra `index.html?evento`.

## O que ele faz pela privacidade de quem vota

- Não existe registro de voto individual: o banco guarda só **um contador por opção** (sem horário, sem ordem, sem nome).
- O WhatsApp, quando pedido, vai para **outra tabela**, sem ligação com o voto, e só com consentimento marcado.
- A tela de WhatsApp **só aparece** se `RESPONSAVEL` estiver preenchido em `config.js` — a pessoa precisa saber com quem está deixando o número.
- A lista de opções aparece em ordem sorteada a cada abertura.
- Sem cookies, sem analytics, sem fontes externas, sem referrer.

## O que ele NÃO garante

- **Voto único:** o bloqueio é só por aparelho. Quem limpar o navegador ou chamar o servidor direto pode votar de novo. Voto único de verdade exige identificar a pessoa, o que briga com anonimato.
- **Anonimato total:** a hospedagem e o Supabase podem manter registro técnico das conexões (como IP). O app não grava isso, mas não controla o provedor.
- **Descentralização tipo Bitcoin:** este app usa um banco central. Veja "Descentralizado" abaixo.

## Descentralizado

Para não depender de nenhum servidor ou dono, o caminho é votar em contrato inteligente (blockchain) com a página em IPFS.
Em troca: cada voto é público e fica para sempre, quem vota precisa de carteira e taxa, uma pessoa pode criar várias carteiras,
e não dá para pedir WhatsApp. Anonimato com voto único em blockchain existe (provas de conhecimento zero), mas exige um cadastro
de pessoas verificadas. Não está neste projeto.
