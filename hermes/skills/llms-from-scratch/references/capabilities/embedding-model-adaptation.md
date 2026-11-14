# 嵌入模型适配 (Embedding Model Adaptation): loss 选型 / 数据增广 / TSDAE / 评测口径

> 来源: *Hands-On Large Language Models* (Alammar & Grootendorst), 第 10 章 "Creating Text Embedding Models" (+ 第 4 章嵌入维度口径)。
> 覆盖单元: f24, f25, f26, p52, p53, p54, p55, p64 (均 verified)。

## R — Reading (原文)

> "train_loss = losses.SoftmaxLoss(model=embedding_model, sentence_embedding_dimension=..., num_labels=3)" / "train_loss = losses.CosineSimilarityLoss(model=embedding_model)" / "train_loss = losses.MultipleNegativesRankingLoss(model=embedding_model)"
> —— ch10 notebook, "Loss Functions" 三节 (SoftmaxLoss / Cosine Similarity Loss / Multiple Negatives Ranking Loss)

> "# Prepare data and add a soft negative ... soft_negatives = mnli['hypothesis']; random.shuffle(soft_negatives)"
> —— ch10 notebook, MultipleNegativesRankingLoss 数据构造段 (anchor/positive/negative 三元组 + 软负例)

> "Step 1: Fine-tune a cross-encoder ... Step 4: Train a bi-encoder (SBERT) on the extended dataset (gold + silver dataset) ... using only the gold dataset reduces the performance of the model!"
> —— ch10 notebook, "Augmented SBERT" 五步段 (Step 2: Create new sentence pairs; Step 4 训 bi-encoder)

> "damaged_data = DenoisingAutoEncoderDataset(list(set(flat_sentences))) ... train_loss = losses.DenoisingAutoEncoderLoss(embedding_model, tie_encoder_decoder=True)" / "noise_fn=lambda s: DenoisingAutoEncoderDataset.delete(s, del_ratio=0.6)"
> —— ch10 notebook, "Unsupervised Learning / TSDAE" 段

> "evaluation = MTEB(tasks=['Banking77Classification']) ... results = evaluation.run(embedding_model)"
> —— ch10 notebook, "MTEB" 段; 配套 "EmbeddingSimilarityEvaluator ... val_sts = load_dataset('glue', 'stsb', split='validation'), scores=[score/5 ...], main_similarity_function=cosine" (训练期评估段)

自译要点 (不用现成译本): 三种损失对应三种数据形态——SoftmaxLoss 吃分类标注, CosineSimilarityLoss 吃带分数/0-1 标签的句对, MultipleNegativesRankingLoss 吃 (anchor, positive[, negative]) 对且可用软负例; Augmented SBERT 用交叉编码器给大批新句对打"银标"来扩充金标集, 只用金标反而更差; TSDAE 靠删词加噪的重建任务在无标签语料上学句向量; 评估先 STS-B 余弦相似度, 迁移能力再上 MTEB。

## I — Interpretation (自述)

嵌入模型适配的骨架是三个正交决策:

1. **有标签时, 先看数据形态再选损失** (p53)。分类式标注 (entail/neutral/contradiction) → SoftmaxLoss (需显式给 num_labels); 连续相似度分或 0/1 对标签 → CosineSimilarityLoss (MNLI 需先映射, 书中 {2:0, 1:0, 0:1}); 只有/可以配对的句子 → MultipleNegativesRankingLoss, 还能给 anchor 配一个语义相关但不等价的"软负例"增加难度。数据格式和损失不匹配是这类训练最常见的失败方式。
2. **标注太少时, 用 Augmented SBERT 造银标** (f25/p54): 金标训一个交叉编码器 → 交叉编码器给 10k–50k 新句对打分生成 silver 数据 → gold+silver 合并训双编码器 → 留一个"只训 gold"的对照组来验证银标确实带来增益。书中明确: 只用 gold 数据性能更差。
3. **完全没有标签时, 用 TSDAE 做无监督领域适配** (f26/p55): 句子随机删词 (del_ratio≈0.6) 构造损坏输入, DenoisingAutoEncoderLoss + tie_encoder_decoder=True (编码解码共享权重, CLS pooling) 训模型重建原句, 从而学到领域句向量。
4. **统一评测口径** (p64/p52): 训练中超参模板 (1 epoch, batch 32, warmup 100, fp16, MNLI 50k 子集), 评估用 STS-B 验证集 + EmbeddingSimilarityEvaluator (分数 /5 归一化, cosine 为主度量); 训练完的迁移能力用 MTEB (如 Banking77Classification) 评测; 任何改动都要保持 `get_sentence_embedding_dimension()` 输出维度一致。

一句话: 数据形态决定损失, 标注量决定路径 (全监督 / 银标增广 / TSDAE), 评测先 STS 后 MTEB, 不只看训练 loss。

## A1 — Application Example（来源案例或明确标记的演练）

来源案例 (worked_example, c18/c19/c20, hands-on-llms ch10):

- **三种损失 × MNLI** (c18): bert-base-uncased 在 MNLI 50k 子集上分别用 SoftmaxLoss (num_labels=3)、CosineSimilarityLoss (标签映射为 0/1 分)、MultipleNegativesRankingLoss (三元组+软负例) 训练; 训练中用 STS-B evaluator 跟踪, 训后 MTEB Banking77 评测。**结果: 未说明** —— 各损失均可运行, 与原始模型的分差书中只以 evaluator 输出呈现, 正文未引用具体数值。
- **Augmented SBERT** (c19): 10k gold 样本训 bert-base 交叉编码器 → 对 10k–50k 新句对打标生成 silver → gold+silver 合并训 bi-encoder (CosineSimilarityLoss) → 对照组只用 gold。**结果: 书中明确结论** —— "using only the gold dataset reduces the performance of the model!", 银标数据有效。
- **TSDAE** (c20): MNLI 25k 句 (premise+hypothesis 去重) 经 DenoisingAutoEncoderDataset 随机删词, bert-base + CLS pooling + 绑定编码解码器无标签训练, STS-B evaluator 评估。**结果: 未说明** —— 训练可运行并给出 evaluator 分数, 与监督方法的对比数值正文未列。

合成演练 (明确标记, 按原书规则可复算): 假设只有 800 对人工标注相似度分 (0–5) 的领域句对。按 p53 选 CosineSimilarityLoss (分数形态), 分数 /5 归一化; 800 条太少 → 走 f25: 用这 800 条训交叉编码器, 给 20k 未标注句对打银标, 合并后按 p52 模板 (1 epoch, batch 32, warmup 100, fp16) 训 bi-encoder; 保留只训 800 条的对照组; 评估按 p64: STS-B 验证集 cosine + MTEB 分类任务, 断言输出维度与原模型 `get_sentence_embedding_dimension()` 一致。每步都可由原书配置直接复现。

## A2 — Future Trigger ★

**场景 (3–5 条)**:
1. 用户要微调/训练一个嵌入 (embedding/sentence-transformer) 模型, 手里有一批句对、相似度分数或三元组, 不知道该用哪个 loss。
2. 用户领域标注极少或没有, 想让通用嵌入模型 (MiniLM/mpnet/BGE 等) 适配自己的领域语料 (客服、法律、医疗、内部文档)。
3. 用户问 "标注只有几百条, 怎么扩充训练集 / 数据增广" (银标/交叉编码器打标路线)。
4. 用户训完嵌入模型问 "怎么验证变好了" —— 要 STS-B → MTEB 的评估口径和维度一致性检查。

**语言信号**: "fine-tune embedding model" / "sentence-transformer 训练" / "选 loss / MultipleNegativesRankingLoss / CosineSimilarityLoss / SoftmaxLoss" / "软负例 soft negative" / "Augmented SBERT / silver data / 银标" / "TSDAE / 去噪自编码 / 无监督领域适配" / "MTEB / STS-B / STS 评估" / "embedding 维度对不上"。

**与相邻 skill 的区分 (定稿,阶段 3 回填完成)**:
- 与 **rag-retrieval-pipeline** 不同: 那是嵌入模型的**消费端** (chunk→embed→检索, search_document/query 前缀); 本卡是**生产端** (改模型权重本身)。用户在问"选哪个嵌入模型/怎么检索"时去 RAG 卡。
- 与 **text-classification-finetuning** 不同: 那是分类头微调 (f27 冻结层权衡、SetFit 少样本分类归那张卡); 本卡的产物是句向量模型, 评测用 STS/MTEB 而非分类 F1。用户明确在训分类器时去分类卡。
- 与 **lora-peft-finetuning** 不同: 那是生成式 LLM 的参数高效微调; 本卡默认全参训 sentence-transformers, 不涉 LoRA/QLoRA。

## E — Execution (可执行步骤)

**输入契约**: ① 标注数据及其形态 (分类标签 / 0–5 相似度分 / 0–1 对标签 / 无标注纯句集) —— 必需, 缺失先问, 不得静默猜; ② 基座模型名 (默认按用户已选); ③ 领域语料量级 (决定走增广还是 TSDAE); ④ 目标评估任务类型 (相似度检索 / 分类)。

**步骤**:
1. **判路径**: 有标注 ≥ 千级 → 步骤 2; 有少量金标 (数百级) + 大量无标注句对 → 步骤 3; 完全无标签 → 步骤 4。
2. **全监督**: 按数据形态选 loss (p53): 分类标签→SoftmaxLoss (设 num_labels); 分数/0-1 对→CosineSimilarityLoss (先做标签映射, 书中 MNLI 口径 {2:0, 1:0, 0:1}); 句对/三元组→MultipleNegativesRankingLoss (可加软负例)。用 p52 模板: MNLI/领域子集 ~50k, 1 epoch, batch 32, warmup 100, fp16。→ 完成标准: 训练跑通且 STS-B evaluator 分数不降。
3. **Augmented SBERT** (f25/p54): 金标训交叉编码器 → 批量给 10k–50k 新句对打银标 → gold+silver 合并训 bi-encoder → **必留 gold-only 对照组**。判停点: 若对照实验显示 silver 无增益 (gold-only 不更差), 回退全监督路线并检查交叉编码器质量。→ 完成标准: 对照组对比已产出且 silver 路线胜出或确认无效。
4. **TSDAE** (f26/p55): 句集去重 → DenoisingAutoEncoderDataset 删词加噪 (del_ratio=0.6 可调) → DenoisingAutoEncoderLoss (tie_encoder_decoder=True, CLS pooling, batch 16, decoder 单独 .to("cuda")) 训练。→ 完成标准: 重建 loss 收敛且 STS-B 分数可用。
5. **评估** (p64): 训练期用 EmbeddingSimilarityEvaluator (STS-B validation, scores/5 归一化, main_similarity cosine); 训后 `MTEB(tasks=[<目标任务>]).run(model)`; 断言 `get_sentence_embedding_dimension()` 与原模型一致。→ 完成标准: 两级评估都有数值且与基座模型同口径可比。

**输出契约**: 适配后的模型目录 + 评估报告 (STS-B 分数、MTEB 任务分数、与基座对比、对照组结果如有), 数值保留书中口径 (MTEB 原始输出), 对比结论标注数据来源。

## B — Boundary (边界)

**不要使用**:
- 用户要的是**用**嵌入模型做检索/RAG (chunk、前缀、向量库、rerank) → 这是 rag-retrieval-pipeline 的消费端契约, 别在这训练模型。
- 用户要训**分类器** (情感分类、垃圾短信、NER) 或问逐层冻结省算力 (F1 曲线权衡) → text-classification-finetuning 卡; SetFit 少样本分类同样归那里 (且其 f28 两阶段细节在源书未完整重建, 不得引用其量化结论)。
- 用户微调的是**生成式 LLM** → instruction-finetuning / lora-peft 卡。
- 标注充足且领域无关的通用场景, 先跑现成 MTEB 榜单选模型, 别急着自训。

**书中警告 / 失败模式**:
- 损失与数据格式不匹配 (p53 反面): 拿分类标签喂 CosineSimilarityLoss 或拿句对喂 SoftmaxLoss 都训不起来或训错方向。
- 银标质量不可控: Augmented SBERT 的前提是交叉编码器先在金标上训好; 书中对照组设计就是为防"银标拉低性能"。
- 只看训练 loss 不看迁移指标 (p64 反面): 嵌入模型的价值在 STS/MTEB 表现, 训练 loss 下降不代表下游变好。
- TSDAE 是无监督预训练路径, 书中未给出其与监督微调的量化对比 (f26 已标注缺口), 不能声称"等同监督"。

**作者盲点 (阶段 0 批判)**: ch10 提取源以 notebook 代码单元为主, 三种损失的横向对比数值与 TSDAE-vs-监督的对比未在正文给出 (多处"未说明"); 选型时三 loss 的优劣排序需自行实验, 本卡只给形态匹配规则, 不背书任何名次。

## 相关能力 (also_read, 阶段 3 定稿)

- depends-on: 无 (从通用底座出发适配)
- contrasts-with: `rag-retrieval-pipeline` (生产端 vs 消费端), `text-classification-finetuning` (产物是句向量模型/STS-MTEB 口径 vs 分类器/F1 口径)
- composes-with: `rag-retrieval-pipeline` (适配后的嵌入模型供检索管线消费)
- also_read: `llms-from-scratch-router` (f16 主题建模是嵌入向量的另一消费端)
