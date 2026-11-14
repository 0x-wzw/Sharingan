# 决策规则速查 — Build a Large Language Model (From Scratch) × Hands-On Large Language Models

| 能力 | 一句话规则 |
|---|---|
| GPT-2 预训练全流水线 | 从原始文本出发搭建并预训练 GPT-2 基座：分词→批处理→因果注意力→组装→训练循环→困惑度评估→受控解码→存档验证。 |
| 文本分类微调 | 把预训练 LLM 改造成分类器：换分类头→取最后 token logits→定冻结预算→备数据与 padding→交叉熵训练与全集评估。 |
| 指令微调与 LLM-as-a-judge 评估 | 把预训练模型指令微调成助手 (Alpaca 数据、custom collate、-100 掩码) 并用确定性 LLM-as-a-judge 协议自动评估回复质量。 |
| LoRA / PEFT 参数高效微调 | 参数高效微调：LoRA 低秩适配 (A/B 初始化、rank/alpha、挂层选择) 与 QLoRA (nf4) SFT→DPO 两段式偏好对齐。 |
| RAG 检索管线 | 搭建检索管线：chunk 切块→带 search_document/query 前缀嵌入→向量检索→BM25+rerank 混合→RAG 模板接地生成。 |
| 嵌入模型适配 | 适配/训练嵌入模型：句对 loss 选型、银标数据增广 (Augmented SBERT)、TSDAE 无监督领域适配、STS-B→MTEB 评估与维度一致性。 |
| 主题建模五段流水线 | 用嵌入+聚类 (UMAP/HDBSCAN/c-TF-IDF) 的现代路线替代 LDA 做主题建模，并给每个簇生成可读关键词。 |
| Prompt 六要素结构法 | 用六要素结构法系统化设计 prompt 模板，让输出形态稳定而不是靠重掷骰子。 |
| 推理增强三级决策 | 按成本升序在 few-shot CoT→zero-shot CoT→ToT 三级间做推理增强选型，平衡正确率与成本。 |
| 结构化输出两层约束 | 用 prompt 层+约束采样两层手段保证 LLM 输出机器可解析 (JSON/schema)，解决解析失败与格式跑偏。 |
| 多步任务链式拆解 | 把有先后依赖的多步任务拆成 prompt 链，上一步输出作为下一步输入，避免单个长 prompt 后半段跑题。 |
| 对话记忆选型 | 为多轮对话选记忆策略 (窗口/摘要/缓冲)，平衡上下文完整性与 token 费用。 |
| ReAct agent 循环 | 实现 ReAct agent 循环：Thought→Action→Observation 迭代 + 工具调用协议 + 解析容错。 |
| MLM 续训 + NER 标签对齐 | 让 BERT 先 MLM 续训适配领域语料再做 NER/token 分类，核心是子词级标签对齐 (-100 忽略位、B-I 标签)。 |
| 七段 prompt 结构 | 按七段 (persona/instruction/context/data_format/example/tone 等) 拼装或审查 prompt 模板的规则卡。 |
| CoT / zero-shot CoT / ToT 技巧族 | 四个推理技巧的具体 prompt 写法：few-shot CoT、zero-shot CoT、ToT 三专家、链式拆解。 |
| KV cache 加速生成 | 用 KV cache (use_cache/past_key_values) 加速 LLM 生成，及与 gradient checkpointing 的冲突处理。 |
| NER 标签对齐 | NER/token 分类中标签与子词对齐的具体规则：-100 忽略位、首子词打标、B-I 标签修正。 |
| 对话记忆三策略 | 对话记忆三策略 (缓冲/窗口/摘要) 的机制与代码形态。 |
| ReAct 输出格式 | ReAct 的 Thought/Action/Observation 输出格式契约：agent_scratchpad、解析错误处理。 |
| API 成本控制: 先小后大 | 付费 API 批量跑数据前先小样本试跑，控制调用量、token 配额与成本。 |
| GPU 显存清理流程 | 连续训练多个模型之间的 GPU 显存清理流程 (释放模型、empty_cache、重置显存)。 |
| 下载代码三条工程约定 | 数据集/模型权重下载脚本的三条工程约定：显式 timeout、raise_for_status、防静默失败。 |

> 速查只给结论；需要原文依据、案例或反例时读对应能力卡。
