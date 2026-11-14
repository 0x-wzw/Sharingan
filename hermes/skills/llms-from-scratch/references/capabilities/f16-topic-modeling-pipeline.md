# 主题建模五段流水线 (f16) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 5 章 (Text Clustering and Topic Modeling) | 绑定单元: f16 | 支持材料: c13, ce15
> 去向: source-router (llms-from-scratch-router) 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "Hundreds of topics were generated using the default model! To get the top 10 keywords per topic as well as their c-TF-IDF weights, we can use the `get_topic()` function"

— Alammar & Grootendorst, ch05 (chapter05_Chapter 5 - Text Clustering and Topic Modeling.txt @164)

代码锚点 (同章): `UMAP(n_components=5, min_dist=0.0, metric='cosine', random_state=42)` → 聚类用 5 维; `HDBSCAN(min_cluster_size=50, metric='euclidean', cluster_selection_method='eom')`; 可视化另用 `UMAP(n_components=2, ...)`。自译: BERTopic 是装配器——嵌入、降维、聚类、主题表示四段皆可替换, 默认模型能产出数百个主题, 每个主题用 c-TF-IDF 取 top-10 关键词。

## I — Interpretation (自述)

主题建模回答"这批文档在谈些什么"。流水线五段: ①嵌入 (如 gte-small, 把摘要变成向量); ②UMAP 降维 (5 维, min_dist=0, 保留簇结构); ③HDBSCAN 密度聚类 (min_cluster_size=50, 不需要预设主题数, 噪声点标为 -1); ④c-TF-IDF 按类抽词, 每簇变成一组代表关键词, 即"主题"; ⑤(可选) 用 LLM 或表示模型重写主题词使其可读。关键约定: 降维有两次——聚类用高维 (5) 保信息, 可视化用 2 维保可读, 二者不要混用。每段是可替换组件 (换嵌入模型、换聚类器都不影响其他段), 所以调试时可以逐段检查: 簇数异常先看嵌入/UMAP, 关键词质量差先看 c-TF-IDF 与表示模型。

## A1 — Application Example

### 示例: ArXiv 计算语言学摘要聚类 + BERTopic (c13)

- **类型与来源**: 原书 worked_example, ch05 (chapter05 文本)。
- **问题/输入**: maartengr/arxiv_nlp 数据集的计算语言学论文摘要。
- **方法论的使用**: 摘要 → gte-small 嵌入 → UMAP 降到 5 维 → HDBSCAN (min_cluster_size=50) 聚类 → c-TF-IDF 生成主题词; 再用 `find_topics("topic modeling")` 检索主题, 命中 topic 22 (相似度 0.95); 最后用 KeyBERTInspired/MMR/Flan-T5/GPT-3.5 四种表示模型重写主题词并 diff 对比。
- **结论**: 生成数百个主题; BERTopic 论文本身被归入 topic 22, 印证流水线有效性。
- **结果**: 各表示模型的 top-5 关键词差异以表格呈现 (原书未宣布唯一最优)。

## A2 — Future Trigger ★

### 情境

1. 用户拿到一批无标签文档 (摘要/评论/工单), 想知道"里面有哪些主题/类别"。
2. 已有嵌入或聚类结果, 想给每个簇起可读的名字/关键词。
3. 听说过 LDA, 想用嵌入+聚类的现代路线替代。

### 语言信号

- "主题建模 / topic modeling / BERTopic / 发现文档里的主题 (discover topics)"
- "聚类后给每个簇找关键词 / cluster keywords / HDBSCAN / UMAP"
- "discover topics in unlabeled documents / find themes across documents / no labels, what are these about"

### 与相邻 skill 区分

- 与 `rag-retrieval-pipeline`: RAG 是为查询取回文档 (检索契约); 本卡是无查询的分析契约 (整批文档 → 主题)。
- 与 `embedding-model-adaptation`: 那里训练嵌入模型; 这里消费现成嵌入。

## E — Execution

**必需输入**: 文档列表 (str[]); 缺数据规模信息时先问 (几十条文档做不了 min_cluster_size=50, 需调小)。

1. 嵌入全部文档 (句向量模型; 完成标准: 得到 n×d 矩阵)。
2. UMAP 降维 (n_components=5, min_dist=0.0, metric='cosine', random_state=42)。
3. HDBSCAN 聚类 (min_cluster_size=50, metric='euclidean', cluster_selection_method='eom'; 判停: 噪声占比或簇数明显不合理 → 回调 min_cluster_size)。
4. c-TF-IDF 生成每簇关键词 (完成标准: 每个非 -1 簇有 top-k 关键词)。
5. (可选) find_topics 按检索词定位主题; (可选) 用 LLM 重写主题词。
6. 可视化另跑一次 UMAP(n_components=2), 不复用 5 维结果。

**输出契约**: 主题表 (topic_id, 簇大小, top 关键词, 示例文档); -1 为离群文档, 如实报告不强行归类。

## B — Boundary

- 不要用于: 有明确标签的分类任务 (那是分类微调); 需要按查询检索 (RAG); 文档量极少 (<几十条)。
- 作者边界: BERTopic 各段皆可替换, 换组件后默认参数不再适用, 需重调。
- 版本边界 (ce15): 书钉死 transformers==4.41.2 等版本, LangChain/库 API 已变动; 照抄代码会在 import 层失败, 应迁移思路到当前 API。
- 书中参数 (如 5 维、50 簇大小) 未做敏感性分析 (ce16 同源批判), 换语料需自行调参, 不能当普适默认。

## 相关能力 (also_read, 阶段 3)

- composes-with: `embedding-model-adaptation` (主题建模消费嵌入向量; 嵌入模型适配在那边)
