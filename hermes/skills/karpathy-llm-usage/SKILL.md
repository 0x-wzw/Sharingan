---
version: 1.0.0
license: MIT
name: karpathy-llm-usage
description: |
  Karpathy "Deep Dive into LLMs" 能力包：把 LLM 当有损压缩包使用的心智模型、context window 管理、thinking model 选择、deep research 与代码执行工作流、模型档位核查与输出验证纪律；附 vibe coding 与多模态两张 router 卡。不教授 agent harness/loop/graph 工程。Use when 用户纠结 model tier/thinking model、context window 何时开新对话、deep research 初稿如何验证引用、或精确计算/绘图是否可信任模型直接输出时。
metadata:
  tags: [karpathy-llm-usage]
  author: "Cangjie Distillation <agent@example.com>"
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: single
  cangjie.bundle-id: bundle.karpathy-llm-deep-dive
  cangjie.capability-count: 3
  cangjie.entrypoint-count: 1
---
# Deep Dive into LLMs like ChatGPT (Andrej Karpathy, ~2h06m video, Feb 2025) — 全书能力入口

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- agent harness / loop / graph 工程设计 (推文误标的内容不存在于本讲座)
- 具体产品定价与档位细节 (时效快照，见 needs-review)

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. LLM 是互联网的有损概率压缩 (有知识截止日)，默认无工具无浏览
2. context window 是共享工作记忆，换主题就开新对话
3. 难数学/代码才用 thinking model，接受分钟级延迟
4. 精确计算/绘图必须走代码执行，不信模型直接报的数
5. 一切输出先验证：报告查引用、代码查隐含假设

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 决定何时用 thinking model 处理任务；管理 context window / 决定何时开新对话；用 deep research 做带引用调研并验证；让 LLM 正确计算、画图、做数据分析；核查当前 app 实际使用的模型与可用工具；建立输出验证纪律 (引用核对、代码假设审查) | references/capabilities/karpathy-llm-usage.md | references/capabilities/vibe-coding-cursor.md、references/capabilities/multimodal-io.md |
| 用自然语言快速生成小型应用/原型；使用 Cursor composer 跨文件自主编辑 | references/capabilities/vibe-coding-cursor.md | — |
| 判别 LLM app 语音模式的能力 (native vs 转写)；用图像/文档作为 LLM 输入 | references/capabilities/multimodal-io.md | — |

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

- 用户要构建 agent 系统架构 → 转交 agent 工程类资源
- 需要逐字引文核对 → 原始 captions 不可得，只有 notes-layer 证据

## Purpose

把 Karpathy《Deep Dive into LLMs》(2025-02, ~2h06m) 的使用心智模型变成可路由的入口：LLM 是有知识截止日的有损压缩包、context window 是共享工作记忆、难任务才用 thinking model、精确计算/绘图必须走代码执行、一切输出先验证。作为 router：按意图加载 1 张能力卡；不教授 agent harness/loop/graph 工程。

## Instructions

1. 每次任务先读本文件；概览/书名/术语类问题用「核心原则」与 references/overview.md 回答，不加载能力卡。
2. 能力类问题按「能力路由」表按意图加载 **1** 张能力卡（任务明确跨域时最多 2 张）。
3. 输入契约：待完成的 LLM 任务描述；缺任务类型（问答/推理/计算/调研）、可用 app 与档位、是否需引用或数字精度时，先询问，不得静默假设工具可用。
4. 交付前验证（每项产物有验证记录）：报告 → 引用逐条点开核对；代码 → 列出隐含假设（单位、时间范围、过滤条件、舍入）逐条确认；计算 → 与独立来源或二次运行交叉核对。
5. 路由表与 capability-index.md 都无法命中的意图，明确告知超出范围，不要硬套。

## Examples

1. 输入："这个任务该用 o1 吗？"（模型档位困惑）→ 期望：按"难数学/代码才用 thinking model，接受分钟级延迟"原则给判据，并核查当前 app 实际使用的模型与可用工具，加载 karpathy-llm-usage 能力卡。
2. 输入："对话太长太乱了，它开始答非所问"（context window 膨胀）→ 期望：解释 context window 是共享工作记忆、塞入无关 token 既拖慢又干扰，换主题就开新对话（加载同一能力卡）。
3. 输入："帮我做 deep research，带引用" → 期望：说明 deep research 产物是 thinking + 多轮搜索的 ~10 分钟**初稿**，交付前引用逐条点开核对，再加载能力卡。
4. 输入："它算出来的这个数不对/帮我画个图"（代码执行正确性）→ 期望：数值计算、绘图、数据分析必须走"模型写程序 → app 执行 → 结果回填"循环，模型直接报的精确数字是采样产物不是计算结果。

## Limitations

- 不适用：agent harness/loop/graph 工程设计（讲座内容不存在此主题，转交 agent 工程类资源）；具体产品定价与档位细节（时效快照，见 needs-review）。
- 证据层：原始 captions 不可得，全部内容来自 blumify AI 浓缩时间戳 notes-layer 转述——无法逐字引用，按带时间戳的转述代替；未经录像核对的细节见 needs-review.md (NR-01..04)。
- 多模态语音能力对比是轶事 (NR-04)，不作规则引用；纯文本 prompt 任务走主技能。
- 每次任务最多加载 2 张能力卡，不并行加载全部。

## Troubleshooting

- 错误：把该技能用于设计 agent 架构。原因：触发词含"LLM/agent"产生误路由。解决：按「边界与判停」转交 agent 工程类资源，本包不覆盖。
- 错误：引用了逐字原话。原因：误把 notes-layer 转述当原文。解决：只作带时间戳转述；逐字核对需求一律声明 captions 不可得。
- 错误：模型直接报的精确数字被当成计算结果。原因：混淆采样产物与代码执行结果。解决：精确计算/绘图/数据分析一律走代码执行循环并交叉核对。
- 错误：意图在路由表与 capability-index.md 都不命中却硬套。解决：明确告知超出本书范围。

## Prerequisites

- 无外部工具、API 密钥或运行时依赖；所需材料全部在本技能 references/ 内（capabilities 卡、overview.md、glossary.md、cheatsheet.md、capability-index.md、needs-review.md）。
