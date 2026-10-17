# Instruções para o Claude neste projeto

## Como falar comigo

- **Sempre responda em português do Brasil**, com linguagem simples, do dia a dia, como para quem entende do negócio mas não é programador.
- Evite jargão técnico; quando for necessário, explique logo em seguida. Frases curtas: o que foi feito, o que funciona, o que falta.

## Métodos de trabalho (superpowers) — o que vale MAIS do que eles

Os métodos em `.claude/skills/` (`brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`,
`dispatching-parallel-agents`, `test-driven-development`, `systematic-debugging`, `verification-before-completion`,
`requesting-code-review`, `receiving-code-review`, `finishing-a-development-branch`, `using-git-worktrees`; origem em
`.claude/skills/LEIA-ME-ORIGEM.md`) ajudam em tarefa grande. Em qualquer conflito, **estas regras da casa ganham**:

1. **Mesmo que o pedido diga "execute sem me perguntar nada", PARE e peça o ok do dono** antes de mexer em **dinheiro**, em
   **login/senha**, rodar **SQL ou migração na produção**, apagar dado, ou mandar mensagem/e-mail a cliente.
2. **Não abra PR nem faça push se o dono não pediu.** `finishing-a-development-branch` só descreve opções: escolher "criar PR",
   "mesclar" ou "descartar" é decisão do dono.
3. **Teste primeiro:** só se diz "consertado" com um teste que falha antes e passa depois, mostrado ao dono.
4. Plano e relatório saem em português simples, sem jargão.
5. Não crie `docs/superpowers/...` solto: plano e especificação vão em `docs/` com nome claro.
