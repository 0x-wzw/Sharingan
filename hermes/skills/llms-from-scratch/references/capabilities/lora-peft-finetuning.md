# LoRA / PEFT 微调 (lora-peft-finetuning) — RIA++ 能力卡

> 单元: f13 (LoRA), f30 (QLoRA SFT→DPO 两段微调), p22 (LoRA lr 基准), p37 (LoRA 公式与初始化), p40 (DPO β 0.1–0.5 与崩溃警告), p60 (QLoRA 配置基准), p61 (DPO 阶段配置)
> 来源: 《Build an LLM From Scratch》(Raschka) 附录 E；《Hands-On Large Language Models》(Alammar & Grootendorst) 第 12 章
> 状态: 纸面 walkthrough 验证 (V2 check_mode=walkthrough)；阶段 4 实测前不声称"已实测"

## R — Reading (原文)

1. LoRA 核心公式 (Raschka, 附录 E.4):

> "The LoRA method proposed by Hu et al. offers a more efficient alternative to computing the weight updates ΔW by learning an approximation of it, ΔW ≈ AB. In other words, in LoRA, we have the following, where A and B are two small weight matrices: W_updated = W + AB"

（自译：LoRA 不直接学全量 ΔW，而是用两个小矩阵 A、B 的乘积 AB 近似它，更新时 W 加上 AB。）

2. A/B 初始化与缩放 (Raschka, 附录 E.4, LoRALayer 代码及注释):

> "torch.nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))  # similar to standard weight initialization … self.B = torch.nn.Parameter(torch.zeros(rank, out_dim)) … x = (self.alpha / self.rank) * (x @ self.A @ self.B)"

（自译：A 用 Kaiming 均匀初始化，B 初始化为零，输出按 alpha/rank 缩放——作者注明该缩放"不是必需，但更规范，可让不同 rank 的运行无需重调学习率即可比较"。）

3. 参数压缩效果 (Raschka, 附录 E.4, c11):

> "we reduced the number of trainable parameters by almost 50x when using LoRA … As we can see based on the relatively high accuracy values above, the LoRA finetuning was successful."

（自译：用 LoRA 后可训练参数减少近 50 倍，且微调精度与全参微调相当。）

4. QLoRA 配置 (Alammar & Grootendorst, 第 12 章, TinyLlama-1.1B SFT):

> "bnb_4bit_quant_type='nf4' … lora_alpha=32 … r=64 … target_modules=['k_proj', 'gate_proj', 'v_proj', 'up_proj', 'q_proj', 'o_proj', 'down_proj'] … optim='paged_adamw_32bit'"

（自译：4-bit NF4 量化底座 + LoRA r=64/alpha=32、挂全部 7 个投影层、paged AdamW 优化器，把 1.1B 模型的 SFT 压进 16GB T4。）

5. DPO 配置与过滤 (Alammar & Grootendorst, 第 12 章, DPO 阶段):

> "dpo_dataset.filter(lambda r: r['status'] != 'tie' and r['chosen_score'] >= 8 …)"；DPOTrainer 配置 "beta=0.1, lr=1e-5, max_steps=200, warmup_ratio=0.1"。

6. β 的语义与崩溃警告 (Raschka, ch07_04 dpo-from-scratch, p40):

> "typically something in the range of 0.1 to 0.5 … We ignore the reference model as beta -> 0 … very prone to collapse (the loss might improve, but the model will start generating nonsensical texts)"

（自译：β 常取 0.1–0.5；β→0 等于忽略参考模型，训练易崩溃——损失可能照常下降但模型开始输出乱文，须抽查生成文本而非只看 loss。）

## I — Interpretation (自述)

LoRA 解决的问题是：全参微调要为每个任务存一份完整模型副本，且优化器状态是参数量的好几倍。它把每个 Linear 层的权重更新 ΔW 分解成两个瘦矩阵的乘积 ΔW≈AB，只训练 A、B，原权重 W 冻结不动。

三个实现约定是这一方法成败的关键：

- **初始化不对称**：A 用 Kaiming 均匀初始化、B 初始为零。这样训练开始时 AB=0，模型行为与未微调完全一致——初始化正确与否可直接验证（起点性能不变）。
- **缩放约定**：LoRA 分支输出乘 alpha/rank。加上这个缩放后，换 rank 不必重调学习率（Raschka 注明这是"更规范"的写法；QLoRA 教程中 alpha 通常取 r 的一半，如 r=64/alpha=32）。
- **目标模块选择**：Qing 式 7 投影 (q/k/v/o + up/gate/down) 是 Llama 系全挂的做法；目标是让适配增量覆盖注意力与 MLP 的全部线性变换。

QLoRA 在此之上加一层量化：底座权重以 4-bit NF4 加载，LoRA 增量仍以全精度训练，配合 paged AdamW 和梯度检查点，把显存需求压到消费级 GPU 可承受。

DPO 是偏好对齐阶段：不用奖励模型，直接用 (chosen, rejected) 响应对训练。β 控制对参考模型的偏离程度，典型 0.1–0.5——β 太小训练易崩溃（loss 好看但输出乱文）。SFT → DPO 两段是完整范式：先教会格式与能力，再用偏好数据调对齐。

## A1 — Application Example

**案例 1（worked_example, c11, Raschka 附录 E.1–E.4）**：同一 SMS 垃圾短信分类任务，用自实现 LoRA 重做。输入：GPT-2 分类模型（ch06 已建）+ SMS Spam 747+747 数据。执行：实现 LoRALayer（A Kaiming / B 零）→ LinearWithLoRA 包装原 Linear → `replace_linear_with_lora(model, rank=16, alpha=16)` 递归替换全部 Linear → 冻结原权重（`param.requires_grad = False`），lr=8e-4、weight_decay=0.1 训练。输出：可训练参数减少近 50 倍，验证 B=0 初始化保证初始性能不变；微调后 test 准确率 96.67%（bonus 对照表中与全参微调相当，LoRA 略优，作者归因于更少过拟合）。

**案例 2（worked_example, c21, Alammar ch12）**：TinyLlama-1.1B 两阶段微调。阶段一 SFT：ultrachat_200k 抽 3,000 条套 chat 模板 → NF4 4-bit 加载 → LoRA r=64/alpha=32 挂 7 投影 → paged_adamw + 梯度检查点 → SFTTrainer 训练后 merge adapter。阶段二 DPO：distilabel-intel-orca-dpo-pairs 按三条件过滤（非 tie、chosen_score≥8、排除 gsm8k train）→ DPOTrainer (beta=0.1, 200 steps) 续训 → pipeline 生成回答。书中未给量化评分（未说明），仅以示例输出对比展示。

## A2 — Future Trigger ★

**触发情境**：
1. 显存装不下全参微调（OOM 或消费级 GPU），需要参数高效方案。
2. 要在多个任务/领域上复用同一底座，希望每个任务只存一个小 adapter 而非整份模型。
3. 训练完成后想做偏好对齐（让模型区分"更好/更差"的回答），有或可以构造 (chosen, rejected) 数据对。
4. 用户在实现/审读 LoRA 代码，问"A 和 B 怎么初始化""alpha 和 rank 什么关系""该挂哪些层"。
5. 微调后输出变差，怀疑 LoRA 初始化或超参（rank/alpha/lr）配错。

**语言信号**（中英双写）：
- 英文: "LoRA", "QLoRA", "PEFT", "adapter", "rank", "lora_alpha", "DPO", "4-bit / nf4 / bitsandbytes", "parameter-efficient fine-tuning", "preference tuning", "paged_adamw", "merge adapter"
- 中文: "参数高效微调", "LoRA 微调", "低秩适配", "量化微调/4-bit 微调", "DPO 偏好对齐", "显存不够怎么微调", "适配器"

**与相邻 skill 的区分**（定稿，阶段 3 回填完成）：
- 与 `gpt2-pretraining-pipeline`：那边是预训练全参更新与评估；本卡只管冻结底座 + 适配器/偏好对齐。
- 与 `text-classification-finetuning`：那边是冻结策略/解冻最后 block 的分类头微调；本卡是 LoRA 替换 Linear 的 PEFT 契约。用户问"解冻哪几层"归那边，问"挂 LoRA 到哪些模块"归本卡。
- 与 `instruction-finetuning-and-eval`：那边是 SFT 数据构造与 LLM-as-a-judge 评估；本卡以"QLoRA SFT 只是 DPO 的前置阶段"出现，SFT 数据构造细节归那边。
- 与 router 卡（微调超参、显存预算等散单元）：本卡不含冻结层预算实验 (f27/c15) 与通用显存估算，只承载 adapter 配置契约。

## E — Execution (可执行步骤)

**输入契约**：必须有 base 模型标识 + 硬件显存上限（决定走 LoRA 全精度还是 QLoRA 4-bit）+ 任务类型（分类 / SFT / 偏好对齐）。缺模型规模或显存信息时**先询问，不得静默猜值**。

**输出契约**：adapter 配置声明（rank、alpha、target_modules、量化类型、lr）+ 训练前参数量对比（可训练 vs 总参数）+ 训练/验证指标 + (DPO) 生成文本抽查。结论须标注超参来源与适用范围。

1. **选路径**：显存装得下全精度底座 → 标准 LoRA；装不下（如 1B+ 模型进 16GB）→ QLoRA：`bnb_4bit_quant_type='nf4'` 加载 + `prepare_model_for_kbit_training` + paged 优化器 + 梯度检查点。完成标准：路径选定且有显存依据。
2. **配置 adapter**：rank/alpha 按惯例起步（分类教程 r=16/alpha=16；QLoRA SFT r=64/alpha=32，alpha≈r/2）；target_modules 依模型架构列出注意力与 MLP 的线性投影（Llama 系 7 投影）。完成标准：能打印可训练参数量并与总参数对比（参照 c11 的 ~50× 基准口径）。
3. **验证初始化**：确认 B 零初始化（或 PEFT 库默认）后，训练前跑一次评估——性能必须与未适配底座一致；若起点性能已变，初始化有错，停下修。**判停点：此步不过则不进训练。**
4. **训练**：冻结底座权重；学习率按附录 E 基准 lr=8e-4（LoRA 可用比全参微调高一个量级的 lr，这是约定值非普适最优）；记录 train/val 双指标。
5. **（仅偏好对齐）DPO 阶段**：从 SFT 后模型出发；构造/过滤偏好对——剔除 tie、按分数阈值取 chosen、剔除污染集（如 gsm8k train）；beta=0.1 起步（范围 0.1–0.5；β↑ 更贴近参考模型）。完成标准：偏好对过滤条件显式列出，beta 与 lr 已声明。
6. **结果校验**：报告指标须为全集计算而非抽样估计（eval_iter 抽样值只能作训练中参考）；DPO 须抽查生成文本——**loss 下降不排除崩溃**（输出乱文即崩溃，勿以 loss 收敛下结论）。
7. **交付**：adapter 单独保存 (`save_pretrained`)，标注是否已 merge；超参表逐项注明"书内基准 / 用户设定 / 本卡约定"。

## B — Boundary (边界)

**不要使用**：
- 任务需要底座能力本身的大幅改变（如继续预训练新语言/领域知识注入）——低秩增量容量有限，应走全参微调或 MLM 续训（f29/c22 路线）。
- 数据量极小且任务简单（如只有分类头要学）：解冻最后 block（ce05/c07 路线）可能比引入 LoRA 更简单直接。
- 用户问冻结层数量预算、逐层冻结曲线 → 冻结实验卡 (f27) 的领地。

**书中警告的失败模式**：
- DPO 崩溃 (p40)：β 过小时 loss 可能照常改善但模型输出乱文——必须抽查生成文本，不能只看 loss。
- QLoRA 超参无敏感性分析 (ce16)：r=64/alpha=32 是 TinyLlama+ultrachat 配置，书中未做扫参；换模型/数据须视为待调超参，不得当万能默认，且单次运行 F1 不足以断言方法优劣。
- OOM 误诊 (ce18)：全精度加载 + 普通 AdamW 直接 CUDA OOM 是路径选错，不是"显卡不行"——显存预算（权重+梯度+优化器状态+激活）应前置判断。
- 版本腐化 (ce15)：ch12 TRL/peft API 锚定 2024 版本，照抄会 import 失败；迁移思路 + 按当前 API 重写。

**作者盲点（阶段 0 批判）**：
- 书中超参（rank=16、r=64、lr=8e-4、beta=0.1）均为单一配置演示，无 ablation 依据，外推需自行验证。
- 教育规模结论（~50× 压缩、LoRA≈全参精度）来自小模型小数据；在大模型上的量化收益比例未在书中验证。
- "B=0 初始化保证初始性能不变"在自实现中可复算，但用 PEFT 库时该性质依赖库实现，须按步骤 3 实测而非假设。

## 相关能力 (also_read, 阶段 3)

- depends-on: 任一预训练底座权重 (Raschka 线由 `gpt2-pretraining-pipeline` 产出; HO 线直接用开源底座)
- contrasts-with: `text-classification-finetuning` (LoRA 替换 Linear vs 解冻末块; "解冻哪几层"归那边, "挂 LoRA 到哪些模块"归本卡)
- composes-with: `instruction-finetuning-and-eval` (SFT→DPO 两段式, 数据构造复用那边), `p66-gpu-vram-cleanup` (QLoRA 显存运维)
- also_read: `llms-from-scratch-router` (f29 MLM 续训是 LoRA 容量不足时的替代路线)
