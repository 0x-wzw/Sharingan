---
name: harness-starter-stack
approval_source: agent
description: Use when standing up an agentic harness from zero.
version: 1.0.0
author: Hermes Agent (cangjie distillation of @Kiiiiira777's harness post, Nov 2026)
license: MIT
platforms: [linux, macos, windows]
read_scope: profile
source: "X post 2118759929947328571 (@Kiiiiira777, 2026-11-06): Dario Amodei clip + 14 free repos — all repos verified live via gh api"
metadata:
  hermes:
    tags: [agents, harness, onboarding, ladder, starter-stack, cangjie]
    related_skills: [tetherline-doctrine, cangjie, multi-agent-patterns]
---

# Harness Starter Stack — from zero to running the AI

## When to Use

- Someone (or a new team) asks how to go beyond "using AI" to running agents on real work
- Building a first agentic harness and needs a vetted, free, layer-by-layer repo map
- Advising on career-proofing against entry-level white-collar automation

## The core argument

Dario Amodei (Anthropic CEO), asked what a new high-school graduate should do: entry-level law, finance and consulting get hit first — his own prediction is 50% of entry-level white-collar jobs disrupted in 1–5 years, faster than past disruptions allowed adaptation.[1] The post's ladder is the actionable form:

**Prompts → Agents → Harness → Loops → The One Running the AI**

Using AI won't be enough — "AI won't replace you. Someone with a harness will." The durable position is being the operator of the loop, not the prompt writer.[1]

## The repo map, by rung (all free, all verified live 2026-11-07)

**Rung 1 — Skills & plugins (use AI inside real work):**
- `anthropics/skills` (⭐188.8k) — Excel/Word/PowerPoint/PDF agent skills [4]
- `anthropics/knowledge-work-plugins` (⭐35.1k) — plugins for legal, finance, sales, HR, data work [2]
- `anthropics/claude-cookbooks` (⭐54.4k) — effective patterns as recipes [13]

**Rung 2 — Domain agents (one job, done end-to-end):**
- `anthropics/financial-services` (⭐41.1k) — analyst agents: models, memos, research notes [3]
- `virattt/dexter` (⭐27.8k) — autonomous deep financial research [5]
- `assafelovic/gpt-researcher` (⭐30.5k) — deep research on any data, any LLM [6]
- `stanford-oval/storm` (⭐31.8k) — full-length cited research reports [7]

**Rung 3 — The harness (the ladder's point):**
- `langchain-ai/deepagents` (⭐31.1k) — batteries-included agent harness [9]
- `anthropics/claude-agent-sdk-python` (⭐8.5k) — the SDK for building your own [10]
- `humanlayer/12-factor-agents` (⭐27k) — the principles that make agents production-grade [8]

**Rung 4 — Loops & memory (run unattended):**
- `snarktank/ralph` (⭐22.1k) — autonomous loop that runs until the PRD is complete [12]
- `thedotmack/claude-mem` (⭐114.5k) — persistent context across sessions; captures, compresses, re-injects [11]
- `microsoft/playwright-mcp` (⭐39.3k) — browser control — the agent's hands and eyes [13]

**Rung 5 — Learn the field:**
- `microsoft/ai-agents-for-beginners` (⭐79.1k) — 18 lessons [14]

## Build order

1. Pick the rung matching today's work; install ONE repo from it — do not stack all 14.
2. Rung 1→2 in days, rung 3 in weeks, rung 4 only after outputs are verifiable.
3. A harness without verification is a slop factory — pair any loop with checks before it runs unattended (see `tetherline-doctrine` for the trust ladder once one loop works).

## Anti-patterns

- Bookmarking the list instead of shipping one rung (the post has 14.4k bookmarks; the operators are the ones who install)
- Starting at rung 4 — autonomous loops over unverifiable work just burn tokens
- Paying for tools at rung 1–2 — everything on this map is free; spend money only when a verified loop earns it

## Sources (verified 2026-11-07)

- [1] X post: x.com/Kiiiiira777/status/2118759929947328571 (2026-11-06, 731k views, 14.4k bookmarks) — Amodei clip + repo list
- [2]–[14] github.com/anthropics/knowledge-work-plugins, /financial-services, /skills, virattt/dexter, assafelovic/gpt-researcher, stanford-oval/storm, humanlayer/12-factor-agents, langchain-ai/deepagents, anthropics/claude-agent-sdk-python, thedotmack/claude-mem, snarktank/ralph, microsoft/playwright-mcp, anthropics/claude-cookbooks, microsoft/ai-agents-for-beginners — existence, descriptions and star counts verified live via `gh api repos/<repo>`
