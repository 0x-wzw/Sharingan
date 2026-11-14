# 多步任务链式拆解 (f20) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 6/7 章 | 绑定单元: f20 | 支持材料: ce15 (LangChain 弃用缺口)
> 去向: source-router (llms-from-scratch-router) 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测" (f20 缺口: LangChain LLMChain API 已弃用, 阶段 3/4 需按 LCEL 新写法核查)

## R — Reading (原文)

> "Create a title for a story about {summary}. Only return the title." ... "Describe the main character of a story about {summary} with the title {title}. Use only two sentences."

— Alammar & Grootendorst, ch07 (chapter07_Chapter 7 - Advanced Text Generation Techniques and Tools.txt @100/@113; Chain Prompting: title → character → story 三链组合, output_key 逐级传递)

自译: 链式提示把复杂任务拆成多个单步 prompt, 上一步的输出作为下一步 prompt 的输入变量 (如 title 注入 character 链), 产物逐级精化。

## I — Interpretation (自述)

一个 prompt 里同时"起标题、造人物、写故事", 任一环失败全盘报废且难定位。Chain Prompting 把它拆成串联的窄任务: 每个链只做一件事、易调试、可缓存中间产物 (标题不用重跑)、可在任意链换模型 (标题用小模型, 故事用大模型)。核心机制是变量注入: 上游 output_key 成为下游 prompt 的 {占位符}。代价是延迟叠加与上游错误的传播 (标题起差, 故事跟着差), 所以关键链要加校验/重试。

## A1 — Application Example

### 示例: 标题→角色→故事三链 (原书 ch07 代码例 + 合成复算)

- **类型与来源**: 原书 worked_example (chapter07 代码块); 运行结果正文未展示成稿 (未说明)。
- **问题/输入**: 一段 summary, 要产出完整故事。
- **方法论的使用**: 链 1 用 {summary} 生成 title (output_key="title"); 链 2 用 {summary}+{title} 生成两句话的角色描述; 链 3 用三者生成故事。每链一个 PromptTemplate, 输出经 output_key 注入下游。
- **结论**: 结构成立, 每步产物独立可查; 按规则可对任意 summary 复算 (合成复算: 任一链输出为空/超长即该链失败点, 单独重跑该链)。

## A2 — Future Trigger ★

### 情境

1. 用户的任务有明显的先后依赖 (先生成大纲, 再逐段展开, 再润色)。
2. 单个长 prompt 输出质量不稳/后半段跑题, 想拆步。
3. 问"怎么把多步流程串起来 / prompt chaining / LLMChain"。

### 语言信号

- "拆成多步 / chain / 分步生成 / 上一步结果作为下一步输入 / prompt chaining"
- "LangChain 链 / LLMChain / pipeline prompt"

### 与相邻 skill 区分

- 与 f22 (ReAct): 链式是静态流水线 (步骤预先定死); ReAct 是动态循环 (下一步取决于工具观察)。需要工具/搜索 → ReAct。
- 与 f21/p62 (记忆): 记忆是同一对话上下文管理; 链式是任务级数据传递。

## E — Execution

**必需输入**: 任务的目标产物 + 可识别的步骤序列; 步骤不清时先与用户一起列链, 不静默设计。

1. 把任务写成依赖有向链 (每链一个动词级子任务 + 输入变量)。完成标准: 每链 prompt 只含一个子任务, 依赖关系显式。
2. 为每链定 output_key 与格式约束 (结构化节点配合 f19)。
3. 逐链运行: 校验该链输出非空、符合格式; 失败 → 单链重试 (带上错误), 不整链重跑。
4. 全链通过后交付最终产物。

**输出契约**: 最终产物 + 各链中间产物存档 (便于定点重跑); 完成标准 = 末链输出满足原始任务要求。

## B — Boundary

- 不要用于: 单步就能做好的任务 (拆链纯增延迟); 需要运行时决定是否/如何调用工具的任务 (转 ReAct)。
- API 边界 (ce15): 书中 LLMChain/PromptTemplate 代码基于旧版 LangChain, 类名与用法已弃用; 迁移思路 (变量注入+单步校验) 到 LCEL 或原生循环, 照抄会 import 失败。
- 失败模式: 上游链质量差被静默传播——关键链缺校验时, 错误会到末链才暴露。

## 相关能力 (also_read, 阶段 3)

- composes-with: `f22-react-agent-loop` (链式提示是 ReAct 工具循环的前身)
