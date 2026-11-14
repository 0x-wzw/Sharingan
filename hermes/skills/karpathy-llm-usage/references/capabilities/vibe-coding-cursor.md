# Cursor vibe coding 工作流 (vibe-coding-cursor) — Router 能力卡

> 来源: Karpathy *Deep Dive into LLMs* [1:08:18] | 绑定单元: f06 | 支持材料: c04, g05, g06
> 证据层: notes-layer 转述 (原始 captions 不可得) | 去向: source-router (karpathy-llm-usage-router) 服务

## R — Reading (notes-layer 转述)

- "[1:08:18] Cursor + Claude 3.7 Sonnet API, full project context; composer = autonomous agent editing across files; tic-tac-toe app from ~5 sentences, installed libraries, confetti, sound file; fallback to manual programming always available."

## I — Interpretation

Vibe coding 的骨架: 用自然语言意图驱动 AI 编码工具产出可运行项目, 而非手写代码。三个要素: (1) 工具持有全项目上下文 (不只单文件); (2) composer 类 agent 模式可跨文件自主创建/编辑; (3) 产出后人工验证, 手动编程始终是 fallback。适用边界是原型/小应用, 不是生产代码。

## A1 — 来源案例 (c04)

井字棋小应用: ~5 句自然语言描述 → composer 自动安装依赖库、加 confetti 动画、配声音文件, 产出完整可运行 app。结果: 书中演示成功 (notes-layer)。

## A2 — Future Trigger

用户想"几句话做一个 app/网页/小工具"、提到 Cursor composer/agentic editor、要求快速原型; 不适用于已有生产代码库的维护、评审, 或 agent 系统设计 (转主技能 B 段)。中文: vibe coding、快速原型、Cursor。

## E — Execution

1. 配置工具: Cursor + 强模型 API (以当前可用模型为准, 原文提及的 Claude 3.7 已时效)。完成标准: composer 可用。
2. 用几句自然语言写清意图描述 (功能、外观、交互)。完成标准: 描述覆盖验收点。
3. 让 composer 跨文件生成; 运行验证产出是否可跑、是否符合意图。
4. 分支: 产出不符 → 补充描述迭代; 工具/agent 失效 → 切手动编程 fallback, 不死磕。

输出契约: 可运行的本地项目 + 运行验证记录。

## B — Boundary

- 不适用于生产级、安全关键代码 — 作者明确保留手动编程 fallback; g05 定义即"接受代码为黑盒快速产出"。
- 依赖具体产品能力 (composer), 时效快照; agent harness/图架构设计不在本卡 (ce04 防护)。
