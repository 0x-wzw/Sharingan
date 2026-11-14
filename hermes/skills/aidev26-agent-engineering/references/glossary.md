# Candidates — Glossary (ai-dev-26-sf)

> Extractor: glossary-extractor · 2026-10-08 · 15 talks read in full + 7 Stage-0 anchors
> Stage 0 terms (evals, hill climbing, vibe check, simulation environment, deterministic shells, schemas before prompts, containment/scoped access/intent policies, agentic engineering, dark factory, parallel skill development, Context Hub pattern, taste, truth-seeking, agent memory) carried forward in BOOK_OVERVIEW.md; Stage 1 additions below.

| term | 定义（讲者用法） | 母本 |
|---|---|---|
| red teaming / blue teaming | 红队=结构化测试发现缺陷；蓝队=修复发现的缺陷 | 040 Giskard |
| multi-turn attacks | 多轮对话中分步完成的攻击，单轮评测不可见 | 040 |
| user simulator (persona) | 带人设与意图的模拟用户，替代静态 golden dataset | 040 |
| system prompt leakage | 通过角色扮演/枚举等策略诱出系统提示 | 040 |
| Pareto frontier (agent) | 准确率-成本（或延迟）平面上不可同时改进的最优配置族 | 007 AI21 |
| vertical scaling | 更多 token：更长推理链、更多循环、critique-repair loops | 007 |
| horizontal scaling | best-of-n 并行采样+排序选择；成本×n 延迟近不变 | 007 |
| ensemble / portfolio | 异构模型组合，各解不同子集；比单模型省成本降延迟 | 007 |
| anytime generation | 任意预算/时延点都可取当前最优候选的生成方式 | 007 |
| durable execution | 保证代码在故障下执行到底：状态持久化+失败点续跑 | 029 Temporal |
| workflow / activity / worker | 编排逻辑 / 易失败的对外动作 / 执行计算的容器 | 029 |
| replay (durable) | 重放已完成步骤的记录以恢复状态，不重复执行副作用 | 029 |
| semantic cache | 语义缓存：加速对长期记忆层的查找 | 033 Oracle |
| token threshold / offload | 用量阈值（50%/80%）触发摘要压缩并把短期记忆移入长期存储 | 033 |
| context rot | 上下文增长导致性能衰减；标称窗口≠可用窗口 | 037 Chroma |
| dumb zone | 超出可用窗口后输出质量不可信的区间（实测 40–100K） | 037 |
| agentic search | 模型+搜索工具+自主停止的循环；读路径与写路径共用 | 037 |
| hybrid search | dense+sparse 向量混合检索，平衡语义与词面 | 037 |
| push down (compute) | 把计算推到数据层旁执行以省网络成本（先验：OLAP 惯例） | 037 |
| defect rate (agent loop) | 反馈回路后输出的缺陷频率；agent 机会大小的限制量 | 046 Brooker |
| failure severity vs density | 严重度≠频率；基准应度量前者 | 046 |
| correct by construction | 用框架/语言让正确性由构造保证（Hydro/Cedar/Lean/Strata） | 046 |
| auto-formalization | 自然语言政策→数学精确规约（Cedar/Lean 编码）的对话式过程 | 046 |
| ride the priors | 优先复用模型已被 50 年语料训练过的接口语义 | 030 Box |
| file system semantics | write/edit/glob/grep 等 FS 操作作为 agent 通用接口 | 030 |
| FS shim | 为非 FS 数据源包一层文件系统接口（Chroma FS 案例） | 030 |
| agent data stack | 每 agent 独立的联邦查询+本地加速数据层，隔离生产系统 | 004 Spice AI |
| working set replication | 把后端数据工作集复制到本地嵌入式库（DuckDB/SQLite/Arrow） | 004 |
| connection pooler mode | 连接池模式（session→transaction）调整案例中的具体修复 | 004 |
| converged database | 单引擎承载向量/图/关系/空间/JSON 的收敛式存储 | 033 |
| tool description verbosity | LLM 增写工具描述以提升语义检索命中 | 033 |
| LLM OS | 上下文窗口=RAM、工具=系统调用的心智模型 | 030/037 |
| System 1 / System 2 (context) | 快而廉价的注意力 vs 慢而贵的推理——检索系统据此分工 | 037 |
| agentic engineering stage 检查 | —（防幻觉占位行，无此术语） | — |
