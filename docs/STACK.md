# Sharingan stack map — layer discipline (v2.2.2)

Tetherline governs autonomy. Sharingan is the distillation harness. Application layers
run under doctrine. Outputs stay canonical in the vault. Every local skill is tagged
`metadata.layer` accordingly; `metadata.stack-source` names the canonical repo/vault
where a layer's content lives.

## The layers

| Layer | Count | Skills | Governing law |
|---|---|---|---|
| **doctrine** | 6 | tetherline-doctrine, tetherline-protocol, trust-ladder, verification-skill-builder, swarm-org-design, sample-and-garden | Canonical: repo `0x-wzw/tetherline`. No swarm/autonomy decision without these. |
| **harness** | 8 | mediacrawler-cangjie, skillevaluator-harness, rea-harness, youtube-crawler, wechat-video-ingest, venture-validation-machine, mermaid-fleet-map, (+ Sharingan itself) | Canonical: repo `0x-wzw/Sharingan`. Deterministic toolchains; Tier-1 gated. |
| **application** | 6 | venture-machine, parallel-venture-validation, intelligence-weekly-synthesis, self-evolution, handoff-authoring, handoff_backup | Run UNDER doctrine: any agent fan-out needs a trust-tier + verification suite first. |
| **operator** | 12 | obsidian-vault, vault-search, hermes-rag-ops, find-skills, prompt-optimizer, kanban-swarm, note-taking, research/internet-research, skepsis, strategy-architect, … | Single-owner runbooks; human gates stay human. |
| **craft** | 100 | design/dev/media/lark/cloudflare suites + fde funnel + distilled bundles | Domain outputs; where vault-canonical (llms-from-scratch, karpathy-llm-usage, fde-*), `stack-source: vault`. |

Distribution is over both local profiles (default + cangjie), 187 SKILL.md files, all
YAML-valid as of 2026-11-14.

## Cross-layer rules

1. **Doctrine before spawn** — any application-layer skill that fans out agents
   (parallel builds, swarm work) must name its trust tier and verification suite
   (laws 1–3). `verification-skill-builder` runs before any new swarm.
2. **Harness before scale** — scaling past the current ceiling requires a harness
   capability (SkillEvaluator Tier-1 or equivalent), not a bigger prompt (law 2).
3. **Canonical-source rule** — a skill tagged `stack-source: vault` is never mirrored
   into Sharingan; `repo:` skills sync from their repo (tetherline-sync,
   sharingan-sync crons, 12h change-detectors).
4. **One doctrine** — superseded frameworks (poteto-swarm-method) exist only as
   attribution inside Tetherline; no dual-doctrine pointers (v2.2.1 swap).
5. **Failures garden upward** — repeated agent failures across application layers
   become tetherline skills/rules (law 5), not per-skill patches.

## Sync topology

```
0x-wzw/tetherline ──(tetherline-sync cron)──> ~/.hermes/skills/{6 doctrine skills}
0x-wzw/Sharingan  <─(sharingan-sync cron)──> ~/.hermes/{profiles}/skills (policy skills, incl. harness/rea)
kangarooking/cangjie-skill ──(audited LOCAL_DIFF sync)──> Sharingan toolchain
Obsidian Vault ──(canonical outputs)──> profile skills (never mirrored into repos)
```

Upstream state as of v2.3.0: Sharingan = upstream v2.5.0..main fully consumed;
REA integrated as Stage-1/Stage-4 evidence provider (`harness/rea/SKILL.md`);
Tetherline upstream watch tracks MiroFish / Paperclip / GBrain / Kimi-K3 / ruflo.
