# LLM 使用决策与验证纪律 (karpathy-llm-usage) — Promoted 能力卡

> 来源: Andrej Karpathy, *Deep Dive into LLMs like ChatGPT* (~2h06m 视频, 2025-02, vMhwv4nOJyg)。
> 覆盖单元: f01–f05, p01–p04, ce01–ce03 (均 verified) | 支持材料: c01–c03, g01–g07 (GLOSSARY)。
> 证据层声明: 全部 R 段引文是 **notes-layer 转述** (blumify AI 浓缩笔记), 原始 captions 不可得, 无法逐字引用 — 按 V1 规则以带时间戳的转述代替, 全部标记 notes-layer。
> 去向: promoted (karpathy-llm-usage) | 纸面 walkthrough 验证, 阶段 4 未实测前不声称"已实测"。

## R — Reading (notes-layer 转述, 带时间戳)

- "[00:00] self-contained neural net, ~1TB 'zip file' ~1T params; pre-training compresses internet into probabilistic knowledge w/ cutoff; post-training attaches assistant persona; no tools/calculator/browsing by default; context window = shared working memory, extra tokens distracting + slow sampling, start new chat on topic switch."
- "[15:42] thinking models: RL-tuned, internal monologue strategies; higher accuracy on hard math/code; minutes to respond."
- "[24:06] deep research = thinking + many searches ~10min cited report; treat as first draft, verify citations."
- "[52:35] model writes program, app runs it, result returns as text; enables correct calculation/plotting; advanced data analysis = junior data analyst; scrutinize generated code — sneaky implicit assumptions."
- "Model selection notes: track pricing tier & which model you actually get — free tiers may silently serve smaller models."

## I — Interpretation (自述)

把 LLM 用好的骨架是四个连续决策, 每个决策都有明确的开关:

1. **先定位任务难度档** (f03): 任务是难数学、多步代码、需要试错的推理 → 开 thinking model (o-series/R1 类, 内部独白策略), 接受分钟级响应; 日常查询/写作 → 普通模型, 不为简单任务白等。
2. **先查档位与工具, 再提问** (p02/f01): LLM 默认是无工具、无计算器、无浏览的概率压缩体 (有知识截止日)。当前 app 免费档可能静默路由到小模型, 也可能没开代码执行/搜索。提问前先确认: 实际模型是什么、代码执行开着吗、搜索开着吗。
3. **按输出类型选正确性来源** (f05 vs 直接回答): 数值计算、绘图、数据分析必须走"模型写程序 → app 执行 → 结果回填"循环 — 模型自己报的精确数字是采样产物, 不是计算结果 (ce01)。deep research 报告 (f04) 是 thinking + 多轮搜索的初稿, 交付前引用逐条核对 (p03)。
4. **管理上下文, 验证产出** (f02/p01/p04): context window 是共享工作记忆, 塞入无关 token 既拖慢又干扰 → 换主题就开新对话 (ce03)。任何产物交付前: 报告查引用、代码查模型自行引入的隐含假设 (单位、过滤、范围), 运行成功 ≠ 语义正确 (ce02)。

## A1 — Application Example (来源案例, notes-layer)

- **c01** [52:35]: 同一道大数乘法, Grok 3 幻觉出错, ChatGPT/Claude 走代码执行算对 — 证明正确性来自代码执行开关, 不是模型品牌。
- **c02** [52:35]: ChatGPT 生成的数据分析代码运行成功, 但含"隐秘的隐含假设", 结果语义错误 — 触发 p04 审查纪律。
- **c03** [15:42]: Claude 3.5 Sonnet 未开 thinking 也解出一个 bug — 说明 thinking 是"难任务"开关而非必需 (单例, NR-01)。

## A2 — Future Trigger ★

**场景**:
1. 用户问"这个任务该不该用 thinking/reasoning 模型 / o1 / R1"。
2. 用户抱怨 LLM 算数/统计算错, 或要精确计算、画图、跑数据分析。
3. 用户要做带引用的调研 (deep research / Perplexity 类), 不知道怎么用、怎么核。
4. 用户怀疑 app 给的答案质量差 → 查实际模型档位与可用工具。
5. 用户问"要不要开新对话/上下文太长了怎么办"。

**语言信号** (中英): "reasoning model / thinking model / 该用 o1 吗"; "它算错了 / hallucination / 编了个数"; "deep research / 帮我查文献并给引用"; "免费版是不是小模型 / 档位"; "context window / 开新对话 / 太长了"。中文: 推理模型、幻觉、精确计算、调研报告、上下文窗口、档位。

**与相邻能力区分**: 用户要在真实项目里写代码/原型 → vibe-coding-cursor (router); 语音/图片输入 → multimodal-io (router); 用户要设计 agent harness/循环/图架构 → 本 skill 明确不覆盖 (ce04 误标防护), 转交 agent 工程资源。

## E — Execution (可执行步骤)

输入契约: 一个待完成的 LLM 任务描述。缺失时应先问: 任务类型 (简单问答/难推理/计算/调研)、可用 app 与档位、是否需要引用或数字精度。不得静默假设工具可用。

1. **分档** (完成标准: 明确选中 thinking 或普通): 难数学/代码/多步推理 → thinking model; 其余 → 普通模型。若 unsure, 先普通, 失败再升级。
2. **核查环境** (完成标准: 模型名+工具开关已确认): 查当前 app 实际路由模型 (档位), 确认代码执行、搜索是否开启。免费档或不明 → 按 NR-03 以当前文档为准。
3. **选正确性路径** (分支): 需要精确数字/图表/数据处理 → 强制走代码执行循环 (写程序→运行→回填), 不接受模型直接报数。需要调研综述 → deep research, 产物定级为 first draft。普通生成 → 直接回答。
4. **验证** (完成标准: 每项产物有验证记录): 报告 → 引用逐条点开核对; 代码 → 列出隐含假设 (单位、时间范围、过滤条件、舍入) 并逐条确认; 计算结果 → 与独立来源或第二次独立运行交叉核对。
5. **上下文维护** (判停点): 对话换主题或明显变慢 → 开新对话, 只带必要背景。验证失败且无法修复 → 停止交付, 报告失败原因。

输出契约: 结论 + [所选档位 | 所用工具路径 | 验证记录]。缺任一要素不算完成。

## B — Boundary (边界)

- **不要用于**: 构建 agent harness/循环/图架构 — 本讲座内容只是 app 内工具使用, 转发推文的 "agents, harnesses, loops and graphs" 标签是误标 (ce04)。也不要用于生产代码评审 (用 vibe-coding 卡或工程类资源)。
- **作者警告的失败模式**: 算术幻觉 (ce01)、代码隐含假设 (ce02)、上下文污染 (ce03)。
- **作者盲点** (阶段 0 批判): 全档付费视角, 低预算场景覆盖弱; 产品名/档位是 2025-02 快照, 已过时风险高 (NR-02/NR-03)。
- **证据边界**: 全部规则来自 AI 浓缩笔记, 无逐字引文可核; 单例轶事不构成模型间能力结论。
