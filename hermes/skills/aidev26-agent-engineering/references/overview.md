# Opus AI Dev 26 x SF — Overview (sidecar)

来源：AI Dev 26 x SF 会议（DeepLearning.AI，48 talks，~213K 词，2026）。

核心模式（15 talks 全文精读 + 语料统计支撑）：
1. 评测先行——evals 是工程+哲学；容器化 agentic eval；失败分桶 model/harness/problem；严重度分级
2. 确定性外壳——schemas before prompts；manager 独占决策；规则即代码；缓存先于计算；全值溯源
3. 三层安全——containment（凭据外置）→ scoped access → intent policies；模型自评永远不能当第一层
4. Durable execution——workflow/activity/worker 三原语；replay 续跑；反 restart 论证
5. 记忆架构——阈值摘要压缩；ID 引用；读写双 agentic-search 循环；文件系统接口先验；遗忘机制
6. Pareto 优化——配置扫描→垂直/水平扩展→异构 ensemble→预算感知编排→anytime 输出
7. 红队工程——自然语言行为→CI 测试套件；persona 多轮模拟；工具调用内部审查
8. 组织转型——"构建构建之物"；瓶颈后移（PM/设计/法务/市场）；通才 AI-native 团队

局限声明：前沿团队样本偏差；vendor 立场（仿真/沙箱/文档提取/优化运行时各有立场）；工具名为 2026-09 快照。
完整分析见 pipeline 工作区 BOOK_OVERVIEW.md。
