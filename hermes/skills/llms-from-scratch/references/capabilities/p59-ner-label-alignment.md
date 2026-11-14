# NER 标签对齐 (p59) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 11 章 | 绑定单元: p59 (母方法: f29 MLM 续训 + NER 对齐, 见 f29-mlm-continued-pretraining-ner-alignment.md) | 支持材料: c17, ce15
> 去向: source-router 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "# If the label is B-XXX we change it to I-XXX" ... "updated_label = -100 if word_idx is None else label[word_idx]"

— Alammar & Grootendorst, ch11 (chapter11_Chapter 11 - Fine-Tuning BERT.txt @555)

自译: 子词化后, 词内第 2 个起的所有子词若原标签是 B-XXX 就改成 I-XXX; 特殊 token 无词对应, 标 -100 供交叉熵忽略。

## I — Interpretation (自述)

这是 f29 中 NER 分支的核心规则, 三条判据按序执行: ①word_idx 为 None (特殊 token) → -100; ②词的首子词 → 原标签; ③后续子词 → B- 前缀改 I-。前提是 tokenizer 提供 word_ids 映射。评估时 seqeval 自动忽略 -100, 实体级 F1 才有效。任何一条走错 (如全部沿用原标签、或把 -100 填 0) 都会让训练与指标静默失真。

## A1 — Application Example

### 示例: "ChatGPT" 对齐演算 (c17 依据的规则; 原书样例 train[848])

- **类型与来源**: 原书 worked_example (ch11 align_labels 与 original/updated 打印); 下列子词演算为按 p59 规则的合成复算。
- **问题/输入**: 词 "ChatGPT" 标 B-PER。
- **方法论的使用**: tokenizer 拆为 [Chat, ##GPT] → 首子词保 B-PER; 后续子词 B-PER→I-PER; 结果 [B-PER, I-PER]; 特殊 token [CLS]/[SEP] → -100。
- **结论/预期输出**: 标签序列与子词一一对应; updated 序列可直接进 Trainer。

## A2 — Future Trigger ★

### 情境

1. NER/token 分类训练报标签长度不匹配, 或 F1 低得可疑。
2. 用户问"标签和 token 对不齐怎么办 / -100 含义"。

### 语言信号

- "label alignment / 子词对齐 / B- I- / -100 / seqeval / ner_tags"

### 与相邻 skill 区分

- f29 是完整两分支 (MLM+NER); 本卡只管对齐规则。句级分类无对齐问题 (text-classification-finetuning)。

## E — Execution

**必需输入**: 词级标注样本 + fast tokenizer (需 word_ids)。

1. tokenize(..., return_offsets_mapping/word_ids) 建立子词→词映射。
2. 逐 token 应用三条判据 (None→-100; 首子词→原标签; 后续→B改I)。
3. 抽查 ≥2 条打印 original vs updated; 判停: 任意子词标签序列错位 → 修 word_idx 逻辑再训。
4. 训练 + seqeval overall_f1 (自动跳过 -100)。

**输出契约**: 对齐后 labels + 抽查对比 + F1; 完成标准 = 抽查全对且 F1 报告完整。

## B — Boundary

- 不要用于: 词级 tokenizer (无子词拆分) 场景规则退化为恒等; 非token分类任务。
- 指标边界: seqeval 实体级 F1 ≠ token accuracy, 报告要写明口径。
- 版本边界 (ce15): transformers tokenizer/Trainer 签名随版本变, 规则不变、代码按当前版写。

## 相关能力 (also_read, 阶段 3)

- composes-with: `f29-mlm-continued-pretraining-ner-alignment` (NER 续训流程)
