---
version: 1.0.0
license: MIT
name: fde-system-outcome
description: |
  AI项目怎么向高管/CFO卖出价值；agent应该部署进哪套系统；多客户多子公司怎么复制落地。agent 长在客户已有的系统里（零再培训），价值按三桶卖给对应买家，基线在先、before/after 说话。Use when 要决定 agent 部署进哪套系统、向 CFO/高管定价卖价值、或多客户多子公司复制 rollout 时。
metadata:
  tags: [fde-system-outcome]
  author: "Cangjie Distillation <agent@example.com>"
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.fde-framework.system-outcome
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.fde-enterprise-ai-framework
  cangjie.source-title: 一图讲透 FDE：企业AI落地完整框架（v2 扩展版：+ Lab0 产品化 + Varick 实战 playbook）
---
# 按系统落地与按结果销售：build-in-place + outcome pricing

## R — Reading (原文)

> "Put the agents in the tools the client already uses... Staff keep working where they
> already work, so there's zero retraining."（把 agent 放进客户已在用的工具里——
> 员工留在原地处工作，零再培训。）
> —— Varick Agents FDE playbook，source/varick-fde-playbook.md

> "Baseline every KPI before you build. Six months later, show them the before and after."

## I — Interpretation (自述)

落地与销售的两条铁律：

1. **Build in-place（按系统落地）**：agent 的"手"长在客户的系统 of record 里——
   在 Salesforce 里挖数据、在 Salesforce 里行动，审批走 Slack。绝不推销"迁移到
   AI 原生 CRM"——客户为上一次迁移花了 $10M 和好几年，你一开口就出局。例外
   只有一个：还没上 CRM 的 SMB，直接给他上一套。
2. **按系统分组规模化（PE 战术）**：26 家被投公司 × 10 部门 × 10 流程 = 数千
   工作流。按软件分组——5 家 NetSuite 一条轨道、4 家 Dynamics 一条轨道——
   同一问题解多次、卖给同一买家（CFO）多次。这是"deploy once, sell repeatedly"
   的杠杆结构。
3. **按结果销售（outcome pricing）**：把脏流程映射出来 → 展示干净版本 → 每条
   标价与 KPI。价值三桶对买家：成本节省→CFO（月结 22 天–6 周 → 4–8 天）、
   收入提升→CHRO/销售、风险缓释→全 C-suite。**每个 agent 的月成本**标注在
   流程旁——"那个数字低得吓人"。
4. **证明协议**：基线在先（4 周审计+POC）→ 建设（4 周）→ 第 3 与第 6 个月出
   before/after 报告。来源 AP 判例：17→7 步、24 天→6 天、直通率 18%→87%、
   $31→$6——这套数字格式就是销售语言。

与主框架的关系：资源协同（角色分工）在这里具体化为"零再培训"；运营反馈回环
在这里具体化为 3/6 月 before/after 报告；试点通过闸门的"业务采纳"证据在这里
具体化为按买家角色定制的 KPI 叙事。

## A1 — Application Example（来源案例或明确标记的演练）

来源真实案例：AP 流程 before/after（见上，量化到每张发票）；PE 组合按 NetSuite/
Dynamics 分轨道复制同一套 agent；月结周期 22 天–6 周 → 4–8 天卖给 CFO。
（合成演练：为"合同评审流程"设计 outcome pitch——买家=法务 VP，价值桶=风险
缓释；基线=平均评审 9 天/漏审率 4%；提案=在既有 CLM 系统内加审阅 agent，
人审保留（fde-workflow-triage 的 Human 桶）；定价=每 agent 月成本 vs 外聘
律师费；第 6 个月报告口径=漏审率与周期天数的 before/after。）

## A2 — Future Trigger ★

1. **情境**：向企业/高管推销 AI 项目怎么定价与叙事；决定 agent 部署进哪套系统；
   多客户/多子公司复制方案；续约谈判需要价值证据。
2. **语言信号**："怎么向 CFO 卖 AI" / "AI 项目 ROI 话术" / "agent 部署到哪个
   系统" / "零培训落地" / "outcome-based pricing" / "before after 证据" /
   "多实体 rollout" / "value buckets"。
3. **相邻区分**：与 fde-solution-definition 不同——那张卡产出方案定义（对内
   立项），本卡是对外销售与规模化部署的策略。与 fde-pilot-execution 不同——
   那张卡执行与过闸，本卡决定**agent 长在哪**（系统集成策略）与**怎么收钱**。

## E — Execution (可执行步骤)

**输入契约**：已过四分法的步骤映射（哪些步给 agent）、客户系统清单、买家角色
（CFO/CHRO/VP…）。缺买家信息先询问——价值桶匹配错误=.pitch 致命伤。

1. **系统落位**：对每个 Agent 桶步骤，指定宿主系统（数据在哪，行动就在哪）+
   人工触达通道（如 Slack 审批）。完成标准：每个 agent 有宿主与通道，零新系统
   引入（除非 SMB 无 CRM 的例外）。
2. **价值桶匹配**：把预期收益归入 成本节省/收入提升/风险缓释 三桶之一，对应
   到买家角色。完成标准：每条流程有主买家与主价值桶。
3. **定价叙事**：为每条流程写 before/after 表——步骤数/周期天/回环数/直通率/
   单位成本，右列放 agent 月成本。完成标准：所有"after"数字可追溯到基线协议
   （fde-process-mapping 第 4 步）。
4. **分组复制**（多实体场景）：按系统 of record 给客户/子公司分组，同组共用
   一条 agent 轨道；对每组重复销售给同一角色买家。
5. **输出契约**：pitch 包——before/after 表（含 agent 月成本列）、价值桶×买家
   矩阵、部署拓扑图（agent↔系统↔审批通道）、3/6 月复测时间表。

## B — Boundary (边界)

- **不要**用于：没有基线就谈价值（先回 fde-process-mapping）；向刚完成大迁移的
  客户推销换系统；把"AI 原生平台"话术对准重资产 ERP 客户（来源原话：那你就
  输了）。
- **失败模式**：价值桶配错买家（跟 CIO 谈成本、跟 CFO 谈酷炫）；after 数字
  无基线背书（客户复算即崩）；复制时忽略组内差异（同为 NetSuite 但流程
  监管环境不同）。
- **作者盲点**：来源未给定价模型本身（固定费/分成/carry 的适用条件只在 PE
  语境点到）；未讨论多实体间数据隔离与合规差异——跨区部署时须补法律尽调。

## Purpose

决定 agent 部署进哪套系统（build in-place：长在客户已有系统 of record 里，零再培训），以及如何按结果销售：价值三桶（成本节省/收入提升/风险缓释）匹配对应买家（CFO/CHRO/全 C-suite），基线在先、before/after 数字说话，多客户按系统 of record 分组复制同一套 agent 轨道。

## Instructions

完整可执行步骤见 `## E — Execution`；紧凑步骤列表：

1. 收集输入：已过四分法的步骤映射、客户系统清单、买家角色；缺买家信息先询问。
2. 系统落位：每个 Agent 桶步骤指定宿主系统 + 人工触达通道（如 Slack 审批），零新系统引入（SMB 无 CRM 例外）。
3. 价值桶匹配：预期收益归入成本节省/收入提升/风险缓释之一，对应买家角色。
4. 定价叙事：每条流程写 before/after 表（步骤数/周期天/回环数/直通率/单位成本 + agent 月成本列），after 数字须可追溯基线协议。
5. 多实体场景按系统 of record 分组，同组共用一条 agent 轨道、重复销售给同一买家。
6. 输出 pitch 包：before/after 表、价值桶×买家矩阵、部署拓扑图、3/6 月复测时间表。

## Examples

1. 输入："这个 agent 该部署到客户的哪套系统？" → 期望：指定宿主系统 of record（数据在哪行动就在哪）+ 审批通道，不推销迁移到 AI 原生 CRM；仅对尚未上 CRM 的 SMB 建议直接上一套。
2. 输入："怎么向 CFO 卖这个 AP agent" → 期望：价值桶=成本节省，before/after 表沿用来源判例格式（17→7 步、24 天→6 天、直通率 18%→87%、$31→$6），右列标 agent 月成本，第 3 与第 6 个月复测。
3. 输入："26 家子公司怎么复制这套 agent" → 期望：按 NetSuite/Dynamics 等系统 of record 分轨道，同组解同一问题、卖给同一角色（CFO）多次；同时标注组内监管环境差异风险。

## Limitations

- 前提是有基线：没做基线就谈价值 → 先回 fde-process-mapping。
- 不适用于向刚完成大迁移的客户推销换系统，或把"AI 原生平台"话术对准重资产 ERP 客户。
- 来源未给定价模型本身（固定费/分成/carry 的适用条件只在 PE 语境点到），本卡不补。
- 多实体间数据隔离与合规差异未讨论，跨区部署须补法律尽调。

## Troubleshooting

- 错误：pitch 被客户否决。原因：价值桶配错买家（跟 CIO 谈成本、跟 CFO 谈酷炫）。解决：先确认买家角色，再按三桶重新匹配。
- 错误：客户复算 after 数字后信任崩塌。原因：after 数字无基线背书。解决：所有"after"可追溯到基线协议，否则不进 pitch。
- 错误：复制轨道在新子公司失效。原因：忽略组内差异（同为 NetSuite 但监管环境不同）。解决：分组复制前逐组核查流程与合规差异。

## Prerequisites

- 输入契约要求：已过四分法的步骤映射（来自 fde-workflow-triage 方向的能力链）、客户系统清单、买家角色（CFO/CHRO/VP…）；基线协议来自 fde-process-mapping 第 4 步。
- 无外部工具或 API 密钥要求。
