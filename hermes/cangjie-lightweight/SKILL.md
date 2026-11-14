---
name: cangjie
approval_source: agent
description: Use when distilling content into executable Agent Skills.
version: 1.0.0
author: Hermes Agent
license: MIT
read_scope: profile
metadata:
  hermes:
    tags: [cangjie, skills, distillation, github, sync]
    related_skills: [grounded-citations, hermes-flywheel-csi-monitoring]
---

# Cangjie — distill high-value content into executable Agent Skills

Cangjie (仓颉) turns books, talks, interviews, and profiles into executable
skills: research the source, extract the METHOD, publish it as a skill the
agent can load and follow. Named after the mythical inventor of Chinese
characters — turn what was said into what can be run.

## When to Use

- The user asks to "turn it into a skill" after research, a talk, an interview, a book, or a person profile
- The user invokes the cangjie profile (`cangjie` CLI = `hermes -p cangjie`)
- Publishing or syncing distilled skills to the `0x-wzw/cangjie-skill` GitHub repo

## Procedure

1. **Research the source with grounding.** Fan out searches, build a citation
   ledger, extract the full text (talk transcripts included — the full text
   hides in the web cache file, read the omitted middle), attach verbatim
   evidence for load-bearing claims. See the `grounded-citations` skill.
   X/Twitter sources: fetch via `https://api.fxtwitter.com/<user>/status/<id>`
   — returns full JSON (text, media, view/bookmark counts) without auth;
   fetching x.com directly is blocked for bots. Video posts: the fxtwitter
   JSON carries the mp4 (`media.all[0].url`) — download it and run
   `video_analyze` for a frame-by-frame transcript; on-screen captions are
   primary evidence. Compare the uploader's caption against the footage and
   distill only what the source demonstrates — where the caption claims more
   than the video shows, encode the gap as an anti-pattern, not a fact. When an X post is a
   pointer to a repo or site, the linked artifact is the primary source — clone/read it
   (README, findings/, docs/ dirs) and distill from the artifact, not the tweet text.
2. **Extract the method, not the biography.** The skill encodes: the rules,
   the order, the rejection triggers, the WHY behind each rule. Discard
   narrative, dates, and people-drama. One rule per lesson; fold repeats into
   one stronger rule.
3. **Author the SKILL.md in Hermes format.**
   - Frontmatter: `name`, `approval_source: agent`, `description` ≤ 60 chars
     trigger-first ("Use when …" — longer is REJECTED outright), `version`,
     `author`, `license`, `source` (the distillation provenance — see step 5),
     `metadata.hermes.tags` + `related_skills`.
   - Body: `## When to Use` near the top, then imperative sections, then
     anti-patterns, then verified sources. Lint enforces all of this.
   - For repo sources, cite `repo@<commit-sha>` in Sources — content drifts, and the sha
     pins what was actually distilled (verify the sha resolves via `gh api` before
     publishing).
4. **Install in the default profile** with skill_manage (action=create,
   category dir). Then copy the same file into the cangjie profile:
   `~/.hermes/profiles/cangjie/skills/<category>/<name>/SKILL.md`.
5. **Distribution policy (Zehan, 2026-11-07): GitHub = code + releases ONLY.** Files and information (SKILL.md markdown, catalogues) live on the **Obsidian vault** (`Knowledge/40-Templates/cangjie/`) and **Notion** (🤖 Hermes Agent → "Cangjie — Distilled Skills Index"). Never commit skill markdown to GitHub.
6. **Publish**: run `python3 ~/.hermes/scripts/cangjie_skill_sync.py` (cron 04:10, after the dream cycle). It mirrors every `source:`-marked skill into the vault, rebuilds the vault `_INDEX.md`, and cuts a GitHub `bundle-<hash>` release (tag + tar.gz asset) only when the distilled skill set changes. The repo also carries installer code (`install.sh`) — nothing else.
7. **Verify**: `ls ~/obsidian_remote/Knowledge/40-Templates/cangjie/` shows the skill; `gh release list -R 0x-wzw/cangjie-skill` shows the bundle release; append a 🚀 callout block to the Notion index page ("Cangjie — Distilled Skills Index", one paragraph: skill #, name, category, source, method, applicability).

## Pitfalls

- **A skill without `source:` frontmatter never publishes** — the scanner
  cannot distinguish stock skills from distillations without it. Add the field
  even if the source is "synthesized from session research".
- **Policy boundary (2026-11-07): markdown/knowledge NEVER goes to GitHub** — the cangjie-skill repo holds only `install.sh` + releases. If a sync run tries to commit SKILL.md files, the script is pre-policy; rewrite it.
- **GitHub auth lives in `~/.hermes/.cangjie_gh_token` (chmod 600), wired into
  `gh` via `gh auth login --with-token`.** If pushes fail with HTTP 401, the
  token expired — ask for a fresh PAT, write it to that file, re-run the login,
  never echo the token.
- **`gh release upload` must run with `-R 0x-wzw/cangjie-skill` (or from inside
  the repo clone)** — from a non-repo cwd gh resolves the repo via git and fails
  with "not a git repository".
- **Releases are per-BUNDLE, not per-skill-version** — a content-hash tag
  (`bundle-<sha1[:8]>` of the name@version set) prevents release spam when
  individual skills carry different versions.
- **The repo can vanish (deleted/renamed upstream) while the vault wiki entity
  still documents it.** If `gh repo view` fails to resolve, check the vault
  entity (`System/Wiki/entities/github-repos/cangjie-skill.md`) for the
  documented description, recreate the repo with it, push, and re-verify.
- **Run the skill end-to-end with real data before publishing** — a distillation
  whose procedure was never exercised is a plausible-sounding failure the next
  session will trust.
- **Never put the distilled person's private life in the skill** — professional
  footprint and method only.
- **Draft the description to the 60-char budget BEFORE calling skill_manage** —
  the tool rejects >60 chars and rolls back the ENTIRE operations batch, so one
  long description silently discards every other op in the same call. Pre-write
  it trigger-first ending with a period, MEASURE it with `len()` in a tool call
  before submitting (eyeball counts run long), and push detail into the body.

## Related

- `grounded-citations` — evidence and citation ledger for the research half
- `hermes-flywheel-csi-monitoring` — the flywheel dream cycle that the 04:10
  sync hangs off
- Repo: `github.com/0x-wzw/cangjie-skill`; local clone `~/cangjie-skill`;
  sync log `~/.hermes/cron/output/cangjie-sync.log`
