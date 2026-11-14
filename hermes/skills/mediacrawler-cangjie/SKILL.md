---
name: mediacrawler-cangjie
description: |
  Fetch public content from media platforms (Xiaohongshu, Douyin, Bilibili, Kuaishou, Weibo, Tieba, Zhihu) via MediaCrawler, then distill it into executable agent skills via cangjie-skill. Use when the user wants to crawl/collect posts, comments, or creator content from Chinese social media platforms, or when they want to turn crawled content (or any book/video/podcast transcript) into distilled, callable methodology skills. Triggers: "爬取/采集 小红书/抖音/B站/微博/知乎", "crawl xiaohongshu/douyin/bilibili", "distill this content into skills", "拆书/蒸馏成skill", "collect posts about X then turn it into a skill".
metadata:
  layer: harness
  stack-source: repo:0x-wzw/Sharingan
  author: "Cangjie Distillation <agent@example.com>"
---

# MediaCrawler + cangjie-skill: crawl → distill pipeline

Two-stage pipeline. Stage 1 collects public content with MediaCrawler (browser-automation based crawler, no JS reverse engineering). Stage 2 distills the collected transcripts/text into executable agent skills with cangjie-skill's RIA-TV++ pipeline.

## Legal & ethical gate (ALWAYS apply first)

- MediaCrawler is for **learning/research on public data only**. No commercial use, no large-scale scraping, no private data. Respect platform ToS and local law (see MediaCrawler's disclaimer).
- Keep volumes small and human-plausible: use keywords/search with modest page limits (`CRAWLER_MAX_NOTES_COUNT`), add delays, one account, no parallel instances.
- Never crawl private/group content or personal data beyond public posts.

## Stage 1 — Collect (MediaCrawler)

```bash
cd ~/.hermes/profiles/cangjie/skills-src/mediacrawler
# first run: scan QR code to persist login state (headless=False)
~/​.hermes/profiles/cangjie/venv/bin/python main.py --platform xhs --lt qrcode --type search \
  --keywords " semiconductor investment " --start "2026-01-01" --end "2026-10-01"
```

- Platforms: `xhs` `dy` `ks` `bilibili` `wb` `tieba` `zhihu`
- Crawler types: `search` (keyword), `detail` (specific posts), `creator` (a creator's posts)
- Login: `qrcode` (first run, interactive), `cookie` (from browser)
- Output: `data/<platform>/` — JSON/CSV/DB per `SAVE_DATA_OPTION` in `config/base_config.py`
- Keyword search: `--keywords "a || b"` (OR), `--start/--end` date filters, `--page-limit` to cap volume
- **For distillation**, collect text: notes/comments content. For video platforms (dy/bilibili/ks), you need transcripts — either platform subtitles (when available in the response) or run ASR on downloaded media (see `media_downloader/`).

### Environment

- Python venv: `~/.hermes/profiles/cangjie/venv` (has pyyaml, jsonschema, tiktoken, playwright pip pkg)
- **Playwright browser caveat**: Playwright does not ship a chromium build for macOS 12 on this machine. If browser launch fails, fall back to: (a) an existing Chrome/Chromium via `channel="chrome"` in MediaCrawler's browser config, or (b) export data another way and skip Stage 1. Do not waste cycles trying to install unsupported browser builds.
- First login needs an interactive desktop session for QR scan — do it in Terminal.app on the Mac, not headless.

## Stage 2 — Distill (cangjie-skill)

Follow the full `SKILL.md` in `Projects/sharingan/SKILL.md`. Condensed runbook:

1. **Input gate**: confirm with user — text source path (from Stage 1 `data/` or any book/transcript file), title/author/date metadata, purpose (single vs pack). Never distill from memory; no text → stop and ask.
1a. **Source-integrity gate (ALWAYS before Stage 0)**: locate and read the ACTUAL artifact (video transcript, repo text, paper) — never the promotional framing of a tweet/link. Verify the artifact's real topic matches the claimed framing; a mismatch is an integrity finding that must lead the DIGEST and the skill's boundary section, and the skill must refuse to teach what the artifact doesn't contain. X posts are read anonymously via `https://api.fxtwitter.com/<user>/status/<id>` (JSON: author/text/media/article URL); X articles are login-walled — if the claimed substance lives only in an article or raw captions are unavailable, distill only from what is extractable, flag every claim with its extraction layer (e.g. `notes-layer`), and route unverifiable specifics to needs_review rather than cards. User-facing deliverables (summaries, DIGEST, chat reports) are written in English unless the user asks otherwise.
2. **Prep**: convert crawled JSON/CSV → clean plain text under `books/<slug>/source/`. One note/post per block, keep author/date/URL for traceability.
3. **Pipeline** (stages 0→5, strict order, checkpoint via `PIPELINE_STATE.md`):
   - Stage 0: Adler whole-book understanding → `BOOK_OVERVIEW.md`, user confirms
   - Stage 1: 5 parallel extractors (framework/principle/case/counter-example/glossary) → `candidates/`
   - Stage 1.5: triple verification (V1 source sufficiency, V2 executability, V3 task gain) → `verified.md`
   - Stage 1.6: promotion gate → promoted vs router capabilities
   - Stage 2: RIA++ capability cards → `.cangjie/capabilities/cards/`
   - Stage 3: Zettelkasten links + glossary
   - Stage 4: pressure tests (actually run representative tasks)
   - Stage 5: compile → `python3 scripts/cangjie.py compile --bundle books/<slug>/.cangjie/capabilities --out <dir> --output auto`
4. **Toolchain**: run via `~/.hermes/profiles/cangjie/venv/bin/python scripts/cangjie.py …` (venv has the required deps; doctor passes). Work in `~/.hermes/profiles/cangjie/workspace/` so outputs persist.
5. **Deliver**: copy/symlink compiled skills into `~/.hermes/profiles/cangjie/skills/` (or target profile), report install location.
6. **External validation (SkillEvaluator harness)** — after compile, run Tier 1 `skillevaluator quality-check <compiled-dir> -r json` on the output; score <70 blocks install. Tier 2/3 (eval datasets / live Skill Lift) for high-stakes skills only. See `skills/skillevaluator-harness/SKILL.md`.

## Quality red lines (from cangjie-skill, non-negotiable)

- Every capability passes all three verifications; full R/I/A1/A2/E/B card structure
- Quotes ≤150 chars/paragraph (EN ≤100 words); no fabricated cases — synthetic drills labeled as such
- Coverage audit with traceable destinations; missing outputs count as failures in evals
- Keep audit trails: `candidates/` and `rejected/` are never deleted
- **External validation gate**: Tier 1 `skillevaluator quality-check` must run on every compiled
  bundle before install; SCHEMA/SECRET errors block install unless dispositioned in the run
  report with evidence (env-blocked = SKIPPED-ENV; verified FP = ACCEPTED-FP). Compiler emits
  `version`/`license`/`metadata.author` natively since the 2026-11-14 LOCAL_DIFF — no manual
  augmentation needed unless compiler is re-synced from upstream (see `scripts/LOCAL_DIFF.md`).

## Typical requests

- "Crawl posts about [topic] on xiaohongshu, then distill the methodologies into a skill" — Stage 1 search crawl (small volume) → text prep → full cangjie pipeline
- "Turn this podcast transcript into skills" — skip Stage 1, feed transcript straight into Stage 2
- "Collect creator X's recent posts on bilibili" — Stage 1 `creator` crawl, deliver data; distill only on request
