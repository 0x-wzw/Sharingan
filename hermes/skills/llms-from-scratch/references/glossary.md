# Glossary — 合并关键概念词典 (Raschka × Alammar/Grootendorst)

> cangjie-skill 流水线 glossary extractor 产出 (阶段 1)。作为所有下游 skill 的共享词典。
> 覆盖: `books/llms-from-scratch/source/` (Raschka, *Build a LLM From Scratch*, 标签 **[LFS]**) 与 `books/hands-on-llms/source/` (Alammar & Grootendorst, *Hands-On LLMs*, 标签 **[HO**])。
> 每条含 `books` (来源) 与 `def_files` (定义原文所在源文件)。引用均经回原文核验。
> 数量: 24 条核心术语 (≤30 上限)。文末附两书术语对齐/分歧表。

## 术语条目

```yaml
- id: g01
  term: token / token ID
  type: term
  books: [LFS, HO]
  source_chapter: LFS ch02 / HO ch02
  author_definition: |
    [LFS] 文本经正则或 BPE 切分出的单元, 及其在词表中的整数编号; "Next, we convert the text tokens
    into token IDs that we can process via embedding layers later."
    [HO] AutoTokenizer 的输出; 作者用同一句话跑 8 种 tokenizer (BERT/GPT-2/Flan-T5/GPT-4/Phi-3…) 并排比较来定义它。
  key_distinction: |
    ≠ "单词" — 子词 (subword) 才是典型单位; BPE 把词表外的词拆成子词。
    [HO] tokenization 不是通用预处理步骤, 而是每个模型不可分离的组件 (tokenizer 差异直接影响成本与能力)。
  why_it_matters: |
    两书都把 token 当作一切后续处理的原子单位。若沿用"token=单词"的常识,
    分类/成本估算/上下文长度相关的 skill 全部会算错粒度。
  tags: [term, core-concept]
  def_files: [llms-from-scratch/source/ch02_01_main-chapter-code_ch02.txt, hands-on-llms/source/chapter02_Chapter 2 - Tokens and Token Embeddings.txt]

- id: g02
  term: embedding (token embedding)
  type: term
  books: [LFS, HO]
  source_chapter: LFS ch02 §2.7 / HO ch02
  author_definition: |
    [LFS] 可训练的查找表: "Creating token embeddings" — 把 token ID 映射为高维 (768 维) 向量,
    等价于 one-hot × 线性层 (见 ch02_03_bonus embedding-vs-matmul)。
    [HO] 语义空间中的向量, "Contextualized Word Embeddings From a Language Model (Like BERT)"。
  key_distinction: |
    ≠ 预训练 word2vec/GloVe 那种现成静态向量 — [LFS] 的 embedding 是随机初始化、随训练更新的层。
    [HO] 明确区分 static word embedding (上下文无关) 与 contextualized/text embedding (上下文相关)。
    ≠ 泛指的 "特征表示" (feature representation) — 见 g03。
  why_it_matters: |
    "embedding" 是两书共用但用法有别的最高频词。下游 skill 必须知道说话的是哪一种
    (可训练查找表 vs 上下文向量 vs 表示模型输出), 否则会把静态向量当可训练、或反之。
  tags: [term, core-concept]
  def_files: [llms-from-scratch/source/ch02_01_main-chapter-code_ch02.txt, llms-from-scratch/source/ch02_03_bonus_embedding-vs-matmul_embeddings-and-linear-layers.txt, hands-on-llms/source/chapter02_Chapter 2 - Tokens and Token Embeddings.txt]

- id: g03
  term: 表示式模型 (representational / embedding model)
  type: term
  books: [HO]
  source_chapter: HO ch04–05, ch10–11
  author_definition: |
    [HO] SentenceTransformer 类双编码器 (all-mpnet-base-v2, gte-small, all-MiniLM-L6-v2),
    "Text Classification with Representation Models" — 输出向量供分类/聚类/检索用。
  key_distinction: |
    = 把文本整体映射为一个向量 (句子/文本级) 的 encoder 模型。
    ≠ "embedding" 一词的日常混用 — embedding model 输出的文本向量 ≠ word embedding ≠ 训练中的嵌入层。
    ≠ 生成式模型 (g04): 表示式模型输出向量, 生成式模型输出 token。
  why_it_matters: |
    HO 的组织原则是 generative vs. representational 对偶。若把 "embedding model" 误解为
    "带嵌入层的模型", 选型类 skill (分类/聚类/检索) 会整体失真。
  tags: [term, core-concept]
  def_files: [hands-on-llms/source/chapter04_Chapter 4 - Text Classification.txt, hands-on-llms/source/chapter05_Chapter 5 - Text Clustering and Topic Modeling.txt]

- id: g04
  term: 生成式模型 (generative / decoder LLM)
  type: term
  books: [HO, LFS]
  source_chapter: HO ch01, ch03 / LFS ch04–05
  author_definition: |
    [HO] 以 Phi-3-mini-4k-instruct 为标准实验对象的自回归模型, 经 `pipeline("text-generation")`
    或 GGUF+llama.cpp 调用; ch03 用 `model.model(...)` vs `model.lm_head(...)` 切开隐藏状态与 logits。
    [LFS] 自建 GPT-2 骨架逐 token 自回归生成 (generate_text_simple)。
  key_distinction: |
    ≠ 泛指一切能生成文本的模型 — [HO] 特指现代 chat-instruct decoder。
    = 逐 token 预测、概率分布经采样得到输出的自回归模型。
  why_it_matters: |
    "生成式 vs 表示式" 的选型判断是两书共同的分叉点; 沿用常识义会把 encoder 模型也归入生成式。
  tags: [term, core-concept]
  def_files: [hands-on-llms/source/chapter01_Chapter 1 - Introduction to Language Models.txt, hands-on-llms/source/chapter03_Chapter 3 - Looking Inside LLMs.txt, llms-from-scratch/source/ch04_01_main-chapter-code_ch04.txt]

- id: g05
  term: attention score vs attention weight
  type: term
  books: [LFS]
  source_chapter: LFS ch03
  author_definition: |
    [LFS 原文] "By convention, the unnormalized attention weights are referred to as **'attention scores'**
    whereas the normalized attention scores, which sum to 1, are referred to as **'attention weights'**."
  key_distinction: |
    score = softmax 前的未归一化点积 (Q·K / √d); weight = softmax 后、和为 1 的归一化分数。
    ≠ 很多文献/教程把两者混用 — [LFS] 明确区分; [HO] 图示层不严格区分。
  why_it_matters: |
    注意力相关 skill (实现、推导、调试) 的正确性依赖这一区分: 拿 weight 去做 mask/缩放是常见 bug 来源。
  tags: [term, core-concept, terminology-reconciliation]
  def_files: [llms-from-scratch/source/ch03_01_main-chapter-code_ch03.txt]

- id: g06
  term: context vector z^(i)
  type: term
  books: [LFS]
  source_chapter: LFS ch03
  author_definition: |
    [LFS] "A context vector… is a weighted sum over all inputs x^(1) to x^(T) weighted with respect to
    the second input element" — 以第 i 个 token 为 query 时, 按注意力权重对所有输入加权和得到的向量。
  key_distinction: |
    ≠ embedding x^(i) — x 是输入嵌入, z 是聚合了全序列信息后的表示。
    [HO] 同一概念在图中称为 "自注意力后的输出/上下文化表示", 不用 z^(i) 记号。
  why_it_matters: |
    LFS 的注意力推导主线词; 与 g02/g05 一起构成注意力三件套 (x → score/weight → z)。
  tags: [term, core-concept]
  def_files: [llms-from-scratch/source/ch03_01_main-chapter-code_ch03.txt]

- id: g07
  term: causal / masked attention
  type: term
  books: [LFS]
  source_chapter: LFS ch03
  author_definition: |
    [LFS] 只允许当前及之前位置参与注意力的掩码机制 (mask 上三角为 -inf 再 softmax),
    是 GPT 能自回归生成的原因; CausalAttention → MultiHeadAttention 是 ch03 交付物。
  key_distinction: |
    ≠ 双向 (encoder 风格) 注意力 — [HO] ch11 微调的 BERT 就是双向注意力, 两书正好互补。
  why_it_matters: |
    决定了 "decoder 只能看过去" 这一生成模型基本假设; 混淆会导致实现时漏 mask 或错掩。
  tags: [term, core-concept]
  def_files: [llms-from-scratch/source/ch03_01_main-chapter-code_ch03.txt]

- id: g08
  term: context length / sliding window
  type: term
  books: [LFS]
  source_chapter: LFS ch02
  author_definition: |
    [LFS] 模型最大输入 token 数 (GPT-2 为 1024, `context_length`); 用滑动窗口把长文本切成重叠的
    (input, target=右移一位) 训练对 — dataloader 的 max_length/stride。
  key_distinction: |
    ≠ 语料总长度; 也 ≠ [HO] 书中的 n_ctx (Phi-3 为 4k) — 数值随模型而变, 概念相同。
  why_it_matters: |
    数据流水线 skill 的核心参数; 混淆 stride 与 max_length 会造成训练对重叠错误。
  tags: [term]
  def_files: [llms-from-scratch/source/ch02_01_main-chapter-code_ch02.txt, llms-from-scratch/source/ch02_04_bonus_dataloader-intuition_dataloader-intuition.txt]

- id: g09
  term: pretraining (下一词预测)
  type: term
  books: [LFS, HO]
  source_chapter: LFS ch05 / HO ch11 (MLM), ch10 (TSDAE)
  author_definition: |
    [LFS] 在无标注文本上做下一 token 预测, 目标函数只有对每个位置的交叉熵。
    [HO] 同类概念是 MLM (BERT 式完形填空) 与 TSDAE — "Unsupervised Learning: Transformer-based
    Denoising AutoEncoder (TSDAE)"。
  key_distinction: |
    = 无标注、自监督、目标由输入自身构造。
    ≠ finetuning (g10) — 需人工标签/指令数据; [HO] 的领域适配 (MLM/TSDAE) 属于预训练家族而非微调家族。
  why_it_matters: |
    两书对 "预训练" 的形态不同 (CLM vs MLM/去噪), 合并词典必须都收, 否则 skill 会只认一种。
  tags: [term, core-concept]
  def_files: [llms-from-scratch/source/ch05_01_main-chapter-code_ch05.txt, hands-on-llms/source/chapter10_Chapter 10 - Creating Text Embedding Models.txt]

- id: g10
  term: finetuning (分类微调 vs 指令微调)
  type: term
  books: [LFS, HO]
  source_chapter: LFS ch06–07 / HO ch10–12
  author_definition: |
    [LFS] 把预训练权重接到新任务上继续训练。两条路线: 分类微调 (换分类头、小数据、spam 分类器)
    与指令微调 (Alpaca 格式、保持生成头)。
    [HO] 分表示模型线 (Ch11 全参/冻结层/SetFit) 与生成模型线 (Ch12 "instruction tuning (SFT) +
    preference tuning (DPO/PPO)" 两段式)。
  key_distinction: |
    ≠ 笼统的 "再训练" — [HO] 生成模型微调明确 = SFT + 偏好对齐两步。
    ≠ in-context learning (g13) — 微调改权重, ICL 不改权重。
  why_it_matters: |
    两书都把微调拆成结构化路线而非单一动作; 下游微调类 skill 的分支判断依赖这个拆分。
  tags: [term, core-concept]
  def_files: [llms-from-scratch/source/ch06_01_main-chapter-code_ch06.txt, llms-from-scratch/source/ch07_01_main-chapter-code_ch07.txt, hands-on-llms/source/chapter12_Chapter 12 - Fine-tuning Generation Models.txt]

- id: g11
  term: SFT (supervised/instruction tuning) 与 DPO (preference tuning)
  type: term
  books: [HO, LFS]
  source_chapter: HO ch12 / LFS ch07 bonus (dpo-from-scratch)
  author_definition: |
    [HO] "Preference Tuning (PPO/DPO)" — SFT 用 ultrachat 指令数据 (QLoRA), DPO 用 dpo-pairs
    (chosen/rejected, beta=0.1) 做偏好对齐。
    [LFS] ch07 bonus 从零实现 DPO (create-preference-data + dpo-from-scratch.txt)。
  key_distinction: |
    SFT: 模仿示范答案的监督训练; DPO: 在 SFT 之上用偏好对 (正/负回答) 对齐, 不需要奖励模型。
    ≠ RLHF (PPO) — DPO 直接优化偏好, 无显式 reward model。
  why_it_matters: |
    现代 "微调一个助手" 的标准两段式; 两书以不同深度互补 (HO 工程配置 / LFS 从零实现)。
  tags: [term, core-concept]
  def_files: [hands-on-llms/source/chapter12_Chapter 12 - Fine-tuning Generation Models.txt, llms-from-scratch/source/ch07_04_preference-tuning-with-dpo_dpo-from-scratch.txt]

- id: g12
  term: LoRA / QLoRA
  type: term
  books: [LFS, HO]
  source_chapter: LFS 附录 E / HO ch12
  author_definition: |
    [LFS] "Low-rank adaptation (LoRA) is a machine learning technique that modifies a pretrained model
    to better…" — 不更新 W, 只学习低秩增量 ΔW ≈ AB, 训练后可合并或即时应用。
    [HO] QLoRA = 4-bit NF4 量化加载 (BitsAndBytesConfig) + LoRA adapter (r=64, alpha=32,
    target 全部投影层) + paged_adamw_32bit; 单卡 T4 可跑。
  key_distinction: |
    QLoRA ≠ LoRA — Q = 底座量化 (省显存), LoRA = 旁路低秩更新 (省训练量); 两者正交可组合。
  why_it_matters: |
    参数高效微调的代表; skill 需区分量化层与适配器层, 否则配置/合并步骤会出错。
  tags: [term, core-concept]
  def_files: [llms-from-scratch/source/appendix-E_01_main-chapter-code_appendix-E.txt, hands-on-llms/source/chapter12_Chapter 12 - Fine-tuning Generation Models.txt]

- id: g13
  term: in-context learning (zero/one/few-shot)
  type: term
  books: [HO]
  source_chapter: HO ch06
  author_definition: |
    [HO] "In-Context Learning: Providing Examples" — 在 messages 数组里放示范对话对
    (包括用造词示例让模型学会新词)。
  key_distinction: |
    = 不改权重的能力迁移, 与微调形成对照。
    ≠ 训练/学习 — 只是 prompt 里的条件化。
  why_it_matters: |
    "改 prompt 还是改权重" 是两书共同的第一分叉; ICL 是零成本一侧的代表词。
  tags: [term, core-concept]
  def_files: [hands-on-llms/source/chapter06_Chapter 6 - Prompt Engineering.txt]

- id: g14
  term: prompt 工程六要素 (persona / instruction / context / data_format / audience / tone)
  type: term
  books: [HO]
  source_chapter: HO ch06
  author_definition: |
    [HO] 结构化组件拼接: `persona`、`instruction`、`context`、`data_format`、`audience`、`tone` +
    `data` — "Prompt components persona = 'You are an expert in Large Language models…'"。
  key_distinction: |
    ≠ 零散 "咒语技巧" — [HO] 把 prompt 当可组合的模板化结构, 逐项可控。
  why_it_matters: |
    prompt 类 skill 的骨架; 按六要素评审 prompt 是 HO 的特有方法论。
  tags: [term, methodology]
  def_files: [hands-on-llms/source/chapter06_Chapter 6 - Prompt Engineering.txt]

- id: g15
  term: CoT / Zero-shot CoT / ToT
  type: term
  books: [HO]
  source_chapter: HO ch06 ("Reasoning with Generative Models")
  author_definition: |
    [HO] "Chain-of-Thought: Think Before Answering" — 在 prompt 中给出带推理过程的示例 (CoT) /
    追加 "Let's think step-by-step" (Zero-shot CoT) / "三个专家轮流写一步" 模板 (Tree-of-Thought)。
  key_distinction: |
    [HO] 归类为 prompt 技术而非模型能力 — 与 bonus 的 "推理 LLM (DeepSeek-R1)" (训练出来的推理) 相对。
  why_it_matters: |
    区分 "prompt 激活的推理" 与 "训练出的推理" 是选择手段的前提。
  tags: [term]
  def_files: [hands-on-llms/source/chapter06_Chapter 6 - Prompt Engineering.txt, hands-on-llms/source/bonus_7_reasoning_llms.md]

- id: g16
  term: KV cache
  type: term
  books: [HO, LFS]
  source_chapter: HO ch03 / LFS ch04_03 bonus
  author_definition: |
    [HO] "Speeding up generation by caching keys and values" — `model.generate(use_cache=True/False)`
    的显式计时对比。
    [LFS] ch04_03_kv-cache README: 缓存历史 K/V 避免每步重算全部位置。
  key_distinction: |
    = 推理期优化, 不改变模型输出语义。
    ≠ 训练期技巧; 也不是记忆/上下文 (context) 本身。
  why_it_matters: |
    两书都演示同一机制 ([LFS] 从零实现 / [HO] 调 API 对比), 互补覆盖。
  tags: [term]
  def_files: [hands-on-llms/source/chapter03_Chapter 3 - Looking Inside LLMs.txt, llms-from-scratch/source/ch04_03_kv-cache_README.md]

- id: g17
  term: sampling / decoding (temperature, top-k, top_p)
  type: term
  books: [LFS, HO]
  source_chapter: LFS ch05 §5.3 / HO ch01, ch03
  author_definition: |
    [LFS] "two concepts, so-called decoding strategies… *temperature scaling* and *top-k* sampling"
    — 控制生成的随机性与多样性。
    [HO] "Choosing a single token from the probability distribution (sampling / decoding)" —
    temperature/top_p/do_sample 逐个演示。
  key_distinction: |
    temperature: 压平/削尖分布; top-k / top_p: 截断候选集。greedy (argmax) 是采样为零的特例。
  why_it_matters: |
    生成类 skill 的公共旋钮; 参数名跨框架差异 (top-k vs top_p) 是常见混淆点。
  tags: [term, core-concept]
  def_files: [llms-from-scratch/source/ch05_01_main-chapter-code_ch05.txt, hands-on-llms/source/chapter03_Chapter 3 - Looking Inside LLMs.txt]

- id: g18
  term: perplexity
  type: term
  books: [LFS]
  source_chapter: LFS ch05 §5.1.2
  author_definition: |
    [LFS] "Calculating the text generation loss: cross-entropy and perplexity" — 交叉熵损失的指数,
    用作生成模型的可解释评估指标。
  key_distinction: |
    ≠ 准确率 — 适用于生成/语言建模任务, 不适用于分类微调 (那里用 F1/accuracy, 见 g19)。
  why_it_matters: |
    决定 "评估哪类模型用哪个指标" 的选型规则。
  tags: [term]
  def_files: [llms-from-scratch/source/ch05_01_main-chapter-code_ch05.txt]

- id: g19
  term: ignore_index = -100 (padding 掩蔽)
  type: term
  books: [LFS, HO]
  source_chapter: LFS ch07 / HO ch11 (NER 标签对齐)
  author_definition: |
    [LFS] "we replace the token IDs corresponding to `50256` with `-100`" — 用 -100 填充 padding,
    使 cross_entropy 忽略之; 但保留首个 `<|endoftext|>` 以标记回答结束。
    [HO] NER 微调中同样的 -100 对齐技巧 ("align_labels") 用于 token 分类。
  key_distinction: |
    ≠ 简单删除 padding — 位置保留但损失忽略; -100 是 PyTorch cross_entropy 的默认忽略值。
  why_it_matters: |
    指令微调与 token 分类正确性的关键细节, 两书不约而同使用, 是高置信共享知识点。
  tags: [term, pitfall]
  def_files: [llms-from-scratch/source/ch07_01_main-chapter-code_ch07.txt, hands-on-llms/source/chapter11_Chapter 11 - Fine-Tuning BERT.txt]

- id: g20
  term: RAG (retrieval-augmented generation)
  type: term
  books: [HO]
  source_chapter: HO ch08
  author_definition: |
    [HO] 检索 (chunk → embed → FAISS 索引 → 最近邻) + grounding prompt 注入;
    "Example: RAG with Local Models" (LlamaCpp + bge-small); 附带引用可验证。
  key_distinction: |
    = 把检索到的文档塞进 prompt 里做 grounded generation。
    ≠ "向量数据库套壳" — 作者强调 hybrid (BM25 + dense) 与 rerank 才是完整方案;
    dense retrieval 有明确 caveats ("What is the mass of the moon?" 检索失败案例)。
  why_it_matters: |
    HO 独有的应用层枢纽; skill 需携带 caveats, 不能当成无损方案。
  tags: [term, core-concept]
  def_files: [hands-on-llms/source/chapter08_Chapter 8 - Semantic Search.txt]

- id: g21
  term: dense retrieval / hybrid / rerank
  type: term
  books: [HO]
  source_chapter: HO ch08
  author_definition: |
    [HO] dense: 嵌入向量最近邻 ("Dense Retrieval Example"); hybrid: BM25 (rank_bm25) + dense;
    rerank: "Reranking Example" 用 co.rerank 对粗排结果精排。
  key_distinction: |
    dense 擅长语义、会失败于词汇/事实型查询 → 必须 hybrid + rerank 补足。
  why_it_matters: |
    检索类 skill 的三段决策 (稠密→混合→重排) 直接来源于此。
  tags: [term]
  def_files: [hands-on-llms/source/chapter08_Chapter 8 - Semantic Search.txt]

- id: g22
  term: freeze layers (冻结层微调)
  type: term
  books: [HO, LFS]
  source_chapter: HO ch11 / LFS ch06
  author_definition: |
    [HO] "Freeze Layers" — 全参 vs 冻结 (classifier / blocks 1–5) 实验, 给出逐层 F1 曲线
    (前 4 层冻结后性能趋稳)。
    [LFS] ch06 分类微调同样冻结大部分层只训最后块与分类头。
  key_distinction: |
    = 冻结底层、只训高位层/新头, 是预算-性能权衡的标准手段。
    ≠ LoRA (g12) — 冻结是"不训", LoRA 是"旁路低秩地训"。
  why_it_matters: |
    两书独立的同结论实验, 属于可合并的高置信方法。
  tags: [term]
  def_files: [hands-on-llms/source/chapter11_Chapter 11 - Fine-Tuning BERT.txt, llms-from-scratch/source/ch06_01_main-chapter-code_ch06.txt]

- id: g23
  term: SetFit / few-shot 分类
  type: term
  books: [HO]
  source_chapter: HO ch11
  author_definition: |
    [HO] `setfit>=1.0.3`, SetFitTrainer, `sample_dataset num_samples=16` — 16 样本/类的
    few-shot 分类方法。
  key_distinction: |
    = 基于表示模型 + 示例对训练的高效少样本方案。
    ≠ zero-shot 分类 (用 NLI/entailment prompt) — SetFit 需要 16 个标注样本但精度高得多。
  why_it_matters: |
    标注稀缺场景的高性价比路线, HO 独有。
  tags: [term]
  def_files: [hands-on-llms/source/chapter11_Chapter 11 - Fine-Tuning BERT.txt]

- id: g24
  term: LLM-as-a-judge
  type: term
  books: [LFS]
  source_chapter: LFS ch07 §7.8
  author_definition: |
    [LFS] 用另一个本地 LLM (Ollama 跑 Llama 3 8B) 给指令微调模型的输出打分
    (llm-instruction-eval-ollama.txt)。
  key_distinction: |
    = 以 LLM 评 LLM 的相对评估法。
    ≠ 自动指标 (perplexity/accuracy); [LFS] 自身批判: judge 可靠性未系统论证, 结论需谨慎。
  why_it_matters: |
    指令微调评估的唯一书内方案; 下游 skill 必须带上其可靠性边界。
  tags: [term, boundary-marked]
  def_files: [llms-from-scratch/source/ch07_03_model-evaluation_llm-instruction-eval-ollama.txt]
```

## 术语对齐/分歧表 (两书如何说同一件事)

| 概念 | [LFS] 用词 | [HO] 用词 | 合并裁定 |
|---|---|---|---|
| softmax 前的点积 | attention score | (图示中不严格区分) | 以 [LFS] 为准: score=未归一化, weight=归一化 (g05) |
| token 的向量表示 | token embedding (可训练查找表) | word embedding vs contextualized embedding (静态 vs 上下文) | "embedding" 一词必须带限定词使用 (g02/g03) |
| 输出向量供分类/检索的模型 | (不设此分类轴) | representational / embedding model | 概念保留 HO 术语 (g03) |
| 预训练形态 | CLM: 下一词预测 | MLM / TSDAE 去噪 | 都属 pretraining 家族, 目标函数不同 (g09) |
| 微调生成模型 | instruction finetuning (ch07) | SFT + preference tuning (DPO) 两段式 | HO 拆分更细, 采纳两段式框架 (g10/g11) |
| 参数高效微调 | LoRA (附录 E, 从零实现) | QLoRA (量化+adapter, 工程配置) | 术语区分 LoRA/QLoRA (g12) |
| 推理加速 | KV cache bonus (从零) | use_cache 开关对比 | 同一机制 (g16) |
| 解码控制 | temperature + top-k | temperature + top_p (+do_sample) | 同族超参, 记录跨框架差异 (g17) |
| padding 忽略 | ignore_index=-100 | -100 标签对齐 (NER) | 共享知识点 (g19) |
| 冻结策略 | ch06 冻结+分类头 | ch11 逐层冻结 F1 曲线 | 合并为 freeze-layers 方法 (g22) |

## 自检

- [x] `author_definition` 使用书中原文片段 (经回源核验: g01–g24 的 def_files 均为实际命中的源文件)
- [x] `key_distinction` 说明与常识用法/另一本书用法的差异
- [x] `why_it_matters` 说明下游 skill 的澄清需求
- [x] 每条标 books + def_files
- [x] 数量 24 ≤ 30; 无凑数条目
- [x] 检索索引不存在 (两书均无 .cangjie/index/lexical.sqlite), 按规则回退为源文件定向核读
