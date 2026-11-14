# ReAct agent 循环 (f22) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 7 章 | 绑定单元: f22, p63 | 支持材料: ce15
> 去向: source-router (llms-from-scratch-router) 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "Thought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: ...\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question"

— Alammar & Grootendorst, ch07 (chapter07_Chapter 7 - Advanced Text Generation Techniques and Tools.txt @298-304; agent 构造配 handle_parsing_errors=True @340)

自译: ReAct 用纯文本协议驱动 agent——模型交替输出 Thought(思考)/Action(从 tool_names 中选工具)/Action Input, 执行器回填 Observation, 循环到模型自己宣布"I now know the final answer"为止。

## I — Interpretation (自述)

ReAct 是 agent 的最小思维模型: 推理 (Thought) 决定下一步行动, 行动 (Action) 调工具, 工具结果 (Observation) 回填进上下文, 循环往复直到信息足够。三个工程要点: ①Action 必须限定在 [{tool_names}] 内, 否则模型会发明不存在的工具; ②工具的 description 是模型选工具的唯一依据, 写得含糊选择就错; ③解析必须容错 (handle_parsing_errors=True), 模型输出偏离模板时把错误回喂而非崩溃。终止条件由模型自宣 (Final Answer), 须配最大迭代数兜底。

## A1 — Application Example

### 示例: 搜索型问题的一次循环 (原书 ch07 DuckDuckGo agent; 运行结果正文未列最终答案, 未说明)

- **类型与来源**: 原书 worked_example (ch07 代码, AgentExecutor + handle_parsing_errors=True + DuckDuckGo 工具)。
- **问题/输入**: 需要外部信息才能回答的问题。
- **方法论的使用**: initialize_agent(llm, tools=[duckduckgo-search], agent=zero-shot-react-description, verbose=True) → 模型出 Thought → Action: duckduckgo_search + 查询词 → 执行器跑搜索, 结果作 Observation 拼回 → 循环 → Final Answer。
- **结论**: 按协议可对任意需检索的问题复算循环轨迹; 每轮 Thought/Action/Observation 全程可见 (verbose)。

## A2 — Future Trigger ★

### 情境

1. 用户要"能自己查资料/调工具/多步办事"的 agent, 而不是一次问答。
2. agent 不调用工具或调错工具、输出格式坏掉导致循环崩溃。
3. 问"ReAct 怎么实现 / agent 循环 / 工具调用协议"。

### 语言信号

- "ReAct / agent loop / Thought Action Observation / tool calling agent"
- "让它自己搜/自己调工具 / agent 老是不用工具"

### 与相邻 skill 区分

- 与 f20 (链式): 链式步骤静态; ReAct 步骤由模型运行时决定。
- 与 f18 (推理增强): 纯脑内推理无工具维度; 两者可叠加 (Thought 内用 step-by-step)。

## E — Execution

**必需输入**: 任务问题 + 工具清单 (每个工具必须有准确的 name/description); 缺工具描述时先补写, 不给空壳工具。

1. 定义工具集: 每工具 name + description + 输入格式。完成标准: description 能让"只看文字的模型"区分相邻工具。
2. 写 ReAct 模板 (Thought/Action/Action Input/Observation/Final Answer, Action 限 {tool_names}, p63)。
3. 构建执行循环: 解析 Action → 执行 → 回填 Observation; 解析失败 → 回喂错误重试 (handle_parsing_errors); 设最大迭代数 N 兜底。
4. 终止: 出现 Final Answer 或达 N 轮。达上限未出答案 → 如实报告卡点 (哪个工具反复失败), 不伪造答案。

**输出契约**: 最终答案 + 完整轨迹 (每轮 Thought/Action/Observation); 完成标准 = 答案有工具观察支撑。

## B — Boundary

- 不要用于: 不需要外部信息/动作的任务; 步骤固定可预知的流水线 (链式更省更稳)。
- 协议边界: Action 只能从 tool_names 选; description 质量决定选择质量, 是书中的明确行为约束。
- 版本边界 (ce15): 书用旧版 LangChain initialize_agent, 已弃用; 思路迁移到当前 agent API/原生循环。bonus_9_agents.md 是现代 SDK 视角, 与本章文本协议不混用。
- 风险: 工具执行有真实副作用 (下单/发帖) 时必须加人工确认层; 书中演示只含只读搜索。

## 相关能力 (also_read, 阶段 3)

- composes-with: `p63-react-output-format` (ReAct 输出格式约定), `f20-chain-prompting` (链式提示), `f21-conversation-memory-selection` (多轮记忆)
