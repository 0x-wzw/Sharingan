---
name: failure-mode-ordered-post-training
description: 'Use when deciding the order of post-training interventions after a failure diagnosis; not when no diagnosis
  exists.

  '
version: 1.0.0
license: MIT
metadata:
  author: Cangjie Distillation <agent@example.com>
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.wemm-video.failure-mode-ordered-post-training
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.wemm-video
  cangjie.source-title: 'WeMM-Video: Pushing the Frontiers of Open-Source Omni-Modal Video Understanding'
  layer: craft
  stack-source: repo:0x-wzw/Sharingan
  hermes:
    tags:
    - post-training
    - pipeline
    - training-order
    related_skills:
    - wemm-video-router
approval_source: agent
read_scope: profile
source: Sharingan RIA-TV++ distillation of WeMM-Video (arXiv:2611.26409), 2026-11-21; Tier-1 PASS 8/8
---
## R — Reading (source)

"we develop a progressive three-stage post-training pipeline consisting of multi-teacher OPD, anti-repetition MrDPO, and specialist RL, targeting general capability enhancement, generation stabilization, and specialized capability improvement, respectively." (paper p.5 §4.2)

## I — Interpretation

Post-training stages are often ordered by algorithm availability rather than by what is broken. Start from residual failure classes after pre-training and assign one intervention to each: distillation from stronger teachers for a general-capability gap, a stabilization pass for generation degeneration, RL for specialist weakness. The key dependency is that degeneration must be fixed before RL, because repetitive decoding blocks reliable RL training. Convert a failure list into a dependency-ordered pipeline with an exit check per stage.

## A1 — Application Example

Source case (paper p.5): endless decoding persisting after pre-training and OPD led to anti-repetition MrDPO being inserted between OPD and specialist RL; rule/rubric/teacher rewards used in the final stage. Benchmark-level outcomes only; no stage-removal ablation.

## A2 — Future Trigger

Use when asked what to fine-tune next, in what order, or why RL/distillation made things worse. Signals: 'post-training order', 'what to fix first', 'RL made repetition worse', 'distillation then alignment'. Distinct from anti-repetition-loop (one stage's procedure) and teacher-allocation-by-capability (teacher choice).

## E — Execution

1. Enumerate residual failures into general / stability / specialist — completion: each has a measurable check. 2. Map one intervention per class, stabilization before RL — completion: ordered stages with exit checks. 3. Run general-capability stage — completion: benchmark exit passes. 4. Stabilize generation — completion: repetition probe below threshold. 5. Run specialist RL only after Step 4 — completion: specialist task passes with no stability regression.

## B — Boundary

Not a generic recipe when no failure diagnosis exists; do not run all three by default. Thresholds and reward weights are undisclosed. Do not claim the stage order is causally validated; it is the authors' reported design.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
