# 决策规则速查 — WeMM-Video: Pushing the Frontiers of Open-Source Omni-Modal Video Understanding

| 能力 | 一句话规则 |
|---|---|
| Progressive Modality Curriculum | Freeze what works, unfreeze progressively, scale context last when adding a modality. |
| Timestamped Token Interleaving | Give two time-indexed modalities a shared explicit time axis before fusion. |
| Failure Mode Ordered Post Training | Order post-training by diagnosed failure mode, with degeneration fixed before RL. |
| Teacher Allocation By Capability | Choose teachers for capabilities to lift and for capabilities to retain, separately. |
| Anti Repetition Loop | Mine rare degenerate outputs offline and stabilize them with isolated LoRA rounds before RL. |
| Reward Routing By Verifiability | Route each training task to rule, rubric or teacher-consistency rewards by verifiability. |
| Dimension Based Evaluation | Fix dimensions, metric conventions and provenance before comparing model scores. |
| Fixed Rate Signal Tokenization | Compress a continuous signal into a fixed token-per-second stream with local windows. |
| Scarce Modality Data Transfer | Transfer reasoning from a rich adjacent domain plus a small native target set. |
| Weight Format Runtime Matrix | Match checkpoint format to a pinned runtime and verify the overlay before serving. |
| Honest Validation Records | Record every validation scope as pass, fail or pending with artifact revisions. |

> 速查只给结论；需要原文依据、案例或反例时读对应能力卡。
