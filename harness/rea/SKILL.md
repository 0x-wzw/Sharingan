---
name: rea-harness
description: Use when Sharingan needs evidence from a compiled app, JS/Electron bundle, or native binary to ground a distilled capability — REA supplies source-level or binary-level evidence, never a substitute for triple verification.
version: 1.0.0
author: Hermes Agent
license: MIT
read_scope: profile
source: "composed 2026-11-19 from morluto/rea v6.9.0 (MIT) and the rea-agents npm package — integrated into the Sharingan harness as a Stage-1 source-analysis and Stage-4 evidence tool"
metadata:
  layer: harness
  stack-source: "repo:0x-wzw/Sharingan"
  tags: [harness, reverse-engineering, evidence, stage-1, stage-4, rea, mcp]
  related_skills: [skillevaluator-harness, mediacrawler-cangjie, cangjie-skill]
  author: 'Hermes Agent <agent@hermes.local>'
---

# REA Harness — binary and application evidence for Sharingan

## Instructions

1. Check `node --version` against REA's supported Node ranges before any setup.
2. Run `rea setup --dry-run` and review the plan before applying registration changes.
3. Use `analyze-*` CLI commands for scripted evidence; reserve MCP tools for investigation.
4. Attach REA evidence IDs to Stage-1/1.5 candidates; record artifact hash and version.
5. Record `SKIPPED-ENV` when a native engine is absent — never pass a capability on static-only evidence.
6. Leave the Tier-1 SkillEvaluator score as the sole external validation signal.

## When to Use

Use when a Sharingan source is a shipped application, JS/Electron bundle, or binary and a capability claim needs artifact-level evidence. Do not use for ordinary book/transcript distillation.

## Position in the stack

REA (Reverse Engineer Anything) is an **evidence provider** in the harness layer, not a distillation method. It answers questions about *how a shipped artifact actually behaves* when no source is available. It does not replace cangjie's triple verification, and its output is never treated as an independent quality score — that remains SkillEvaluator's role.

| Cangjie stage | REA role | Output |
|---|---|---|
| Stage 0 / 1 | New source type: app, bundle, or binary instead of text | Verified capability claims with artifact evidence |
| Stage 1.5 (V1) | Source-sufficiency check for a claim about implementation | Evidence records attached to the candidate |
| Stage 4 | Pressure-test grounding: does the distilled behavior match the artifact? | Confirming or contradicting evidence |

Rule: **REA evidence is ground truth about an artifact, not validation of a skill.** A capability still needs V2 executability, V3 task gain, and the Tier-1 external gate before it ships.

## What it can and cannot inspect

Requires Node 22.x (>=22.23.4), 24.x (>=24.22.1), or 26.12.1+, plus npm.

Works without any native analysis engine:
- Desktop installation layout and component markers
- Static JavaScript / Electron applications (modules, imports, boundaries)
- Web bundles and captured browser scenarios
- Go binaries, Rust binaries, GPU code objects, GGUF/safetensors headers,
  IL2CPP metadata, Godot PCK, PE certificates/imports, ELF notes, DWARF units

Needs a caller-supplied engine (REA does not install these):
- Native binary pseudocode/decompilation — Hopper, Ghidra, IDA or Kuna
- Android APK resource decoding — apktool
- Managed .NET assemblies — JADX MCP

If a required engine is absent, record `SKIPPED-ENV` with the exact missing prerequisite. Never paraphrase static layering as native decompilation.

## Commands

```bash
# Health check
npx -y rea-agents@latest doctor --format md

# Register with an agent (review changes; MCP entry + skill copy)
npx -y rea-agents@latest setup --client hermes --dry-run --format md
npx -y rea-agents@latest setup --client hermes --yes

# CLI analysis, no engine needed
npx -y rea-agents@latest analyze-javascript-application /absolute/app/path --json
npx -y rea-agents@latest analyze-web-bundle --json

# Hermes
hermes mcp test rea                       # connection + tool count
hermes mcp list                           # registration present
```

## Pipeline integration

1. **Stage 1** — when the source is an artifact, run the relevant `analyze-*` command first. Save its JSON under `books/<slug>/candidates/` with a source manifest naming the exact artifact and its hash.
2. **Stage 1.5 V1** — attach specific REA evidence records to each implementation claim. A marketing headline or README assertion is not evidence; a REA finding with a code reference is.
3. **Stage 4** — for any capability whose A2 claims a concrete implementation behavior, re-check that behavior against the artifact. A contradiction sends the card back to Stage 2; an engine gap is `SKIPPED-ENV`, not a pass.
4. **Stage 5** — list REA evidence IDs in the run report. Tier-1 SkillEvaluator remains the only external validation score.

## Interpretation rules

- REA reports **Unknowns** explicitly. Preserve them; do not fill them with plausible inference.
- Evidence is scoped to one artifact at one point in time. Record version/hash — a later release can invalidate the claim.
- Static analysis of a bundle can prove a declaration exists, not that a runtime path executes. Say which.
- Never claim Tier 3 Skill Lift from REA findings. Different instrument, different question.

## Operational pitfalls

- **Node version gate** — REA refuses Node below its supported patch releases. Check `node --version` before setup; upgrading via NodeSource may need `apt-get update` first because stale package lists hide the newer build.
- **Setup writes config** — `rea setup` registers an MCP server and installs a skill copy. Run `--dry-run` first; a config backup is created. Do not run with `--all-detected` on a shared machine.
- **npx cache dependency** — a setup that records the npx cache path stays valid only while that cache entry exists. For a durable install use `npm install --global rea-agents` and re-run setup.
- **255 MCP tools** — tool discovery is large. Prefer CLI commands for scripted work; reserve MCP tools for agent-driven investigation.

## Provenance

- Upstream: https://github.com/morluto/rea (MIT), npm `rea-agents`, release v6.9.0
- Integration: 0x-wzw/Sharingan harness layer, 2026-11-19
- Companion: `harness/SKILL.md` (SkillEvaluator — external quality gate)
