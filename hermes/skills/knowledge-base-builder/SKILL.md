---
name: knowledge-base-builder
approval_source: agent
description: Use when building on a vault KB from raw daily captures.
version: 1.0.0
author: Hermes Agent
license: MIT
read_scope: profile
source: "session-built 2026-11-12 — FDE knowledge base build-on process, standalone cron spec"
metadata:
  hermes:
    tags: [knowledge-base, vault, radar, synthesis, cron, notion]
    related_skills: [rss-feeds, venture-machine, knowledge-base-builder]
---

# Knowledge-base builder — turn daily radar captures into KB updates

## When to Use

- A knowledge-base cycle has a daily radar (raw captures) and a combined KB report in the vault,
  and a new update must be synthesized on schedule (standalone cron) or on demand.
- First instantiated on the FDE cycle (00-Raw/FDE → 20-Reports FDE-knowledge-base-*).

## Inputs (per cycle)

- **KB file**: `Knowledge/20-Reports/<kb>-combined-<date>.md` — the living report; updates are
  APPENDED as new dated Parts in the same file when it is the cycle's canonical file, or as a
  supersede `<kb>-update-<date>.md` when the file is declared frozen. Never overwrite prior parts.
- **Raw dir**: `Knowledge/00-Raw/<cycle>/` — daily watch files (`*-watch-YYYY-MM-DD.md`), items
  are lines `- **[LANG]** Title - Source` + news.google.com redirect URLs.
- **Marker**: `~/.hermes/cron/output/<cycle>-kb/.last_covered` — last raw date already covered
  by the KB. Initialize from the KB's newest Part header before first run.

## Procedure

1. **Collect** — run the cycle's collector script (`~/.hermes/scripts/kb_build_<cycle>.py`):
   parses watch files newer than the marker, dedupes by normalized title, tracks first-seen
   date + occurrence count, emits draft JSON+md to `~/.hermes/cron/output/<cycle>-kb/`.
2. **Synthesize at title level unless verified.** Unvisited redirect links carry ZERO claims
   beyond their title. Never invent article bodies. A theme needs ≥2 distinct sources or one
   primary source to become a finding.
3. **Update the claim-status table** — for each prior KB claim: Superseded / Extended /
   Corroborated / Unchanged, with the evidence source. This table is the KB's state machine.
4. **Write the update** (vault discipline: liveness check, supersede-as-dated, link back with
   wiki-links to the combined KB), push to WeKnora, update the Notion page (search for the
   cycle's page first; append children, never recreate), append the MOC link in Knowledge MOC.
5. **Advance the marker** only after the vault write is verified.

## Standing rules

- Open questions live in the KB (Part "Watchlist & open questions"); a new recurring signal
  graduates a question or closes one — say which.
- Skeptical/countering sources (e.g. "FDE is high-end outsourcing" debates) are first-class:
  a KB that only accumulates confirmation is a brochure, not a knowledge base.
- Repetition across days is signal, not noise: count occurrences, report first-seen + spread.
- Delivered summary in chat: themes, claim-status deltas, file paths, next scheduled run.
