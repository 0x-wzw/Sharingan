---
version: 1.0.0
license: MIT
name: fde-productization
description: |
  AI FDE产品值不值得采用；FDE哪些工作会被自动化；企业软件售后交付怎么提速。FDE 正在被产品化：可模板化的交付环节变成软件，人的价值向判断与关系两端移动。
metadata:
  tags: [fde-productization]
  author: "Cangjie Distillation <agent@example.com>"
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.fde-framework.productization
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.fde-enterprise-ai-framework
  cangjie.source-title: 一图讲透 FDE：企业AI落地完整框架（v2 扩展版：+ Lab0 产品化 + Varick 实战 playbook）
---
# AI-FDE 产品化：把 FDE 作为产品交付（Lab0 模式）

## R — Reading (原文)

> "We're building an AI FDE that automates entire post-sales delivery for software
> companies — all from discovery, solution design, config, to testing and go-live."
> —— Lab0 (YC P26) launch，source/lab0-yc-launch.md

> "6 months → 10 days."（同上，对"企业软件上线周期"的压缩承诺）

## I — Interpretation (自述)

Lab0 代表 FDE 演进的第三个形态：**人 → 人+AI → AI 产品**。

1. **问题结构**：$200K 合同签订后，售后交付要 3–6 个月定制（FDE/方案架构师
   从零重建），客户价值的 start date 被推后——这是企业软件的"隐藏税"。
2. **产品化方案**：AI FDE 接管售后交付全链条——discovery（参加发现会议并
   提示该问什么）→ handoff 与设计文档生成 → 配置 → 测试 → go-live。
   终局愿景："企业自购软件，由 agent 完成配置"（self-serve enterprise software）。
3. **效果承诺**：6 个月 → 10 天；已服务 Adobe 与数家系统集成商（SI）——
   注意其销售对象是**软件公司**（把 FDE 成本内生化），不是终端企业。
4. **与人的关系**：这不是"替代 FDE"，而是把 fde-process-mapping（映射）、
   四分法（分桶）、配置联调（执行）中**可模板化的部分**变成软件；判断密集
   的部分（组织政治、闸门判定）仍在人手里。

对个人 FDE 的含义：价值重心向两端移动——前端（发现/关系/判断）与兜底
（治理/问责）；中间的"配置与联调"正在被产品化，最先被压缩的就是这段。

## A1 — Application Example（来源案例或明确标记的演练）

来源真实案例：Lab0 与 Adobe 及系统集成商的部署（把其售后交付从月级压到
天级）；痛点结构引用其 "$200K 合同 + 3 个月定制 + 6 个月才能用" 的原叙。
（合成演练：一家 50 人 B2B SaaS 评估采用 AI-FDE 产品——用四分法审其售后
流程：发现会议纪要与需求整理=agent 可吸收；config=agent；UAT 测试=code+agent
混合；go-live 决策=human；客户高层关系=human。结论：可产品化环节约占交付
工时的 60%，与 Lab0 的 6 个月→10 天叙事量级一致。）

## A2 — Future Trigger ★

1. **情境**：软件公司评估"要不要用 AI-FDE 产品替代/增强售后交付"；FDE 从业者
   判断自己哪些工作会被产品化；投资人/观察者评估 FDE 赛道的形态演进。
2. **语言信号**："AI FDE" / "automated implementation" / "post-sales automation" /
   "onboarding 自动化" / "企业软件上线慢怎么办" / "self-serve enterprise" /
   "FDE 产品化" / "implementation copilot"。
3. **相邻区分**：与 fde-three-stage-landing 不同——那张卡是 FDE 的**方法论**
   （人怎么做事），本卡是 FDE 的**产品形态**（事怎么变成软件）。与
   fde-system-outcome 不同——那张卡是交付策略，本卡讨论交付本身的自动化。

## E — Execution (可执行步骤)

**输入契约**：软件公司的售后交付流程清单（或评估者自己的 FDE 工作内容清单）
+ 各环节工时占比。缺工时数据先询问或用两周自查日志估算。

1. **可产品化扫描**：用四分法对售后交付流程分桶（delete/code/agent/human）。
   完成标准：每个交付环节有桶归属。
2. **压缩测算**：对 agent/code 桶环节，估算产品化后的周期压缩（对照 Lab0 的
   月级→天级量级校准预期）。完成标准：给出"最短可行上线周期"的保守估计。
3. **边界判定**：human 桶（go-live 判定、客户关系、组织政治）保留给人，并
   明确 AI 产品在这些环节只做辅助（纪要/提示/文档）。
4. **引入路径**（对软件公司）：POC（1 条产品线）→ 并行运行 → 按 go-live 周期
   缩短与交付成本下降计价续约。对应 fde-system-outcome 的 before/after 协议。
5. **输出契约**：产品化评估——四分桶结果、可压缩周期测算、human 保留清单、
   POC 计划与计价口径。

## B — Boundary (边界)

- **不要**用于：把本卡当"AI 取代 FDE"的论据（本卡结论恰恰相反——判断与关系
  环节保值）；非软件交付场景（如内部落地）直接套用——内部落地回主框架。
- **失败模式**：把 discovery 全自动化（发现会议的核心是信任建立，AI 只能辅助
  提问）；产品化未跑通就去销售（Lab0 也是先有 Adobe 交付案例）；忽略 SI 渠道
  （Lab0 同时与系统集成商合作——渠道比替代更现实）。
- **作者盲点**：来源是融资叙事（YC launch），效果数字未经独立验证；"10 天"
  的口径（配置完成 vs 业务采纳）未定义——用主框架的话说，这是"效果达标"而非
  "试点通过"；FDE 从业者评估时须区分两者。

## Purpose

Covers the third form of FDE evolution: human → human+AI → AI product, exemplified by Lab0 (YC P26) automating post-sales delivery for software companies — discovery, solution design, config, testing, go-live — with a promised compression of "6 months → 10 days". Templatable delivery steps become software; human value moves to the two ends: front-end judgment/relationships and back-stop governance/accountability. Not "replacing the FDE" — judgment-dense parts stay human.

## Instructions

Follow the full executable procedure in the `## E — Execution` section; the canonical step sequence is:

1. Productizable scan: bucket each post-sales delivery step with the four-way triage (delete/code/agent/human) — every step gets a bucket.
2. Compression estimate: for agent/code-bucket steps, estimate cycle compression after productization, calibrated against Lab0's month→days magnitude; produce a conservative "shortest viable go-live cycle" estimate.
3. Boundary ruling: keep human-bucket steps (go-live decision, customer relationships, organizational politics) with people; AI products there only assist (notes / prompt suggestions / documents).
4. Adoption path (for software companies): POC on 1 product line → parallel run → price renewal on go-live-cycle shortening and delivery-cost reduction, per fde-system-outcome's before/after protocol.
5. Output contract: the productization assessment — four-bucket result, compression estimate, human-retained list, POC plan and pricing basis.

## Examples

- Input: a 50-person B2B SaaS evaluating an AI-FDE product → four-way triage of its post-sales flow: discovery minutes/requirements = agent; config = agent; UAT testing = code+agent mix; go-live decision = human; executive customer relationships = human. Result: ~60% of delivery hours are productizable, consistent in magnitude with Lab0's 6-months→10-days narrative.
- "Should our software company buy an AI-FDE product to replace/augment post-sales delivery?" → run the scan + compression estimate, then the POC→parallel-run adoption path with before/after pricing.
- FDE practitioner asking "which of my tasks will be automated?" → bucket your own work list; expect config/integration work to compress first while front-end discovery/relationship and governance/accountability work retains value.

## Limitations

- NOT to be used as an argument that "AI replaces FDE" — the card's conclusion is the opposite: judgment and relationship steps retain value.
- Not directly applicable to non-software-delivery scenarios (e.g. internal landing) — internal landing goes back to the main framework.
- Source evidence is a fundraising narrative (YC launch); the effect numbers are independently unverified, and the "10 days" definition (config complete vs business adoption) is undefined — per the main framework this is "effect met", not "pilot passed"; practitioners must distinguish the two (作者盲点).

## Troubleshooting

- **Error:** Discovery is fully automated. **Cause:** Overreach into trust-building work. **Solution:** The core of discovery meetings is trust building — AI only assists with questions/notes (失败模式).
- **Error:** Product sold before it works. **Cause:** Selling ahead of a proven delivery case. **Solution:** Productize and prove first — even Lab0 had the Adobe delivery case before selling (失败模式).
- **Error:** SI channel ignored. **Cause:** Framed purely as replacement. **Solution:** Work with system integrators — channel beats replacement (Lab0 partners with SIs) (失败模式).
- **Error:** Missing hours-split data for the delivery flow. **Cause:** No measured work breakdown. **Solution:** Ask first, or estimate via a two-week self-audit log (输入契约).

## Prerequisites

- Input contract: the software company's post-sales delivery process list (or the evaluator's own FDE work-item list) plus hours share per step; if hours data is missing, ask or estimate from a two-week self-audit log.
- No external tools, API keys, or network access are required.
