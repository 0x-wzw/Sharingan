---
version: 1.0.0
license: MIT
name: fde-workflow-triage
description: |
  哪些流程步骤适合交给AI；这个环节该用agent还是人工；自动化方案怎么收敛权限范围。每步只贴一个标签：删除、纯代码、智能体、人工——先删 waste 再建 agent，高风险步永远留人工。Use when 拿到流程步骤清单要判定哪些步给 AI/agent 还是留人工、或 agent 方案权限需要收敛时。
metadata:
  tags: [fde-workflow-triage]
  author: "Cangjie Distillation <agent@example.com>"
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.fde-framework.workflow-triage
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.fde-enterprise-ai-framework
  cangjie.source-title: 一图讲透 FDE：企业AI落地完整框架（v2 扩展版：+ Lab0 产品化 + Varick 实战 playbook）
---
# 工作流四分法：delete / code / agent / human

## R — Reading (原文)

> "Every step gets one label: delete, plain code, agent or human."（每一步只贴一个标签：删除、纯代码、智能体、人工。）
> —— Varick Agents FDE playbook（@startupideaspod, 2026-10-01），source/varick-fde-playbook.md

> "An agent that pays invoices end to end opens the door to phishing scams."（端到端付款的智能体会给钓鱼诈骗开门。）
> —— 同上，human-in-the-loop 桶的判例

## I — Interpretation (自述)

这是 FDE 落地的**核心决策引擎**：流程被拆成步骤后，每一步必须且只能归入四桶之一——

1. **Delete（删除）**：AI 时代这步应该消失。它的血统是 Hammer 1990（HBR《Reengineering
   Work: Don't Automate, Obliterate》）——把 22 天只剩 17 分钟实际工作的流程"提速一倍"
   只省 8 分钟，因为时间都堆在排队与交接里。先删再建，别给 waste 自动化。
2. **Plain code（纯代码）**：if X then Y，零判断。方差大？那是 switch case，不是 agent。
3. **Agent（智能体）**：需要判断 **且** 有历史数据可学。判据是"判断 + 数据"双条件——
   发票上写 monitors 大概率是办公用品（除特定供应商）、组报价（客户/金额/资源）。
4. **Human-in-the-loop（人工）**：错了代价太高的步。审批、谈判、签约、付款。
   判据不是"AI 做不到"，而是"**做错的不可逆代价**"。

判例：销售订单流程 20 步中只有 5 步进 agent 桶。四分法的产出是**步骤×桶**的映射表，
它直接决定 agent 的部署范围与人工兜底设计（与主框架的兜底旁路接口）。

## A1 — Application Example（来源案例或明确标记的演练）

来源真实案例（Varick，匿名化 AP 流程）：17 步映射后 17→7 步、24 天→6 天、
异常回环 6→1、发票直通率 18%→87%、单张成本 $31→$6（-80%）。
大部分提升来自"流程本身的修正"（删步+去回环），不是把 AI 硬贴上去。
（另：合成演练——对"报销审批"流程跑四分法：发票真伪核验=code（OCR+规则），
费用归类=agent（有历史报销数据），超标准审批=human，纸质单据拍照上传环节=delete
（直接改入口）。每步归属可按双条件复算。）

## A2 — Future Trigger ★

1. **情境**：拿到了流程图/步骤清单，决定哪些步给 AI 哪些步留人工；评估"给整条
   流程上 agent"的提案；agent 方案权限收不住要收敛。
2. **语言信号**："哪些步骤适合自动化" / "这个环节该用 agent 还是人工" /
   "workflow triage" / "human in the loop 哪些环节" / "什么该删什么该自动"。
3. **相邻区分**：与 fde-process-mapping 不同——那张卡产出步骤与回环清单（映射），
   本卡对每步做**归属判定**（分流）。与 fde-risk-human-fallback 不同——兜底卡设计
   失败退路，本卡决定哪些步一开始就不给 AI。

## E — Execution (可执行步骤)

**输入契约**：已映射的流程步骤清单（来自 fde-process-mapping），含每步的判断
含量与历史数据可得性。缺历史数据信息时先询问——"agent 桶"要求判断+数据双条件。

1. **逐桶判定**（顺序执行，先删后建）：
   a. 这步在 AI 时代还应存在吗？→ 否 → **Delete**（记录删除理由）；
   b. 零判断可执行？→ 是 → **Plain code**；
   c. 需要判断 **且** 有历史数据？→ 是 → **Agent**（标注所用数据源；数据成熟度
      台阶须 ≥ AI READY——低于此线降级 code/human，见路由卡原则 8）；
   d. 做错的不可逆代价高（钱/法务/信任）？→ 是 → **Human**（标注审批人角色）。
2. **边界检查**：每个 Agent 桶步骤必须回答"错了谁接"（→ 接 fde-risk-human-fallback
   兜底设计）；每个 Human 桶步骤必须回答"AI 在旁边能帮什么"（辅助而非替代）。
3. **配比审视**：统计四桶分布。Agent 桶 = 0（过保守）或 = 全部（过激进）都触发复审。
   来源判例：20 步中 5 步进 agent 是健康比例的参考。
4. **输出契约**：步骤×桶映射表（步骤 / 桶 / 判定依据 / Agent 桶的数据源 / Human
   桶的审批角色 / Delete 桶的消失后去向），并测算分桶后的预期步数与周期变化。

## B — Boundary (边界)

- **不要**用于：还没做流程映射就先分桶（先映射后分桶，顺序不可倒）；把四分法
  当组织裁员依据（本卡只分派工作方式，不做人事结论）。
- **失败模式**：给"零判断"步骤上 agent（成本翻倍无收益）；给高风险步上 agent
  因为"模型很准"（来源判例：端到端付款 agent = 钓鱼诈骗之门）；忘记 Delete 桶
  （把 waste 自动化是 Hammer 批判的原罪）。
- **作者盲点**：四桶判定全凭从业者经验，来源未给量化阈值（如"判断含量"怎么测）；
  本卡用双条件与反例判例补全（E 段已标注）。桶间冲突（一步既需要判断又高风险）
  时来源未给规则——实践约定：先 Human 后优化，逐步放权。

## Purpose

流程拆成步骤后的核心决策引擎：每一步必须且只能归入四桶之一——Delete（先删 waste 再建 agent，血统 Hammer 1990）、Plain code（零判断 if-then）、Agent（判断 + 历史数据双条件）、Human-in-the-loop（做错的不可逆代价高）。产出"步骤×桶"映射表，直接决定 agent 部署范围与人工兜底设计。

## Instructions

完整可执行步骤见 `## E — Execution`；紧凑步骤列表：

1. 收集输入：已映射的流程步骤清单（含每步判断含量与历史数据可得性）；缺数据信息先询问。
2. 逐桶判定（先删后建）：应消失？→ Delete；零判断？→ Plain code；判断+数据双条件？→ Agent（数据成熟度 ≥ AI READY，否则降级 code/human）；不可逆代价高？→ Human（标注审批人角色）。
3. 边界检查：每个 Agent 桶步骤回答"错了谁接"（接 fde-risk-human-fallback）；每个 Human 桶步骤回答"AI 在旁边能帮什么"。
4. 配比审视：统计四桶分布；Agent 桶 = 0 或 = 全部触发复审（来源判例：20 步中 5 步是健康参考）。
5. 输出步骤×桶映射表（含判定依据/数据源/审批角色/删除后去向）并测算预期步数与周期变化。

## Examples

1. 输入："这条 20 步的销售订单流程哪些步给 agent？" → 期望：逐桶判定后仅约 5 步进 Agent 桶，每步附判定依据与数据源，高风险步留 Human。
2. 输入："报销审批流程怎么分桶" → 期望：发票真伪核验=code（OCR+规则）、费用归类=agent（有历史报销数据）、超标准审批=human、纸质拍照上传=delete（直接改入口）。
3. 输入："给整条付款流程上 agent 的提案怎么样" → 期望：判例否决端到端付款 agent（钓鱼诈骗之门），付款步归 Human 桶并标注审批人角色。

## Limitations

- 前提是已完成流程映射：先映射后分桶，顺序不可倒（映射 → fde-process-mapping）。
- 不做人事结论：本卡只分派工作方式，不是组织裁员依据。
- 四桶判定无量化阈值（"判断含量"怎么测来源未给），以双条件与反例判例操作化（E 段已标注）。
- 桶间冲突（一步既需判断又高风险）来源未给规则，实践约定：先 Human 后优化、逐步放权。

## Troubleshooting

- 错误：agent 无权限收敛、方案权限范围失控。原因：没逐桶判定就整条流程上 agent。解决：回到逐桶判定，只有判断+数据双条件步进 Agent 桶。
- 错误：给零判断步骤上了 agent。原因：误把方差当判断。解决：方差大是 switch case，归 Plain code，成本翻倍无收益的 agent 拆掉。
- 错误：高风险步被自动化。原因："模型很准"说服了评审。解决：判据是不可逆代价不是准确率，钱/法务/信任步永远留 Human。
- 错误：分桶后收益低于预期。原因：忘了 Delete 桶，把 waste 自动化。解决：先删后建，记录每步删除理由与消失后去向。

## Prerequisites

- 输入契约要求：来自 fde-process-mapping 的流程步骤清单，含每步判断含量与历史数据可得性；Agent 桶数据成熟度须 ≥ AI READY（路由卡原则 8）。
- 无外部工具或 API 密钥要求。
