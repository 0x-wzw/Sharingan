# 能力索引（完整版）

| capability_id | 标题 | 重要度 | 意图 | 关键词 | 能力卡 |
|---|---|---|---|---|---|
| cap.karpathy-llm-deep-dive.llm-usage-decisions | LLM 使用决策与验证纪律 | critical | 决定何时用 thinking model 处理任务；管理 context window / 决定何时开新对话；用 deep research 做带引用调研并验证；让 LLM 正确计算、画图、做数据分析；核查当前 app 实际使用的模型与可用工具；建立输出验证纪律 (引用核对、代码假设审查) | lossy zip file、context window、thinking model、reasoning model、deep research、code execution、advanced data analysis、hallucination、verify outputs、model tier、有损压缩、上下文窗口、推理模型、幻觉、验证输出、档位 | capabilities/karpathy-llm-usage.md |
| cap.karpathy-llm-deep-dive.vibe-coding-cursor | Cursor vibe coding 工作流 | medium | 用自然语言快速生成小型应用/原型；使用 Cursor composer 跨文件自主编辑 | vibe coding、cursor、composer、prototype、快速原型、井字棋 | capabilities/vibe-coding-cursor.md |
| cap.karpathy-llm-deep-dive.multimodal-io | 多模态输入输出判别与用法 | medium | 判别 LLM app 语音模式的能力 (native vs 转写)；用图像/文档作为 LLM 输入 | native audio、transcription、voice mode、image input、patches、多模态、语音模式、图片输入 | capabilities/multimodal-io.md |
