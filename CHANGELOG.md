# Changelog — Sharingan

## v2.1.0 — 2026-11-14
- **Removed** 5 design/branding mirror skills (brutalist-ui, high-end-visual-design,
  minimalist-ui, taste, output) — external-repo artifacts, not part of Sharingan's
  methodology-distillation focus
- **Added** 17 Tier-1-hardened skills from the local cangjie profile fleet audit:
  the two-book LLM bundle (llms-from-scratch, 23 capabilities), karpathy-llm-usage,
  skillevaluator-harness, media crawlers (mediacrawler-cangjie, youtube-crawler,
  wechat-video-ingest), the FDE funnel (10 skills + router), aidev26-agent-engineering,
  and the venture-validation-machine umbrella
- INDEX.md updated: 26 mirrored skills with per-skill provenance and audit status

---

## v2.0.0 — 2026-11-14
Merge of the Ubuntu VM cangjie stack (0x-wzw lineage) into the Sharingan pipeline:
- `hermes/`: 14 distilled skills (provenance in `hermes/INDEX.md`) + `cangjie-lightweight`
  short-form path; routing rule added to SKILL.md (long-form -> RIA-TV++, short-form -> lightweight)
- `scripts/vault_mirror.py`: vault-mirror + bundle-release sync reference
- NOTICE: second lineage attribution (0x-wzw/cangjie-skill policy build, 2026-11-07 code+releases-only policy)


## v1.0.0 — 2026-11-14
First public release. Fork of cangjie-skill v2.5.0 (MIT) with an integrated
external-validation harness.

### Added (vs upstream)
- `harness/`: NVIDIA SkillEvaluator integration — Tier 1 quality gate becomes a
  mandatory pre-install step; disposition protocol for SKIPPED-ENV and verified
  false positives
- `harness/augment_frontmatter.py`: idempotent author/version frontmatter injector
  (fallback for pre-patch compilations)
- Compiler emits SKILL_SPEC-compliant frontmatter (`version`, `license`,
  `metadata.author` in `Name <email@host>` form) natively in
  `compile_single.py` / `compile_pack.py`
- `scripts/LOCAL_DIFF.md`: audited vendor-divergence record for upstream re-syncs
- Operational pitfalls library from live distillation runs (2026-11-08/14):
  two full books (Raschka × Alammar/Grootendorst, 97 verified units → 6 promoted +
  17 router cards, routing 34/34) and one video lecture

### Changed
- Rebranded to Sharingan; upstream attribution retained in NOTICE and LICENSE

### Removed (vs upstream tree)
- Sample distillation outputs (books/, dist/) — keep the toolchain, not the data
