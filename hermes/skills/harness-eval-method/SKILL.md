---
name: harness-eval-method
approval_source: agent
description: Use when comparing agent harnesses with honest eval design.
version: 1.0.0
author: Hermes Agent
license: MIT
read_scope: profile
source: "garrytan/g-harness-evals repo @ edacaa8 + tweet 2121463161069228382, distilled 2026-11-13"
metadata:
  hermes:
    tags: [evals, harness, benchmarking, agents, cost, methodology]
    related_skills: [harness-starter-stack, tetherline-doctrine, venture-machine]
---

# Harness-eval method — compare agent harnesses honestly

## When to Use

- Choosing between agent harnesses (Claude Code, Codex, OpenClaw, Hermes, Pi, QM…) for a model
- Designing an eval for ANY agent stack, or judging a benchmark claim someone else published
- Deciding where rules and skills must live so agents actually follow them

## The method (Garry Tan's harness-evals)

1. **Fix model + tasks; swap only the harness.** One variable. Never compare a harness to
   another model's home harness (Claude Code ↔ Codex never compare — each belongs to its
   model maker). Home harness = the baseline every swap is measured against.
2. **Primary metric: cost per SOLVED task** — not per try, not pass rate. On easy task sets
   pass rates indistinguishably cluster; cost separates (one harness ran ~2x per solved task,
   ~81% of the gap from context re-sent/cache writes every request). Rank by paired cost
   ratios over commonly-scored tasks; ranks may share or skip.
3. **Preregister the tests.** "Behind" / "within 15 points" / "can't tell" come from tests
   fixed BEFORE the run (Holm-corrected for multiple comparisons) — never from subtracting
   the table's shown numbers. Give 95% ranges on every cell; label gaps the ranges could hide.
4. **Keep a public corrections ledger.** Metering gotchas surface later (reservation charges
   on non-streamed replies, an egress sidecar cutting slow calls while still billing) —
   republish corrected costs with exact bounds, say which ranks move and which do not, and
   state "largest possible correction" when the true effect is bounded, not known.
5. **Anti-contamination: reaching the answer key scores a FAIL.** Web tools touching the
   key invalidated tries even where the work passed.
6. **Outage + refusal rules with amendments.** Rerun-and-replace (spend stays in cost),
   and report how fragile each verdict is: which conclusions survive dropping refused tries
   or reclassifying outage tries — several flipped under amendment alone.
7. **Label "dev" vs confirmed.** Public tasks the builders could see = dev results, hold
   only for pinned versions; confirmation requires hidden tasks. Disclose every conflict of
   interest on the same page as the numbers (own projects, investors, affiliations).
8. **Mine failures with a frozen codebook.** 1,998 labelled failures, 20 root-cause classes,
   labeler agreement κ 0.936, then rank causes. Top cause (44%): the agent answered from the
   wrong conversation — the answer lived in another channel its session never saw.

## What the evals found (use it on your own stack)

- **Rules followed only when seen on EVERY turn**: per-turn hook or system prompt → 30/30;
   with no rule 4-6/30. A rule said once fades by later turns (2-4/10).
- **An unmentioned skill can sit unread** — the model saw its name every request and opened
   it 0 times in 30 turns on two harnesses. **Name the skill in the prompt if you rely on
   it** (naming fixed it: 30/30). Corroborates poteto-swarm-method's verification rules.
- **Reading skill text ≠ following it**: told to run 4 workflow skills, the model read the
   text every time and followed 0 of 46 sessions' steps, at ~2x cost per try.
- **A shared brain unscoped returns records the asker may not read** (+9.5 pts retrieval
   failures; scoped brains 0-0.5%). Bind access scope in the brain/installer — never in the
   prompt — before tuning anything else.
- **Give agents cross-conversation memory and test it** before prompt-tuning; it is the
   single biggest failure class in multi-user settings.

## Pitfalls

- Pass-rate comparison on tasks too easy for the model is noise — separate on cost or
  harden the tasks (14 of 20 tasks scored identically in every cell in one run).
- One model per harness means a "harness difference" is harness-and-model; say so.
- Times measured with concurrent tries on one machine are contaminated — note the concurrency.
- Re-sent context dominates cost: check what a harness re-sends per request before picking.
- A cost correction can be bounded-but-unknown; publish the bound, not a guess.

## Sources

- Repo: github.com/garrytan/g-harness-evals (MIT, 372 commits; inspected @ edacaa8, 2026-11-13):
  README rankings + findings/{rule-placement, harness-cost, where-agents-fail, 2026-11-02-opus-gstack-steps-not-followed}
- Announcement: x.com/garrytan/status/2121463161069228382
- Corroborations: poteto-swarm-method (skills unread unless named); venture-machine (cost-per-
  solved-task = the same economics as the venture funnel's cost-per-evidence scorecard)
