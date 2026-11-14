---
name: venture-machine
approval_source: agent
description: Use when operating the venture validation funnel machine.
version: 1.0.0
author: Hermes Agent
license: MIT
read_scope: profile
source: "session-built 2026-11-09 — venture machine operation (kanban funnel, driver, bots, triage, Sahati experiment)"
metadata:
  hermes:
    tags: [ventures, kanban, funnel, automation, cron, entrepreneurship]
    related_skills: [parallel-venture-validation, poteto-swarm-method, venture-machine]
---

# Venture Machine — operating the validation funnel

## When to Use

- Running, extending, or repairing the ventures kanban funnel (ideation → shortlist → parallel build → triage → graduation → experiment)
- Creating venture build tasks, scoring plans, or wiring a new experiment's landing page
- Debugging the driver, dispatcher, or venture-builder bots

## Where things live

- **Board**: `ventures` (Hermes kanban) — `hermes kanban boards list`; dispatcher spawns the
  `venture-builder` profile per task (ticks 60s, max-retries 2 default)
- **Profile**: `~/.hermes/profiles/venture-builder/` — AGENTS.md is the constitution (output
  contract: durable write to `/home/ubuntu/ventures/plans/<task-id>-<slug>.md` + attach;
  24 steps/10 tactics; $0 spend; [assumption] tagging; kill criterion)
- **Driver**: `~/ventures/ventures_kanban_driver.py` (cron 05:20 daily) — harvest done-task
  attachments → plans/, create daily ideation task, enforce ≤6 concurrent, rewrite `_board.md`
- **Ideation pool**: `~/ventures/ideation/` (deep-scan 48 + fan-out 50 + daily files)
- **Plans**: `~/ventures/plans/` — one file per task; mirrored conceptually to the funnel
- **Graduation state**: triage scorecard /25 (home-fit, cost-to-evidence, evidence-quality,
  moat, reg-friction); graduation = taste gate 2, reserved to Zehan
- **Experiments**: `~/ventures/sahati/` — letters (draft-then-confirm) + landing page
  (`sahati-teoh.pages.dev`) + lead API (`sahati-api.zehan-teoh.workers.dev`, KV SAHATI_LEADS,
  admin token `~/.hermes/.secrets/sahati_admin_token`)

## Procedure (recurring loop)

1. **Daily (automated)**: driver runs 05:20 — harvest, ideation task, ceiling, heartbeat.
   Touch nothing; read `~/ventures/_board.md` for state.
2. **Weekly report (cron `fd49f5bc0f1b`, Mon 08:30, deliver origin)**: canonical script at
   `~/.hermes/scripts/venture_weekly_report.py` (dev copy `~/ventures/`) — collects board
   state, new plans, ideation delta, experiment metrics (GET sahati-api /stats with custom
   UA) → `~/.hermes/cron/output/venture-weekly/`; the agent cron formats + delivers to origin.
   Edit the prompt via cronjob_manage only after reading the full prompt from jobs.json.
3. **Shortlist (human)**: from ideation/deep-scan files → create tasks:
   `hermes kanban create "Build plan: X" --assignee venture-builder --body "category: … region: … idea: … kill: …"`
4. **Triage (agent, mechanical)**: extract Step-13 kill + Step-20 experiment + costs from each
   plan; score /25 (home-fit, cost-to-evidence, evidence-quality, moat, reg-friction).
5. **Graduate (human)**: pick winner → wire the plan's Step 19-22 as real moves
   (regulator letters draft-then-confirm; landing page via pages.dev + KV worker pattern).

## Pitfalls (learned in operation)

- **`hermes kanban list --json` is on stdout; gateway warnings go to stderr** — parse stdout
  only, else `[default]` in the dashboard warning breaks JSON indexing.
- **Scratch workspaces are ephemeral** — the worker must write durable output to the
  absolute plans path AND attach; do not rely on workspace files.
- **Set wrangler secrets AFTER first deploy and verify with `wrangler secret list`** —
  `npx wrangler secret put X --stdin <<< val` silently no-ops; use `cat file | npx wrangler
  secret put X` and confirm the list output.
- **Drive-by flag: `human gates stay human`** — never auto-create build tasks from ideation
  (generator must not grade itself); never auto-send regulator letters (draft-then-confirm).
- **The engine regresses upstream** — before syncing vendor code down, diff local fixes
  (same lesson as shunshi branch-table regression).
- **Kill-criterion thresholds are [assumption] heuristics** — the experiment stage tests
  them; never present them as validated.

## Related

- `parallel-venture-validation` — the method being automated
- `poteto-swarm-method` — trust-ladder + swarm-ceiling rules
- Vault: `Knowledge/20-Reports/2026-11-09-venture-process-funnel.md` (full process + ledger)
