---
version: 1.0.0
license: MIT
name: fde-process-mapping
description: |
  帮我们摸清现有流程的现状；AI项目ROI基线怎么定；多地区多系统的流程盘点。先建 human API：访谈与过程挖掘对账出真实流程，回环按钱和时间计价，KPI 基线在动工前锁定。
metadata:
  tags: [fde-process-mapping]
  author: "Cangjie Distillation <agent@example.com>"
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.fde-framework.process-mapping
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.fde-enterprise-ai-framework
  cangjie.source-title: 一图讲透 FDE：企业AI落地完整框架（v2 扩展版：+ Lab0 产品化 + Varick 实战 playbook）
---
# 流程映射与基线：human API 与"先基线后建设"

## R — Reading (原文)

> "Build a 'human API' before you build a single agent."（在写第一个 agent 之前，
> 先建一张"human API"。）—— Varick Agents FDE playbook，source/varick-fde-playbook.md

> "We find the real process. We measure the time, baseline all of the KPIs."（Vas, Varick Agents）

## I — Interpretation (自述)

FDE 的第一步永远是**搞清真实流程**——不是组织架构图上写的流程，而是实际发生的
那一条。方法拼图：

1. **Human API**：把"一件事现在怎么流转"当成 API 来逆向——谁调用谁、传什么、
   超时怎么办。来源案例：收购了 8 家公司、5 个地区、23 套系统——芝加哥跑
   SAP+Salesforce+Workday，多伦多跑 NetSuite+HubSpot+ADP。同一业务动作在
   不同站点走完全不同的路。
2. **双工具**：访谈（人怎么说）+ 过程挖掘（系统里实际怎么跑，如 CRM 数据上
   跑 process mining）。来源判例：访谈说 6 步，挖掘出 14 步；20 步里 7 个回环，
   61% 的请求提前回环、法务打回 12%、30% 的报价要重走审批。
3. **回环计价**：每个回环按金钱与时间双重计价。"合作方打回 35%" 这种数字
   就是 ROI 叙事的弹药。
4. **基线先行**：所有 KPI 在动工前测好基线。来源铁律："baseline before you
   build"，6 个月后拿出 before/after 对比。没有基线，就没有可证明的价值。

这一步对应主框架"方案定义阶段的流程拆解"，但把执行细节补齐了：访谈+挖掘
双源、回环计价、基线协议。

## A1 — Application Example（来源案例或明确标记的演练）

来源真实案例（60 人会计事务所，$12M 营收，400 客户，4 套系统）：客户送账的
格式五花八门（包括笔记本拍照）；自称 6 步，实测 14 步；催款 70% 要二次跟进；
合作方打回率 35%。AP 流程（Fortune 1000 客户）：访谈+挖掘 2–3 周完成映射，
产出 17→7 步、24 天→6 天、直通率 18%→87%、$31→$6/张。
（合成演练：为"月结流程"写基线协议——基线指标=结账天数/调整分录数/加班小时，
测量窗口=近 3 个完整月结周期，数据源=ERP 时间戳+工时系统；复算可验。）

## A2 — Future Trigger ★

1. **情境**：刚接手一个客户/一家公司的 AI 落地，要先摸清现状；项目谈崩于
   "AI 没带来可证明的价值"（缺基线）；多地区多系统负债整合。
2. **语言信号**："流程梳理/现状调研" / "process mapping" / "怎么算 ROI" /
   "基线怎么定" / "human API" / "process mining" / "systems of record 盘点" /
   "我们流程很乱，先帮我们理清"。
3. **相邻区分**：与 fde-opportunity-discovery 不同——那张卡是"找值得做的场景"，
   本卡是"把选定流程的真实运行方式与基线摸透"。与 fde-solution-definition 的
   流程拆解不同——那张卡产出数据标准（定义层），本卡是现场作业方法（执行层）。

## E — Execution (可执行步骤)

**输入契约**：目标流程名、客户/组织的系统清单（哪怕是粗列表）、访谈对象范围。
系统清单完全未知时，先做 Monday 盘点（见下）再继续。

1. **系统盘点（human API 第一层）**：列出所有系统 of record 与每条业务路径的
   站点差异。完成标准：系统×地区矩阵成形，每格标注"谁在用/存什么"。
2. **双源映射**：访谈（每角色 30–60 分钟）+ 过程挖掘（在 CRM/ERP/工单系统上
   拉事件日志）。完成标准：步骤清单 = 访谈版与挖掘版**对账后的合并版**，
   两者差异显式记录（差异即发现）。
3. **回环标注与计价**：标出每个回环（谁打回/打回率/重做成本），按钱和时间
   双重计价。完成标准：每个回环有 $ 与小时数。
4. **基线协议**：选定成功指标（与 fde-solution-definition 的目标定义衔接），
   测好基线值与测量窗口，写进文档。完成标准：每个 KPI 有基线数字+取数口径。
5. **输出契约**：流程现状包——步骤清单（含回环与打回率）、系统×地区矩阵、
   回环计价表、KPI 基线协议。

## B — Boundary (边界)

- **不要**用于：还没跑这条流程的现状（新流程设计用别的卡）；拿访谈当真值
  （必须与系统数据对账——"说 6 步实际 14 步"是常态不是例外）。
- **失败模式**：跳过基线直接建设（6 个月后无法证明价值=白干）；只做单点映射
  忽略站点差异（23 套系统就要 23 套真相）；把过程挖掘当万能（没有数字痕迹的
  线下环节仍要靠访谈）。
- **作者盲点**：来源未给访谈/挖掘的配比与抽样量；未处理"员工怕被自动化而
  隐瞒真实流程"的政治学问题——实践约定：先承诺"先删 waste 再谈人"的顺序来
  换取真实信息。

## Purpose

The FDE first step is always to find the real process — not the one on the org chart. Builds a "human API" before any agent is written: reconciles interviews with process mining to reconstruct the actual flow, prices every loop in money and time, and locks KPI baselines before build ("baseline before you build"), so value can be proven with before/after six months later.

## Instructions

Follow the full executable procedure in the `## E — Execution` section; the canonical step sequence is:

1. Systems inventory (human API layer 1): list all systems of record and per-site differences per business path — complete when a system×region matrix exists with "who uses it / stores what" per cell.
2. Dual-source mapping: interviews (30–60 min per role) + process mining (event logs from CRM/ERP/ticketing) — the step list is the reconciled merge, with interview-vs-mining differences explicitly recorded (differences are findings).
3. Loop annotation and pricing: mark every loop (who rejects / rejection rate / rework cost), priced in both dollars and hours.
4. Baseline protocol: pick success metrics (linking to fde-solution-definition's target definition), measure baseline values and measurement window, write them into a document — every KPI gets a baseline number and extraction definition.
5. Output contract: the process status package — step list (with loops and rejection rates), system×region matrix, loop pricing table, KPI baseline protocol.

## Examples

- Input: a 60-person accounting firm ($12M revenue, 400 customers, 4 systems) where documents arrive in every format including notebook photos → interviews claim 6 steps, mining finds 14; 70% of collections need second follow-up; partner rejection rate 35% — the priced loops become the ROI narrative.
- AP process for a Fortune 1000 customer: 2–3 weeks of interview+mining mapping → output 17→7 steps, 24 days→6 days, straight-through rate 18%→87%, $31→$6 per invoice.
- "刚接手一个客户，AI落地从哪开始" / "怎么算 ROI" → run the Monday systems inventory, then dual-source mapping, then lock the baseline protocol before any build.

## Limitations

- NOT for processes that have not yet run (new-process design belongs to another card).
- Interviews are never ground truth — they must be reconciled against system data ("said 6 steps, actually 14" is the norm, not the exception).
- Process mining is not universal: offline steps without digital traces still require interviews (失败模式).
- The source gives no interview/mining ratio or sampling sizes, and does not handle the politics of staff hiding the real process for fear of automation — the working convention is to commit to "delete waste first, then talk about people" to buy truthful information (作者盲点).

## Troubleshooting

- **Error:** Six months later there is no provable value. **Cause:** Build started before baselines were measured (跳过基线直接建设). **Solution:** Baseline every KPI before construction — without a baseline there is no provable value (失败模式).
- **Error:** Step list matches interviews but not reality. **Cause:** Interviews taken as truth without reconciliation against system event logs. **Solution:** Always run dual-source mapping and record the interview-vs-mining diff explicitly.
- **Error:** One mapping that ignores site differences. **Cause:** Single-point mapping while the same business action runs differently per site (23 systems = 23 truths). **Solution:** Complete the system×region matrix before mapping.
- **Error:** Process mining yields nothing for some steps. **Cause:** Those steps are offline with no digital traces. **Solution:** Cover them via interviews — mining is one of two sources, not a replacement (失败模式).

## Prerequisites

- Input contract: target process name, the organization's system list (even a rough one), and the interviewee scope. If the system list is entirely unknown, do the Monday inventory first, then continue.
- No external tools, API keys, or network access are required.
