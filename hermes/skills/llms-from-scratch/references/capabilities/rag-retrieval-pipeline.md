# RAG 检索管线 (rag-retrieval-pipeline) — RIA++ 能力卡

> 单元: f23 (检索递进流程), p49 (search_document/search_query 非对称约定), p50 (BM25+重排架构), p51 (BM25 预处理三步)
> 来源: 《Hands-On Large Language Models》(Alammar & Grootendorst) 第 8 章 (Semantic Search); verified-principle-b.md p49–p51 与 verified-framework.md f23 均定位 alammar ch08
> 状态: 纸面 walkthrough 验证 (V2 check_mode=walkthrough)；阶段 4 实测前不声称"已实测"

## R — Reading (原文)

1. 非对称嵌入约定 (第 8 章 §2, p49):

> "response = co.embed(texts=texts, input_type="search_document",).embeddings … query_embed = co.embed(texts=[query], input_type="search_query",).embeddings[0]"

（自译：给文档建索引用 `search_document` 类型，查询时用 `search_query` 类型——两类前缀由嵌入模型区分对待。）

2. 稠密索引与检索 (第 8 章 §3–§4, f23):

> "dim = embeds.shape[1] index = faiss.IndexFlatL2(dim) index.add(np.float32(embeds)) … distances, similar_item_ids = index.search(np.float32([query_embed]), number_of_results)"

（自译：把文档向量加入 FAISS 的 L2 平面索引，查询向量取最近邻。）

3. 稠密检索的失效提示 (第 8 章 "Caveats of Dense Retrieval" 节):

> "query = "What is the mass of the moon?" results = search(query)"

（自译：作者用"月球质量"这类语料中根本没有答案的事实型查询，显式演示纯稠密检索的失效场景——检索层会返回不相关结果而非"无答案"。）

4. BM25 预处理三步 (第 8 章, p51):

> "for token in text.lower().split(): token = token.strip(string.punctuation) … if len(token) > 0 and token not in _stop_words.ENGLISH_STOP_WORDS: tokenized_doc.append(token)"

（自译：小写分词 → 去标点 → 滤空串与英文停用词；语料和查询必须共用同一分词器。）

5. BM25 召回 + 重排精排 (第 8 章, p50):

> "bm25_scores = bm25.get_scores(bm25_tokenizer(query)) top_n = np.argpartition(bm25_scores, -num_candidates)[-num_candidates:] … results = co.rerank(query=query, documents=docs, top_n=top_k, return_documents=True)"

（自译：BM25 先召回 num_candidates 个候选，rerank API 再对候选精排取 top_k。）

6. RAG grounding 模板 (第 8 章 "The RAG Prompt" 节):

> "template = \"\"\"<|user|>\nRelevant information:\n{context}\n\nProvide a concise answer the following question using the relevant information provided above:\n{question}<|end|>\n<|assistant|>\"\"\""

（自译：把检索到的文档作为 context 注入提示模板，要求模型仅依据所给信息作答。）

## I — Interpretation (自述)

这套方法论解决的是：LLM 不知道私有/新近知识时会编造答案。解法不是改模型，而是先从语料里"找对上下文"，再让模型只根据上下文回答。管线是递进式的五段：

1. **切块 (chunk)**：把长文档拆成适于嵌入的小段（书中以影介按句拆分演示；切块粒度细节在书正文散文中，提取文本未含，为已标注缺口）。
2. **嵌入 (embed)**：用检索型嵌入模型编码，遵守非对称约定——建索引用 `search_document`，查询用 `search_query`；混用会静默损失检索质量。
3. **稠密检索 (dense)**：向量入 FAISS L2 索引，查询取最近邻。擅长语义相似，但有硬边界：专名、数字、事实型查询的关键区分信息会被嵌入平滑掉，"语料外/精确词"查询会返回自信的不相关结果。
4. **词法召回+重排 (hybrid+rerank)**：BM25 按词频精确匹配补稠密的盲区（预处理三步统一：lower→去标点→滤停用词），先取 num_candidates 个候选，再用 rerank 交叉编码器精排取 top_k——BM25 管召回、rerank 管精度。
5. **接地生成 (RAG)**：把 top 文档放进固定模板的 context 段，指令模型"仅依据以上信息作答"；API 路线用带 citations 的 chat 接口，本地路线用 Phi-3 GGUF + LangChain RetrievalQA。

核心决策规则：dense-only 只配当原型；生产检索 = dense 与 BM25 各自召回 → rerank 合并精排 → 模板接地生成。

## A1 — Application Example

**案例 1（worked_example, c14, alammar 第 8 章全节）**：以 Interstellar 影介为语料演示完整管线。
- **问题/输入**：一段电影简介，查询 "how precise was the science" 与失效对照查询 "What is the mass of the moon?"。
- **方法论的使用**：拆句 → Cohere embed（search_document）→ FAISS IndexFlatL2 → search() 稠密检索；对照 BM25Okapi keyword_search（同一 bm25_tokenizer 预处理语料与查询）；用 "mass of the moon" 演示稠密检索在语料外事实查询上的失败；co.rerank 精排；keyword_and_reranking_search 组合 BM25 召回 + rerank；最后把检索文档交给 co.chat（带 citations）或本地 Phi-3 + BGE + FAISS + RetrievalQA 做接地生成。
- **结论**：dense 与词法检索均能命中"科学准确性"相关句子；语料外查询暴露检索层局限（检索失败被误认为模型失败）；RAG 回答附 citations。
- **结果**：书内 notebook 演示为可运行输出（各段均打印 top-3 命中）；具体命中排序细节原书报告为演示性输出，未附量化指标。

**合成演练（标记为演练，p49/p51 规则复算）**：索引 10 个文档时全部用 `input_type="search_document"`，查询用 `input_type="search_query"`；把 "What is the mass of the Moon?" 过 bm25_tokenizer，应得 `[mass, moon]`（what/is/the/of/the 被停用词滤除）。混用 input_type 属失败分支；按 p51 规则可逐字复算。

## A2 — Future Trigger ★

### 用户会在什么情境下需要这个 skill?

1. 要给聊天机器人/助手接私有知识库或文档库，问"怎么让模型引用我的文档回答"。
2. 已有稠密检索/RAG 原型，但某些查询（专名、编号、数值、精确术语）检不准，要升级为 hybrid/rerank。
3. 从零搭检索层：需要决定 chunk 粒度、选嵌入模型与 input_type、选向量索引。
4. RAG 回答质量差，需要区分"检索层失败"还是"生成层失败"。
5. 要在 API 与本地/离线两条路线之间做 RAG 落地方案选型。

### 语言信号 (用户的话里出现这些就应激活)

- "RAG / 检索增强 / 让 LLM 基于我的文档回答 / grounded answer / cite sources"
- "向量检索不准 / semantic search misses / BM25 / hybrid search / rerank 重排"
- "chunk 切块 / embedding 索引 / FAISS / search_document / search_query"
- "回答幻觉、但我不确定是检索的问题还是模型的问题"

### 与相邻 skill 的区分 (定稿,阶段 3 回填完成)

- 与 `embedding-model-adaptation` 的区别：那是**训练/适配嵌入模型本身**（loss 选择、TSDAE、MTEB 评估）；本卡是**消费**现成嵌入模型搭检索管线。需要微调嵌入模型时转那边。
- 与 `llms-from-scratch-router`（f17/p44 等 prompt 卡）的区别：prompt 类卡管提示词结构；本卡管"检索到什么再填进提示"，核心在检索层。
- 与 agent/ReAct 类卡的区别：ReAct 管工具循环决策；本卡管单轮检索-生成管线。

## E — 可执行步骤 (Execution)

**必需输入**：语料来源（文件/文本，UTF-8）；查询样例集合；若走本地路线需指定生成模型与嵌入模型；API key（用户自行提供，不得代填密钥）。缺失语料或查询样例时先询问，不得静默用示例数据代替用户语料。
**交付物与完成标准**：可运行的检索管线代码 + 对样例查询的 top-k 检索结果 + （RAG 模式）带 context 的提示与生成回答；检索结果须列出得分与原文片段，RAG 回答须可溯源到 context 片段。

1. **切块**
   - 把语料拆为可嵌入的片段（默认按句/段落；粒度为约定值——书中正文有散文讨论但提取文本未含，实施时向用户确认粒度，不得虚构"书中规定值"）。
   - 完成标准：片段无空段，覆盖全部语料，单段长度适配嵌入模型上限。

2. **嵌入 + 建索引**
   - 文档统一 `input_type="search_document"`；查询统一 `search_query`（p49，硬约定）。向量转 float32 入 FAISS IndexFlatL2（或等价向量库）。
   - 完成标准：索引计数 == 文档数；混用 input_type 视为失败，立即纠正。

3. **稠密检索基线**
   - 用查询向量取最近邻 top-k。
   - 完成标准：能对样例查询返回带距离的 top-k 片段。
   - 判停条件：样例查询含专名/数字/精确术语且 top-k 全不相关（ce14 的 warning_signs），或查询疑为语料外事实（"mass of the moon" 型）→ 不要只调模型，进入步骤 4。

4. **hybrid 召回 + rerank**
   - BM25 前处理三步（lower→去标点→滤停用词）**同时**用于语料与查询（p51，共用分词器）；BM25 取 num_candidates 候选 → rerank 精排取 top_k（p50）。dense 与 BM25 结果可合并去重后统一 rerank。
   - 完成标准：原 top-k 失准的查询在 hybrid 结果中命中正确片段，或确认语料中确无答案。

5. **RAG 接地生成**
   - 用模板注入 context（"Relevant information: {context}" 式），指令模型仅依据 context 作答；要求引用/citations。API 路线：chat 接口带 documents；本地路线：Phi-3 GGUF 类模型 + 向量库 retriever + RetrievalQA。
   - 完成标准：回答中的每个事实可对应到 context 片段；无 context 支撑的回答被标记而非照单输出。
   - 失败处理：检索层无命中 → 明确告知"语料中未找到答案"，不进入生成；这本身是有效输出。

## B — Boundary (Boundary)

### 不要在以下情况使用此 skill

- 用户要**训练或微调嵌入模型**（loss 选择、领域适配）→ 用 `embedding-model-adaptation`，本卡只消费嵌入。
- 语料本身就是问答对、且查询是纯语义改写的小规模场景——dense-only 足够时不要过度工程化上 BM25+rerank。
- 问题与私有语料无关（通用知识问答）——不需要检索层。
- 要做多轮 agent 工具循环——那是 ReAct/agent 范畴，不是单轮检索管线。

### 作者在书中警告的失败模式 (ce14)

- **纯 dense 检索在词汇/事实型查询上失败**：专名、数字等关键区分信息在嵌入中被平滑，查询排到无关文档之后，RAG 答案错误；用户误以为"模型不行"，实为检索层失败。警示信号：含专名/术语/数字的查询 top-k 全不相关，而同义改写反而命中。
- **语料外查询静默返回不相关结果**（"What is the mass of the moon?"）：检索层不会说"无答案"，必须人工/流程判停。
- **BM25 前处理不一致**：语料与查询若用不同分词器，词法匹配静默失效（p51 规则）。

### 作者的盲点 / 时代局限

- 教程代码为版本快照：Cohere API、LangChain `PromptTemplate`/`RetrievalQA`、LLMChain 式写法已部分弃用（ce15 同类问题），实施须核对当前 API，不得照抄。
- chunking 策略在书中是散文讨论而非可复算规则（f23 V2 已标注缺口）——实施时粒度需实测调优，不能声称有"书中标准值"。
- 书中演示无量化检索指标（recall/MRR），只有定性 top-3 输出；评估环节需另行设计。

### 容易混淆的邻近方法论

- `embedding-model-adaptation`：适配模型 vs 消费模型（见 A2）。
- 通用 prompt 工程（f17/p44）：本卡的核心变量是"检索质量"，不是提示词措辞。
- 长上下文直塞（不检索全塞 context）：绕过检索层，小语料可行但与本卡方法正交，成本与精度特征不同。

---

## 相关 skills (阶段 3 填充)

- depends-on: 无 (消费现成嵌入模型)
- contrasts-with: `embedding-model-adaptation`, `llms-from-scratch-router`
- composes-with: `instruction-finetuning-and-eval` (生成端), `f17-prompt-six-elements` / `p44-seven-segment-prompt` (模板结构)

## 相关能力 (also_read, 阶段 3 定稿)

- depends-on: 无 (消费现成嵌入模型, 不训练模型)
- contrasts-with: `embedding-model-adaptation` (本卡消费嵌入 vs 那边生产/适配嵌入模型)
- composes-with: `instruction-finetuning-and-eval` (grounded generation 的生成端), `f17-prompt-six-elements` / `p44-seven-segment-prompt` (RAG 模板的结构化设计), `f22-react-agent-loop` (多轮工具循环时的升级路径)
- also_read: `llms-from-scratch-router` (f19 结构化输出卡约束生成端格式)
