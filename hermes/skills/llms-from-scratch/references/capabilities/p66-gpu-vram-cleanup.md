# GPU 显存清理流程 (p66) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Hands-On Large Language Models (Alammar & Grootendorst) 第 10 章 | 绑定单元: p66 | 支持材料: ce18 (显存/OOM), ce15
> 去向: source-router 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "⚠️ **VRAM Clean-up** - You will need to run the code below to partially empty the VRAM (GPU RAM). If that does not work, it is advised to restart the notebook instead."

— Alammar & Grootendorst, ch10 (chapter10_Chapter 10 - Creating Text Embedding Models.txt @143)

代码锚点 (同章 @147/@551, @154-163): `trainer.accelerator.clear()`; `del model, trainer`; `gc.collect()`; `torch.cuda.empty_cache()`。自译: 依次删引用、回收 Python 对象、清 CUDA 缓存; 不行则重启 notebook。

## I — Interpretation (自述)

连续实验 (训完一个模型换下一个) 的 OOM 多因旧模型仍被引用。释放顺序有讲究: 先删所有 Python 引用 (变量、trainer、accelerator), 否则 empty_cache 清不动; 再 gc.collect() 触发回收; 最后 torch.cuda.empty_cache() 归还缓存块。Accelerator 场景用 accelerator.clear() 一并处理。判停是硬性的: 流程走完仍 OOM → 重启内核, 不要反复徒劳尝试。

## A1 — Application Example

### 示例: 连续训练间的 VRAM 清理 (原书代码 SOP; 合成复算步骤)

- **类型与来源**: 原书 worked_example (ch10 嵌入模型训练间的清理代码块); 单次释放量级未列数字 (未说明)。
- **问题/输入**: 训完一个 SBERT, 立即训下一个, 报 OOM。
- **方法论的使用**: del model/trainer → gc.collect() → torch.cuda.empty_cache() (accelerator 场景先 accelerator.clear()) → 不行则重启 notebook; 可用 nvidia-smi/Colab 资源面板复核。
- **结论/预期输出**: 引用删净后 empty_cache 才有效; 显存占用回落即可续训。

## A2 — Future Trigger ★

### 情境 / 语言信号

1. notebook/脚本里连续训练两个模型后 OOM; 关键词 "CUDA out of memory / empty_cache / 释放显存 / 清 VRAM"。

### 与相邻 skill 区分

- 与 p65: 那是 API 费用; 本卡是本机显存。与 `gpt2-pretraining-pipeline` 的训练排障: 单次训练中的 OOM (调 batch/梯度检查点) 不在本卡范围, 本卡管实验间的清理。

## E — Execution

**必需输入**: 当前进程内待释放对象清单 (模型/trainer/dataloader)。

1. 删引用: del model, trainer (及 optimizer、缓存变量); accelerator 场景先 trainer.accelerator.clear()。
2. gc.collect()。
3. torch.cuda.empty_cache()。
4. 复核 nvidia-smi / 资源面板。判停: 仍不足 → 重启 notebook/内核, 不要绕过。

**输出契约**: 释放后显存读数; 完成标准 = 新实验可启动或已按判停重启。

## B — Boundary

- 不要用于: 单次训练内的 OOM (应减 batch/开梯度检查点/换量化); 多进程共享 GPU 的他人占用 (查 nvidia-smi 归属)。
- 常见失败: 只 empty_cache 不 del 引用——显存纹丝不动; 这是机制问题不是玄学。
- 版本边界 (ce15): Trainer/accelerator API 随版本变, 四步顺序不变、调用按当前版。

## 相关能力 (also_read, 阶段 3)

- composes-with: `lora-peft-finetuning` (QLoRA 训练后的显存释放), `f29-mlm-continued-pretraining-ner-alignment` (续训显存运维)
