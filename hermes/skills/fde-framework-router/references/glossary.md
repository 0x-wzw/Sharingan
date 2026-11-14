# GLOSSARY — 术语表

- **FDE (Forward Deployed Engineer)**：一线驻场工程师——深入客户/业务现场，把
  AI 能力按现场约束交付落地的工程角色。本框架的方法论主体视角。
- **场景池 (use-case pool)**：五入口收集的候选 AI 场景的统一暂存与梳理机制。
- **是否值得做 (worth-doing gate)**：机会发现阶段的闸门；判否走"暂缓/观望"。
- **暂缓/观望 (hold/watch)**：闸门否决路径——留观而非删除，条件变化可重入。
- **价值评估 (value assessment)**：场景对齐业务价值的量化估计。
- **优先级排布 (prioritization)**：按影响范围对场景排序。
- **成功指标 (success metrics)**：目标定义的产物；可判定达标与否的量化标准。
- **流程拆解 (process decomposition)**：现有业务流程分步建模，顺带定义数据标准。
- **数据准备 (data readiness)**：数据源清单、获取方式与质量风险约束的落实。
- **方案设计 (solution design)**：技术路线收口（模型/集成/兜底入口）。
- **是否可行 (feasibility gate)**：方案定义阶段闸门；判否走"调整范围"回环。
- **调整范围 (scope adjustment)**：可行性不足时的回环——缩场景/降指标/换路径。
- **试点规划 (pilot plan)**：试点范围、时长、时间节奏的设计。
- **资源协同 (resource alignment)**：角色分工与跨团队协同安排。
- **环境准备 (environment setup)**：算力、数据权限、集成与合规环境就位。
- **能力构建 (capability build)**：模型与应用开发，接受问题修正回环。
- **联调测试 (integration test)**：端到端贯通测试。
- **效果达标 (effectiveness gate)**：受控环境下对照成功指标的技术验收闸门。
- **问题修正 (issue-fix loop)**：构建期回环——缺陷修复，短周期高频。
- **试点运行 (pilot run)**：真实业务环境的小范围运行。
- **试点通过 (pilot-acceptance gate)**：业务验收闸门（指标达成 + 业务采纳双维）。
- **优化迭代 (optimization loop)**：试点期回环——以试点通过为收敛条件。
- **规模化推广 (scale-out)**：分批推广至全量，每批带验收。
- **上线运营 (operations)**：生产运行监控、值班、兜底预案生效期。
- **运营反馈 (operations-feedback loop)**：运营期回环——固定节奏收集并落实改进。
- **持续优化 (continuous improvement)**：以运营反馈为输入的长期改进状态。
- **风险处理 (risk handling)**：全程旁路——AI 环节风险的识别/登记/分级/应对。
- **人工兜底 (human fallback)**：全程旁路——AI 失效时的降级与人工接管路径。
- **Human API**：把组织内"一件事实际怎么流转"（谁→谁、传什么、超时怎么办）当
  API 逆向的映射方法（Varick 术语）。
- **过程挖掘 (process mining)**：在 CRM/ERP/工单系统事件日志上重建真实流程步骤
  与回环的技术；与访谈对账使用。
- **四分法 (workflow triage)**：流程步骤的唯一标签体系——delete / plain code /
  agent / human（Varick）。
- **Delete 桶**：AI 时代应当消失的步骤（Hammer 1990 "Don't Automate, Obliterate"
  血统——先删再建）。
- **Human 桶**：做错不可逆代价高的步骤（审批/谈判/签约/付款），永远留人工。
- **基线先行 (baseline before you build)**：所有 KPI 在动工前测好基线的铁律；
  3/6 月 before/after 报告是价值证明协议。
- **回环计价**：每个流程回环按金钱与时间双重定价，作为 ROI 叙事的证据。
- **Build in-place（按系统落地）**：agent 的数据读取与行动都发生在客户既有的
  系统 of record 内，人工审批走既有 IM；零再培训，绝不推销换系统。
- **价值三桶**：成本节省 / 收入提升 / 风险缓释——分别对应 CFO / CHRO-销售 /
  全 C-suite 的买家叙事。
- **按系统分组 (PE scale tactic)**：多实体场景按系统 of record 分组复用同一
  agent 轨道，向同一买家重复销售。
- **Sidekick / Background agents**：对话式辅助 agent（10–20% 提效）与常驻
  后台 agent（70–80% 提效）的两类部署形态。
- **AI-FDE 产品化**：把 FDE 交付中可模板化环节做成软件（Lab0 模式：discovery
  辅助→设计文档→配置→测试→go-live）。
