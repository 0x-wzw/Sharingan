# MLM 继续预训练 + NER 标签对齐 (f29) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 11 章 (Fine-Tuning BERT) | 绑定单元: f29, p59 | 支持材料: c17, c22, ce15
> 去向: source-router (llms-from-scratch-router) 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "# If the label is B-XXX we change it to I-XXX" ... "updated_label = -100 if word_idx is None else label[word_idx]"

— Alammar & Grootendorst, ch11 (chapter11_Chapter 11 - Fine-Tuning BERT.txt @555, align_labels 注释与实现)

同章 (@401): `mlm_probability=0.15` (MLM 续训); (@580/@601) `seqeval = evaluate.load("seqeval")` → `overall_f1`。自译: 词级 NER 标签过 tokenizer 后, 词被拆成多个子词——首子词保留 B- 标签, 后续子词由 B- 改为 I-, 特殊 token 标 -100, 评估时跳过。

## I — Interpretation (自述)

这一卡覆盖两个"把 BERT 适配到你的领域"的前置动作。①MLM 继续预训练: 在领域语料上以 15% 掩码率再跑 masked language modeling, 让 bert-base 学会领域词汇分布 (影评语料 → "horrible" 后面会猜什么变了他)。②NER 标签对齐: token 分类要求"每个子词一个标签", 而人工标注是"每个词一个标签"。规则三条: 词首子词继承原标签 (B-XXX); 同词后续子词把 B- 改成 I- (它们不是新实体起点); [CLS]/[SEP]/[PAD] 等特殊 token 无对应词 → -100, 交叉熵与 seqeval 均跳过。对齐错一个, F1 就静默失真, 所以这是 NER 微调最常见错误点; 最终以 seqeval overall_f1 判停。

## A1 — Application Example

### 示例 1: CoNLL-2003 NER 标签对齐演算 (c17)

- **类型与来源**: 原书 worked_example, ch11 (align_labels 逐条演算, 样例 train[848]; 最终 F1 原书未列数值, 未说明)。
- **问题/输入**: CoNLL-2003 词级 ner_tags + bert-base-cased tokenizer。
- **方法论的使用**: tokenize(is_word_labels=True) 得 word_idx → 逐 token: word_idx None → -100; 首子词 → 原标签; 后续子词 → B- 改 I-; 打印 original vs updated 对比。
- **结果**: 书展示对齐前后标签序列差异; 训练后用 seqeval overall_f1 评估, 并以 pipeline 对 "My name is Maarten." 验证实体识别。

### 示例 2: 领域 MLM 续训 (c22)

- **类型与来源**: 原书 worked_example, ch11 (MLM 节)。
- **问题/输入**: rotten_tomatoes 影评训练集。
- **方法论的使用**: mlm_probability=0.15, 再预训练 bert-base-cased 10 epochs; 用 "What a horrible [MASK]!" 对比原版与域内版的 fill-mask 补全分布。
- **结果**: 两版补全词分布并列展示, 书未点评优劣 (未说明)。

## A2 — Future Trigger ★

### 情境

1. 用户要做 NER/token 分类, 标签与子词对不上、报错或 F1 异常低。
2. 想让 BERT 先"懂行话"再做下游任务 (领域自适应续训)。
3. 问 "tokenizer 前后标签怎么对齐 / -100 是什么 / B-I 标签"。

### 语言信号

- "NER 标签对齐 / label alignment / subword / -100 / B-PER I-PER / seqeval"
- "MLM 续训 / 领域自适应 / domain-adaptive pretraining / fill-mask"
- "继续预训练 / 在领域语料上再训练 BERT / 遮蔽语言模型 / 领域自适应预训"
- 区分: 与 `embedding-model-adaptation` (领域适配) 的分界——那边是句向量模型 (sentence embeddings); 本卡关键词特指 BERT 类 token 模型的继续预训练 + NER/命名实体识别标注对齐。

### 与相邻 skill 区分

- 与 `text-classification-finetuning`: 那是序列级单标签 (取最后 token logits); 本卡是 token 级多标签 (逐 token 对齐)。
- 与 `embedding-model-adaptation`: 适配的是句向量模型; 本卡适配的是 BERT 类 token 模型。

## E — Execution

**必需输入**: 词级标注数据集 (tokens + 标签序列)、tokenizer; 数据无词级标注时说明无法做对齐, 先问标注格式。

1. tokenize with word_ids (fast tokenizer)。完成标准: 每 token 可得 word_idx 或 None。
2. 对齐: None → -100; 词首子词 → 原标签 (保留 B-); 后续子词 → B-XXX 改 I-XXX (p59)。
3. 打印样例 original/updated 对比, 人工抽查 ≥2 条。
4. (可选) 领域 MLM: 领域语料 + mlm_probability=0.15 续训, 完成标准 = fill-mask 探针显示领域词分布变化。
5. 训练后 seqeval overall_f1 评估 (评估自动跳过 -100)。

**输出契约**: 对齐后 dataset + 对齐对比样例 + F1; 完成标准 = 对齐抽查无误且 F1 报告完整。

## B — Boundary

- 不要用于: 句级分类/回归 (无标签对齐问题); 生成式任务。
- 边界细节: 特殊 token 必须 -100, 若用 0 会被当成 O 标签污染指标; seqeval 的实体级 F1 与 token 级 accuracy 不是一回事, 别混报。
- 版本边界 (ce15): 书钉 transformers==4.41.2, Trainer/evaluate API 有变动, 思路照迁、代码按当前版重写。
- 作者盲点: 书未给对齐错误导致的 F1 损失量化, "常见错误点"结论来自任务性质推断, 实际影响需自测。

## 相关能力 (also_read, 阶段 3)

- composes-with: `p59-ner-label-alignment` (NER 标签对齐), `p66-gpu-vram-cleanup` (续训显存运维)
