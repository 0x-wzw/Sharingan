# Local vendor diffs — re-apply before syncing cangjie-skill upstream
(lesson: "the engine regresses upstream" — venture-machine)

## 2026-11-14 — compile frontmatter: SKILL_SPEC compliance for NVIDIA SkillEvaluator Tier 1
- compile_single.py build_entry_md fm_lines: emit `version`, `license: MIT`, `metadata.author`
  ("Cangjie Distillation <agent@example.com>" + `# source:` comment from bundle book.author).
- compile_pack.py capability card fm_lines: same three fields.
- Reason: SkillEvaluator SCHEMA-HIGH errors without metadata.author; QUALITY-MEDIUM without version.
# Local vendor diffs — re-apply before syncing cangjie-skill upstream
(lesson: "the engine regresses upstream" — venture-machine)

## 2026-11-14 — compile frontmatter: SKILL_SPEC compliance for NVIDIA SkillEvaluator Tier 1
- compile_single.py build_entry_md fm_lines: emit `version`, `license: MIT`, `metadata.author`
  ("Cangjie Distillation <agent@example.com>" + `# source:` comment from bundle book.author).
- compile_pack.py capability card fm_lines: same three fields.
- Reason: SkillEvaluator SCHEMA-HIGH errors without metadata.author; QUALITY-MEDIUM without version.

## 2026-11-14 — v2.0.0 merge: Ubuntu cangjie stack (0x-wzw lineage)

- Added `hermes/` — 14 distilled skills + `cangjie-lightweight/SKILL.md` + `INDEX.md`
  (mirror of the Ubuntu VM vault pack; vault stays canonical). Additive except:
  SKILL.md routing section (marker: `Routing: long-form vs short-form (v2.0.0)`),
  CHANGELOG, NOTICE.
- Added `scripts/vault_mirror.py` — reference pointer to the VM mirror-sync
  (`0x-wzw/hermes-harness` scripts/cangjie_skill_sync.py; cron 04:10 on the VM).

## 2026-11-14 (fleet audit) — author email must be a PII-safe placeholder
- SkillEvaluator's PII validator flags real-looking emails ([PII-HIGH] Non-placeholder email address).
- Author email convention: `agent@example.com` everywhere (compiler output, harness docs, augment script).

## 2026-11-14 (upstream sync v2.5.0..main, 7 commits) — LOCAL_DIFF re-applied
- Synced 30 files from upstream main (also_read dual-contract fix #32, lazy PyYAML #31,
  DeepSeek Harness bundle, toolbook validation refresh, methodology/docs refresh).
- LOCAL_DIFF frontmatter patch re-applied to compile_single.py + compile_pack.py
  (upstream overwrote them; hunks don't conflict). Verified: 26/26 tests pass,
  test compile emits SKILL_SPEC frontmatter, Tier 1 runs clean.

## 2026-11-21 — YAML safety for book titles containing a colon
- `scripts/compile_pack.py`: emit `cangjie.source-title` via `json.dumps(..., ensure_ascii=False)`
  (quoted YAML scalar). Unquoted titles with `: ` (e.g. "WeMM-Video: Pushing the Frontiers…")
  made compiled promoted SKILL.md frontmatter unparseable and tripped the staging hard-gate.
- Local vendor patch; re-apply after any upstream compiler sync.

