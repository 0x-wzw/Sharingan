# 决策规则速查 — AI Dev 26 x SF — Agent Engineering Practices from 48 Conference Talks

| 能力 | 一句话规则 |
|---|---|
| Agent Evals — literacy, agentic benchmarks, simulation ladder | Interpret third-party benchmarks with heuristics, build containerized agentic evals that test model+harness+problem, hill-climb without overfitting, and escalate to simulation for interactive agents. |
| Red-Team Suite — behaviors to CI test suites | Turn natural-language behavior descriptions into versioned, CI-integrated red-team test suites with multi-turn persona simulators across injection/hallucination/off-topic/leakage. |
| Production Shells — deterministic architecture for stochastic cores | Wrap every model call in typed validated interfaces, concentrate decisions in a manager agent over explicit rules, cache extraction, and ground every value to its source. |
| Sandbox Security — containment, scope, intent | Layer agent safety: micro-VM containment with zero credentials inside, scoped per-session access on top, intent policies last — never model self-judgment first. |
| Durable Agents — checkpoint execution for long runs | Structure agent workflows as durable executions: persist every activity result, retry by configuration, replay completed steps and resume from failure — never restart. |
| Agent Memory — flat token curves, forgetting, FS priors | Design memory as layered stores with token thresholds, summarize-and-reference offloading, agentic read/write search loops, and file-system interfaces that ride model priors. |
| Agent Optimization — Pareto across accuracy, cost, latency | Sweep configurations into a Pareto frontier, then push it out with vertical scaling (repair loops), horizontal scaling (best-of-n), heterogeneous ensembles, and budget-aware dynamic orchestration. |
| Org Shift — from vibe coding to agentic engineering | Reframe the engineering organization around 'building the thing that builds the thing': evals as the quality gate, bottlenecks migrating downstream, generalist AI-native teams, parallel human/agent skill development. |

> 速查只给结论；需要原文依据、案例或反例时读对应能力卡。
