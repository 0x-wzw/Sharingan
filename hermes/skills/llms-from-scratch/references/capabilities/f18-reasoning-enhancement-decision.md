# 推理增强三级决策 (f18) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 6 章 (Prompt Engineering) | 绑定单元: f18, p45 | 支持材料: ce15
> 去向: source-router (llms-from-scratch-router) 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "Imagine three different experts are answering this question. All experts will write down 1 step of their thinking, then share it with the group. Then all experts will go on to the next step, etc. If any expert realises they\'re wrong at any point then they leave."

— Alammar & Grootendorst, ch06 (chapter06_Chapter 6 - Prompt Engineering.txt @255, ToT 三专家 prompt)

同章 @241 (zero-shot CoT): "…how many apples do they have? Let's think step-by-step."。自译: 推理增强有代价递增的三级——few-shot CoT (给出带推理步骤的示例)、zero-shot CoT (只追加一句"让我们一步步想")、Tree of Thoughts (多专家分步推演, 出错者退出)。

## I — Interpretation (自述)

数学/多步推理任务上, 直接要答案的错误率高。书的决策是按"示例可得性 → 错误率"逐级加码: 手里有带解题步骤的示例就用 few-shot CoT (最便宜且稳定); 没有示例就在 prompt 末尾加 "Let's think step-by-step" (一行代码的免费增益); 仍出错才上 ToT 三专家 (token 成倍增加, 但能通过自我纠错挽回偏差)。核心认知: 推理质量主要来自让模型显式产出中间步骤, 而非更礼貌的措辞; 层级存在的意义是避免一上来用最贵的手段。

## A1 — Application Example

### 示例: 苹果算术题的三级递进 (合成演练, 依据 ch06 原文 prompt 规则)

- **类型与来源**: 原书未提供逐级对照实验, 以下为按原书规则构造的合成演练 (标注为合成; 书中两 prompt 均为原文)。
- **问题/输入**: "The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?"
- **方法论的使用**: 无手头示例 → 直接用 zero-shot CoT, 追加 "Let's think step-by-step." → 模型逐步写出 23-20=3, 3+6=9; 若中途算错 (如写成 3+6=8), 升级为三专家 ToT prompt, 每位专家逐步演算, 错误方在互查中退出。
- **结论/预期输出**: 正确答案 9, 附完整步骤; ToT 下多数专家路径收敛到 9。

## A2 — Future Trigger ★

### 情境

1. 模型对数学/逻辑/多步规划题直接作答频频出错, 用户要求提高正确率。
2. 用户问"要不要用思维链 / CoT / ToT / 让模型一步步想"。
3. 需要在成本与正确率间取舍的推理类 prompt 设计。

### 语言信号

- "CoT / chain of thought / 思维链 / step-by-step / Tree of Thoughts / ToT"
- "模型总是算错 / 推理错误率高 / reasoning prompt"

### 与相邻 skill 区分

- 与 f17/p44: 那是输出形态工程; 本卡是正确率工程, 二者可叠加在同一 prompt 里。
- 与 f22 (ReAct): ReAct 需要"行动/工具"维度; 纯脑内推理不需要工具。

## E — Execution

**必需输入**: 推理题原文; 若用户已有带步骤的示例, 必须拿到示例本身 (缺则问, 不自造假冒用户示例)。

1. 判级: 有 few-shot 示例 → 用 L1 (示例 + 问题); 无 → L2 zero-shot CoT (追加 "Let's think step-by-step."); L2 结果仍错且任务关键 → L3 ToT 三专家 prompt。
2. 每级运行后核验中间步骤是否自洽 (数字/事实可复算)。
3. 判停: L2 已正确 → 停, 不上 L3 (省成本)。

**输出契约**: 最终答案 + 显式推理步骤; 升级记录 (用了哪级、为何升级)。完成标准 = 中间步骤逐步复算无误。

## B — Boundary

- 不要用于: 检索/事实问答 (缺知识, 想再多也没用, 应转 RAG); 简单任务 (白付 token 成本)。
- 代价边界: ToT 输出成倍增长, 延迟与费用显著上升, 书中定位为最后手段。
- 边界盲点 (作者/批判): 书用单一算术示例演示, 未给出跨任务的错误率量化, "逐级增益"方向可信但幅度需自测。
- 版本边界 (ce15): 现代 reasoning 模型已内化逐步推理, 先确认模型本身能力再叠 prompt 技巧。

## 相关能力 (also_read, 阶段 3)

- composes-with: `p45-cot-zeroshot-tot-patterns` (同主题双卡)
