---
name: venture-validation-machine
approval_source: agent
description: Use when running the end-to-end venture machine — ideation to parallel validation to unattended building to triage to graduation. Combines parallel-venture-validation (method), venture-machine (funnel ops), tetherline-doctrine (swarm engineering — supersedes poteto-swarm-method).
version: 1.0.0
author: Hermes Agent
license: MIT
read_scope: profile
source: "composed 2026-11-09 from parallel-venture-validation v1.1.0 + venture-machine v1.0.0 + poteto-swarm-method v1.0.0"
metadata:
  hermes:
    tags: [ventures, validation, swarm, kanban, funnel, automation, entrepreneurship]
    related_skills: [parallel-venture-validation, venture-machine, tetherline-doctrine, harness-starter-stack]
---

# Venture Validation & Building Machine — composed operating system

Umbrella skill fusing three layers. Load the sub-skill for depth; this one defines how they snap together and which rules override.

## The three layers

| Layer | Skill | Role |
|---|---|---|
| Method | `parallel-venture-validation` (Cheek/MIT Sloan) | WHY + the validation pipeline: fan-out 130 ideas → human shortlists ≈6 → one bounded agent per venture (24-step plan, 10 tactics, $0) → parallel unattended runs → commit on evidence only |
| Funnel ops | `venture-machine` | WHERE + the standing implementation: `ventures` board, venture-builder profile constitution, daily 05:20 driver, ideation pool, plans/, triage scorecard /25, weekly report cron `fd49f5bc0f1b`, Sahati experiment stack |
| Swarm engineering | `tetherline-doctrine` (Lauren Tan) | HOW to scale it: autonomy bounded by verifiability, trust ladder, verification skills, verification-model-as-judge, gardening, deterministic work in tools |

## The composed pipeline (one graph)

1. **Ideate (auto, daily)** — driver cron generates/feeds the ideation pool. Deterministic; touch nothing. *(ops)*
2. **Shortlist (HUMAN GATE 1 — taste)** — human picks ≈6 candidates from ideation/deep-scan files → `hermes kanban create "Build plan: X" --assignee venture-builder --body "category: … region: … idea: … kill: …"`. Generator must never grade itself. *(method)*
3. **Parallel build (auto, bounded)** — ≤6 concurrent venture-builder agents, identical plan template, fixed bounds, per-venture cost counters from step one, durable write to plans/ AND attach. Bounded jobs that fail are evidence. *(method + ops)*
4. **Verify before scoring (auto)** — every factual claim in a plan gets a machine-checkable signal before it counts: link resolves, API responds, repo builds. Unverifiable output caps that venture's autonomy and its score. **Use a different model as judge** where LLM judging is needed. *(swarm)*
5. **Triage (agent, mechanical)** — extract Step-13 kill + Step-20 experiment + costs → score /25 (home-fit, cost-to-evidence, evidence-quality, moat, reg-friction). Comparable template makes this arithmetic, not narrative. *(method + ops)*
6. **Graduate (HUMAN GATE 2 — Zehan only)** — pick the survivor by evidence-density: the venture whose first experiment closes the MOST open assumptions in one pass. Wire its Step 19–22 as real moves. *(method)*
7. **Experiment (auto-with-gates)** — regulator scope-inquiry letters draft-then-confirm (never auto-send); landing page via pages.dev + KV lead worker; fake-door metrics feed the weekly report. *(ops)*
8. **Garden (continuous)** — agent failures → environment fixes: repeated mistakes across agents become new skills, lint rules, or driver checks; count gardening as gardening in the weekly report. Sample landed plans; don't review every one. *(swarm)*

## Binding rules (composited; violations = stop)

1. **Human gates stay human** — shortlist (gate 1) and graduation (gate 2). No exceptions, no drive-bys.
2. **Autonomy is bounded by verifiability** — no verification signal, no autonomy escalation; cap the swarm, don't widen it.
3. **Trust ladder order: local → skills → verification skill → cloud agents → automerge** — never skip rungs. The venture machine is at "cloud agents" rung ONLY because plan-writing has a verifiable output contract (durable file + attach).
4. **Kill-criterion thresholds are [assumption] heuristics** — the experiment stage tests them; never present as validated.
5. **Draft-then-confirm** for any outbound real-world communication (regulator letters).
6. **$0 spend during validation** — spend counters are metrics, not budget approvals.
7. **Identical template per candidate** — comparability is the point; consolidate steps only if kill criteria, cheapest-falsifiable-experiment, and concierge-MVP steps stay aligned.
8. **Children see only their context field** — exclusion lists, dedupe baselines, category, region, kill criterion travel VERBATIM in every venture-builder brief.
9. **Diff local fixes before syncing vendor code down** — the engine regresses upstream.
10. **Durable output contract** — plans written to the absolute plans path AND attached; scratch workspaces are ephemeral.

## Operational pitfalls (from live operation — venture-machine)

- Parse only stdout from `hermes kanban list --json`; gateway warnings pollute stderr.
- `wrangler secret put X --stdin` silently no-ops — use `cat file | npx wrangler secret put X`, verify with `wrangler secret list`.
- Weekly report prompt edits: read the full prompt from jobs.json via cronjob_manage first.
- Board state reads from `~/ventures/_board.md`; don't touch the driver's cron lane.

## When to load which sub-skill

- Designing/repairing the funnel, driver, or builder constitution → `venture-machine`
- Questioning the validation method itself (batch size, gates, evidence standard) → `parallel-venture-validation`
- Scaling beyond ~6 concurrent, adding verifier agents, or automerge decisions → `tetherline-doctrine`
- Full process + ledger history: vault `Knowledge/20-Reports/2026-11-09-venture-process-funnel.md`

## Anti-patterns (any one = reject the plan)

- Serial triage of ideas
- Committing before evidence (enthusiasm-gated graduation)
- Generator grading its own output
- Swarm without a verification skill (human becomes the hidden test harness)
- Headline trusted over source artifact (the Cheek clip shows plan-building only, $0 / 0-of-24 steps — demand the artifact)
- One-off treatment of a mistake two+ agents repeated (that's an environment bug)
