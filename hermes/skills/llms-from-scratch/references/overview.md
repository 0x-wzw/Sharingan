# book/overview.md — llms-from-scratch × hands-on-llms 能力 Bundle 总览 (阶段 3)

> 编译时随产物分发。来源: `books/llms-from-scratch/BOOK_OVERVIEW.md` (阶段 0, 保留其全部论证) + `books/llms-from-scratch/references.md` R-01 (reference 单元 f31, 全文并入下方参考区)。
> 相关词典见同目录 `glossary.md` (24 条核心术语 + 两书术语对齐/分歧表)。

## 1. 书的基本信息

- **主骨架**: *Build a Large Language Model (From Scratch)*, Sebastian Raschka, Manning, 2024 — 不依赖任何 LLM 库, 用 PyTorch 逐行实现 GPT-2 风格模型的完整生命周期 (分词 → 注意力 → 架构 → 预训练 → 微调), 让读者从内部机制理解 LLM。
- **耦合层**: *Hands-On Large Language Models*, Alammar & Grootendorst, 2024 — 应用技术补齐 Raschka 的刻意缺口 (嵌入、聚类/主题建模、语义检索、prompt 工程、BERT 分类、多模态、生成工具)。
- 结构为严格**递进/流水线**: 每章产物是下一章输入 (数据 → 注意力 → 模型 → 预训练权重 → 微调); ch06/ch07 是并列的两条微调路线; 附录 D/E 是第 5/6 章的深化。
- 完整的结构/解释/批判/应用潜力分析 (13 条核心命题、论证链、作者盲点、最强反对意见、12 项任务基准) 见 `books/llms-from-scratch/BOOK_OVERVIEW.md`, 内容全部有效。

## 2. 参考区 — R-01 (原候选 f31) 双路线心智模型 (reference, 全文保留)

**title**: 生成式 vs 表示式; 改权重 vs 不改权重 — 全书选型二维地图
**type**: framework (重建性)

- **判定理由**: V1 支持材料真实但分散 — "two-step approach" 在 ch04/ch12 命中, "representative and generative" 语义命中; 但该二维地图是候选对两书组织结构的**跨章重建**, 原文没有一处集中陈述。按 task-first-v2 判据记 reference, 不独立成能力。
- **V2**: 作为检查单可用 — 新任务 → 先问输出形式 (文本 vs 向量) → 再问是否需要改权重 → 穷尽 prompt/RAG 再微调。
- **保留理由**: 去重后与 f15 (分类选型) 部分重叠, 但覆盖面更广 (含 embedding 训练 / 生成微调), 作为导览保留。
- **审计状态**: 判定由候选期 "verified 待定" → 验证期 "reference" (verified-framework.md 总览中原 f31* 记录保留); 最终非 rejected, 保留于 references.md, 无审计线索删除。

### 作为上层导览的使用方式

这张二维地图是本 Bundle 全部能力卡的**导航检查单**:

- **轴一 (输出形式)**: 要文本/类别 → 生成式路线 (GPT 类 decoder); 要向量 (相似度/检索/聚类) → 表示式路线 (embedding/encoder 模型)。对应术语见 glossary g03/g04。
- **轴二 (是否改权重)**: 不改权重 → prompt 工程 (f17/p44/f18/p45)、RAG (rag-retrieval-pipeline)、in-context learning (g13); 改权重 → 微调家族 (text-classification-finetuning / instruction-finetuning-and-eval / lora-peft-finetuning / embedding-model-adaptation)。
- 与 f15/f19/f21/f24/f27/f30 等 verified 流程单元的关系: 它们是这张地图上**具体格子的可执行展开**; f31 本身不独立成能力卡, 只做导览。

## 3. 能力地图 (Stage 1.6 送达, Stage 3 链接后)

**Promoted 能力 (6, 各自独立入口)** — 推荐学习顺序按依赖推出:

1. `gpt2-pretraining-pipeline` — 从原始文本训练出基座 (全卡自足, 一切的起点)
2. `text-classification-finetuning` — 预训练权重 → 类别 logits (depends-on #1)
3. `instruction-finetuning-and-eval` — 预训练权重 → 指令助手 + LLM-as-a-judge 评估 (depends-on #1)
4. `lora-peft-finetuning` — 参数高效微调 / QLoRA SFT→DPO (composes-with #3)
5. `rag-retrieval-pipeline` — 检索管线 chunk→embed→hybrid→rerank→grounded generation (消费现成嵌入; composes-with #3)
6. `embedding-model-adaptation` — 嵌入模型生产端 (loss 选型 / 银标 / TSDAE / STS→MTEB; 供 #5 消费)

**Router 能力 (18, 由 source-router 入口服务)**: f16 (主题建模), f17/p44 (prompt 六要素/七段), f18/p45 (CoT/ToT 推理决策), f19 (结构化输出), f20 (链式提示), f21/p62 (会话记忆), f22/p63 (ReAct), f29/p59 (MLM 续训 + NER), p48 (KV cache), p65 (API 成本), p66 (显存运维), p67 (下载/代码约定)。

**链接网络 (阶段 3)**: 18 条关系边, 每张卡的 also_read / depends-on / contrasts-with / composes-with 见各卡末尾 "相关能力" 段。核心结构: 预训练管线是三个微调卡的共同依赖; LoRA↔分类微调 (c08 消融) 与 RAG↔嵌入适配 (消费端 vs 生产端) 是两条对比轴; router 卡内部按同主题双卡成对链接 (f17↔p44, f18↔p45, f21↔p62, f29↔p59, f22↔p63, f20↔f22)。
