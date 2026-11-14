# 多模态输入输出判别与用法 (multimodal-io) — Router 能力卡

> 来源: Karpathy *Deep Dive into LLMs* [1:16:28] | 绑定单元: p05 | 支持材料: g01 (边界)
> 证据层: notes-layer 转述 | 去向: source-router (karpathy-llm-usage-router) 服务

## R — Reading (notes-layer 转述)

- "[1:16:28] advanced voice mode handles audio natively as tokens (fake audio = transcription, true audio = native); images as patches input (labels, blood tests, memes) + DALL-E/Ideogram output; mobile app live video."
- NR-04: Super Whisper 占比、NotebookLM podcasts、Grok 语音合规度对比 — 仅 notes-layer, 未核实, 不进入执行规则。

## I — Interpretation

多模态用法的核心是一个判别: 当前 app 的语音模式是 **native** (音频作为 token 直接进模型, 保留语气/背景等副语言信息) 还是 **转写** (先转文字, 副语言丢失)。需要判断语气、情绪、环境音的任务必须 native; 纯内容听写转写即可。图像侧: 图像被切成 patch 作为输入 (标签、化验单、梗图皆可), 输出可用图像生成模型。

## A1 — 来源演练 (合成, 明确标记)

原书未给完整步骤案例。合成演练: 任务"听一段客户投诉录音判断情绪" → 按 p05 判别: 需要语气 → 要求 native-audio 模式; 若 app 只有转写 → 说明局限或换 app。可按判别标准复算。

## A2 — Future Trigger

用户问"它听得懂语气吗"、要传图片/文件给 LLM、要生成图片、区分语音模式时; 不适用于纯文本任务 (主技能)。中文: 语音模式、原生音频、转写、图片输入。

## E — Execution

1. 判别任务是否依赖副语言信息 (语气/情绪/背景音)。完成标准: 判别完成。
2. 是 → 要求 native-audio 模式并验证 app 支持; 否 → 转写即可。
3. 图像输入: 直接附图 (patch 输入); 需要图像输出 → 用配套图像生成模型。
4. 具体产品支持情况以当前文档为准 (原文产品名为 2025-02 快照, NR-02)。

输出契约: 模式选择结论 + 支持性验证 (该模式确实开启)。

## B — Boundary

- 语音合规度、各厂商对比是轶事 (NR-04), 不作规则引用; 纯文本 prompt 任务走主技能。
