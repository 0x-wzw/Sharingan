---
name: llms-from-scratch
description: |
  Raschka《从零构建大模型》× Alammar《Hands-On Large Language Models》双书能力包：从原始文本搭建并预训练 GPT-2 基座，再展开分类/指令/PEFT 三条微调路线与 RAG 检索、嵌入适配两条应用管线，附 prompt 工程、记忆、agent 循环等 router 卡。
version: 1.0.0
license: MIT
metadata:
  author: Cangjie Distillation <agent@example.com>  # source: Sebastian Raschka; Jay Alammar & Maarten Grootendorst
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: single
  cangjie.bundle-id: bundle.llms-from-scratch
  cangjie.capability-count: 23
  cangjie.entrypoint-count: 1
---
# Build a Large Language Model (From Scratch) × Hands-On Large Language Models — 全书能力入口

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- 与两书无关的通用 ML/工程问题
- 未经书中方法支撑的生产级训练配方

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. 递进流水线：每章产物是下一章输入 (数据→注意力→模型→预训练→微调)
2. 先穷尽 prompt/RAG 等不改权重路线，再考虑微调
3. 微调路线按输出契约区分：类别 logits / 自由生成+judge 评分 / adapter 配置
4. 检索层与生成层问题分开归因；嵌入模型分生产端与消费端
5. 一切结论以可复算的验证/评估步骤收尾 (困惑度、F1、judge 打分)

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 从零实现并预训练 GPT 类基座模型；加载 OpenAI GPT-2 官方权重验证自建实现；预训练损失不降/NaN/train-val 分叉/MPS-CUDA 报错排障；加 warmup/梯度裁剪/余弦退火稳定化并估算训练成本；把自建 GPT 权重逐组件迁移到 Llama 类架构 | references/capabilities/gpt2-pretraining-pipeline.md | references/capabilities/text-classification-finetuning.md、references/capabilities/instruction-finetuning-and-eval.md、references/capabilities/lora-peft-finetuning.md、references/capabilities/p48-kv-cache-acceleration.md |
| 把预训练模型微调为文本分类器；决定冻结多少 transformer 层；分类数据准备与 padding 策略；选择分类路线 (专用模型/嵌入+LogReg/零样本/生成式)；核对分类微调的消融结论 | references/capabilities/text-classification-finetuning.md | references/capabilities/lora-peft-finetuning.md、references/capabilities/instruction-finetuning-and-eval.md、references/capabilities/embedding-model-adaptation.md、references/capabilities/gpt2-pretraining-pipeline.md |
| 把语言模型微调成听指令的助手；修复模型生成停不下来/padding 掩码错误；给指令模型搭可复现的自动化评估；核对指令微调教程的 epoch/规模/掩码细节 | references/capabilities/instruction-finetuning-and-eval.md | references/capabilities/gpt2-pretraining-pipeline.md、references/capabilities/text-classification-finetuning.md、references/capabilities/lora-peft-finetuning.md、references/capabilities/rag-retrieval-pipeline.md、references/capabilities/f17-prompt-six-elements.md、references/capabilities/p44-seven-segment-prompt.md |
| 显存不够时做参数高效微调；实现或审读 LoRA 代码 (初始化/rank/alpha/挂层)；给多个任务复用同一底座只存 adapter；做 DPO 偏好对齐 (chosen/rejected 数据对)；排查 LoRA 微调后输出变差 | references/capabilities/lora-peft-finetuning.md | references/capabilities/instruction-finetuning-and-eval.md、references/capabilities/text-classification-finetuning.md、references/capabilities/gpt2-pretraining-pipeline.md、references/capabilities/p66-gpu-vram-cleanup.md |
| 给助手接私有知识库/文档问答；稠密检索对专名/编号/数值检不准，升级 hybrid+rerank；从零搭检索层 (chunk 粒度/嵌入模型/向量索引)；区分 RAG 回答差是检索层还是生成层问题；在 API 与本地离线路线间选型 | references/capabilities/rag-retrieval-pipeline.md | references/capabilities/embedding-model-adaptation.md、references/capabilities/instruction-finetuning-and-eval.md、references/capabilities/f17-prompt-six-elements.md、references/capabilities/p44-seven-segment-prompt.md、references/capabilities/f22-react-agent-loop.md、references/capabilities/f19-structured-output-two-layer.md |
| 为句对/相似度/三元组数据选训练 loss；标注极少时做领域适配 (银标/TSDAE)；扩充嵌入训练集 (交叉编码器打标)；验证嵌入模型变好 (STS-B→MTEB) 并查维度一致 | references/capabilities/embedding-model-adaptation.md | references/capabilities/rag-retrieval-pipeline.md、references/capabilities/text-classification-finetuning.md、references/capabilities/lora-peft-finetuning.md |
| 从无标签文档发现主题；给聚类簇起可读名字/关键词；用 BERTopic 路线替代 LDA | references/capabilities/f16-topic-modeling-pipeline.md | references/capabilities/embedding-model-adaptation.md、references/capabilities/rag-retrieval-pipeline.md |
| 系统化改进不稳定的 prompt 输出；为重复性任务写可复用 prompt 模板；设计 system prompt 的组成部分 | references/capabilities/f17-prompt-six-elements.md | references/capabilities/p44-seven-segment-prompt.md、references/capabilities/f19-structured-output-two-layer.md、references/capabilities/f18-reasoning-enhancement-decision.md、references/capabilities/rag-retrieval-pipeline.md、references/capabilities/instruction-finetuning-and-eval.md |
| 决定要不要用思维链/ToT；提高数学/逻辑/多步推理正确率；在推理成本与正确率间取舍 | references/capabilities/f18-reasoning-enhancement-decision.md | references/capabilities/p45-cot-zeroshot-tot-patterns.md、references/capabilities/f17-prompt-six-elements.md、references/capabilities/f22-react-agent-loop.md |
| 让模型一定输出 JSON/固定 schema；修复输出解析失败/夹带说明文字；了解约束采样/grammar 选项 | references/capabilities/f19-structured-output-two-layer.md | references/capabilities/f17-prompt-six-elements.md、references/capabilities/f20-chain-prompting.md |
| 拆解有先后依赖的多步任务；单长 prompt 后半段跑题/质量不稳；实现 prompt chaining/流水线 | references/capabilities/f20-chain-prompting.md | references/capabilities/f22-react-agent-loop.md、references/capabilities/f21-conversation-memory-selection.md |
| 给聊天机器人加记忆；解决聊着聊着忘了前面/上下文费用暴涨；压缩超长对话历史 | references/capabilities/f21-conversation-memory-selection.md | references/capabilities/p62-conversation-memory-three-strategies.md、references/capabilities/f22-react-agent-loop.md、references/capabilities/f20-chain-prompting.md |
| 搭建能自己调工具/查资料的 agent；修 agent 不调工具/调错工具/解析崩溃；实现 ReAct 工具调用协议 | references/capabilities/f22-react-agent-loop.md | references/capabilities/p63-react-output-format.md、references/capabilities/f20-chain-prompting.md、references/capabilities/f21-conversation-memory-selection.md、references/capabilities/f18-reasoning-enhancement-decision.md |
| NER 标签与子词对不上报错或 F1 异常低；让 BERT 先懂行话再下游任务；理解 -100/B-I 标签/seqeval 口径 | references/capabilities/f29-mlm-continued-pretraining-ner-alignment.md | references/capabilities/p59-ner-label-alignment.md、references/capabilities/text-classification-finetuning.md、references/capabilities/embedding-model-adaptation.md、references/capabilities/p66-gpu-vram-cleanup.md |
| 把需求结构化成 prompt；审查 prompt 缺哪些段；同一模板换 data 复用 | references/capabilities/p44-seven-segment-prompt.md | references/capabilities/f17-prompt-six-elements.md、references/capabilities/rag-retrieval-pipeline.md |
| 写 CoT/ToT 的具体 prompt；模型推理出错时在 prompt 层补救 | references/capabilities/p45-cot-zeroshot-tot-patterns.md | references/capabilities/f18-reasoning-enhancement-decision.md |
| 加速 LLM 推理/生成很慢；use_cache 与 gradient checkpointing 冲突 | references/capabilities/p48-kv-cache-acceleration.md | references/capabilities/gpt2-pretraining-pipeline.md |
| 修标签长度不匹配报错；理解 -100 与 B-I 标签对齐规则 | references/capabilities/p59-ner-label-alignment.md | references/capabilities/f29-mlm-continued-pretraining-ner-alignment.md |
| 实现 chat memory 三种策略；压缩聊天历史的代码写法 | references/capabilities/p62-conversation-memory-three-strategies.md | references/capabilities/f21-conversation-memory-selection.md |
| 手写 agent 解析器/模板；修 ReAct 输出解析崩溃 | references/capabilities/p63-react-output-format.md | references/capabilities/f22-react-agent-loop.md、references/capabilities/f19-structured-output-two-layer.md |
| 用付费 API 跑全量数据集前控制成本；估算 token 配额/批量调用费用 | references/capabilities/p65-api-cost-control.md | references/capabilities/p66-gpu-vram-cleanup.md、references/capabilities/f17-prompt-six-elements.md |
| notebook 连续训练后 OOM；释放 CUDA 显存/清 VRAM | references/capabilities/p66-gpu-vram-cleanup.md | references/capabilities/lora-peft-finetuning.md、references/capabilities/f29-mlm-continued-pretraining-ner-alignment.md、references/capabilities/gpt2-pretraining-pipeline.md |
| 写下载脚本；修下载偶发挂起/静默失败 | references/capabilities/p67-download-code-conventions.md | references/capabilities/gpt2-pretraining-pipeline.md |

**非能力类查询**：
- 书名/作者/章节/整书概览 → references/overview.md
- 术语解释 → references/glossary.md
- 决策规则速查（不需要原文依据时） → references/cheatsheet.md
- 完整意图与关键词索引（本表未覆盖的意图先查这里） → references/capability-index.md

## 加载规则

- 每次任务先读本文件，再按路由表加载 **1** 张能力卡；任务明确跨域时最多加载 2 张。
- 概览/书名类问题不加载能力卡，用「核心原则」与 overview.md 回答。
- 路由表与 capability-index.md 都无法命中的意图，明确告知超出本书范围，不要硬套。

## 边界与判停

- 请求超出两书覆盖的技术范围
- 用户只需要与 LLM 无关的通用编程帮助
