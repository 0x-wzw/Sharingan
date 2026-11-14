# 对话记忆三策略 (p62) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 7 章 | 绑定单元: p62 (母方法: f21 对话记忆选型, 见 f21-conversation-memory-selection.md) | 支持材料: ce15
> 去向: source-router 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "memory = ConversationBufferMemory(memory_key=\"chat_history\")" / "memory = ConversationBufferWindowMemory(k=2, memory_key=\"chat_history\")" / "ConversationSummaryMemory"

— Alammar & Grootendorst, ch07 (chapter07_Chapter 7 - Advanced Text Generation Techniques and Tools.txt @169/@195-198/@245-248)

自译: buffer 全量、window(k) 截窗、summary 压缩——三种把历史塞回 prompt 的策略, 对应信息保留与 token 成本的不同取舍点。

## I — Interpretation (自述)

三策略一句话: buffer 不丢信息但爆上下文; window 成本恒定但 k 外必忘; summary 保留远期要点但每次多一次 LLM 调用且摘要有损。按"远期依赖有无 × token 预算"二问定位, 细节判据与验证方法见 f21 卡。

## A1 — Application Example

### 示例: k=2 记名字忘年龄 (原书实验)

- **类型与来源**: 原书实验 (ch07)。
- **问题/输入**: 多轮自我介绍, window k=2。
- **方法论的使用**: 只回填最近 2 轮; 第 1 轮的年龄滑出窗口。
- **结果**: 记得名字、忘年龄——窗口遗忘为机制必然 (原书内容, 未给出推荐策略, 未说明)。

## A2 — Future Trigger ★

### 情境 / 语言信号

1. 聊天应用"忘了前面"或费用暴涨; 关键词 "ConversationBufferMemory / chat memory / 上下文压缩"。

### 与相邻 skill 区分

- f21 是选型决策框架; 本卡是三策略本身与代码形态。链式 (f20) 传任务变量, 非对话历史。

## E — Execution

**必需输入**: 对话场景的远期依赖与预算。

1. 二问定位: 远期要用早轮信息? 预算充裕? → buffer / window(k) / summary。
2. 实现 + memory_key 对齐 prompt 模板。
3. 探针验证 (早轮信息晚轮提问)。判停: 探针失败换策略。

**输出契约**: 策略 + 参数 + 探针结果。

## B — Boundary

- 不要用于: 单轮任务; 长期用户画像存储 (那是数据库)。
- 有损边界: summary 可能丢细节, 关键事实走结构化存储。
- 版本边界 (ce15): langchain.memory 已重构, 思路迁移到 LCEL/消息历史。

## 相关能力 (also_read, 阶段 3)

- composes-with: `f21-conversation-memory-selection` (同主题双卡)
