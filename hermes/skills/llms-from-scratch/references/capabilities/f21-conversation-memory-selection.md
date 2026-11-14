# 对话记忆选型 (f21) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 7 章 | 绑定单元: f21, p62 | 支持材料: ce15
> 去向: source-router (llms-from-scratch-router) 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "memory = ConversationBufferWindowMemory(k=2, memory_key=\"chat_history\")"

— Alammar & Grootendorst, ch07 (chapter07_Chapter 7 - Advanced Text Generation Techniques and Tools.txt @198)

同章 (@169/@245): `ConversationBufferMemory(memory_key="chat_history")` 与 `ConversationSummaryMemory`。自译: 三种记忆策略——全量缓存 (buffer)、滑动窗口 (window, 只留最近 k 轮)、滚动摘要 (summary, 用 LLM 把旧对话压缩成摘要)。

## I — Interpretation (自述)

LLM 本身无状态, "记得上一句"全靠把历史塞回 prompt。三种策略是 token 成本与信息保留的三角: buffer 全留——远期信息不丢, 但上下文线性膨胀终会爆; window(k) 只留最近 k 轮——成本恒定, 但 k 轮之外必忘; summary 用模型压缩旧历史——能以小 token 保留远期要点, 但每轮多一次 LLM 调用, 且摘要有损 (细节可能失真)。选型依据是"应用是否依赖远期信息 + token 预算": 记名字的闲聊窗口就够, 跨会话的项目约束需要摘要。

## A1 — Application Example

### 示例: k=2 窗口的遗忘实验 (原书实验 + 规则复算)

- **类型与来源**: 原书实验 (ch07: window k=2 下模型记得名字、忘掉年龄), 结果为原文内容。
- **问题/输入**: 多轮自我介绍对话, window k=2。
- **方法论的使用**: 每轮只回填最近 2 轮 chat_history; 年龄在第 1 轮说出, 第 3 轮询问时已滑出窗口。
- **结论**: 模型答得出名字、答不出年龄——窗口记忆"遗忘"是机制必然, 不是 bug。
- **结果**: 原书以此演示三策略差异 (最终推荐未说明, 留给任务决定)。

## A2 — Future Trigger ★

### 情境

1. 用户在搭聊天机器人/对话 agent, 遇到"聊着聊着就忘了前面说的"或"上下文费用暴涨"。
2. 问"怎么给对话加记忆 / chat memory / conversation history 管理"。
3. 上下文超长报错, 需要压缩历史。

### 语言信号

- "对话记忆 / chat memory / ConversationBufferMemory / 记不住前面的话 / 上下文太长"
- "窗口记忆 / summary memory / 聊天历史压缩"

### 与相邻 skill 区分

- 与 f20 (链式): 链式传的是任务变量, 本卡传的是对话历史。
- 与 f22 (ReAct): agent 内部也有 scratchpad 记忆, 但本卡面向多轮用户对话层。

## E — Execution

**必需输入**: 对话场景 (是否需远期信息)、预期轮数/token 预算; 缺任一项时询问。

1. 判定远期依赖: "第 1 轮的信息第 20 轮还要用吗?" 否 → window (k 按业务轮数定); 是 → 继续。
2. 判定预算: 历史总量远小于上下文窗口 → buffer; 接近/超出 → summary。
3. 实现: 选对应 Memory 类, memory_key 与 prompt 模板对齐。
4. 验证: 用"早轮信息晚轮提问"探针测试 (如先报年龄, 20 轮后问年龄)。判停: 探针失败 → 策略与需求不匹配, 换级。

**输出契约**: 所选策略 + k/摘要 prompt 配置 + 探针测试结果; 完成标准 = 探针通过且 token 用量在预算内。

## B — Boundary

- 不要用于: 单轮问答; 无状态批处理。
- 有损边界: summary 是模型生成, 可能漏掉用户在意的细节; 关键事实 (ID/约束) 应显式存结构化状态而非靠摘要。
- 版本边界 (ce15): 书中 langchain.memory API 已大幅重构 (ConversationXxxMemory 多已弃用), 迁移思路到 LCEL/消息历史或应用层实现。
- 相邻混淆: 不要把"长期用户画像存储"误当对话记忆——那是数据库设计, 不是本卡。

## 相关能力 (also_read, 阶段 3)

- composes-with: `p62-conversation-memory-three-strategies` (同主题双卡), `f22-react-agent-loop` (多轮 agent 记忆)
