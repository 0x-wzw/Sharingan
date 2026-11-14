# 结构化输出两层约束 (f19) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 6 章 (Prompt Engineering) | 绑定单元: f19, p46 | 支持材料: ce15
> 去向: source-router (llms-from-scratch-router) 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "response_format={\"type\": \"json_object\"}, temperature=0"

— Alammar & Grootendorst, ch06 (chapter06_Chapter 6 - Prompt Engineering.txt @332, llama-cpp-python 代码块: "Create a warrior for an RPG in JSON format.")

自译: 程序要可靠消费 LLM 输出时, 先给一个 one-shot JSON 示例做"软约束"; 仍被打破时升级为"硬约束"——用 API 的 response_format=json_object 或本地栈的文法约束采样 (grammar/constrained decoding), 并配 temperature=0 降低漂移。

## I — Interpretation (自述)

LLM 输出进程序的第一杀手是格式不合法。书的两层模型: 软约束 (prompt 里放一个目标 JSON 样例, 让模型模仿) 零基础设施、覆盖大多数场景; 硬约束 (推理引擎在采样时屏蔽不合法 token, 或 response_format 参数) 从机制上保证语法合法, 但要求 API/本地栈支持。决策规则: 软约束先行, 被打破才上硬约束——避免为偶发失败提前建本地推理栈。配套: temperature=0 减少随机漂移; 解析侧仍要容错 (重试一次, 带上错误信息回喂)。

## A1 — Application Example

### 示例 1: RPG 角色生成 (原书代码例)

- **类型与来源**: 原书 worked_example, ch06 代码块。
- **问题/输入**: "Create a warrior for an RPG in JSON format."
- **方法论的使用**: create_chat_completion + response_format={"type":"json_object"} + temperature=0。
- **结果**: 返回可直接 json.loads 的角色对象 (原书展示输出, 字段未在正文逐项点评, 未说明)。

### 示例 2: 递进判停演练 (合成, 依据 p46 规则)

- **类型与来源**: 原书未提供失败-升级案例, 以下为按规则构造的合成演练 (标注为合成)。
- **问题/输入**: 要求模型输出 {"name": str, "level": int}。
- **方法论的使用**: ①prompt 内嵌 one-shot JSON → 输出合法, 停; ②若输出夹带 "Here is the JSON: ..." 前缀 → 上 response_format 硬约束 + T=0 → 语法保证合法。
- **结论/预期输出**: 每层可判停; 层 ①失败是上 ② 的明确触发条件。

## A2 — Future Trigger ★

### 情境

1. 用户要把 LLM 输出喂给程序 (JSON/API/数据库), 遇到解析失败。
2. 问"怎么让模型一定输出 JSON / structured output / constrained decoding"。
3. 正在写 prompt 要求固定 schema, 但偶尔仍跑偏。

### 语言信号

- "JSON 输出 / structured output / json_object / schema / 约束采样 / grammar"
- "解析失败 / 输出多了说明文字 / extract JSON from response"

### 与相邻 skill 区分

- 与 f17/p44: data_format 段描述"大概格式"; 本卡保证"机器可解析"的硬契约。
- 与 f20 (链式): 链式各节点间传结构化数据时, 每个节点内部用本卡。

## E — Execution

**必需输入**: 目标 schema (字段名/类型); 缺 schema 时先与用户确认, 不猜字段。

1. 写软约束 prompt: 指令 + one-shot 合法 JSON 示例 (字段与 schema 完全一致)。
2. 运行并尝试解析 (json.loads)。成功 → 停。
3. 失败 → 判定栈能力: API 支持 response_format / 本地栈支持文法约束 → 上硬约束 + temperature=0; 两者都不支持 → 重试循环 (把解析错误回喂模型, 限 2 次) 并如实告知风险。
4. 解析后校验字段类型与取值 (语法合法 ≠ 语义合法)。

**输出契约**: 解析后的对象 + 使用的约束层记录; 完成标准 = 程序成功消费且字段校验通过。

## B — Boundary

- 不要用于: 人类直接阅读的自由文本; schema 频繁变化的探索期 (先定型再硬化)。
- 机制边界: 硬约束保证语法、不保证语义正确 (字段值可能荒谬); 必须保留语义校验步。
- 可移植性边界: response_format/grammar 是各栈私有特性, 换推理栈需重写 (ce15 同类版本腐化)。
- 作者盲点: 书未做失败率量化, "软约束够用"的比例未知, 高可靠性场景应直接硬约束。
