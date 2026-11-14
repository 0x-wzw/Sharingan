# ReAct 输出格式 (p63) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 7 章 | 绑定单元: p63 (母方法: f22 ReAct agent 循环, 见 f22-react-agent-loop.md) | 支持材料: ce15
> 去向: source-router 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "Thought: ... Action: the action to take, should be one of [{tool_names}]\nAction Input: ...\nObservation: ...\n... (this Thought/Action/Action Input/Observation can repeat N times)\nFinal Answer: the final answer to the original input question"

— Alammar & Grootendorst, ch07 (chapter07_Chapter 7 - Advanced Text Generation Techniques and Tools.txt @298-304; @340 handle_parsing_errors=True)

自译: 模型按 Thought→Action→Action Input→Observation 四字段循环输出, Action 只能取 tool_names 之一, 可重复 N 轮, 直到 Final Answer。

## I — Interpretation (自述)

这是 f22 循环的文本协议契约: 四字段是解析器的锚点, {tool_names} 约束防幻觉工具, "repeat N times" 说明循环结构, handle_parsing_errors=True 是解析失败时的容错约定 (错误回喂而非崩溃)。模板变量的 input_variables 含 tools/tool_names/input/agent_scratchpad (@313), scratchpad 用于拼接历史轮次。

## A1 — Application Example

### 示例: 一轮 ReAct 轨迹复算 (合成, 依据原书模板)

- **类型与来源**: 原书未逐轮展示运行轨迹 (未说明), 以下为按 p63 模板构造的合成演练。
- **问题/输入**: 需搜索的问题。
- **方法论的使用**: 模型出 "Thought: I should search" → "Action: duckduckgo_search" → "Action Input: <query>" → 执行器回填 "Observation: <结果>" → 下一轮或 "Final Answer: ..."。
- **结论/预期输出**: 每段有协议锚点可解析; Action 若写未知工具名, 解析层报错并回喂。

## A2 — Future Trigger ★

### 情境 / 语言信号

1. 手写 agent 解析器/模板; 关键词 "Thought Action Observation / agent_scratchpad / handle_parsing_errors"。

### 与相邻 skill 区分

- f22 是 agent 搭建全流程; 本卡是输出格式契约。结构化 JSON 输出走 f19 (不同协议)。

## E — Execution

**必需输入**: 工具清单 (name/description)。

1. 模板含四字段 + Final Answer, Action 候选注入 {tool_names}, input_variables 齐 (@313)。
2. 解析器按锚点切段; 失败 → 回喂错误重试 (handle_parsing_errors), 设最大轮数。
3. 终止以 Final Answer 为准。

**输出契约**: 轨迹记录 + 最终答案; 完成标准 = 每轮可解析且答案有观察支撑。

## B — Boundary

- 不要用于: 固定步骤流水线 (链式更稳); 需要 JSON 机器契约处 (走 f19)。
- 版本边界 (ce15): 旧版 LangChain agent 类已弃用; 协议思想迁移到当前工具调用 API (原生 function calling) 时, 文本协议部分由 API 承担。
- 风险: 无最大轮数兜底时, 模型可无限循环烧 token。

## 相关能力 (also_read, 阶段 3)

- composes-with: `f22-react-agent-loop` (ReAct 循环与输出格式)
