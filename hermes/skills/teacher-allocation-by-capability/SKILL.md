---
name: teacher-allocation-by-capability
description: 'Use when selecting teachers in multi-teacher distillation; not when only one teacher exists.

  '
version: 1.0.0
license: MIT
metadata:
  author: Cangjie Distillation <agent@example.com>
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.wemm-video.teacher-allocation-by-capability
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.wemm-video
  cangjie.source-title: 'WeMM-Video: Pushing the Frontiers of Open-Source Omni-Modal Video Understanding'
  layer: craft
  stack-source: repo:0x-wzw/Sharingan
  hermes:
    tags:
    - distillation
    - teacher-selection
    - retention
    related_skills:
    - wemm-video-router
approval_source: agent
read_scope: profile
source: Sharingan RIA-TV++ distillation of WeMM-Video (arXiv:2611.26409), 2026-11-21; Tier-1 PASS 8/8
---
## R — Reading (source)

"stronger external teachers provide supervision for text and vision-language tasks... while teachers from the same model family are employed to retain existing audio and audio-visual capabilities. We further leverage cross-modal distillation to transfer knowledge from text to audio tasks." (paper p.5 §4.2)

## I — Interpretation

Picking the strongest teacher for every task in multi-teacher distillation quietly erodes capabilities the student already had. Split teachers by intent: external stronger teachers lift the capabilities you want to improve; same-family teachers retain capabilities you must not lose; cross-modal distillation moves knowledge from a data-rich modality into a poorer one. A teacher must be chosen for retention as well as improvement, and the retention benchmark must be checked after distillation, not assumed.

## A1 — Application Example

Source case (paper p.5): external teachers lift text/VL reasoning, same-family teachers retain audio/AV behavior, text-to-audio transfer improves speech understanding and instruction following. Retention reported qualitatively; no teacher-ablation table.

## A2 — Future Trigger

Use when asked which teacher to distill from, or when distillation improved one benchmark but degraded another. Signals: 'which teacher model', 'distillation degraded', 'keep original capability', 'multi-teacher'. Distinct from failure-mode-ordered-post-training (stage order) and scarce-modality-data-transfer (data mixture).

## E — Execution

1. Classify capabilities as lift or retain — completion: two named lists. 2. Assign external teacher to lift, same-family to retain — completion: capability→teacher mapping with rationale. 3. Add a cross-modal path only where a rich modality can supervise a poor one — completion: named source/target. 4. Distill, then check lift and retain benchmarks — completion: lift improves, retain does not regress.

## B — Boundary

Not when only one teacher exists or there is no capability split. 'Same family' is not defined operationally; define it locally. Do not present reported gains as causal proof of the rule.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
