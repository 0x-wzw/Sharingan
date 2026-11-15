---
name: wechat-video-ingest
description: "Acquire public WeChat Channels (视频号) posts and turn them into text + image OCR captures: weixin.qq.com/sph/<id> → Firecrawl JS-render scrape → extract cover image URL from the markdown payload → curl the image → ilmu vision OCR with structure-preserving transcription. Use when the user shares a weixin.qq.com/sph link or asks to capture/distill a WeChat Channels video. Triggers: 'wechat video', '视频号', 'sph link', 'capture this weixin post', 'ingest wechat channels'."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  layer: harness
  stack-source: repo:0x-wzw/Sharingan
  hermes:
    tags: [wechat, ingestion, ocr, firecrawl, ilmu, cangjie, media]
    related_skills: [mediacrawler-cangjie, pixelshot-page-capture]
  provenance:
    validated_on:
      - "ACWomNhi1O (2026-10-08, v1 FDE source — full infographic OCR)"
      - "A2yLcXCaOA (2026-10-17, 数产白话 ladder — cover-only teaser)"
      - "ANGeAkU5fY (2026-10-17, 老江 training path — full caption in payload)"
---

# WeChat Video Ingest & OCR

Acquire a public WeChat Channels (视频号) post and produce two artifacts: (1) the post's text content (caption, metadata, engagement stats) and (2) a structure-preserving OCR transcription of its cover/infographic image. This is Stage-1 of the cangjie crawl→distill pipeline for WeChat sources.

## What you get per source type (observed across 3 validated runs)

| Payload type | You get | You don't get |
|---|---|---|
| **Infographic post** (image card) | Full on-image text via OCR | Video narration (stream behind auth) |
| **Teaser card** (caption truncated) | Title/hashtags + cover | The body content — treat as teaser only |
| **Full-caption post** | Complete caption text natively | Any on-image detail beyond the cover |

**Never assume which type until you've scraped.** A cover OCR that lacks the expected content does NOT mean the content doesn't exist — check whether the caption itself carried it (the ANGeAkU5fY case: content was in the caption, not the image).

## Prerequisites

- `FIRECRAWL_API_KEY` in `~/.hermes/.env`
- `ILMU_API_KEY` in `~/.hermes/.env` (ilmu vision-capable model; `ilmu-glm-5.3-flash` verified)
- `curl`, `python3` (stdlib only — urllib, json; no extra deps)
- No cookies/login needed for public posts (verified)

## Procedure

### 1. Scrape the post (Firecrawl JS-render)

The page is a pure JS shell — a plain fetch returns nothing useful. waitFor 10s is the verified minimum.

```bash
set -a; source ~/.hermes/.env; set +a
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -d '{"url":"https://weixin.qq.com/sph/<ID>","formats":["markdown"],"waitFor":10000}' \
  -o /tmp/wxsph-<ID>.json
```

Check `success:true` in the JSON. Failure modes: `Unauthorized: Token missing` (env not sourced — re-source .env), HTTP 401 (key rotated).

### 2. Extract the payload

The markdown payload contains, in order: cover image `![](url)`, location, **full caption text**, date, author avatar, author name, engagement stats (like/share/comment/collect), QR block.

```python
import json
d = json.load(open("/tmp/wxsph-<ID>.json"))
md = d["data"]["markdown"]
start = md.find("![](") + 4
end = md.find(")", start)
img_url = md[start:end]          # finder.video.qq.com stodownload URL, ~470-510 chars
print(md)                         # caption + author + date live here — read it before OCR
```

**Read the caption first.** If it's complete (ends with a full sentence, carries the claim), the caption IS the primary content and the cover is secondary. Classify per the table above.

### 3. Download the cover image

```bash
curl -s "$IMG_URL" -o /tmp/wxsph-<ID>-cover.jpg
file /tmp/wxsph-<ID>-cover.jpg   # expect: JPEG 540x720
```

The stodownload URL is time-limited — download immediately, don't save the URL for later.

### 4. Vision OCR via ilmu

Python stdlib script — no SDK needed. Key requirements verified across runs:

```python
import base64, json, os, urllib.request

# load env from ~/.hermes/.env (os.environ.setdefault per line)
payload = {
    "model": "ilmu-glm-5.3-flash",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": (
                "Extract ALL on-image text, structure-preserving: keep layout hierarchy "
                "(titles, numbered items, color blocks, arrows, captions). Transcribe in "
                "the original language exactly — do not summarize or translate. "
                "Note explicitly if expected content is ABSENT from the image."
            )},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
        ],
    }],
    "max_tokens": 4096,
    "temperature": 0.1,
}
# POST to https://api.ilmu.ai/v1/chat/completions, Bearer ILMU_API_KEY
```

- **base64 data URI works** (`data:image/jpeg;base64,...`) — no separate image hosting needed
- **temperature 0.1** for transcription fidelity
- **Ask for absence-flagging** — the model will correctly report "no numbered list on this image" rather than hallucinating structure

### 5. File the capture

- Vault: `Knowledge/00-Raw/` with Schema v2 frontmatter (`type: raw`, `source: wechat-channels`, `source_id: weixin.qq.com/sph/<ID>`, `url:`), transcribed caption + OCR, and an explicit "video body NOT transcribed" open-item note
- Cangjie bundle (if distilling): `workspace/books/<slug>/source/<name>.md` + cover JPG, then update `source/SOURCE.md`
- **Before writing any insights: verify which payload type you got.** Attribute only what you actually hold — caption OR OCR, never inferred (the 2026-10-17 correction: a skill was written attributing invented content to a URL pre-fetch; deleted same day)

## Red lines

1. **Public posts only.** No private/group content, no login bypass, respect WeChat ToS — same legal gate as mediacrawler-cangjie.
2. **No attribution before acquisition.** Never write insight content citing a sph URL you haven't scraped.
3. **Video streams are behind auth.** Transcription of narration requires the user to watch/provide audio; do not promise video-body extraction.
4. **Credit the author** (account name + date) in every capture and derived artifact.

## Known limits

- Captions are sometimes truncated by the card ("teaser" type) — the video body or a linked article may hold the rest
- Cover images are 540×720 JPEG; dense infographics may need per-region crops for full OCR fidelity
- Engagement stats are captured as displayed (four numbers, meaning unlabeled — record verbatim, don't guess which is which)
- rag-health gate: if `~/.hermes/logs/hermes-rag-health.json` shows `fail`, skip the handoff-embedding step per vault protocol

## Related

- `mediacrawler-cangjie` — the Stage-2 distill pipeline this feeds
- Cangjie acquisition recipe (original note): vault `Knowledge/00-Raw/cangjie-fde-skill-distillation.md` §Learnings
