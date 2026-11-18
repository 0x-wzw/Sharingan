<div align="center">

# 🔴 Sharingan

### Distill methodologies from books, lectures, podcasts, and repos into externally-validated, callable AI agent skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Release: v1.0.0](https://img.shields.io/badge/Release-v1.0.0-8b5cf6.svg)](./CHANGELOG.md)
[![Method: RIA--TV++](https://img.shields.io/badge/Method-RIA--TV++-2ea44f.svg)](./docs/RUNBOOK.md)
[![External Validation: NVIDIA SkillEvaluator](https://img.shields.io/badge/Tier--1--gated-NVIDIA%20SkillEvaluator-76b900.svg)](./harness/SKILL.md)

**A harness, not a skill: point it at a book, lecture, or podcast — it runs the RIA-TV++ pipeline and emits skills you can invoke, each gated by an independent quality score. The outputs live in your skill directories / vault; the harness lives here.**

</div>

---

## What is Sharingan?

Sharingan is a **content-to-skill pipeline**: feed it a book, a lecture transcript, a podcast, or a repo's notebooks, and it distills the *methodologies* inside into atomic, agent-invocable skills — each one verified against its source, pressure-tested, compiled deterministically, and gated by an external evaluator.

> Named after the Uchiha eye technique: it copies what it sees, understands the mechanics behind it, and reproduces it faithfully. Attribution included.

**Fork lineage:** Sharingan is a production-hardened fork of [kangarooking/cangjie-skill](https://github.com/kangarooking/cangjie-skill) (MIT) with an integrated external-validation harness. See [NOTICE](./NOTICE) for upstream attribution and [scripts/LOCAL_DIFF.md](./scripts/LOCAL_DIFF.md) for the exact divergence record.

## What Sharingan adds over upstream

| Addition | What it does |
|---|---|
| **External validation gate** (`harness/`) | NVIDIA [SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator) Tier 1 runs on every compiled skill before install; SCHEMA/SECRET errors block unless dispositioned with evidence |
| **Artifact evidence** (`harness/rea/`) | [REA](https://github.com/morluto/rea) supplies source/binary-level evidence for Stage-1 claims and Stage-4 grounding; never a substitute for triple verification or the Tier-1 score |
| **SKILL_SPEC-compliant frontmatter** | Compiler emits `version`, `license`, and `metadata.author` (`Name <email@host>`) natively — passes independent static quality checks by construction |
| **Audited compiler diffs** | Every vendor patch is recorded in `scripts/LOCAL_DIFF.md` so upstream re-syncs never silently regress |
| **Operational pitfalls library** | Verified-false-positive handling (gitleaks vs content hashes), environment-blocked scanners (`SKIPPED-ENV` ≠ FAIL), YAML block-scalar rules — learned from real distillation runs |

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
```

Requirements: Python 3.10+, PyYAML, jsonschema, tiktoken. Run `python3 scripts/cangjie.py doctor` to self-check.

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
├── harness/            # NVIDIA SkillEvaluator integration + fallback augment script
├── registry/ docs/ tests/ benchmarks/ website/ assets/
```

## Honest limitations

- Tier 3 live "Skill Lift" evaluation requires an LLM provider key + Docker sandbox; keyless installs validate Tier 1 (static) only
- `skillspector` (security scanner) ships via NVIDIA's pinned runtime; without it, the security validator reports INCOMPLETE — recorded as environment-blocked, never as passing
- Compiled `BUILD_MANIFEST.json` content hashes trip gitleaks `generic-api-key` — a known false positive; verify the line is a hex digest and disposition with evidence
- Video/repo sources are often extraction-lossy (code cells without prose); units that only exist in a condensed layer are flagged `needs_review`, never compiled as active

## Attribution

- Upstream: [cangjie-skill v2.5.0](https://github.com/kangarooking/cangjie-skill) by kangarooking (MIT) — the RIA-TV++ methodology, extractors, and compiler are derived from it
- External validation: [NVIDIA SkillEvaluator v0.9.0](https://github.com/NVIDIA/SkillEvaluator) (Apache-2.0) — integrated, not bundled
- Fork maintenance & operational hardening: 0x-wzw, 2026

## License

[MIT](./LICENSE) — same as upstream. See [NOTICE](./NOTICE) for third-party attribution.
