# GPT-2 预训练全流水线 (text → batches → attention → assembly → pretrain → eval → decode → checkpoint)

## R — Reading (原文)

**引文 1 (数据步, f03/p01/p02):** ch02 @435:
> "Since we want the model to predict the next word, the targets are the inputs shifted by one position to the right"

**引文 2 (外部权重验证, f02/p25):** ch05 @1181:
> "We know that we loaded the model weights correctly because the model can generate coherent text; if we made even a small mistake, the model would not be able to do that"

**引文 3 (appendix-D warmup, f12/p34):** appendix-D @146:
> "In learning rate warmup, we gradually increase the learning rate from a very low value (`initial_lr`) to a user-specified maximum (`peak_lr`)"

**引文 4 (MPS 排障, f08/p41):** troubleshooting.md "Apple Silicon and MPS Support" @61:
> "Some notebooks and scripts use `cuda` when available and otherwise fall back to `cpu`, without selecting Apple's `mps` backend."

自译要点: ① 目标张量 = 输入右移一位,滑窗 stride 控制样本重叠;② 权重加载正确与否的最强外部验证是能否生成连贯文本;③ warmup 从 initial_lr 线性爬升到 peak_lr;④ 多数示例刻意不选 mps 后端,因其旧版本结果不稳定。

## I — Interpretation (自述)

这条能力是一条从原始文本到可用 checkpoint 的完整搭建-训练-验收链,分八段:

1. **数据步** — 文本用 tiktoken 分词(endoftext 作为唯一文档分隔符,`allowed_special` 需显式放行),按固定窗口切块;target 窗口相对 input 右移一位,实现"预测下一个 token";stride 决定相邻样本重叠程度,常规取 stride = context_length(不重叠);上线前先做 token 预算 sanity check(语料 token 量 vs 模型容量,避免拿 5k token 喂 124M 参数)。
2. **注意力步** — 自注意力四步:点积得 score → 除以 √head_dim 缩放 → softmax 前施加因果掩码(-inf 填上三角)→ softmax 归一化得 weight;多头要求 d_out % num_heads == 0,用 `nn.Linear` 投影、`register_buffer` 存掩码、dropout 按 1/(1-p) 缩放。
3. **组装步** — 按 GPT-2 124M 基准配置(emb=768, 12 层, 12 头, ctx=256 教育版)拼装:token+position embedding → Pre-LN transformer block(残差 + GELU tanh 近似)→ final LayerNorm → 输出 head;可估算参数量/显存,注意 weight tying。
4. **预训练步** — AdamW 训练循环,配 train/val 双损失监控;若要稳定训练,叠 appendix-D 三件套:LR warmup(约占 0.1%–20% 总步数)、梯度裁剪 max_norm=1.0、余弦退火到 min_lr。
5. **评估步** — 未训模型先手算一遍 logits→log→平均→负号→cross-entropy→exp 得 perplexity,建立基线;训练中用 calc_loss_loader 式聚合看 train/val 分叉。
6. **解码步** — 贪心(argmax)做确定性基线;生成用 temperature + top-k 控制随机性,温度→0 退化为贪心。
7. **验收步** — 加载 OpenAI 官方 GPT-2 权重,能生成连贯文本即证明逐层实现无误(这是最强验证);再用训练后模型生成对比训练前乱码。
8. **运维步** — `state_dict` + optimizer state 保存 checkpoint,加载后复核;设备按 cuda→mps→cpu 降级,MPS 需按版本门槛验证结果一致性。

一句话:每一段都有可复核的中间产物——批形状、注意力权重和为 1、参数量对表、损失曲线、perplexity 数值、生成文本、权重加载验证——流水线断在哪一段都能定位。

## A1 — Application Example(书中案例)

**案例 1 (c01, worked_example, 第 5 章 5.1–5.2):** 在单篇短篇《The Verdict》(5,145 tokens,90/10 切分)上预训练 124M GPT-2(context 256,10 epochs,AdamW lr=0.0004)。输入:完整训练循环 + 双损失 loader。执行:训练前生成乱码 → 训练 → 训练/验证损失同时下降再分叉。输出/结论:训练损失降到 <1,验证损失 <7;模型最终逐字复述训练文本——语料太小,记忆化是教育场景内的预期结果,不是 bug。未说明生产规模外推结果(原书未提供)。

**案例 2 (c02, worked_example, 第 5 章 5.1.2):** 对两个 2×3 token 样例("every effort moves" / "I really like")手动演算:目标 token 概率→log→平均(-10.7722)→取负得 cross-entropy=10.7722→exp≈48,725 perplexity,与 `torch.nn.functional.cross_entropy` 结果一致。这是评估步的基准演算,可逐数复算。

**案例 3 (ce02 视角, 失败边界, 第 5 章):** 同一训练里,"损失还在降"被误当进步——验证损失回升而训练损失持续下降,末段生成内容在训练集逐字可查。诊断信号:train/val 交叉点即过拟合起点。

**合成演练(标注:非书中案例,按原书规则可复算):** 假设 ctx=256、stride=256、语料 5,145 tokens、drop_last=True、batch_size=2。窗口起点为 0,256,…,4864(最后一个起点需满足起点+256 ≤ 5145,即 4889 为最后可用起点,起点序列 0,256,…,4608 共 19 个窗口 ×2 样本方向)。演练目的:验证 stride=ctx 时无重叠且最后不完整窗口被丢弃——能按 f03/p02 规则机械推出窗口数,即掌握数据步。

## A2 — Future Trigger ★

**触发情境:**
1. 用户要从零实现/讲解 GPT 类模型:分词→DataLoader→注意力→组装→训练循环→评估→生成→存档全链。
2. 用户在预训练(或小语料教育级预训练)时遇到:损失不降/NaN、train-val 分叉、MPS/CUDA 报错、版本环境问题。
3. 用户想加载 OpenAI GPT-2 官方权重到自建模型并验证实现正确性。
4. 用户要给训练加稳定化(warmup/梯度裁剪/余弦退火)或做训练成本/token 预算估算。
5. 用户要把自建 GPT 权重迁移到 Llama 类架构(逐组件对照)。

**语言信号(中英):** "build GPT from scratch / 从零搭建 GPT"、"pretraining loop / 预训练训练循环"、"dataloader stride / shifted targets / 下一词预测"、"causal multi-head attention / 因果注意力"、"perplexity / cross-entropy / 困惑度"、"temperature top-k sampling / 温度采样"、"load GPT-2 weights / 加载官方权重"、"warmup, cosine decay, gradient clipping / 预热、余弦退火、梯度裁剪"、"mps cuda fallback / MPS 报错"、"save checkpoint / 保存断点"。

**与相邻 skill 的区分(定稿,阶段 3 回填完成):** 微调类技能(text-classification / instruction-finetuning / lora-peft)都以"已有预训练权重"为前提,输出是微调后模型——本技能的契约是**从原始文本训练出基座**,不含分类头/指令数据/adapter;router 能力卡覆盖本技能之外的非 promoted 单元。若用户只问 tokenizer 或只问注意力单点,本卡仍适用(对应段独立可执行),但若问的是检索/embedding 管线则应路由到 RAG/embedding 技能。

## E — Execution (可执行步骤)

**输入契约:** 必需——① 原始语料(UTF-8 文本或文件路径);② 目标规模配置(默认 GPT-2 124M 基准:emb 768/12 层/12 头/vocab 50257;教育版 ctx=256,生产可调);③ 训练预算(epochs/batch_size/lr,默认 lr=0.0004, AdamW);④ 设备(`cuda`/`mps`/`cpu`,未知则探测)。缺失 ① 或 ② 时先询问,不得静默用占位语料冒充真实训练。可选——是否加载官方 OpenAI 权重验收、是否启用 appendix-D 稳定化。

**步骤:**

1. **环境与设备**(f08/f14/p41):探测 `torch.cuda.is_available()` → `torch.backends.mps.is_available()` → cpu。MPS 分支:先确认 PyTorch 版本满足门槛,跑短训练冒烟测试,与 cpu 结果对比;若损失发散,先在 cpu 上复跑定位。完成标准:选定设备并打印版本,冒烟训练损失有限。
2. **数据步**(f03/p01–p04/p21):tiktoken 分词(`allowed_special={"<|endoftext|>"}`);按 max_length/stride 切 (input, target) 对,target=input 右移一位;按比例切 train/val;**判停点**——token 预算 sanity check:若语料 token 量远小于参数量(如 <10⁴ vs 124M),向用户声明教育级预期(会过拟合/记忆化),确认后再继续。完成标准:取一个 batch,`inputs[0][1:] == targets[0][:-1]` 成立,batch 形状 (B, T) 正确。
3. **注意力步**(f04/p06–p13):实现因果多头注意力——score=QKᵀ/√d_head(d_out % num_heads==0 先断言)→ softmax 前掩码(掩码放 softmax **前**,用 -inf)→ softmax 得 weight(weight 和为 1 用作断言)→ `nn.Linear` 投影 + dropout + `register_buffer` 存掩码。完成标准:给定固定输入,权重矩阵每行和≈1,未来位置权重=0。
4. **组装步**(f05/p14–p18):embedding → N×Pre-LN block(残差、GELU tanh、final LayerNorm)→ 输出 head;打印 `numel()` 与 124M 对表(±weight tying 口径内);估算显存。完成标准:前向输出 logits 形状 (B, T, 50257),参数量与基准一致。
5. **预训练步**(c01/f12/p34–p36/p39):AdamW 循环;基线配 train/val 双损失 loader;启用稳定化则——warmup(前 0.1%–20% 步线性爬到 peak_lr)→ 训练主体 → 余弦退火至 min_lr(每步按半余弦公式更新)→ 梯度裁剪 `clip_grad_norm_(max_norm=1.0)`(反向后、step 前)。**判停点**——val loss 回升而 train loss 下降(交叉点后):停训并报告过拟合,勿按"损失还在降"继续。**分支**——损失 NaN/inf:先降 lr、检查裁剪是否启用、再查数据步 target 错位。完成标准:得到损失曲线,train/val 值都报告,过拟合状态明确标注。
6. **评估步**(f06/c02/p20):未训模型先复算 c02 基线(log-prob→平均→取负→CE→exp=perplexity)确认度量实现;训练后对 train/val loader 聚合平均损失,perplexity=exp(loss)。完成标准:两个数值 + 基线对照,口径(均值聚合方式)写明。
7. **解码步**(f07/p19/p23):`generate` 循环;确定性用 argmax,采样用 temperature+top-k(先截断 top-k 再缩放 logits 再 softmax);temperature→0 退化验证与贪心一致。完成标准:训练前生成乱码、训练后语法大致正确(教育级),两种模式均可复现。
8. **验收与运维**(f02/f32/p24–p25):加载官方 GPT-2 权重(名称映射逐键核对,shape 全等断言),生成连贯文本即最强验证;checkpoint 保存 `model.state_dict()` + optimizer state,重载后对同一输入 logits 全等复核。**分支**——用户目标是 Llama 类架构:按 ch05_07 对照表逐组件换(RoPE/RMSNorm/SwiGLU/GQA)再迁移权重。完成标准:连贯文本生成 + 重载 logits 一致。
9. **交付**:报告包含——配置表、batch 形状校验结果、参数量、损失曲线要点(train/val 终值)、perplexity、生成样本、权重加载验证结论、checkpoint 路径、设备与版本记录(便于排障复现)。

**输出契约:** 结构化报告(上述第 9 条字段)+ 代码文件 + checkpoint 文件。数值(损失/perplexity/参数量)须来自实际运行输出,禁止估算冒充实测;`state_dict` 路径与重载校验结果必须写明。

## B — Boundary (边界)

**不要使用:** ① 有现成预训练权重、只想做分类/指令/LoRA 微调——那三个微调技能的契约不同(输出是分类 logits / 回答 / adapter);② 只问检索、embedding、RAG 管线;③ 只想要 LLM 应用层(prompt、agent、记忆)——不涉及训练;④ 用户要的是生产级分布式预训练(DDP/FSDP、多节点)——本书口径是单卡教育级,p38 的 ~$69 万成本估算恰说明真实预训练不在本卡射程内;⑤ 需要严格的逐 token 概率保证、KV cache 推理优化训练等进阶话题(本卡只做识别与转介)。

**作者警告的失败模式:** 小语料上训练损失持续下降但模型逐字记忆训练集(ce02)——"损失在降"≠"模型在进步";MPS 后端旧版本结果不稳定或与 cpu 有差异,必须验证后才可用(f08 修正后口径);CUDA 专属选项(pin_memory、torch.compile、DDP)不能想当然搬到 mps;score/weight 术语混用导致漏 softmax 或掩码放错位置(ce01);把 -inf 掩码放在 softmax 之后会造成分布重新归一化泄漏。

**批判阶段的盲点(阶段 0):** 原书是教育取向——单卡、单故事语料、124M 教育配置;"能跑通"与"能用于生产"之间没有桥梁,卡内一切数值基线(损失 <7、perplexity 48,725 等)都是教育级口径,不可作为生产 SLO 引用;appendix-D 超参(warmup 步数区间、max_norm=1.0、min_lr)是示例值而非调优结论。另注:verified.md 的 V2 check_mode 为纸面演练,阶段 4 未实跑前不得声称"已实测"。

## 相关能力 (also_read, 阶段 3)

- depends-on: 无 (本卡自足, 从原始文本出发)
- contrasts-with: 无
- composes-with: `text-classification-finetuning`, `instruction-finetuning-and-eval`, `lora-peft-finetuning` (三者均以本卡产出的预训练权重为输入), `p48-kv-cache-acceleration` (解码步的推理期加速)
- also_read: `llms-from-scratch-router` (本卡未覆盖的散点单元由 router 卡服务)
