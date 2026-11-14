---
version: 1.0.0
license: MIT
name: aidev26-agent-engineering
description: |
  Distilled methodology from the AI Dev 26 x SF conference (48 talks, ~213K words). Covers the engineering of trustworthy agents: eval literacy and containerized eval building, red-team test suites from natural-language behaviors, production architecture (deterministic shells around stochastic cores), layered sandbox security, durable execution for long-running agents, agent memory systems that keep token curves flat, and Pareto optimization across accuracy/cost/latency. Entry routes to the right capability for the task. Use when the task concerns evals, red-teaming, production agent architecture, sandbox security, durable execution, agent memory, cost/latency optimization, or org adoption of agentic engineering.
metadata:
  tags: [aidev26-agent-engineering]
  author: "Cangjie Distillation <agent@example.com>"
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: single
  cangjie.bundle-id: bundle.aidev26-sf-agent-practices
  cangjie.capability-count: 8
  cangjie.entrypoint-count: 1
---
# AI Dev 26 x SF — Agent Engineering Practices from 48 Conference Talks — 全书能力入口

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- Model training/fine-tuning strategy and hardware selection
- Specific vendor product configuration (patterns are vendor-neutral; vendor parts are flagged in card Boundaries)
- Non-agent ML topics from the conference (edge vision, video anomaly detection)

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. {'Measure what you cannot trust': 'evals are engineering plus philosophy'}
2. {'Deterministic shells around stochastic cores': 'schemas before prompts, rules as code'}
3. {'Safety is layered': 'containment before scope before intent; model self-judgment is last'}
4. {'Durability over restarts': 'persist activity state, resume from failure'}
5. {'Memory must forget': 'thresholds, summaries, just-in-time retrieval'}
6. Optimize the Pareto frontier, not the single point

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| interpret benchmark scores for a model；build an eval suite for my agent；my eval says good but users say bad | references/capabilities/opu-agent-evals.md | references/capabilities/opu-redteam-suite.md、references/capabilities/opu-production-shells.md |
| red team my chatbot before release；test my agent for prompt injection；my bot leaked its system prompt | references/capabilities/opu-redteam-suite.md | references/capabilities/opu-agent-evals.md |
| move my agent demo to production；make agent decisions auditable；structure a multi-agent pipeline | references/capabilities/opu-production-shells.md | references/capabilities/opu-sandbox-security.md、references/capabilities/opu-durable-agents.md |
| run my agent safely for long periods；give an agent tool access without risking my machine；sandbox a coding agent | references/capabilities/opu-sandbox-security.md | references/capabilities/opu-production-shells.md |
| my agent crashes mid-run and loses everything；run an agent for hours or days reliably；add retries without spaghetti failure code | references/capabilities/opu-durable-agents.md | references/capabilities/opu-production-shells.md |
| give my agent long-term memory；my context window keeps bloating；where should the agent store what it learns | references/capabilities/opu-agent-memory.md | references/capabilities/opu-production-shells.md |
| my agent is too expensive or too slow；improve accuracy without exploding cost；which model should each step use | references/capabilities/opu-agent-optimization.md | references/capabilities/opu-agent-evals.md |
| how should my team adopt AI coding；what roles emerge in agentic engineering；convince leadership about agent adoption | references/capabilities/opu-org-agentic-shift.md | references/capabilities/opu-agent-evals.md |

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

- No eval set or acceptance definition and the user will not co-create one — measuring is the method, refuse to ship blind
- Request requires bypassing sandbox/audit controls ("just give the agent root")
- Task is a one-off script where the harness overhead exceeds value (say so and do the simple thing)

## Purpose

Distilled methodology from the AI Dev 26 x SF conference (48 talks, ~213K words) on engineering trustworthy agents. Covers eval literacy and containerized eval building, red-team test suites from natural-language behaviors, production architecture (deterministic shells around stochastic cores), layered sandbox security, durable execution for long-running agents, agent memory that keeps token curves flat, and Pareto optimization across accuracy/cost/latency. Acts as the entry point that routes each task to the right capability card.

## Instructions

1. Read this file first on every task (per 加载规则).
2. Match the user's intent against the 能力路由 (capability routing) table above.
3. Load exactly **1** capability card from `references/capabilities/`; load at most 2 when the task explicitly spans domains.
4. For overview/book-level questions, load no capability card — answer from 核心原则 (core principles) and `references/overview.md`.
5. If neither the routing table nor `references/capability-index.md` matches the intent, explicitly state the request is outside this book's scope — do not force-fit.

## Examples

- "Interpret benchmark scores for a model" / "my eval says good but users say bad" → load `references/capabilities/opu-agent-evals.md`, optionally supplementing with `opu-redteam-suite.md` and `opu-production-shells.md`.
- "Red team my chatbot before release; my bot leaked its system prompt" → load `references/capabilities/opu-redteam-suite.md`, supplementing with `opu-agent-evals.md`.
- "My agent crashes mid-run and loses everything; add retries without spaghetti failure code" → load `references/capabilities/opu-durable-agents.md`, supplementing with `opu-production-shells.md`.

## Limitations

- Does NOT cover model training/fine-tuning strategy or hardware selection.
- Does NOT cover specific vendor product configuration — patterns are vendor-neutral; vendor-specific parts are flagged in each card's Boundaries.
- Excludes non-agent ML topics from the conference (edge vision, video anomaly detection).

## Troubleshooting

- **Error:** Intent matches no routing-table row. **Cause:** Query is outside the book's capability domain. **Solution:** Check `references/capability-index.md` first; if still unmatched, tell the user it is out of scope instead of forcing a card.
- **Error:** No eval set or acceptance definition exists and the user will not co-create one. **Cause:** Request wants to ship unmeasured. **Solution:** Refuse to ship blind — measuring is the method (边界与判停).
- **Error:** Request asks to bypass sandbox/audit controls ("just give the agent root"). **Cause:** Security controls are seen as friction. **Solution:** Stop — containment precedes scope precedes intent; model self-judgment is last.
- **Error:** Task is a one-off script. **Cause:** Harness overhead exceeds value. **Solution:** Say so and do the simple thing instead of applying the harness.

## Prerequisites

- The capability card files referenced by the routing table must exist under `references/capabilities/` (e.g. `opu-agent-evals.md`, `opu-production-shells.md`), plus `references/overview.md`, `references/glossary.md`, `references/cheatsheet.md`, `references/capability-index.md`.
- No external tools, API keys, or network access are required.
