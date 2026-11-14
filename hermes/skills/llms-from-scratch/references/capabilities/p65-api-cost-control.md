# API 成本控制: 先小后大 (p65) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 4 章 | 绑定单元: p65 | 支持材料: c12, ce15
> 去向: source-router 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "only run this when you have sufficient tokens as this will call the API for the entire test dataset (1066 records)"

— Alammar & Grootendorst, ch04 (chapter04_Chapter 4 - Text Classification.txt @256)

自译: 用付费 API 对评测集逐条推理前, 先确认配额——书中全量调用是 1066 条, 每条都计费; 先小样本验证, 再估算全量成本, 才决定是否跑。

## I — Interpretation (自述)

付费 API 评测的固定 SOP 是三段: ①用 5–10 条样本验证 prompt/参数确实有效 (这步几乎免费); ②按单条实测 token 数 × 全量条数估算总成本, 向用户确认配额; ③全量跑, 带断点保存与失败重试。核心是行为约束"先小后大", 防止一个坏 prompt 烧完整份测试集。任何"我要对 N 条数据调 API"的请求都应先走①②。

## A1 — Application Example

### 示例: GPT-3.5 全测试集分类前的成本闸 (c12 依据)

- **类型与来源**: 原书 worked_example, ch04 (五路分类对比含 GPT-3.5 API 路线; @256 为原书明确警告)。
- **问题/输入**: rotten_tomatoes 测试集 1066 条, 想用 GPT-3.5 逐条分类。
- **方法论的使用**: 先小样本试 prompt → 单条成本 ×1066 估算 → 确认配额后全量。
- **结果**: 原书给出该警告并展示各路 classification_report; API 路线最终分数正文未列名次 (未说明)。

## A2 — Future Trigger ★

### 情境 / 语言信号

1. 任何"用 OpenAI/Cohere 等付费 API 跑一遍整个数据集"的请求; 关键词 "API cost / 跑全量 / token 配额 / batch 调用"。

### 与相邻 skill 区分

- 与 f17/p44 等 prompt 技巧: 那些改 prompt, 本卡控制调用量与成本。GPU 侧显存问题走 p66。

## E — Execution

**必需输入**: 数据条数 N、单价或配额信息; 缺配额数据时先问, 不静默开跑。

1. 小样本 (≤10 条) 验证 prompt 与解析。完成标准: 输出合格。
2. 估算: 单条 token 数 × N × 单价; 报告给用户确认。
3. 确认后全量: 分批 + 断点保存 (每批落盘) + 失败重试。判停: 中途报配额不足 → 停止并报告已完成量。

**输出契约**: 预估表 (N, 单条 token, 总成本) + 全量结果文件; 完成标准 = 用户确认后才发生全量调用。

## B — Boundary

- 不要用于: 本地模型推理 (无 API 计费, 但仍有时间成本可类比执行)。
- 边界: 单价随模型/服务商变动, 估算用实测 token 数不用拍脑袋; 缓存/批量折扣按当前文档 (ce15 版本腐化同类)。
- 失败模式: prompt 未验证就全量跑, 结果不可用且钱已花——不可逆, 必须闸在小样本步。
