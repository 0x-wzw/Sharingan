---
stage: mirror
created: 2026-11-14
tags: [cangjie, sharingan, hermes, skills]
---

# Hermes-format distilled skills — Ubuntu VM mirror v2.0.0 merge + v2.1.0 refresh

The Ubuntu VM's cangjie stack (2026-11-14 merge). Canonical knowledge lives in the
Obsidian vault (`Knowledge/40-Templates/cangjie/`); this directory is the distributable
mirror gathered into Sharingan at release v2.0.0.

- `skills/` — 26 distilled skills (Hermes format, <=60-char trigger-first descriptions)
- `cangjie-lightweight/SKILL.md` — the SHORT-FORM distillation path (tweets, clips, repos,
  papers -> one Hermes skill): fetch source, extract the method, author Hermes-format
  SKILL.md, install, mirror to vault + bundle releases. Routing rule: long-form
  (books/courses/podcasts) -> the RIA-TV++ pipeline (this repo's main skill);
  short-form -> this path.

| Skill | Version | Source |
|---|---|---|
| harness-eval-method/SKILL.md | 1.0.0 | garrytan/g-harness-evals repo @ edacaa8 + tweet 2121463161069228382, distilled 2026-11-13 |
| harness-starter-stack/SKILL.md | 1.0.0 | X post 2118759929947328571 (@Kiiiiira777, 2026-11-06): Dario Amodei clip + 14 free repos — all repos… |
| knowledge-base-builder/SKILL.md | 1.0.0 | session-built 2026-11-12 — FDE knowledge base build-on process, standalone cron spec |
| multi-agent-economy/SKILL.md | 1.2.0 | external repo |
| parallel-venture-validation/SKILL.md | 1.1.0 | X post 2119367655278723559 (@alvinfoo, 2026-11-08) — Paul Cheek (MIT Sloan) clip, transcript extract… |
| poteto-swarm-method/SKILL.md | 1.0.0 | Lauren Tan — 'SpaceX AI Engineer' talk (Sep 2026) + Pocock interview (Oct 2026) + poteto/noodle |
| skepsis-application-framework/SKILL.md | ? | external repo |
| venture-machine/SKILL.md | 1.0.0 | session-built 2026-11-09 — venture machine operation (kanban funnel, driver, bots, triage, Sahati ex… |
| whatsapp-crew-bridge/SKILL.md | 1.0.0 | How Agents Use WhatsApp.md — operator brief, user-provided, distilled 2026-11-11 |
| cangjie-lightweight/SKILL.md | 1.0.0 | session-built pipeline skill (Oct-8 framework + 2026-11 policy sync) |

Policy: these files are mirrors; the vault stays canonical. No secrets — the 04:20
harness_sync-style fail-closed scans apply to any future mirror updates.

## v2.1.0 additions — Tier-1-hardened skills (local cangjie profile, 2026-11-14 fleet audit)

All added skills passed the NVIDIA SkillEvaluator Tier-1 gate (1 residual error each =
environment-blocked skillspector; full reports in the cangjie workspace `skills-audit-r3/`).

| Skill | Version | Source |
|---|---|---|
| aidev26-agent-engineering/SKILL.md | 1.0.0 | session-built — agent-engineering curriculum bundle |
| fde-framework-router/SKILL.md | 1.0.0 | cangjie distillation — FDE routing (10-card funnel) |
| fde-opportunity-discovery/SKILL.md | 1.0.0 | cangjie distillation — FDE stage 1 |
| fde-pilot-execution/SKILL.md | 1.0.0 | cangjie distillation — FDE stage pilot |
| fde-process-mapping/SKILL.md | 1.0.0 | cangjie distillation — AP 17-step case |
| fde-productization/SKILL.md | 1.0.0 | cangjie distillation — FDE productization |
| fde-solution-definition/SKILL.md | 1.0.0 | cangjie distillation — FDE solution definition |
| fde-system-outcome/SKILL.md | 1.0.0 | cangjie distillation — FDE system outcome |
| fde-three-stage-landing/SKILL.md | 1.0.0 | cangjie distillation — FDE landing stages |
| fde-workflow-triage/SKILL.md | 1.0.0 | cangjie distillation — FDE workflow triage |
| karpathy-llm-usage/SKILL.md | 1.0.0 | cangjie distillation of Karpathy "Deep Dive into LLMs" (video vMhwv4nOJyg, Feb 2025) — with tweet-mislabel integrity finding |
| llms-from-scratch/SKILL.md | 1.0.0 | cangjie distillation — Raschka × Alammar/Grootendorst two-book bundle (23 capabilities, routing 34/34) |
| mediacrawler-cangjie/SKILL.md | 1.0.0 | session-built — crawl → distill pipeline runbook |
| skillevaluator-harness/SKILL.md | 1.0.0 | session-built — NVIDIA SkillEvaluator external-validation layer |
| venture-validation-machine/SKILL.md | 1.0.0 | composed umbrella — parallel-venture-validation × venture-machine × poteto-swarm-method |
| wechat-video-ingest/SKILL.md | 1.1.0 | session-built — WeChat Channels → OCR ingest |
| youtube-crawler/SKILL.md | 1.0.0 | session-built — YouTube transcript collector |
