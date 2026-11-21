---
name: reward-routing-by-verifiability
description: 'Use when designing RL rewards over heterogeneous tasks; not when all tasks share one reward type.

  '
version: 1.0.0
license: MIT
metadata:
  author: Cangjie Distillation <agent@example.com>
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.wemm-video.reward-routing-by-verifiability
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.wemm-video
  cangjie.source-title: 'WeMM-Video: Pushing the Frontiers of Open-Source Omni-Modal Video Understanding'
  layer: craft
  stack-source: repo:0x-wzw/Sharingan
  hermes:
    tags:
    - RL
    - rewards
    - routing
    related_skills:
    - wemm-video-router
approval_source: agent
read_scope: profile
source: Sharingan RIA-TV++ distillation of WeMM-Video (arXiv:2611.26409), 2026-11-21; Tier-1 PASS 8/8
---
## R — Reading (source)

"we combine rule-based rewards for deterministic tasks with rubric-based and teacher-consistency rewards for open-ended tasks. A dynamic reward router assigns task-specific rewards, while instruct and thinking modes are jointly optimized through stochastic sampling." (paper p.5 §4.2)

## I — Interpretation

A single reward cannot serve deterministic and open-ended tasks: exact rules are brittle for open answers, teacher/rubric judgments noisy for objective ones. Route each task to a reward type by verifiability — rule for deterministic, rubric plus teacher-consistency for open-ended — and sample instruct and thinking modes together. Treat reward selection as a routing decision driven by a task attribute, not a global hyperparameter.

## A1 — Application Example

Source case (paper p.5): specialist RL filters out already-solved samples, assigns reward types by task nature, extends to longer video contexts. Router logic, weights and rubric construction are not disclosed.

## A2 — Future Trigger

Use when designing rewards for RL over mixed tasks, or when one metric hurts open-ended performance. Signals: 'reward design', 'rule vs rubric', 'verifiable tasks', 'RL on mixed tasks'. Distinct from anti-repetition-loop and failure-mode-ordered-post-training.

## E — Execution

1. Label tasks deterministic or open-ended — completion: every task labeled. 2. Bind rewards by label — completion: task→reward mapping. 3. Filter already-solved tasks — completion: remaining set with difficulty evidence. 4. Sample both modes jointly — completion: both in training trace. 5. Check metrics per reward class — completion: no class masks another's regression.

## B — Boundary

Not when all tasks share one reward type or no reliable verifier/teacher exists. Do not invent router logic or weights, and do not claim reasoning gains causally from routing alone.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
