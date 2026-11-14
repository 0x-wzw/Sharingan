---
stage: mirror
created: 2026-11-14
tags: [cangjie, sharingan, hermes, skills]
---

# Hermes-format distilled skills — Ubuntu VM mirror (v2.0.0 merge)

The Ubuntu VM's cangjie stack (2026-11-14 merge). Canonical knowledge lives in the
Obsidian vault (`Knowledge/40-Templates/cangjie/`); this directory is the distributable
mirror gathered into Sharingan at release v2.0.0.

- `skills/` — 14 distilled skills (Hermes format, <=60-char trigger-first descriptions)
- `cangjie-lightweight/SKILL.md` — the SHORT-FORM distillation path (tweets, clips, repos,
  papers -> one Hermes skill): fetch source, extract the method, author Hermes-format
  SKILL.md, install, mirror to vault + bundle releases. Routing rule: long-form
  (books/courses/podcasts) -> the RIA-TV++ pipeline (this repo's main skill);
  short-form -> this path.

| Skill | Version | Source |
|---|---|---|
| brutalist-ui-skill/SKILL.md | 1.0.0 | external repo |
| harness-eval-method/SKILL.md | 1.0.0 | garrytan/g-harness-evals repo @ edacaa8 + tweet 2121463161069228382, distilled 2026-11-13 |
| harness-starter-stack/SKILL.md | 1.0.0 | X post 2118759929947328571 (@Kiiiiira777, 2026-11-06): Dario Amodei clip + 14 free repos — all repos… |
| high-end-visual-design/SKILL.md | 1.0.0 | external repo |
| knowledge-base-builder/SKILL.md | 1.0.0 | session-built 2026-11-12 — FDE knowledge base build-on process, standalone cron spec |
| minimalist-ui-skill/SKILL.md | 1.0.0 | external repo |
| multi-agent-economy/SKILL.md | 1.2.0 | external repo |
| output-skill/SKILL.md | 1.0.0 | external repo |
| parallel-venture-validation/SKILL.md | 1.1.0 | X post 2119367655278723559 (@alvinfoo, 2026-11-08) — Paul Cheek (MIT Sloan) clip, transcript extract… |
| poteto-swarm-method/SKILL.md | 1.0.0 | Lauren Tan — 'SpaceX AI Engineer' talk (Sep 2026) + Pocock interview (Oct 2026) + poteto/noodle |
| skepsis-application-framework/SKILL.md | ? | external repo |
| taste-skill/SKILL.md | 2.0.0 | external repo |
| venture-machine/SKILL.md | 1.0.0 | session-built 2026-11-09 — venture machine operation (kanban funnel, driver, bots, triage, Sahati ex… |
| whatsapp-crew-bridge/SKILL.md | 1.0.0 | How Agents Use WhatsApp.md — operator brief, user-provided, distilled 2026-11-11 |
| cangjie-lightweight/SKILL.md | 1.0.0 | session-built pipeline skill (Oct-8 framework + 2026-11 policy sync) |

Policy: these files are mirrors; the vault stays canonical. No secrets — the 04:20
harness_sync-style fail-closed scans apply to any future mirror updates.
