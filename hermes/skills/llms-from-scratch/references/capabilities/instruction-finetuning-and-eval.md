# 指令微调与 LLM-as-a-judge 评估 (instruction-finetuning-and-eval)

> Stage 2 RIA++ 能力卡 | 来源书: Build a Large Language Model (From Scratch), Sebastian Raschka | 绑定单元: f10, f11, p29, p30, p31, p32, p33, p47 | 支持材料: c10, ce03, ce04, ce08, ce09, ce10, ce12, ce20

---

## R — 原文 (Reading)

> "Using this -100 ignore_index, we can ignore the additional end-of-text (padding) tokens in the batches ... However, we don't want to ignore the first instance of the end-of-text (padding) token (50256) because it can help signal to the LLM when the response is complete."
>
> — Raschka, ch07 §7.3 (ch07_01_main-chapter-code_ch07.txt @10920)

> "a longer, improved prompt that evaluates responses on a scale of 1-5 (instead of 1 to 100) and employs a grading rubric, resulting in more accurate and less noisy evaluations."
>
> — Raschka, ch07 §7.8 (@1048-1051)

补充锚点: custom_collate (ch07 @8115)、85/10/5 划分与 Alpaca 三段式 (p29, §7.2)、collate 内设备迁移 (p31, §7.4)、"124 million model is too small ... load the medium version with 355 million parameters" (p32/ce08, §7.5)、judge 确定性参数 `{'seed': 123, 'temperature': 0, 'num_ctx': 2048}` (p33, §7.8 + ch07_03 eval 文件)、确定性推理三件套 (p47, alammar ch03/04/07)。

---

## I — 方法论骨架 (Interpretation)

这条方法论把一个只会"续写文本"的预训练模型,改造成能"读懂指令并作答"的助手,然后解决"答案没有标准对错,怎么自动评估"的问题。

数据侧:把每条样本整理成 Alpaca 三段式 prompt(指令 + 可选输入 + 期望回答),按 85/10/5 切成训练/验证/测试集。批处理不能用默认 collate:序列长短不一,需要自定义 collate 函数把每个 batch 动态 pad 到 batch 内最长序列。关键是损失掩码——padding 位置在 targets 里替换为 -100(交叉熵的默认 ignore_index),使模型不为无意义的 padding 付费;但每个响应末尾的第一个 `<|endoftext|>` 必须保留为监督信号,否则模型学不到"回答到此结束",生成时永不停止。设备迁移放进 collate 里,让 DataLoader 在后台并行完成 GPU 搬运。

模型侧:指令遵循是多任务泛化能力,对模型容量有硬下限——教育场景下 355M 是最低可用规模(124M 训练流程完全正确但产出不可用)。约 1 个 epoch 后就开始轻微过拟合,2 epochs 是书中实测配置。

评估侧:指令模型没有单一准确率指标,书中路线是用一个更强的本地模型当裁判:给它"指令 + 正确回答 + 模型回答",让它打分后求平均。裁判自身必须确定性(seed 固定、temperature=0、上下文长度显式设定),且裸 0–100 打分噪声大,改进版用 1–5 分 + rubric。裁判分数是相对参考,不是客观性能。

---

## A1 — 应用示例 (Application Example)

### 示例 1: 1,100 条指令数据微调 GPT-2 medium 355M 并用 Llama 3 评分 (c10)

- **类型与来源**: 原书 worked_example,第 7 章 §7.2–7.8 (ch07_01_main-chapter-code_ch07.txt)
- **问题/输入**: Alpaca 格式 instruction-data.json 共 1,100 条 instruction/input/response 三元组。
- **方法论的使用**: 按 85/10/5 划分 → 自写 custom_collate_fn(pad 用 50256 填 inputs、targets 中除首个 eos 外全部置 -100、batch 内动态对齐、collate 内 `.to(device)`) → 加载 355M 模型,AdamW 训练 2 epochs(A100 上 0.86 分钟)→ 对 110 条测试集逐条生成响应 → 本地 Ollama Llama 3 8B 按给定 input + 正确输出 + 模型回答打 0–100 分求平均,另给出 1–5 分 + rubric 改进版评审 prompt。
- **结论**: 微调前模型只会复读输入;微调后能正确执行如把 "The chef cooks the meal every day." 改为被动语态 "The meal is cooked every day by the chef."。
- **结果**: 作者模型平均分 >50;书中参考基线:Llama 3 8B base 58.51 / instruct 82.65。

### 示例 2: 掩码设计的验证演练 (合成,按 p30/ce03 规则可复算)

- **类型与来源**: 原书未提供单独案例,以下为按原书规则构造的合成演练(标注为合成)。
- **问题/输入**: 某样本 padded 序列 `[prompt..., response, 50256, 50256, 50256]`。
- **方法论的使用**: targets 中仅第一个 50256(响应结束信号)保留为有效标签,其后 2 个 padding 置 -100;`inputs = padded[:-1]`、`targets = padded[1:]` 错位规则不变;cross_entropy(ignore_index=-100) 自动忽略。
- **结论/预期输出**: 有效 loss 只覆盖 prompt-response + 首个 eos;若错误地把全部 50256 置 -100,训练损失仍正常下降(失败静默),但生成不会停止。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?

1. 想把一个开源/自训的语言模型微调成"听指令办事"的助手(而非分类器),手里有 instruction–response 格式数据(或想造这种数据)。
2. 训练已跑通但模型生成不会停止、无限续写,怀疑 collate/掩码写错。
3. 显存或训练时间异常膨胀,怀疑 padding 策略不对(全数据集定长 vs batch 级动态)。
4. 训练完的指令模型没有标准准确率可算,需要一个可复现的自动化评估方案。
5. 拿到一份指令微调教程/代码,想核对 epoch 数、模型规模、掩码细节这些"流程正确但结果不可用"的隐性坑。

### 语言信号 (出现即应激活)

- "SFT / instruction tuning / 指令微调 / instruction fine-tuning"
- "collate / padding / -100 / ignore_index / 掩码 / mask the prompt"
- "模型回答停不下来 / 不会停止 / never stops generating"
- "LLM as a judge / 用大模型打分 / 自动评估回复质量 / AlpacaEval 式评分"
- "微调后答非所问 / 训练 loss 正常但输出质量差"

### 与相邻 skill 的区分 (定稿,阶段 3 回填完成)

- 与 `gpt2-pretraining-pipeline` 的区别: 那是"从文本续写器到文本续写器"的预训练与通用生成评估(perplexity);本 skill 的输入是三元组指令数据、输出契约是"响应生成 + 打分评估",loss 掩码和 collate 是本 skill 独有步骤。
- 与 `text-classification-finetuning` 的区别: 分类取最后 token 的 class logits、输出是类别;本 skill 输出是自由生成文本,数据划分也不同 (85/10/5 vs 70/10/20)。
- 与 `lora-peft-finetuning` 的区别: PEFT 管"怎么省参数地训"(adapter 配置);本 skill 管"训什么数据、怎么掩码、怎么评"。QLoRA SFT 阶段的数据侧可复用本 skill 的准备步骤。

---

## E — 可执行步骤 (Execution)

**必需输入**: 指令数据集(每条含 instruction、可选 input、response 三字段;JSON/JSONL);基座模型权重(指令微调 ≥355M 参数,124M 不可用——缺此信息先询问,不得默认 124M);目标设备。若用户未给评估裁判(如 Ollama + llama3 8B),先询问或明确声明改用其他评估路径。

**交付物与完成标准**: (1) 可运行的 collate + DataLoader;(2) 训练后的模型 checkpoint;(3) 测试集响应文件;(4) 裁判评分均值 + 对照基线。掩码正确性以"targets 中首个 eos 保留、其后 padding 全为 -100"可程序断言;评估以固定 seed/temperature 可复现为准。

1. **数据准备**: 校验每条样本三字段;按 Alpaca 模板 `format_input` 生成 prompt(无 input 时省略 `### Input` 段);按 85/10/5 切 train/val/test。完成标准:三集数量之和等于总数,prompt 无空 instruction。
2. **自定义 collate**: pad token = 50256(batch 内动态对齐到最长,非全数据集定长);targets 中除每个响应末尾首个 eos 外全部置 -100;可选 allowed_max_length 截断;collate 内 `.to(device)`(functools.partial 预填设备)。完成标准:打印一个 batch,确认 inputs/targets 形状错位一位、-100 分布符合规则。
   - **判停点**: 若 batch 检查发现 targets 中首个 eos 也是 -100 → 停,修 collate 再继续 (ce03: 该错误静默,训练 loss 照常下降,事后无法从曲线发现)。
3. **训练**: 加载 ≥355M 模型;先以小 batch 试跑一个 step 验证 loss 有限;再按书中配置 2 epochs(约 1 epoch 后轻微过拟合,以 val loss 曲线为准,勿照搬 3–5 epochs 默认)。完成标准:val loss 出现拐点后停止,保存 checkpoint。
   - **分支**: 若 loss 正常下降但生成质量差且模型 ≤124M → 判定为容量不足 (ce08),换 355M 重跑,不要调参。
4. **生成测试响应**: 对测试集逐条生成,剥离 prompt 前缀只留响应;生成侧用确定性三件套 (p47): temperature=0 / do_sample=False + 固定 seed + 显式上下文长度。完成标准:响应数等于测试集条数,无残留 prompt 文本。
5. **LLM-as-a-judge 评估**: 启动本地裁判(如 Ollama llama3 8B,注意 11434 端口占用与 OLLAMA_HOST 排障);裁判 prompt 提供 input + 正确输出 + 模型响应,要求输出整数分;裁判参数固定 `{'seed': 123, 'temperature': 0, 'num_ctx': 2048}`。解析失败的单条跳过并计数,最后报告平均分 + 有效样本数。完成标准:分数可重复(同参数重跑一致或差异在声明的非确定性范围内)。
6. **解读分数**: 必须对照基线(书中口径:llama3 8B base 58.51 / instruct 82.65);首选 1–5 分 + rubric 的改进版 prompt 而非裸 0–100;小模型裁判与 GPT-4 级裁判 Pearson 相关仅约 0.2–0.5——结论表述限定为"相对比较",不得声称客观性能。

---

## B — 边界 (Boundary)

**不要使用本 skill 的场景**:
- 任务是给文本打类别标签 → 用 `text-classification-finetuning`(类别头 + 分类损失,无响应生成与 judge 评估)。
- 目标是领域续写/补全而非听指令 → 预训练/继续预训练路线。
- 算力受限想省参数 → 先看 `lora-peft-finetuning`(adapter 机制不属本卡),数据/掩码/评估侧仍可复用本卡。

**作者在书中警告过的失败模式**:
- ce03: `targets[targets == 50256] = -100` 一刀切,连首个 eos 也屏蔽——错误静默,损失照常下降,唯一症状是生成永不停止。
- ce04: 全数据集定长 padding(照搬 ch06 做法)→ 个别超长样本让绝大多数 batch 全是 padding,显存平方级浪费,超 1024 上下文直接报错/截断。
- ce08: 124M 模型指令微调——流程正确、loss 正常、产出不可用;误判为"调参问题"会白耗时间。
- ce09: 习惯性 3–5 epochs——小数据集约 1 epoch 后即过拟合,多训反而更机械、更重复。
- ce10: 裸 0–100 裁判打分噪声大、区分度差;小裁判与 GPT-4 级裁判相关性低,绝对分数不可当客观性能。
- ce12: GPT-2 tokenizer 会把 `<|user|>` 等 special token 拆成 5 个碎片 ID——换 prompt 模板前必须确认 tokenizer 注册,否则结构信号丢失。
- ce20: 用 GPT API 批量生成训练数据微调与 OpenAI 竞争的模型违反其 ToS——数据增广技术可行 ≠ 商用合规。
- ce13: Ollama 评估跨操作系统非完全确定,分数可能轻微不一致;报告时声明环境。

**作者盲点 / 批判性边界**:
- 裁判模型本身是强偏差源:书中用单裁判单次评分,无人工校验子集;本书分数 (58.51/82.65) 是教学基线,不是排行榜。
- 1,100 条 + 教育级数据上的结论不能外推为生产规模 SFT 配方;epoch 数、模型规模下限都是与数据规模耦合的实测值。
- 全部验证为纸面 walkthrough (V2),阶段 4 实测前不得声称"已实测"。

**易混淆的相邻方法论**: 分类微调 (同属"微调"但损失/输出契约完全不同)、RLHF/DPO (偏好对齐,改的是偏好而非指令遵循,属 PEFT 卡的 DPO 阶段)、AlpacaEval 等公开评估框架 (本卡是其单机最小实现,非同一协议)。

## 相关能力 (also_read, 阶段 3)

- depends-on: `gpt2-pretraining-pipeline` (预训练权重是本卡输入前提)
- contrasts-with: `text-classification-finetuning` (生成回复 + judge 评分 vs 类别 logits; 85/10/5 vs 70/10/20 划分)
- composes-with: `lora-peft-finetuning` (QLoRA SFT→DPO 两段式中 SFT 数据侧复用本卡), `rag-retrieval-pipeline` (RAG 接地生成以指令模型为生成端)
- also_read: `f17-prompt-six-elements` / `p44-seven-segment-prompt` (judge prompt 与响应模板的结构化设计)
