---
name: skillevaluator-harness
description: Use when validating distilled agent skills with NVIDIA SkillEvaluator — Tier 1 static quality gates, Tier 2 eval-dataset generation, Tier 3 live Skill Lift. External validation layer of the Cangjie skill stack.
version: 1.0.0
author: Hermes Agent
license: MIT
read_scope: profile
source: "composed 2026-11-14 from NVIDIA/SkillEvaluator v0.9.0 (Apache-2.0) — integrated into the cangjie-skill RIA-TV++ pipeline as the external Stage-4/5 validator"
metadata:
  layer: harness
  stack-source: repo:0x-wzw/Sharingan
  tags: [skillevaluator-harness]
  author: "Cangjie Distillation <agent@example.com>"
  hermes:
    tags: [skills, evaluation, validation, skillevaluator, nvidia, cangjie, quality-gates]
    related_skills: [mediacrawler-cangjie, karpathy-llm-usage, llms-from-scratch, poteto-swarm-method]
---

# SkillEvaluator Harness — external validation for distilled skills

## Position in the Cangjie stack

The cangjie-skill pipeline (RIA-TV++) produces skills whose Stage-4 pressure tests are
internal (paper walkthroughs, mechanical assertions, lexical routing harness). NVIDIA
SkillEvaluator adds the **independent external validator** the pipeline itself flags as
outstanding: deterministic quality gates, generated eval datasets, and live with/without-skill
"Skill Lift" measurement.

Mapping:

| Cangjie stage | SkillEvaluator tier | What it adds |
|---|---|---|
| Stage 5 compile (`validate_skill_pack.py`) | **Tier 1** `quality-check` | Independent static scoring /100 (pass ≥70), security scan (pinned SkillSpector), frontmatter/structure checks, semantic overlap between skills |
| Stage 1.5 candidates | **Tier 2** eval-dataset generation | Machine-generated eval cases from the skill's intents/outcomes |
| Stage 4 pressure tests | **Tier 3** live evaluation | Real agent runs with vs without the skill → **Skill Lift** (fixes the "self-judged trigger test" caveat) |

Rule: **internal Stage-4 pass ≠ external validation**. A skill ships as "internal-validated";
only SkillEvaluator results may upgrade it to "externally validated". Never claim Tier 3
Lift without an actual no-skill baseline run.

## Commands (venv: `~/.hermes/profiles/kakashi/venv/bin/`)

```bash
# Tier 1 — deterministic, no API key (always run this first)
skillevaluator quality-check <skill-dir> -r cli -r json -o <out-dir>
# exit 0 + score ≥70 = pass; publication evidence stays INCOMPLETE (expected)

# Tier 1 — structure-only validation
skillevaluator validate <skill-dir> --tiers 1

# Tier 2/3 — need an LLM provider key (NV Build / OpenAI / etc.)
export SKILL_EVAL_LLM_PROVIDER=nv_build   # or openai/anthropic
export NVIDIA_API_KEY='nvapi-...'
skillevaluator rubric-eval <skill-dir> ...
skillevaluator create-eval-dataset <skill-dir> ...   # Tier 2
skillevaluator tier3 evaluate ...                    # Skill Lift (Harbor/NeMo Gym, Docker)
```

CI mode (skill repos): `skillevaluator ci init` opens a setup PR that gates changed skills per PR.
Agent mode: `npx skills add NVIDIA/SkillEvaluator` then ask "is my skill any good?".

## Pipeline integration (what changed)

1. **Stage 5 deliver** — after `compile` and `validate_skill_pack.py`, run Tier 1
   `quality-check` on the compiled output dir. Record the score + findings in the run
   report (`runs/`). A score <70 blocks installation until fixed.
2. **Stage 4 pressure tests** — after internal tests pass, Tier 3 is the *optional* upgrade
   path for high-stakes skills (requires API key + Docker). Tier 2 datasets are the cheap
   intermediate: generate once per promoted skill, store under
   `books/<slug>/.cangjie/capabilities/resources/eval-datasets/`.
3. **Router reachability** — our lexical 34/34 harness remains the fast check; Tier 3
   skill_execution signals are the ground truth when the budget allows.
4. **Semantic overlap** — run Tier 1 across the *whole* promoted set before shipping a
   multi-skill bundle; overlapping skills = promotion-gate criterion violated.

## Interpretation rules

- Quality Score is **static**: it cannot see whether the skill's methodology is any good —
  only cangjie's triple verification can attest that. Report both, never conflate.
- Skill Lift ≤0 on a promoted skill = back to Stage 2 (the card claims don't transfer).
- Datasets must assert **outcomes only** — grading skill use inflates lift against the
  no-skill baseline (upstream issue #456; tier3 validate warns, fails only --strict).
- Tier 3 requires Docker + sandbox; on the Mac (no torch/Docker-heavy flows), record
  `SKIPPED-ENV` like any other environment-blocked test.

## Learned-in-operation pitfalls (2026-11-14, first run on llms-from-scratch)

- **~~Compiled SKILL.md lacks `metadata.author`~~ FIXED at source** — compiler patched
  (see `Projects/sharingan/scripts/LOCAL_DIFF.md`) to emit `version`, `license`,
  `metadata.author` (`Name <email@host>` form) natively from bundle `book.author`.
  `augment_frontmatter.py` kept only as fallback for pre-patch compiles.
- **BUILD_MANIFEST.json content hashes trip gitleaks `generic-api-key`** — expected on
  every compiled bundle (SHA-256 digests of capability files). Verify the line is a hex
  digest, then record as ACCEPTED-FP with line-level evidence. `.gitleaksignore` cannot
  suppress it (fingerprint embeds the matched string and self-redacts).
- **skillspector is environment-gated** — it runs via `uv tool run` and has no public
  package; Security Scan stays INCOMPLETE without it. Record SKIPPED-ENV; INCOMPLETE ≠ FAIL.
- LLM-backed checks need `SKILL_EVAL_LLM_PROVIDER` + key; keyless runs cover the 10
  static validators only.
- **verified.yaml must use YAML block scalars** (`description: |`) — plain multi-line
  scalars containing colons are refused by the parser.

## Provenance

- Repo: https://github.com/NVIDIA/SkillEvaluator (v0.9.0, Apache-2.0, PyPI `skillevaluator`)
- Paper: arxiv.org/abs/2608.20614 · Docs: docs.nvidia.com/skills/skillevaluator
- Installed into the cangjie profile venv (`pip install skillevaluator`)

## Purpose

External validation layer of the cangjie skill stack. NVIDIA SkillEvaluator adds the independent external validator the RIA-TV++ pipeline itself flags as outstanding: deterministic Tier-1 quality gates, generated Tier-2 eval datasets, and live with/without-skill Tier-3 Skill Lift measurement. Internal Stage-4 pass ≠ external validation — only SkillEvaluator results may upgrade a skill to "externally validated".

## Prerequisites

- `skillevaluator` installed in `~/.hermes/profiles/kakashi/venv/bin/` (`pip install skillevaluator`, PyPI package)
- Tier 1 `quality-check` is deterministic and needs no API key — always run this first
- Tier 2/3 need an LLM provider key (`SKILL_EVAL_LLM_PROVIDER` + `NVIDIA_API_KEY` or OpenAI/anthropic); keyless runs cover the 10 static validators only
- Tier 3 Skill Lift requires Docker + sandbox (Harbor/NeMo Gym); on this Mac record `SKIPPED-ENV` instead
- skillspector runs via `uv tool run` and has no public package — without it the Security Scan stays INCOMPLETE

## Instructions

1. Run Tier 1 first: `skillevaluator quality-check <skill-dir> -r cli -r json -o <out-dir>` — exit 0 + score ≥70 = pass; publication evidence stays INCOMPLETE (expected).
2. After Stage 5 `compile` and `validate_skill_pack.py`, record the Tier-1 score + findings in the run report (`runs/`); a score <70 blocks installation until fixed.
3. For promoted skills, generate a Tier-2 eval dataset once (`create-eval-dataset`) and store it under `books/<slug>/.cangjie/capabilities/resources/eval-datasets/`.
4. For high-stakes skills, Tier 3 is the *optional* upgrade path (requires API key + Docker); never claim Skill Lift without an actual no-skill baseline run.
5. Before shipping a multi-skill bundle, run Tier 1 across the whole promoted set — overlapping skills violate the promotion gate.
6. Report the static Quality Score and cangjie's triple verification separately; never conflate them.
   Full command reference: `## Commands`; integration detail: `## Pipeline integration`.

## Examples

1. Tier 1 gate on a compiled bundle: `skillevaluator quality-check <skill-dir> -r cli -r json -o <out-dir>` → score ≥70 with publication evidence INCOMPLETE and a gitleaks `generic-api-key` ACCEPTED-FP for BUILD_MANIFEST.json → pass, install.
2. Cheap intermediate for a promoted skill: `export SKILL_EVAL_LLM_PROVIDER=nv_build; export NVIDIA_API_KEY=...` then `skillevaluator create-eval-dataset <skill-dir>` → dataset asserting outcomes only, stored in `resources/eval-datasets/`.
3. Multi-skill bundle ship: Tier 1 run across the whole promoted set flags semantic overlap between two skills → promotion-gate criterion violated, resolve before shipping.

## Limitations

- Tier 2/3 require an LLM provider key; Tier 3 additionally requires Docker + sandbox and does not run on this Mac (record `SKIPPED-ENV`).
- skillspector is environment-gated (`uv tool run`, no public package) — Security Scan stays INCOMPLETE without it; INCOMPLETE ≠ FAIL.
- The Quality Score is static: it cannot see whether the skill's methodology is any good — only cangjie's triple verification attests that.
- Skill Lift ≤0 on a promoted skill means the card claims don't transfer — back to Stage 2; datasets must assert outcomes only (grading skill use inflates lift, upstream issue #456).
- BUILD_MANIFEST.json hashes are an accepted gitleaks false positive that `.gitleaksignore` cannot suppress (fingerprint embeds the matched string and self-redacts).

## Troubleshooting

- **Compiled SKILL.md lacks `metadata.author`** → FIXED at source: the compiler now emits `version`, `license`, `metadata.author` natively from bundle `book.author`; `augment_frontmatter.py` remains as fallback for pre-patch compiles (see `Projects/sharingan/scripts/LOCAL_DIFF.md`).
- **gitleaks flags `generic-api-key` on BUILD_MANIFEST.json** → expected on every compiled bundle (SHA-256 digests of capability files); verify the line is a hex digest and record ACCEPTED-FP with line-level evidence — `.gitleaksignore` cannot suppress it.
- **Security Scan INCOMPLETE** → skillspector is environment-gated; record SKIPPED-ENV. INCOMPLETE ≠ FAIL.
- **LLM-backed checks unavailable / Tier 2-3 refused** → set `SKILL_EVAL_LLM_PROVIDER` + provider key; keyless runs cover only the 10 static validators.
- **verified.yaml multi-line scalar refused by parser** → use YAML block scalars (`description: |`); plain multi-line scalars containing colons are rejected.
- **Skill Lift ≤0** → card claims don't transfer; return the skill to Stage 2 of the cangjie pipeline.
