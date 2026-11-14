---
version: 1.0.0
license: MIT
name: youtube-crawler
description: |
  Collect YouTube video/playlist transcripts into the cangjie workspace for distillation into agent skills. Uses youtube_transcript_api (captions) with yt-dlp auto-subs fallback and optional audio download for ASR. No browser/Playwright needed — works on macOS 12. Use when the user provides YouTube links, asks to "crawl youtube", "抓取YouTube字幕", "distill this video/playlist into a skill", or wants a YouTube channel/playlist turned into distilled skills. Triggers: "crawl youtube", "youtube transcript", "distill youtube video", "拆YouTube视频", "youtube playlist to skill".
metadata:
  layer: harness
  stack-source: repo:0x-wzw/Sharingan
  tags: [youtube-crawler]
  author: "Cangjie Distillation <agent@example.com>"
---

# YouTube → cangjie-skill: transcript → distill pipeline

Stage-1 collector for YouTube (the one platform MediaCrawler does **not** cover).
Lands output in the exact `workspace/sources/` format the cangjie-skill RIA-TV++
pipeline already consumes (same layout as `sources/conversations-andrew-ng/`).

## Legal & ethical gate (ALWAYS apply first)

- Public videos only. Respect YouTube ToS and copyright — collect transcripts for
  **research/learning and skill distillation**, never redistribution of media.
- Keep volumes human-plausible: default 4 s delay between videos, `--playlist-limit`
  default 15, never parallel instances.
- Auto-generated captions are ASR output — expect transcription noise; the distill
  pipeline's verify stages handle it, but flag `method: ytdlp-subs` runs for review.

## Usage

```bash
# Single video (URL or 11-char ID)
~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/profiles/cangjie/skills/youtube-crawler/youtube_crawler.py \
  https://www.youtube.com/watch?v=aircAruvnKk --name nn-chapter-1

# Multiple videos
… youtube_crawler.py aircAruvnKk IHZwWFHWa-w Ilg3gGewQ5U --name nn-foundations

# Playlist (flat expand via yt-dlp, capped)
… youtube_crawler.py "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi" \
    --name 3b1b-nn --playlist-limit 10

# With audio download for ASR fallback (no captions available)
… youtube_crawler.py <id> --name some-talk --with-audio
```

Accepted targets: `watch?v=` URLs, `youtu.be/` URLs, `/shorts/` URLs, bare 11-char
video IDs, `playlist?list=` URLs.

## Acquisition chain (in order)

1. **youtube_transcript_api** (hermes-agent venv, HTTP-only, no browser) —
   manual captions preferred, language preference from `--languages` (default `en en-US`).
2. **yt-dlp `--write-auto-subs`** (cangjie venv) — fallback when the API fails
   (age-restricted, region-locked, API outage).
3. **`--with-audio`** — downloads `bestaudio[ext=m4a]` for later ASR (ilmu-asr-v4.2
   is available on the ilmu endpoint) when no captions exist at all.

## Output layout (distill-ready)

```
workspace/sources/<name>/
  001-<Video Title>.en.vtt      # WebVTT, matches existing sources/ convention
  002-<Video Title>.en.vtt
  manifest.json                 # video_id, title, author, url, status, method, files
  <name>.txt                    # combined plain text: "===== NNN-Title =====" sections
```

The combined `<name>.txt` is the direct distill input. Re-running with the same
`--name` skips videos already in `manifest.json` (idempotent, resumable) and
regenerates the `.txt` from all captured items.

## Stage 2 — Distill

Feed `workspace/sources/<name>/<name>.txt` into the cangjie-skill RIA-TV++
pipeline exactly as documented in `Projects/sharingan/SKILL.md`
(Adler → 5 extractors → triple verify → promotion gate → RIA++ cards →
Zettelkasten → pressure tests → compile). Compiled skill lands in `skills/`.

## Environment & caveats

- `youtube_transcript_api` v1.2.4 lives in `~/.hermes/hermes-agent/venv` (invoke via
  that venv's python — the system python cannot import it).
- `yt-dlp` 2026.08.19 lives in `~/.hermes/profiles/cangjie/venv/bin/`.
- **No Playwright/browser needed** — deliberately avoids the macOS 12 chromium gap.
- Heavy yt-dlp use can trip YouTube bot checks; keep playlists modest and delays on.
- If both caption paths fail (music video, no subs, hard block), the item is marked
  `status: failed` in the manifest with the reason — decide ASR or skip per video.

## Verified

- Single video: `aircAruvnKk` → 27 KB VTT + 18 KB txt (oEmbed metadata + captions) ✓
- Playlist expand: 3B1B neural-nets playlist → 5 items flat-listed ✓
- URL parsing: watch / youtu.be / shorts / bare ID ✓

## Purpose

Stage-1 collector for YouTube — the one platform MediaCrawler does not cover. Lands transcripts in the exact `workspace/sources/` format the cangjie-skill RIA-TV++ distill pipeline already consumes. No browser/Playwright needed; works on macOS 12.

## Prerequisites

- `youtube_transcript_api` v1.2.4 in `~/.hermes/hermes-agent/venv` (invoke via that venv's python — the system python cannot import it)
- `yt-dlp` 2026.08.19 in `~/.hermes/profiles/cangjie/venv/bin/` (auto-subs fallback, playlist expansion)
- No browser/Playwright needed — deliberately avoids the macOS 12 chromium gap
- `--with-audio` items need a later ASR step (ilmu-asr-v4.2 on the ilmu endpoint)

## Instructions

1. Apply the legal & ethical gate first: public videos only, research/learning/skill-distillation use, 4 s delay between videos, `--playlist-limit` (default 15), never parallel instances.
2. Run `youtube_crawler.py <target> --name <slug>` (accepts watch/youtu.be/shorts URLs, bare 11-char IDs, playlist URLs; multiple IDs in one call).
3. Let the acquisition chain do its work: youtube_transcript_api captions → yt-dlp `--write-auto-subs` fallback → optional `--with-audio` for ASR when no captions exist.
4. Check `workspace/sources/<name>/manifest.json` for per-video `status`/`method`; the combined `<name>.txt` is the direct distill input. Re-runs with the same `--name` are idempotent/resumable.
5. Feed `<name>.txt` into the cangjie-skill RIA-TV++ pipeline (Stage 2 distill, per `Projects/sharingan/SKILL.md`).
   Full command reference: `## Usage`; output layout: `## Output layout (distill-ready)`.

## Examples

1. Single video: `youtube_crawler.py https://www.youtube.com/watch?v=aircAruvnKk --name nn-chapter-1` → 27 KB VTT + 18 KB txt.
2. Playlist: `youtube_crawler.py "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi" --name 3b1b-nn --playlist-limit 10` → 5 items flat-listed.
3. No captions at all: `youtube_crawler.py <id> --name some-talk --with-audio` → downloads `bestaudio[ext=m4a]` for later ASR.

## Limitations

- Public videos only; collect transcripts for research/learning and skill distillation, never redistribution of media — respect YouTube ToS and copyright.
- Keep volumes human-plausible (default 4 s delay, playlist cap 15, no parallel instances); heavy yt-dlp use can trip YouTube bot checks.
- Auto-generated captions are ASR output — expect transcription noise; the distill pipeline's verify stages handle it, but flag `method: ytdlp-subs` runs for review.
- If both caption paths fail (music video, no subs, hard block), the item is marked `status: failed` with the reason — ASR or skip is decided per video.

## Troubleshooting

- **youtube_transcript_api import fails** → it lives in `~/.hermes/hermes-agent/venv`, not the system python; invoke via that venv's python.
- **API path fails (age-restricted, region-locked, API outage)** → the yt-dlp `--write-auto-subs` fallback covers these; flag the `method: ytdlp-subs` run for review.
- **Item marked `status: failed` in manifest** → both caption paths failed (music video, no subs, hard block); decide ASR (`--with-audio`) or skip per video.
- **YouTube bot check tripped** → too-heavy yt-dlp usage; keep playlists modest (`--playlist-limit`) and delays on, never run parallel instances.
