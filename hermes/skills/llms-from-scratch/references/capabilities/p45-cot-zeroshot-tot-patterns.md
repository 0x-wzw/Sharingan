# CoT / zero-shot CoT / ToT 技巧族 (p45) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 6 章 | 绑定单元: p45 (母方法: f18 推理增强三级决策, 见 f18-reasoning-enhancement-decision.md) | 支持材料: ce15
> 去向: source-router 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "Imagine three different experts are answering this question. All experts will write down 1 step of their thinking, then share it with the group. ... If any expert realises they\'re wrong at any point then they leave."

— Alammar & Grootendorst, ch06 (chapter06_Chapter 6 - Prompt Engineering.txt @255)

同章 @241: "…Let's think step-by-step."。自译: 技巧族四件——few-shot CoT (带步骤的示例)、zero-shot CoT (追加一句话)、ToT 三专家 (分步互查, 错者退出)、链式拆解 (复杂任务分多 prompt)。

## I — Interpretation (自述)

四个技巧共享一个原理: 让模型显式产出中间步骤, 中间步骤本身就是纠错场。few-shot CoT 靠示例教"怎么想"; zero-shot CoT 靠一句话触发; ToT 靠多路径互查; 链式把长推理切成可校验的段。选择时按成本升序尝试, 详见 f18 的三级决策。

## A1 — Application Example

### 示例: 三专家 prompt 演算 (合成, 依据 ch06 原文 prompt)

- **类型与来源**: 原书未提供运行案例, 以下为按原文 prompt 规则构造的合成演练 (标注为合成)。
- **问题/输入**: ch06 苹果算术题 (23-20+6)。
- **方法论的使用**: 套用三专家 prompt; 三位专家各写一步 (23-20=3 → 3+6=9 → 核对), 讨论结果一致即收敛。
- **结论/预期输出**: 答案 9, 附专家分步讨论; 若某专家算成 3+6=8, 在互查步被指出并退出。

## A2 — Future Trigger ★

### 情境

1. 用户问各推理技巧怎么写/选哪个。
2. 模型推理出错, 要在 prompt 层补救。

### 语言信号

- "思维链 / CoT / ToT / tree of thoughts / step-by-step prompt"

### 与相邻 skill 区分

- f18 是选级决策 (何时用哪级); 本卡是各技巧的 prompt 写法。检索缺口用 RAG, 不是推理技巧能解决的。

## E — Execution

**必需输入**: 推理题; 有示例则要示例原文。

1. 按成本升序: few-shot CoT (有示例) → zero-shot CoT (无示例, 追加 "Let's think step-by-step.") → ToT 三专家 (仍错时)。
2. 每级核验中间步骤可复算性。判停: 当前级已正确即停。

**输出契约**: 答案 + 步骤 + 所用技巧级; 完成标准 = 步骤复算无误。

## B — Boundary

- 不要用于: 知识缺失型问题 (想不出没有的知识); 简单任务 (白付成本)。
- ToT 成本成倍; 书未量化各技巧增益幅度, 结论方向可信、幅度自测。
- 版本边界 (ce15): 推理模型已内化逐步推理, 先验模型能力再叠技巧。

## 相关能力 (also_read, 阶段 3)

- composes-with: `f18-reasoning-enhancement-decision` (同主题双卡)
