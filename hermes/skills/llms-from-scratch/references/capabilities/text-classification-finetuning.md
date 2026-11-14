# 文本分类微调 text-classification-finetuning

<!-- RIA++ 能力卡 | book: llms-from-scratch × hands-on-llms | units: f09, f15, f27, p26, p27, p28, p42, p43, p56, p57, p58 | cases: c07, c08, c09 | counter-examples: ce04, ce05, ce06, ce07, ce11, ce16, ce17 | date: 2026-11-08 -->

## R — 原文 (Reading)

**f09/p26 — 只训输出层不够,解冻最后 block(Raschka ch06 §6.5):**

> "Technically, it's sufficient to only train the output layer. However, as I found in Finetuning Large Language Models, experiments show that finetuning additional layers can noticeably improve the performance. So, we are also making the last transformer block and the final LayerNorm ... trainable"

**c07 — SMS 数据准备与训练规模(Raschka ch06 §6.2–6.7):**

> "we subsample (undersample) the dataset so that it contains 747 instances from each class... The training takes about 5 minutes on an M3 MacBook Air laptop computer and less than half a minute on a V100 or A100 GPU..."

**ce05 原文与 p27 同节支撑:因果注意力下取最后一个 token 的 logits 做分类(`model(input)[:, -1, :]`),准确率不可微故以交叉熵为代理(Raschka ch06 §6.5–6.6)。**

**c08 — 消融结论(Raschka ch06 bonus additional-experiments):**

> "Row 1 vs. 2 ... Training the last output token position results in substantially better performance... Using LoRA... even improves the performance by 1% point (row 11 vs. 5)... likely due to less overfitting."

**ce04 — padding 策略原文(Raschka ch06 §6.3 vs ch07 §7.3):**

> "pad all messages to the length of the longest message ... We choose option 2 and pad all messages to the longest message in the dataset" (ch06);ch07 改进为 batch 级动态 padding。

**f27/c15 — 冻结曲线(Alammar ch11):**

> "'Effect of Frozen Encoder Blocks on Training Performance' ... annotate('Performance stabilizing', xy=(4, y[4]))" — 全参 F1≈0.854,冻结前 4 块趋稳(0.82–0.84,峰值 0.8434),只剩最后 1 块时跌至 0.702。

**f15/p42/p43 — 分类路线(Alammar ch04):cardiffnlp 专用情感模型、嵌入+LogisticRegression、类原型均值+余弦相似度("average the embeddings per class and apply cosine similarity")、零样本(标签描述嵌入)、Flan-T5 生成式(输出需 "Do not give any other answers" + 严格相等解析)、GPT-3.5 API。**

*(以上引文均 ≤100 词,出自源码提取文本;中文转述为自译。)*

## I — 方法论骨架 (Interpretation)

把一个预训练语言模型改造成分类器的完整方法,骨架是五步:

1. **改头**:LLM 原本输出词表 logits;分类只需 num_classes 个输出,替换最后一层为新的分类头(随机初始化)。
2. **取数**:因果/双向模型都要选对"读哪个位置"——因果模型(GPT)取**最后一个 token** 的 logits,因为因果掩码下末位聚合了全序列信息;BERT 类取 [CLS] 或平均池化。
3. **冻结预算**:不必全参微调,也不该只训分类头——默认解冻**最后一个 transformer block + final LayerNorm**;更精细的做法是做逐层冻结实验,找 F1 曲线的"趋稳拐点"来决定冻结多少。
4. **数据与 padding**:先检查类别平衡(不平衡则下采样多数类),按比例切分,pad 到固定长度(注意长度方差大时按 batch 动态 pad 更省),并断言 max_length ≤ 模型上下文。
5. **损失与评估**:只在被选位置的 logits 上算交叉熵;训练日志中的准确率若来自抽样 (eval_iter) 只是估计值,报告性能必须全集复算;分类指标用 accuracy/F1,生成式路线的文本输出要固定标签+严格解析。

换头 → 选位置 → 定冻结 → 备数据 → 训练+全集评估,这五步构成一条可复用到任何分类任务的流水线。

## A1 — 书中的应用 (Past Application)

### 案例 1: SMS 垃圾短信二分类(c07,worked_example,Raschka ch06 §6.2–6.8)

- **输入/问题**: UCI SMS Spam Collection,ham:spam ≈ 6:1,需二分类。
- **方法执行**: 欠采样至 747+747 → 0.7/0.1/0.2 切分 → pad 到数据集最长 120 token → 换 2 类输出头,冻结主干、解冻最后 block + final LayerNorm → AdamW lr=5e-5 训 5 epochs → 只在最后 token 的 logits 上算交叉熵 → 推理新短信。
- **结论/预期输出**: M3 MacBook Air 约 5 分钟;书中表列 train/val/test acc = 96.63/99.33/95.00%(训练≈验证、测试略低 = 轻度过拟合,预期内)。

### 案例 2: 19 组消融对照表(c08,reported_case,ch06 bonus 02)

- **输入/问题**: 微调配置的每个设计选择值得多少?
- **方法执行**: A100 上单变量对照:last vs first token、可训练层(last_block / last_layer / all)、模型规模、随机 vs 预训练权重、LoRA、padding 策略、去 causal mask、embedding 平均。
- **结论**: last token 远优于 first(96.63% vs 78.46% 训练 acc);last_two_blocks 优于 last_block 和 all;355M 反而 84.67%(更大≠更好);pad 到 1024 显著变差;LoRA 略优且更快省内存。

### 案例 3: IMDb 多模型横评(c09,reported_case,ch06 bonus 03)

- **输入/问题**: 从零实现的 GPT-2 与专用分类模型差多少?
- **结论**: 124M GPT-2 全参微调 test 91.88%(Muon 优化器 92.40% 但训练 acc 98%+,过拟合);BERT 90.89%、DeBERTa-v3 94.69%、LogisticRegression 基线 88.85% —— 自实现模型已与专用编码器同档。

### 案例 4: 逐层冻结曲线(c15/f27,reported_case,Alammar ch11)

- **输入/问题**: BERT 在 rotten_tomatoes 上冻结多少层不损失性能?
- **方法执行**: bert-base-cased + HF Trainer,F1 指标,12 级冻结深度逐一重训。
- **结论**: 全参 F1≈0.854;冻结前 4 块趋稳(~0.84,峰值 0.8434);只训最后 1 块跌至 0.702。原书提供实验代码与图,未另行说明跨任务普适性。

*(书为教程书,无作者亲历叙事案例;以上均为书中可运行示例/作者报告的实验结果,类型与来源已标注。)*

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?

1. 手头有一批带标签的文本(短信/评论/工单/邮件),想训练一个分类器,又想用 LLM 的表示能力。
2. 已经有一套 LLM/GPT 代码(比如从头实现的或预训练过的),想把"下一词预测"改成"类别预测"。
3. 训练完成了但不知道准确率是否可信、冻结哪些层、超参从哪起步。
4. 标注数据很少或没有,想先问"有没有不用训练的分类路线"。
5. 听说过 LoRA、冻结层、few-shot 分类,想知道在分类任务里怎么选。

### 语言信号

- 中文:"微调一个文本分类器"、"把 GPT/BERT 改成分类"、"垃圾短信/情感分类"、"冻结哪几层"、"训练/验证准确率"、"类别不平衡"、"padding 长度"
- 英文:"finetune for classification / classification head / last token logits / freeze layers / unfreeze last block / spam or sentiment classification / class imbalance / pad to max length / eval accuracy"

### 与相邻 skill 的区分(定稿,阶段 3 回填完成)

- vs `instruction-finetuning-and-eval`:本 skill 的输出契约是**类别 logits**;instruction skill 是生成回复 + judge 评分。用户要"模型回答问题"→instruction;要"输出一个类别"→本 skill。
- vs `lora-peft-finetuning`:本 skill 默认冻结+解冻末块;用户明确要参数高效/显存受限时才切 LoRA 路线(本 skill 的选型节会指向它)。
- vs `embedding-model-adaptation`:用户要的是"句向量/检索"而非"类别标签"→embedding skill。
- vs `gpt2-pretraining-pipeline`:从原始文本从头预训练→pipeline;在已有预训练权重上加分类能力→本 skill。

## E — 可执行步骤 (Execution)

**输入契约**:带标签文本数据集(字段:文本 + 类别标签;需知类别数与分布)、一个预训练模型(权重可加载)、设备。缺失类别数/标签映射/数据划分比例时先询问,不得静默猜值。

**输出契约**:三集(train/val/test)指标表(字段:split、accuracy、F1,注明是全集还是抽样估计)、可复用的推理函数(输入文本→类别标签)、冻结/可训练参数清单。

1. **路线选型**(f15)
   - 有标注且量大 → 微调路线(继续步骤 2);标注极少(每类约 16 条)→ 考虑 SetFit/少样本路线(p58:每类 16 条,3 epochs × 20 对);完全无标注 → 类原型均值+余弦相似度(p42)或零样本标签描述嵌入;可接受 API 成本 → 生成式 prompt 分类(p43,先小样本试成本)。
   - 完成标准:已明确写出所选路线与理由。
2. **数据准备**(p28, ce11)
   - 打印类别分布;不平衡→每类下采样至少数类数量(或声明用 imbalanced-learn 等替代);标签映射成 0..C-1;按 0.7/0.1/0.2 切分(划分比例是本书约定,可按需调整但需声明);pad 到固定长度,断言 max_length ≤ 模型上下文;长度方差大时改 batch 级动态 pad(ce04)。
   - 完成标准:三集 shape 打印确认,batch 内含 padding 且无越界。
3. **改头 + 冻结**(p26, ce05)
   - 替换 out_head 为 nn.Linear(emb_dim, num_classes);遍历参数 `requires_grad=False` 后解冻最后一个 transformer block 与 final LayerNorm。
   - 判停点:若算力/显存受限或想少训参数 → 转入步骤 3b。
3b. **冻结预算实验**(f27, ce17):从"全参"到"只训头"之间取 3–5 个冻结深度逐一重训,画 F1 曲线找"趋稳"拐点,取拐点配置。
   - 完成标准:可训练参数清单已列出,F1 曲线或至少 2 个冻结深度对照已有。
4. **训练**(c07, p56)
   - 基准超参:Raschka 路线 AdamW lr=5e-5, 5 epochs(c07);BERT/HF Trainer 路线 lr=2e-5, batch 16, wd=0.01, 1 epoch 起(p56)。损失只取所选位置 logits 算交叉熵(p27:因果模型取 `[:, -1, :]`)。
   - 判停点:train/val 损失分叉(过拟合)→ 减 epoch 或加冻结;验证准确率 ≈ 多数类占比 → 回步骤 2 查类别平衡。
   - 完成标准:训练曲线已记录,val 指标不再提升。
5. **评估与报告**(ce07)
   - **全集**复算三集指标(不用训练日志的 eval_iter 抽样估计值);报告注明评估口径。
   - 完成标准:输出契约中的指标表已产出,推理函数对一条新样本返回合法标签。
6. **对照校准**(c08, c09):与简单基线(逻辑回归/多数类)和消融结论对照——last vs first token、冻结深度、模型规模、padding 长度各影响多少;解释自己结果偏离书中基准的原因。

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill

- 任务是生成文本/回答指令 → 用 instruction-finetuning。
- 需要的是句向量、相似度、检索 → 用 embedding/RAG 路线。
- 完全无标注且不想训练 → 先走零样本/类原型路线(f15),别直接上微调。
- 从原始语料预训练模型本身 → gpt2-pretraining-pipeline。

### 作者在书中警告的失败模式

- **类别不平衡**:不检查分布直接训,模型永远预测多数类,准确率虚高召回为零(ce11;书中 ham:spam≈6:1,显式下采样到 1:1)。
- **只训输出层**:准确率明显偏低;反向全解冻则小数据过拟合(ce05)。
- **数据集级定长 padding**:个别超长样本让绝大多数 batch 全是 padding,浪费显存;超上下文直接越界(ch06 用 assert 拦截;ce04)。
- **抽样估计当全集性能**:训练日志里 eval_iter=5 的准确率只是估计,直接引用属评估口径错误(ce07)。
- **取错 token 位置**:消融显示 first-token 训练 acc 78.46% vs last-token 96.63%(c08);因果模型必须取最后 token(p27)。
- **推理函数隐性截断**:用 `pos_emb.weight.shape[1]` 取上下文长度得到 768 而非 1024,代码不报错但长输入被静默截断——必须用 shape[0] 且 assert(ce06)。
- **冻结层数/超参当作普适默认**:书中 F1 曲线与超参基准绑定其数据集与模型;单次运行、单 seed 的对比结论不稳健,不可直接外推(ce16, ce17)。

### 作者的盲点 / 时代局限

- 消融在单一数据集(SMS/IMDb)单次运行得出,未做显著性检验;1% 级差异可能来自方差。
- 书中分类微调 5 epochs、特定 lr 等默认值未做敏感性分析,换数据分布需重测。
- f27 冻结曲线结论来自 BERT/rotten_tomatoes;对生成式 GPT 侧仅可作方向性参考。
- 生成式分类的严格相等解析脆弱:原文未明示 strip,返回 " negative " 即解析失败(p43 边界记录)。

### 容易混淆的邻近方法论

- **指令微调**:同样"在预训练模型上继续训练",但数据格式(Alpaca 三元组 vs 文本+标签)、损失掩码(-100 忽略 vs 全 token 分类损失)、输出契约(回复 vs 类别)完全不同;ch06 的 0.7/0.1/0.2 划分与 ch07 的 85/10/5 不可串用(p28/p29)。
- **LoRA**:同为参数高效手段,但机制是低秩增量而非层冻结;书中消融显示 LoRA 在此任务略优且更快(c08)——算力受限时优先比较两者而非默认冻结。

---

## 审计信息

- 支撑单元(全部 verified):f09, f15, f27, p26, p27, p28, p42, p43, p56, p57, p58
- 支持案例:c07 (worked_example), c08/c09 (reported_case), c15/c16 (alammar 侧对照)
- 反例映射:ce04, ce05, ce06, ce07, ce11, ce16, ce17
- 验证方式:V1/V2/V3 纸面 walkthrough;阶段 4 实测前不声称"已实测"
- 蒸馏时间:2026-11-08

## 相关能力 (also_read, 阶段 3)

- depends-on: `gpt2-pretraining-pipeline` (预训练权重是本卡输入前提)
- contrasts-with: `lora-peft-finetuning` (解冻末块 vs LoRA 旁路, c08 消融示 LoRA 略优), `instruction-finetuning-and-eval` (类别 logits vs 回复生成), `embedding-model-adaptation` (输出类别标签 vs 句向量, SetFit 边界见 B 段)
- composes-with: 无 (本卡独立交付分类器)
- also_read: `llms-from-scratch-router` (f15 之外的零样本/生成式路线补充)
