# Prompt 六要素结构法 (f17) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 6 章 (Prompt Engineering) | 绑定单元: f17, p44 | 支持材料: ce15
> 去向: source-router (llms-from-scratch-router) 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "persona = \"You are an expert in Large Language models. You excel at breaking down complex papers into digestible summaries.\" ... query = persona + instruction + context + data_format + audience + tone + data"

— Alammar & Grootendorst, ch06 (chapter06_Chapter 6 - Prompt Engineering.txt @125-137; 代码注释 "The full prompt - remove and add pieces to view its impact on the generated output")

自译: prompt 由 persona(角色)、instruction(指令)、context(背景)、data_format(输出格式)、audience(受众)、tone(语气)、data(待处理文本) 七段拼装; 书明确建议逐段增删来观察其对输出的影响。

## I — Interpretation (自述)

把 prompt 从"咒语"变成可诊断的工程件: 复杂任务不靠一个天才句子, 而按六个功能槽位 (data 除外, 它是原料) 组装——谁在做 (persona)、做什么 (instruction)、背景约束 (context)、输出长什么样 (data_format)、给谁看 (audience)、什么口吻 (tone)。核心用法是组合式 + 消融式: 先填满六段得到基线输出; 输出不理想时, 逐段增删做对比, 定位起作用的组件——这把"prompt 不好使"变成可归因的调试。对重复性任务, 六要素就是一份模板, 换 data 即可复用。

## A1 — Application Example

### 示例: 论文摘要 prompt 的逐段消融 (合成演练, 依据 ch06 原文做法)

- **类型与来源**: 原书未提供完整案例叙事, 以下为按原书"remove and add pieces"规则构造的合成演练 (标注为合成)。
- **问题/输入**: 让 LLM 总结一篇 LLM 综述, 基线输出太啰嗦。
- **方法论的使用**: 基线 = 七段全拼; 删除 tone 段 → 输出风格无变化, 说明该任务 tone 非关键; 删除 data_format 段 → 输出从 bullet+段落变成大段散文, 定位问题在格式约束缺失; 回补 data_format 并收紧为"仅 3 个 bullet" → 输出达标。
- **结论/预期输出**: 六要素消融能定位失效段; 每段增删后的输出差异可直接对比复算。

## A2 — Future Trigger ★

### 情境

1. 用户的 prompt 输出不稳定/格式跑偏, 想系统化改进而不是重掷骰子。
2. 要为一个重复性任务 (摘要、改写、抽取) 写可复用的 prompt 模板。
3. 用户问"prompt 应该包含哪些部分 / 怎么写好 system prompt"。

### 语言信号

- "prompt 模板 / prompt structure / persona / system prompt 怎么写"
- "输出格式不稳定 / 让模型按固定格式回答 / tone / audience"

### 与相邻 skill 区分

- 与 f18/p45 (推理增强): 那是"让模型想得更对", 本卡是"让输出形态稳定"; 推理类难题叠加使用。
- 与 f19 (结构化输出): JSON 等硬格式契约优先用 f19 的约束手段, 本卡负责整体语义结构。

## E — Execution

**必需输入**: 任务描述 + 待处理文本; 缺任一段的素材时逐项询问 (如受众是谁、要什么格式), 不静默猜。

1. 按六槽位写模板: persona / instruction / context / data_format / audience / tone + data, 顺序固定 (p44)。完成标准: 每段一句话、无槽位空缺。
2. 拼 query 并运行, 保存基线输出。
3. 输出不达标 → 逐段消融 (一次只动一段), 记录差异, 定位责任段。
4. 修改责任段 (如 data_format 更具体), 复跑验证。判停: 连续两段增删均无影响而输出仍差 → 问题在模型能力或任务表述, 转推理增强 (f18) 或换模型。

**输出契约**: 最终 prompt 文本 (分段标注) + 消融记录表 (改动段, 输出差异); 完成标准 = 输出满足 data_format 且用户确认。

## B — Boundary

- 不要用于: 单轮简单问答 (六段全拼是过度工程); 需要 JSON 级硬保证的场景 (应上 f19 约束采样)。
- 作者边界: 书中演示为摘要任务, 各段措辞需按任务改写, 模板不是原文照抄。
- 版本边界 (ce15): 示例基于 GPT-3.5-turbo 时代 API, 现代模型对结构化 prompt 的敏感度更高, 消融结论需在新模型上重验。
- 失败模式: 六段堆满修辞但不给 data_format 的具体样例, 输出格式仍会漂移。

## 相关能力 (also_read, 阶段 3)

- composes-with: `p44-seven-segment-prompt` (同主题双卡), `rag-retrieval-pipeline` (RAG 模板设计), `instruction-finetuning-and-eval` (judge prompt 设计)
