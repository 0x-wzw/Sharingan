# GLOSSARY — 共享词典 (Karpathy Deep Dive into LLMs)

全部为 notes-layer 作者用法 (blumify 浓缩笔记), 非字典义。

- **lossy zip file (of the internet)**: pre-training 把互联网概率性压缩进 ~1T 参数的自包含神经网络, 有知识截止日; ≠ 精确记忆, 内容须验证。[00:00]
- **context window**: 模型与用户共享的工作记忆; 多余 token 干扰+拖慢, ≠ 越大越好。[00:00]
- **thinking model**: RL 训出的内部独白策略模型 (o-series/R1 类), 难数学/代码更准, 分钟级延迟。[15:42]
- **deep research**: thinking + 多轮搜索 → ~10 分钟带引用报告; 产物是 first draft。[24:06]
- **code execution loop**: 模型写程序→app 执行→结果回填 context; LLM 计算正确性的来源。[52:35]
- **vibe coding**: 自然语言意图驱动产出小应用, 接受代码为黑盒, 手动 fallback 常驻。[1:08:18]
- **composer (Cursor)**: 持全项目上下文、跨文件自主编辑的 agent 模式; ≠ 独立 agent 工程。[1:08:18]
- **LLM council**: 跨厂商 (OpenAI/Anthropic/Google/xAI) 全档订阅的能力组合, 对冲单一模型盲区。[Model selection]
