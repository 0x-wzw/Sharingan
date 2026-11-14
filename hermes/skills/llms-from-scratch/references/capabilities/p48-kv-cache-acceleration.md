# KV cache 加速生成 (p48) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 3/12 章 | 绑定单元: p48 | 支持材料: ce15
> 去向: source-router 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "model.generate(\n  input_ids=input_ids,\n  max_new_tokens=100,\n  use_cache=True\n)"

— Alammar & Grootendorst, ch03 (chapter03_Chapter 3 - Looking Inside LLMs.txt @121-127; 对照 @131-137 use_cache=False)

ch12 @96: `model.config.use_cache = False` (训练时)。自译: 自回归生成时缓存已算过的 Key/Value 投影, 新 token 只算增量; HF generate 默认开启。训练/梯度检查点场景须显式关闭。

## I — Interpretation (自述)

逐 token 生成若每步重算全部历史的 K/V, 复杂度随长度平方膨胀; KV cache 把历史 K/V 存下来, 每步只算新 token。工程上就两件事: 推理时保持 use_cache=True (默认即是, 除非显式关了); 微调/训练时设 use_cache=False (与 gradient checkpointing 冲突且无意义)。显存代价是 K/V 随上下文线性增长, 超长上下文要留预算。

## A1 — Application Example

### 示例: use_cache True/False 计时对比 (原书 %%timeit 例)

- **类型与来源**: 原书 worked_example (ch03 两段 %%timeit -n 1, max_new_tokens=100, True vs False)。
- **问题/输入**: 同一输入, 生成 100 个新 token。
- **方法论的使用**: 仅切换 use_cache 参数跑 %%timeit 对比耗时。
- **结果**: 书以计时对比呈现加速 (具体数值在原书输出单元, 正文未引数字, 未说明); 方向 = False 显著更慢。

## A2 — Future Trigger ★

### 情境

1. 生成慢, 问"怎么加速 LLM 推理"。
2. 微调时报 gradient checkpointing 与 use_cache 冲突。

### 语言信号

- "KV cache / use_cache / 推理加速 / 生成很慢 / past_key_values"

### 与相邻 skill 区分

- 与 `gpt2-pretraining-pipeline`: 训练管线内部已按此约定关 cache; 本卡面向推理服务与单点答疑。

## E — Execution

**必需输入**: 推理栈 (HF generate / llama.cpp / vLLM 等)。

1. 检查推理路径未显式禁用 cache (HF 默认 True)。
2. 用 %%timeit 或吞吐计数对比验证。判停: 无差异 → 栈未走该路径, 查实现。
3. 训练/微调代码设 use_cache=False (与 gradient checkpointing 共存)。

**输出契约**: 耗时对比数据 + 最终配置; 完成标准 = 计时差异可复现或说明原因。

## B — Boundary

- 不要用于: 训练阶段 (必须关); 单 token 生成的极端短输出 (收益可忽略)。
- 显存边界: 长上下文下 K/V 显存线性增长, cache 不是免费的。
- 版本边界 (ce15): HF/TRL API 随版本变动, 现代栈多自带 paged/continuous attention 优化, 默认行为需查当前文档。

## 相关能力 (also_read, 阶段 3)

- composes-with: `gpt2-pretraining-pipeline` (本卡是其解码步的推理期加速; 训练期 use_cache=False 与梯度检查点冲突的口径见那边)
