---
name: parallel-venture-validation
approval_source: agent
description: Use when triaging many venture ideas with parallel agents.
version: 1.1.0
author: Hermes Agent (cangjie distillation of Paul Cheek / MIT Sloan clip via @alvinfoo)
license: MIT
platforms: [linux, macos, windows]
read_scope: profile
source: "X post 2119367655278723559 (@alvinfoo, 2026-11-08) — Paul Cheek (MIT Sloan) clip, transcript extracted from video + MIT Sloan writeups"
metadata:
  author: "Zehan Teoh <zehan@example.com>"
  layer: application
  stack-source: vault
  hermes:
    tags: [entrepreneurship, validation, parallel-agents, ventures, mit-sloan, cangjie]
    related_skills: [harness-starter-stack, tetherline-doctrine, grounded-citations]
---

# Parallel Venture Validation — test many, keep the winners

## When to Use

- A batch of business/venture ideas needs triage before committing real time or money
- Building an agent workflow that evaluates N candidates simultaneously instead of serially
- Advising founders or students on the post-AI validation cycle (idea → evidence → commitment)

## The method (Paul Cheek, MIT Sloan — "Building a Startup at AI Agent Speed")

**Core shift:** the competitive advantage is no longer having ideas — an agent can
surface 130 of them. The advantage is **how fast you can validate, experiment and
execute**. Serial evaluation (one idea per week) is dead; parallel evaluation is
the new default.[1]

**The pipeline, in order:**

1. **Fan out generation.** Point one agent at idea discovery with no artificial
   cap — Cheek's run produced **130 ideas** in an "Idea Hub". Quantity first;
   taste filters later.
2. **Human narrows to a shortlist (≈6).** The human checks boxes — this is the
   taste gate. Do not let the generator agent also pick the winners (same-context
   bias); the human reads categories and picks the batch.
3. **Spawn one bounded agent per candidate, all simultaneously.** Each venture
   gets the same structured plan: in the clip, a **24-step plan + 10 tactics**
   per venture (market segmentation → beachhead market → personas → pricing →
   TAM). Identical structure across candidates = comparable evidence.
4. **Let them run unattended** — "operate while we sleep". Live per-venture
   counters (steps done, tactics, cost, elapsed time) are the visible evidence
   stream; the human checks in, not sits in.
5. **Commit only after evidence.** Agents run cheap experiments across the batch;
   the human then picks the single venture to "pour our heart and soul into".
   Commitment is the LAST step, gated on evidence — never on enthusiasm.

**The rule in one line:** test six in the time one used to take, and let cost
and step counters — not opinion — decide the shortlist's survivor.

## Design rules for the agent harness

- **Identical plan template per candidate** — comparable outputs are the whole
  point; free-form runs produce incomparable evidence.
- **Bounded jobs**: fixed step count (e.g. 24), fixed tactic budget (e.g. 10),
  fixed cost cap — a venture node that cannot finish is evidence too.
- **Per-venture cost counters from step one** ($0.00 ticking up) — spend is a
  validation metric, not just a bill.
- **The human picks the shortlist AND the final winner**; agents do the work
  between those two gates.
- **Parallel by default**: six agents building simultaneously beats one agent
  doing six rounds — wall-clock time is the constraint that changed.
- **Enforce the DECISIVE steps, not the literal count** — bots consolidate a
  24-step spec into 17-19 top-level entries with part headers; comparability
  survives as long as kill criteria, the cheapest-falsifiable-experiment, and
  the concierge-MVP steps align across candidates.

## Operating it as a standing pipeline (proven pattern)
- Run it on the Hermes kanban dispatcher: dedicated builder profile whose
  AGENTS.md constitution carries the output contract, the template skeleton,
  and the bounds; board `--default-workdir` points at a durable ventures dir;
  a daily cron driver harvests, feeds ideation, and enforces the ceiling.
  Full commands and the fake-door measurement stack: `references/deployment.md`.
- **Triage scorecard axes**: home-market founder fit, cost-to-evidence,
  demand-evidence quality, moat, regulatory friction (/25). The comparable
  template makes scoring arithmetic, not narrative.
- **Graduate by evidence-density**: pick the venture whose first experiment
  closes the MOST open assumptions (regulatory + demand + channel) in one pass.
- **$0 validation move**: formal regulator scope-inquiry letters resolve the
  regulatory assumption for free — draft-then-confirm, never send autonomously.
- **Fan-out with parallel lane agents**: uniform JSON via `output_schema`; put
  the EXCLUSION LIST verbatim in every child's context — children see only the
  context field, never the parent conversation.

## Anti-patterns

- **Serial triage** — evaluating ideas one at a time "for weeks"; that's the
  pre-agent habit the method exists to kill.
- **Committing before evidence** — pouring effort into idea #1 because it was
  first, not because it survived the batch test.
- **Trusting the headline over the source** — this tweet's caption says
  "tested six ventures overnight"; the clip itself only shows the parallel
  plan-building phase, with $0 spend and 0-of-24 steps. The results framing is
  the uploader's, not demonstrated. Demand the evidence artifact before
  repeating a claim.[1]
- **Letting the generator grade itself** — generation and selection are
  separate gates (see `harness-starter-stack` rung 3 for the harness pattern).

## Sources (verified 2026-11-09)

- [1] X post + 41s video: x.com/alvinfoo/status/2119367655278723559 (2026-11-08,
  5,024 views) — Paul Cheek, Senior Lecturer, MIT Sloan; transcript extracted
  frame-by-frame: "Idea Hub 130", six ventures checked, 24-step plans, "operate
  while we sleep", "pour our heart and soul into" the survivor
- [2] MIT Sloan "Ideas Made to Matter" — AI-driven enterprises piece (Jul 2026)
- [3] MIT Sloan — "No One Works Here" excerpt: replace human bottlenecks with
  AI for efficiency (Aug 2026)
