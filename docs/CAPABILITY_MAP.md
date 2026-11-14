# Sharingan ↔ cangjie-skill capability map

Upstream: [kangarooking/cangjie-skill](https://github.com/kangarooking/cangjie-skill) v2.5.0 (MIT, 2026-10-02) — the fork base.
This map is the audited 1:1 / modified / added / removed inventory as of Sharingan v2.1.2.

## Inherited unchanged (upstream ≡ Sharingan)

| Capability | Path (both) | Role |
|---|---|---|
| RIA-TV++ methodology (Stage 0→5) | `methodology/00–07` | Adler overview → parallel extract → triple-verify → promotion gate → RIA++ cards → Zettelkasten → pressure tests → deliver |
| 5 parallel extractors | `extractors/{framework,principle,case,counter-example,glossary}-extractor.md` | Stage 1 fan-out prompts |
| Deterministic toolchain | `scripts/cangjie.py`, `cangjie_common.py`, `compile_single.py`, `compile_pack.py`, `count_tokens.py`, `validate_skill_pack.py` | compile → single/pack, atomic publish, three-strike read-only rule |
| Round-trip flows | `scripts/apply_skill_patch.py`, `repair_flow.py`, `update_flow.py`, `diff_sources.py`, `impact_analysis.py` | patch/update/repair skills from re-reads |
| Evals | `scripts/run_output_evals.py`, `run_trigger_evals.py`, `benchmark.py`, `select_output_strategy.py`, `build_chunks.py`, `build_index.py` | output/trigger eval harness, benchmarks |
| Schemas | `schemas/capability{,-bundle}.schema.json`, `change-set`, `dependency-graph`, `eval-suite`, `failure-case`, `output-decision`, `registry-entry-v1`, `contracts/` | compile source of truth |
| Templates | `templates/` | BOOK_OVERVIEW / DIGEST / SKILL / test-prompts |
| Community registry | `registry/` (22 distilled skills) | published examples, mirrored as-is |
| Tests | `tests/test_{compile_resources,output_evals,quality_contracts}.py` | toolchain self-tests |
| Benchmarks | `benchmarks/naval/` | phase-0/1 routing + metrics evidence |

## Modified (divergence audited in `scripts/LOCAL_DIFF.md`)

| Capability | Change | Why |
|---|---|---|
| `compile_single.py` / `compile_pack.py` frontmatter emission | emit `version`, `license: MIT`, `metadata.author` (`Name <email@host>`, PII-safe placeholder) | NVIDIA SkillEvaluator Tier-1 SCHEMA/PII compliance by construction |
| SKILL.md packaging | **removed** — `SKILL.md` → `docs/RUNBOOK.md`, plain runbook, no skill frontmatter | Sharingan is a harness, not a skill (v2.1.2) |

## Added (Sharingan-only)

| Capability | Path | Role |
|---|---|---|
| External-validation harness | `harness/SKILL.md`, `harness/augment_frontmatter.py` | NVIDIA SkillEvaluator Tier-1 gate as mandatory pre-install step; disposition protocol (SKIPPED-ENV / ACCEPTED-FP with evidence); fallback author injector |
| Audited vendor divergence | `scripts/LOCAL_DIFF.md` | every local patch recorded; re-apply before upstream syncs (regression lesson) |
| Vault-mirror reference | `scripts/vault_mirror.py` | vault-canonical outputs ↔ repo mirror sync reference |
| Hermes-format skill mirror | `hermes/` (INDEX + 14 skills + cangjie-lightweight) | distributable mirror of operator/process skills; policy: **outputs stay canonical in the vault**, mirror carries process & infrastructure only |
| Short-form distillation path | `hermes/cangjie-lightweight/` | tweets/clips/papers → single Hermes skill (v1.1.0), with long-form/short-form routing rule |

## Removed (upstream had, Sharingan does not)

| Capability | Upstream path | Reason |
|---|---|---|
| Skill packaging of the toolchain itself | `SKILL.md` (name/description frontmatter) | harness ≠ skill (v2.1.2) |
| Sample distillation outputs | `books/naval-almanack-skill/`, `dist/` | toolchain ships, data doesn't |
| Promo/social assets | `assets/` QR codes, star-history, promo video refs, `generate_star_history.py` usage | community-growth artifacts, not harness capability (files partially retained, unused) |
| Upstream CI workflows | `.github/workflows/` (pages deploy, registry check, star-history) | Sharingan validates via SkillEvaluator CLI + local runs instead |

## Interface between the two

- Sharingan consumes upstream **releases** (toolchain), re-applies `scripts/LOCAL_DIFF.md`, and re-validates with SkillEvaluator Tier 1 before treating a sync as good.
- Upstream `registry/` entries are mirror-only — new distillations go to the vault / profile skills, not the registry.
- Compiler output contract upstream = valid cangjie bundle; Sharingan adds = SKILL_SPEC-compliant frontmatter + external Tier-1 gate.
