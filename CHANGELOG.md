# Changelog — Sharingan

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
