---
version: 1.0.0
license: MIT
name: fde-framework-router
description: |
  来源路由入口：FDE 企业AI落地完整方法论（三阶段四闸门主框架 + 流程映射/四分法/ 按系统落地与按结果销售/产品化四项实战扩展）。当请求横跨落地全流程、或不确定 该聚焦哪个阶段/哪张卡时由此进入，按阶段判定路由。不适用于与AI落地无关的 一般项目管理问题。Use when the request spans the full AI-landing journey or the right stage/capability is unclear.
metadata:
  tags: [fde-framework-router]
  author: "Cangjie Distillation <agent@example.com>"
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: router
  cangjie.bundle-id: bundle.fde-enterprise-ai-framework
  cangjie.capability-count: 10
  cangjie.entrypoint-count: 9
---
# 一图讲透 FDE：企业AI落地完整框架（v2 扩展版：+ Lab0 产品化 + Varick 实战 playbook） — 来源路由入口（compact pack）

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- 具体模型/框架选型（方案设计层的子问题）
- 个人效率类AI工具使用技巧
- 无组织落地语境的纯算法研究

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. 机会先行：五入口建场景池，'是否值得做'闸门不过就暂缓观望
2. 定义先于构建：六项定义齐且'是否可行'，才允许进入实施
3. 基线在先：动工前测好所有 KPI 基线（baseline before you build），6个月后拿 before/after 说话
4. 四分法分诊：每步只贴一个标签 delete/code/agent/human——先删 waste 再建 agent，高风险步永远留人工
5. 试点是闸门：效果达标≠试点通过，两道验收分开，不过就回环修正
6. 按系统落地：agent 长在客户已有的系统 of record 里，零再培训；绝不推销换系统
7. 风险与人工兜底是全程旁路：AI 失效降级运行，不允许击穿业务
8. 数据先于智能：agent 落地前，先报出当前数据成熟度台阶
   （METADATA→LINEAGE→QUALITY→AI READY→ONTOLOGY→KG→SEMANTIC LAYER→DATA AGENT，
   概念到落地有序不可跳——数据台阶不够时 agent 桶降级为 code/human，见
   fde-workflow-triage 的"判断+数据"双条件）
9. 技能成于完整流程：工具带先行（codex/MCP/CLI/大模型/工作台/harness/loop），
   在真实业务中边学边干——能力单位是"独立跑通一条完整流程"，不是工具证书；
   培训顺序（先工具带）与项目顺序（先发现）不冲突：前者对个人，后者对项目

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 企业AI落地该从哪一步开始；如何规划AI转型/落地的阶段和路线图；AI项目为什么总是烂尾，如何按框架推进 | references/capabilities/fde-three-stage-landing.md | 已晋级为独立 Skill `fde-three-stage-landing`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| 帮我们梳理有哪些AI应用场景；这个AI场景值不值得立项；AI落地方向太乱怎么收敛 | references/capabilities/fde-opportunity-discovery.md | 已晋级为独立 Skill `fde-opportunity-discovery`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| AI项目立项前要定义哪些东西；怎么写AI项目的成功指标和数据准备；AI方案可行性怎么评估 | references/capabilities/fde-solution-definition.md | 已晋级为独立 Skill `fde-solution-definition`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| AI试点怎么设计和验收；试点效果不达标怎么修正；AI项目怎么从试点走向规模化推广 | references/capabilities/fde-pilot-execution.md | 已晋级为独立 Skill `fde-pilot-execution`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| AI系统出错或效果不稳时怎么办；怎么设计AI的人工兜底和降级方案 | references/capabilities/fde-risk-human-fallback.md | references/capabilities/fde-workflow-triage.md |
| AI落地项目怎么建立迭代反馈机制；试错成本太高，如何设计回环 | references/capabilities/fde-feedback-loops.md | references/capabilities/fde-pilot-execution.md、references/capabilities/fde-system-outcome.md |
| 帮我们摸清现有流程的现状；AI项目ROI基线怎么定；多地区多系统的流程盘点 | references/capabilities/fde-process-mapping.md | 已晋级为独立 Skill `fde-process-mapping`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| 哪些流程步骤适合交给AI；这个环节该用agent还是人工；自动化方案怎么收敛权限范围 | references/capabilities/fde-workflow-triage.md | 已晋级为独立 Skill `fde-workflow-triage`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| AI项目怎么向高管/CFO卖出价值；agent应该部署进哪套系统；多客户多子公司怎么复制落地 | references/capabilities/fde-system-outcome.md | 已晋级为独立 Skill `fde-system-outcome`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| AI FDE产品值不值得采用；FDE哪些工作会被自动化；企业软件售后交付怎么提速 | references/capabilities/fde-productization.md | 已晋级为独立 Skill `fde-productization`（已安装时优先直接使用；本卡仅作原文与背景补充） |

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

- 用户只想要原文/图转录，不要求执行指导 → 输出结构化转录即可
- 纯技术问题（训练/微调/调试）且无企业落地语境 → 改用对应技术skill
- 信息不足以判断所处阶段 → 先用E段阶段判定问题清单问清，不要假设

## Purpose

Routing entry point for the FDE enterprise-AI-landing methodology (three-stage / four-gate main framework plus four practical extensions: process mapping, workflow triage, sell-by-outcome, and productization). Use it when a request spans the whole landing journey or it is unclear which stage or card to focus on — it determines the stage and routes to one capability card. Not for general project management unrelated to AI landing.

## Instructions

1. Read this file first on every task (per 加载规则).
2. Match the user's intent against the 能力路由 (capability routing) table above.
3. Load exactly **1** capability card from `references/capabilities/`; at most 2 when the task explicitly spans domains. Where a card has been promoted to an independent installed skill (e.g. `fde-process-mapping`, `fde-productization`), prefer that skill directly and use the card only as source/background supplement.
4. For overview/book-level questions, load no capability card — answer from 核心原则 (core principles) and `references/overview.md`.
5. If neither the routing table nor `references/capability-index.md` matches the intent, explicitly state the request is outside scope — do not force-fit.

## Examples

- "How should we plan our AI transformation roadmap? Why do our AI projects keep failing?" → load `references/capabilities/fde-three-stage-landing.md` (or the installed `fde-three-stage-landing` skill).
- "Help us figure out which AI use cases are worth pursuing; our AI direction is too scattered" → load `references/capabilities/fde-opportunity-discovery.md` (or the installed `fde-opportunity-discovery` skill).
- "What should an AI project define before approval? How do we evaluate feasibility?" → load `references/capabilities/fde-solution-definition.md` (or the installed `fde-solution-definition` skill).

## Limitations

- Does NOT cover specific model/framework selection (a sub-problem of solution design).
- Does NOT cover personal-efficiency AI tool usage tips.
- Excludes pure algorithm research without an organizational landing context.

## Troubleshooting

- **Error:** User only wants the original text/diagram transcribed, not execution guidance. **Cause:** Reading request, not a landing task (边界与判停). **Solution:** Output a structured transcription only.
- **Error:** Question is purely technical (training/fine-tuning/debugging) with no enterprise-landing context. **Cause:** Out of this router's domain. **Solution:** Switch to the corresponding technical skill.
- **Error:** Not enough information to determine the current stage. **Cause:** Key context missing. **Solution:** Use the E-stage stage-determination question list to ask first — do not assume.

## Prerequisites

- The capability card files referenced by the routing table must exist under `references/capabilities/`, plus `references/overview.md`, `references/glossary.md`, `references/cheatsheet.md`, `references/capability-index.md`.
- Where noted, the corresponding promoted standalone skills (e.g. `fde-three-stage-landing`, `fde-opportunity-discovery`, `fde-process-mapping`) should be installed.
- No external tools, API keys, or network access are required.
