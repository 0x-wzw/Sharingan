# 七段 prompt 结构 (p44) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 6 章 | 绑定单元: p44 (母方法: f17 六要素结构法, 见 f17-prompt-six-elements.md) | 支持材料: ce15
> 去向: source-router 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "query = persona + instruction + context + data_format + audience + tone + data"

— Alammar & Grootendorst, ch06 (chapter06_Chapter 6 - Prompt Engineering.txt @137)

自译: 一个完整 prompt 由七段字符串顺序拼接——角色、指令、背景、输出格式、受众、语气、待处理数据; 每段一行, 以换行分隔。

## I — Interpretation (自述)

这是 f17 六要素结构法的编码约定: 七个槽位、固定顺序、直接字符串拼接。价值在于把"写 prompt"变成"填模板"——每段职责单一, 便于复用与消融。执行要点: 各段都写完整句子并换行分隔; data 恒在最后; 任何一段缺失都先问用户而不是留空或删槽。

## A1 — Application Example

### 示例: 论文摘要 prompt 拼装 (原书代码例 + 合成消融)

- **类型与来源**: 原书 worked_example 代码 (ch06 persona="You are an expert in Large language models..." 七段全文); 消融结果未展示, 未说明。逐段增删对照为按书内注释规则构造的合成演练。
- **问题/输入**: 总结一篇论文。
- **方法论的使用**: 按 L137 顺序拼 query → 运行; 删 data_format 段重跑, 对比输出结构差异。
- **结论/预期输出**: 拼装正确即输出含 bullet+段落结构; 删 data_format 后结构漂移, 验证该段责任。

## A2 — Future Trigger ★

### 情境

1. 用户要求把一段需求"结构化成 prompt"或审查 prompt 缺什么段。
2. 复用场景: 同一模板换 data 反复使用。

### 语言信号

- "prompt 模板 / 七要素 / persona instruction context / 怎么拼 prompt"

### 与相邻 skill 区分

- f17 是完整方法论 (含消融调试); 本卡是七段拼装规则本身。推理增强 (f18) 与硬格式 (f19) 各自解决正确率与机器可解析问题。

## E — Execution

**必需输入**: 任务描述 + 待处理文本; 任一槽位素材缺失时逐项询问。

1. 按序写七段 (每段一句, 换行分隔): persona / instruction / context / data_format / audience / tone / data。完成标准: 七段齐、data 在末。
2. 拼接运行, 存基线输出。
3. 输出不佳 → 逐段消融定位 (一次一段)。

**输出契约**: 拼好的 prompt (分段标注) + 消融记录; 完成标准 = 输出满足 data_format。

## B — Boundary

- 不要用于: 已有成熟模板的微调/模型内建结构; 单轮闲聊。
- 顺序约定是本书口径, 不是行业强制标准; 与现有团队模板冲突时以用户模板为准。
- 版本边界 (ce15): 示例基于旧 API, 对现代模型七段敏感度更高, 消融需重验。

## 相关能力 (also_read, 阶段 3)

- composes-with: `f17-prompt-six-elements` (同主题双卡), `rag-retrieval-pipeline` (RAG 模板设计)
