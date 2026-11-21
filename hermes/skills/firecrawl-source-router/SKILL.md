---
name: firecrawl-source-router
description: |
  Routes Firecrawl questions to the evidence-ranked capability cards distilled from the pinned 41b36df source, including reference and needs-review items.
version: 1.0.0
license: MIT
metadata:
  author: Cangjie Distillation <agent@example.com>  # source: Firecrawl contributors
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: router
  cangjie.bundle-id: bundle.firecrawl
  cangjie.capability-count: 7
  cangjie.entrypoint-count: 8
---
# Firecrawl repository @ 41b36df — 来源路由入口（compact pack）

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- First-scrape tutorial (external docs)
- Full agent/MCP onboarding (external docs)
- Production architecture design

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. Pin the revision before trusting deployment docs
2. Baseline first, extend only with a named prerequisite
3. Prefer source-verifiable rules over marketing claims
4. Record evidence for every decision
5. Never publish the unauthenticated internal admin listener

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| Confusing development and self-hosting environment files | references/capabilities/dev-vs-selfhost-env-isolation.md | 已晋级为独立 Skill `dev-vs-selfhost-env-isolation`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| Publishing the unauthenticated admin internal listener | references/capabilities/admin-internal-listener-exposure.md | 已晋级为独立 Skill `admin-internal-listener-exposure`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| Before production: conditional hardening checklist | references/capabilities/before-production-hardening-gates.md | 已晋级为独立 Skill `before-production-hardening-gates`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| Schema-driven model selection for LLM extraction | references/capabilities/llm-extraction-model-selection.md | 已晋级为独立 Skill `llm-extraction-model-selection`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| Prompt-injection triage「capability, not politeness」 | references/capabilities/prompt-injection-capability-triage.md | 已晋级为独立 Skill `prompt-injection-capability-triage`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| Engine forcing：模式语义与 3 步优先级 | references/capabilities/engine-forcing-precedence.md | 已晋级为独立 Skill `engine-forcing-precedence`（已安装时优先直接使用；本卡仅作原文与背景补充） |
| Verification done-criteria：编译不算，需真实请求 | references/capabilities/verification-done-criteria.md | 已晋级为独立 Skill `verification-done-criteria`（已安装时优先直接使用；本卡仅作原文与背景补充） |

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

- Evidence missing
- Source path outside the pinned revision
- Task requires external documentation
