<div align="center">

# 🔴 Sharingan

### Distill methodologies from books, lectures, podcasts, repos, and shipped artifacts into externally-validated, callable AI agent skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Release: v2.3.0](https://img.shields.io/badge/Release-v2.3.0-8b5cf6.svg)](./CHANGELOG.md)
[![Method: RIA--TV++](https://img.shields.io/badge/Method-RIA--TV++-2ea44f.svg)](./docs/RUNBOOK.md)
[![External Validation: NVIDIA SkillEvaluator](https://img.shields.io/badge/Tier--1--gated-NVIDIA%20SkillEvaluator-76b900.svg)](./harness/SKILL.md)
[![Artifact Evidence: REA](https://img.shields.io/badge/Evidence-REA%20v6.9.0-76b900.svg)](./harness/rea/SKILL.md)

**A harness, not a skill: point it at a book, lecture, podcast, repo, or application binary — it runs the RIA-TV++ pipeline and emits skills you can invoke, each grounded in evidence and gated by an independent quality score. The outputs live in your skill directories / vault; the harness lives here.**

</div>

---

## What is Sharingan?

Sharingan is a **content-to-skill pipeline**: feed it a book, a lecture transcript, a podcast, a repo's notebooks, or a shipped application, and it distills the *methodologies* inside into atomic, agent-invocable skills — each one verified against its source, pressure-tested, compiled deterministically, and gated by an external evaluator.

> Named after the Uchiha eye technique: it copies what it sees, understands the mechanics behind it, and reproduces it faithfully. Attribution included.

**Fork lineage:** Sharingan is a production-hardened fork of [kangarooking/cangjie-skill](https://github.com/kangarooking/cangjie-skill) (MIT), with an integrated external-validation harness and an artifact-evidence lane. The upstream RIA-TV++ version is tracked independently as `cangjie.version`; this fork's release is `sharingan.version`. See [NOTICE](./NOTICE) for upstream attribution and [scripts/LOCAL_DIFF.md](./scripts/LOCAL_DIFF.md) for the exact divergence record.

## What Sharingan adds over upstream

| Addition | What it does |
|---|---|
| **External validation gate** (`harness/SKILL.md`) | NVIDIA [SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator) Tier 1 runs on every compiled skill before install; SCHEMA/SECRET errors block unless dispositioned with evidence |
| **Artifact evidence** (`harness/rea/SKILL.md`) | [REA](https://github.com/morluto/rea) v6.9.0 supplies source- and binary-level evidence for Stage-1 claims and Stage-4 grounding. Evidence, not validation — never a substitute for triple verification or the Tier-1 score |
| **SKILL_SPEC-compliant frontmatter** | Compiler emits `version`, `license`, and `metadata.author` (`Name <email@host>`) natively — passes independent static quality checks by construction |
| **Audited compiler diffs** | Every vendor patch is recorded in `scripts/LOCAL_DIFF.md` so upstream re-syncs never silently regress |
| **Operational pitfalls library** | Verified-false-positive handling (gitleaks vs content hashes), environment-blocked scanners (`SKIPPED-ENV` ≠ FAIL), YAML block-scalar rules — learned from real distillation runs |
| **Layer discipline** (`docs/STACK.md`) | doctrine → harness → application → operator → craft, with one canonical source per layer and a Tier-1 gate before distribution |

## The pipeline (RIA-TV++ v2.5)

```
Stage 0    Adler whole-book understanding      → BOOK_OVERVIEW.md        (user confirms)
Stage 1    5 parallel extractors               → candidates/             (frameworks, principles, cases, counter-examples, glossary)
Stage 1.5  Triple verification (V1/V2/V3)      → verified.md             (source / executable / task-gain)
Stage 1.6  Promotion gate                      → promoted vs router      (≤7 discoverable entries)
Stage 2    RIA++ capability cards              → cards/*.md              (R/I/A1/A2/E/B)
Stage 3    Zettelkasten links + glossary       → cross-linked bundle
Stage 4    Pressure tests                      → honest pass/fail        (SKIPPED-ENV recorded, never faked)
Stage 5    Compile + external gate + install   → SKILL.md + references/  (SkillEvaluator Tier 1)
```

Every stage writes a checkpoint (`PIPELINE_STATE.md`) — interrupted runs resume instead of restarting. Audit trails (`candidates/`, `rejected/`) are never deleted.

## Where REA fits

REA is an **evidence provider**, not a second evaluator. It answers "how does this shipped artifact actually behave?" when no source is available.

| Stage | REA use | Evidence |
|---|---|---|
| Stage 0 / 1 | App, JS/Electron bundle, or binary as a source type | `analyze-*` JSON + artifact hash/version in `candidates/` |
| Stage 1.5 (V1) | Source-sufficiency check for implementation claims | REA finding IDs attached to each candidate |
| Stage 4 | Grounding: does the distilled behavior match the artifact? | Confirming or contradicting evidence; contradiction → Stage 2 |

Rules that are enforced, not aspirational:
- REA never produces a SkillEvaluator score. Only Tier 1 upgrades a skill to "externally validated".
- A missing native engine (Hopper/Ghidra/IDA/Kuna) is `SKIPPED-ENV`, never a pass.
- Static analysis proves a declaration exists, not that a runtime path executes — the report says which.
- REA's explicit Unknowns are preserved; they are never filled with plausible inference.

Requires Node 22.x ≥22.23.4, 24.x ≥24.22.1, or 26.12.1+, plus npm. See [`harness/rea/SKILL.md`](./harness/rea/SKILL.md) for setup, dry-run discipline, and operational pitfalls.

## Non-negotiable quality rules

1. Every capability passes all three verifications (V1 source sufficiency, V2 executability, V3 task gain)
2. Quotes ≤150 chars/paragraph (EN ≤100 words); no fabricated cases — synthetic drills are labeled as such
3. Internal Stage-4 pass ≠ external validation — only SkillEvaluator results may upgrade a skill's status
4. Human gates stay human: the overview confirmation and the final promotion decision are user-gated
5. "Trust the headline over the source" is a rejection trigger — the artifact is distilled, not the marketing around it

## Install

```bash
# The harness is runbook-driven: point a skill-aware agent at docs/RUNBOOK.md
# (Claude Code, Codex, OpenClaw, Hermes Agent), then:
#   "Run the Sharingan pipeline on <book/transcript/repo>"

# External validation (optional but recommended):
pip install skillevaluator          # NVIDIA SkillEvaluator v0.9+
skillevaluator quality-check ./my-distilled-skill -r cli   # Tier 1 gate

python3 harness/augment_frontmatter.py ./my-distilled-skill   # fallback author injector

# Artifact evidence (optional; needs supported Node):
npx -y rea-agents@latest doctor --format md
npx -y rea-agents@latest setup --client hermes --dry-run --format md   # review first
```

Requirements: Python 3.10+, PyYAML, jsonschema, tiktoken. Run `python3 scripts/cangjie.py doctor` to self-check.

## Distribution / sync

`docs/STACK.md` defines the layer map. In a Hermes fleet, `harness_sync.py` runs daily at 04:20 (job `79b7e3736cda`) and:

1. Pulls this repo first (remote authorship wins on conflict; local variants are archived).
2. Distributes `harness/*/SKILL.md` into the local skill tree **only after a clean Tier-1 gate** — a failing skill is skipped, never installed.
3. Mirrors the vault distill pack without clobbering files changed remotely.
4. Runs a fail-closed secret scan before any push.

Manual run: `python3 ~/.hermes/scripts/harness_sync.py`.

## Repository map

```
├── docs/RUNBOOK.md     # the RIA-TV++ runbook (Sharingan is a harness, not a skill)
├── docs/STACK.md       # layer map: doctrine → harness → application → operator → craft
├── methodology/        # per-stage methodology prompts (Stage 0 → 5)
├── extractors/         # 5 extractor prompts for Stage 1
├── templates/          # BOOK_OVERVIEW / DIGEST / SKILL / test-prompts templates
├── schemas/            # capability-bundle JSON schemas (compile source of truth)
├── scripts/            # deterministic toolchain: cangjie.py, compile_*, validate_skill_pack
│   └── LOCAL_DIFF.md   # audited divergence from upstream — re-apply before syncs
├── harness/
│   ├── SKILL.md        # NVIDIA SkillEvaluator — external quality gate
│   ├── rea/SKILL.md    # REA — artifact evidence for Stages 1 / 1.5 / 4
│   └── augment_frontmatter.py  # fallback author injector
├── registry/ docs/ tests/ benchmarks/ website/ assets/
```

## Honest limitations

- Tier 3 live "Skill Lift" evaluation requires an LLM provider key + Docker sandbox; keyless installs validate Tier 1 (static) only
- `skillspector` (security scanner) ships via NVIDIA's pinned runtime; without it, the security validator reports INCOMPLETE — recorded as environment-blocked, never as passing
- Compiled `BUILD_MANIFEST.json` content hashes trip gitleaks `generic-api-key` — a known false positive; verify the line is a hex digest and disposition with evidence
- Video/repo sources are often extraction-lossy (code cells without prose); units that only exist in a condensed layer are flagged `needs_review`, never compiled as active
- REA without a native engine cannot decompile machine code; static bundle/header analysis is not a substitute for runtime observation

## Attribution

- Upstream: [cangjie-skill v2.5.0](https://github.com/kangarooking/cangjie-skill) by kangarooking (MIT) — the RIA-TV++ methodology, extractors, and compiler are derived from it
- External validation: [NVIDIA SkillEvaluator v0.9.0](https://github.com/NVIDIA/SkillEvaluator) (Apache-2.0) — integrated, not bundled
- Artifact evidence: [REA v6.9.0](https://github.com/morluto/rea) (MIT, npm `rea-agents`) — integrated, not bundled
- Fork maintenance & operational hardening: 0x-wzw, 2026

## License

[MIT](./LICENSE) — same as upstream. See [NOTICE](./NOTICE) for third-party attribution.
