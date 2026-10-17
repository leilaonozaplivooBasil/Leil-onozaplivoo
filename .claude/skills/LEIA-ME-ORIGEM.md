# De onde veio este conjunto de métodos (copiado em 17/10/2026, a pedido do dono)

**superpowers** — github.com/obra/superpowers, **v7.0.0, commit bb92a77**, licença MIT (`_superpowers-origem/LICENSE-superpowers`).
É a **mesma cópia fixa e conferida** que entrou no projeto do app (`leilonozap`, PR #710): ver lá `.claude/skills/LEIA-ME-ORIGEM.md` para o detalhe.

- **12 métodos:** `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`,
  `test-driven-development`, `systematic-debugging`, `verification-before-completion`, `requesting-code-review`,
  `receiving-code-review`, `finishing-a-development-branch`, `using-git-worktrees` + a tabela de ferramentas em
  `using-superpowers/references/claude-code-tools.md`.
- **Cópia FIXA:** só muda por commit nosso (nada de atualizar sozinho pela internet).
- **Lido antes de entrar:** o gancho do plugin só injeta texto local; não há `curl`/`eval`/chamada de rede escondida nos métodos.
- **Ficou de fora de propósito:** o servidor visual do brainstorming (`scripts/` e `visual-companion.md`; carrega um logo do autor = telemetria),
  o método que abre chamado no GitHub do autor (`diagnosing-superpowers`), o texto que obriga o uso de método em tudo
  (`using-superpowers/SKILL.md` e o gancho) e o `writing-skills`.
- **Única edição de conteúdo:** o prefixo `superpowers:` dos nomes foi tirado e o `brainstorming/SKILL.md` ganhou uma NOTA DA CASA
  mandando ignorar a oferta do servidor visual.
- **Regras da casa que valem MAIS do que qualquer método daqui:** `CLAUDE.md`, seção "Métodos de trabalho (superpowers)".
- **Como usar:** `/brainstorming <o que você quer>`, depois `/writing-plans`, depois `/subagent-driven-development`.
- `context-switch.md` (já existia) continua como estava.
