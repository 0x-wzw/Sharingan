---
name: dimension-based-evaluation
description: 'Use when designing or reading a multi-benchmark comparison; not for a single-task sanity check.

  '
version: 1.0.0
license: MIT
metadata:
  author: Cangjie Distillation <agent@example.com>
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.wemm-video.dimension-based-evaluation
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.wemm-video
  cangjie.source-title: 'WeMM-Video: Pushing the Frontiers of Open-Source Omni-Modal Video Understanding'
  layer: craft
  stack-source: repo:0x-wzw/Sharingan
  hermes:
    tags:
    - evaluation
    - benchmarks
    - metrics
    related_skills:
    - wemm-video-router
approval_source: agent
read_scope: profile
source: Sharingan RIA-TV++ distillation of WeMM-Video (arXiv:2611.26409), 2026-11-21; Tier-1 PASS 8/8
---
## R — Reading (source)

"The evaluation is organized around five critical dimensions... incorporates 33 representative benchmarks... For existing models, we report official results where available and our own evaluations otherwise." (paper pp.6–7 §5.1, Table 1 footnotes)

## I — Interpretation

Benchmark comparison fails when metric conventions are mixed or vendor numbers are treated as locally reproduced. Fix dimensions first, select benchmarks per dimension, then apply each benchmark's footnoted metric convention (judge, subset order, lower-is-better). Mark every number as official-reported or locally reproduced, and report both inference modes for a flagship so reasoning gains are visible against non-thinking baselines. Every number carries its metric and provenance.

## A1 — Application Example

Source case (paper pp.6–13): 33 AV benchmarks over five dimensions, 32 silent-video over seven, with footnotes defining judges (GPT-4o, GPT-6-Luna), subset ordering and WER/CER. Some rows official, others the authors' own evaluations.

## A2 — Future Trigger

Use when comparing models or evaluating a new system across benchmarks, or when two reported scores conflict. Signals: 'which benchmark', 'compare models', 'metric definition', 'fair evaluation'. Distinct from honest-validation-records (completion status) and reward-routing-by-verifiability (training rewards).

## E — Execution

1. Declare dimensions for the modality — completion: list with rationale. 2. Map benchmarks to dimensions with metric/judge — completion: benchmark registry. 3. Mark each number official vs local — completion: provenance column filled. 4. Report both modes where a switch exists — completion: mode-labeled results. 5. Compare only within identical conventions — completion: no cross-convention ranking.

## B — Boundary

Not for a single-task sanity check and not a license to accept vendor numbers as neutral. Source-specific judges are not universal defaults. Benchmark deltas do not establish causal attribution.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.

# Dimension Based Evaluation

## Purpose

"The evaluation is organized around five critical dimensions... incorporates 33 representative benchmarks... For existing models, we report official results where available and our own evaluations oth

## Instructions

1. Read the capability description and confirm the trigger matches the current task.
2. Follow the method in this skill in order; do not skip its verification steps.
3. Record the evidence and the outcome; mark anything unverifiable explicitly.
4. If the method's prerequisites are missing, stop and report the gap rather than improvising.

## Examples

```
Task: <a task matching this skill's trigger>
Action: apply the steps above in order
Result: <verified outcome or explicit gap>
```

## Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| Trigger does not fit the task | Over-broad routing | Check the "not for" boundary in the description |
| Prerequisites missing | Environment not prepared | Stop and document the missing input or dependency |
| Output cannot be verified | Evidence not captured | Re-run the method's verification step before reporting |
