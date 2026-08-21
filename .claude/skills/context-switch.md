# Skill: Context Switching Under Interruption

**When to use:** An unexpected demand arrives while focused on a multi-phase implementation. Pause, handle it, resume without losing reasoning or technical continuity.

---

## State 1: Pause Main Work

Before switching to the new demand, snapshot the main work:

1. **Document the current position**
   - What phase/file/function am I in?
   - What's the immediate next step?
   - Save this in a single sentence: "Paused at [location]. Next: [step]."

2. **Ensure git state is clean**
   - Commit any uncommitted changes with a message like: `Paused: [what was being worked on]`
   - If mid-experiment, stash with: `git stash save "context-switch: [what I was doing]"`
   - Result: `git status` shows clean working directory.

3. **Mark the current branch**
   - Note the branch name (e.g., `claude/inventory-bottleneck-analysis-umfduz`)
   - Note what remote work is waiting (any open PRs, pending CI, etc.)

4. **Write the pause state**
   - In this chat: "**PAUSED.** Working on [feature]. Next: [step]. On branch `[name]`."

---

## State 2: Handle the Interrupt

New demand arrives. Establish scope and execution path:

1. **Scope the demand**
   - What exactly is being asked?
   - How long will it take?
   - Does it block the main work or run parallel?

2. **Execute the demand**
   - Use a fresh mental context — don't mix it with main work reasoning.
   - Follow the same git discipline: commit before returning.

3. **Confirm completion**
   - Summarize: "Interrupt resolved. [What was done]."
   - Git state: clean, committed, on the work branch.

---

## State 3: Resume Main Work

Return to the paused work with full reasoning restored:

1. **Switch context back**
   - In this chat: "**RESUMING.** Was on [feature], at [position]."

2. **Re-anchor to the plan**
   - Read the plan file (or task list) that governs the main work.
   - Confirm: "Next step is [X]."

3. **Continue as if uninterrupted**
   - The pause/interrupt record is here in the chat; you don't lose it.
   - Main branch/PR/reasoning is intact in git and in the conversation history.

---

## Key Principles

- **Commits are state checkpoints.** Every switch point is marked by a commit (pause, interrupt end, resume).
- **Chat is the record.** This conversation thread shows where pauses happened and why.
- **No half-finished work.** Before pausing or interrupting, always finish or explicitly stash.
- **One task at a time.** Don't mix main work and interrupt reasoning in the same thought.

---

## Example Flow

```
USER: [Working on inventory bottleneck, Phase 1]
ME: [Implementing estoque_baixa_atomica function]

USER: "Before proceeding, we have a new demand in the app. 
       Tell me if you understand, and handle it."

ME: **PAUSED.** Working on Fase 1: atomic inventory deduction (baixar_estoque_central RPC).
    Next: Add CHECK constraint to products table.
    On branch `claude/inventory-bottleneck-analysis-umfduz`.

[Handle new demand: implement fix, commit]

ME: Interrupt resolved. [Summary of what was done and pushed].

[User confirmation or next new demand]

ME: **RESUMING.** Was on Fase 1 inventory bottleneck, at CHECK constraint step.
    Continuing with: [next action].
```

---

## For This Session

**Current main work:** Inventory bottleneck fix (Fase 0–4 per plan).
**Current branch:** `claude/inventory-bottleneck-analysis-umfduz`
**Pause trigger:** User requests context switch.
**Resume trigger:** User says "continue" or after interrupt is resolved and committed.

Use this skill every time the context needs to flip. It keeps the reasoning intact.
