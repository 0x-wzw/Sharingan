---
name: wemm-video-router
description: 'Source router entry for WeMM-Video: routes requests about its progressive modality curriculum, timestamped token
  interleaving, fixed-rate audio tokenization, scarce-data transfer, format-to-runtime serving matrix and honest validation
  records to the matching capability card.

  '
version: 1.0.0
license: MIT
metadata:
  author: Cangjie Distillation <agent@example.com>
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: router
  cangjie.bundle-id: bundle.wemm-video
  cangjie.capability-count: 11
  cangjie.entrypoint-count: 8
  layer: craft
  stack-source: repo:0x-wzw/Sharingan
  hermes:
    tags:
    - wemm-video
    - distilled
    related_skills: []
approval_source: agent
read_scope: profile
source: Sharingan RIA-TV++ distillation of WeMM-Video (arXiv:2611.26409), 2026-11-21; Tier-1 PASS 8/8
---
# WeMM-Video: Pushing the Frontiers of Open-Source Omni-Modal Video Understanding — 来源路由入口（compact pack）

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- How to download or run WeMM-Video checkpoints
- Model-size and quantization internals not defined by the source
- Causal claims without ablation

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. Align new modalities before unfreezing the backbone
2. Make time explicit before fusing temporal streams
3. Order interventions by diagnosed failure mode
4. Choose teachers for retention as well as improvement
5. Fix degeneration before RL
6. Every score carries its metric convention and provenance

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| add a new modality without breaking the existing one；which layers to freeze during fine-tuning；curriculum for multimodal fine-tuning | references/capabilities/progressive-modality-curriculum.md | 已晋级为独立 Skill `progressive-modality-curriculum`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| align audio with video；interleave time-indexed streams；find which frame matches a sound | references/capabilities/timestamped-token-interleaving.md | 已晋级为独立 Skill `timestamped-token-interleaving`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| what to fine-tune next；post-training stage order；RL made things worse | references/capabilities/failure-mode-ordered-post-training.md | 已晋级为独立 Skill `failure-mode-ordered-post-training`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| which teacher model to distill from；distillation degraded another benchmark；multi-teacher distillation | references/capabilities/teacher-allocation-by-capability.md | 已晋级为独立 Skill `teacher-allocation-by-capability`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| model keeps repeating itself；endless generation after fine-tuning；fix degeneration before RL | references/capabilities/anti-repetition-loop.md | 已晋级为独立 Skill `anti-repetition-loop`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| reward design for mixed tasks；rule vs rubric rewards；RL on verifiable and open tasks | references/capabilities/reward-routing-by-verifiability.md | 已晋级为独立 Skill `reward-routing-by-verifiability`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| which benchmarks to use；compare two models fairly；metric definition mismatch | references/capabilities/dimension-based-evaluation.md | 已晋级为独立 Skill `dimension-based-evaluation`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| audio tokens for LLM；token rate for continuous signal；streaming sensor token budget | references/capabilities/fixed-rate-signal-tokenization.md | references/capabilities/timestamped-token-interleaving.md、references/capabilities/progressive-modality-curriculum.md |
| not enough reasoning data；transfer reasoning to new modality；scarce labels | references/capabilities/scarce-modality-data-transfer.md | references/capabilities/teacher-allocation-by-capability.md、references/capabilities/progressive-modality-curriculum.md |
| which runtime for quantized checkpoint；GGUF vs AWQ serving；serving container fails | references/capabilities/weight-format-runtime-matrix.md | references/capabilities/honest-validation-records.md |
| is this system verified；validation status report；what has not been tested | references/capabilities/honest-validation-records.md | references/capabilities/dimension-based-evaluation.md、references/capabilities/weight-format-runtime-matrix.md |

**非能力类查询**：
- 书名/作者/章节/整书概览 → references/overview.md
- 术语解释 → references/glossary.md
- 决策规则速查（不需要原文依据时） → references/cheatsheet.md
- 完整意图与关键词索引（本表未覆盖的意图先查这里） → references/capability-index.md

## 加载规则

- 每次任务先读本文件，再按路由表加载 **1** 张能力卡；任务明确跨域时最多加载 2 张。
- 概览/书名类问题不加载能力卡，用「核心原则」与 overview.md 回答。
- 路由表与 capability-index.md 都无法命中的意图，明确告知超出本书范围，不要硬套。

## 边界与判停

- Source does not disclose a required parameter - mark needs-review and do not invent it
- Only benchmark deltas available - report as source-reported, not causal
- Validation rows marked pending must stay pending
