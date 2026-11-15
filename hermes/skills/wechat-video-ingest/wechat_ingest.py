#!/usr/bin/env python3
"""wechat-video-ingest: Firecrawl scrape + cover download + ilmu vision OCR.

Usage:
  python3 wechat_ingest.py <sph_id_or_url> [--outdir DIR] [--skip-ocr]

Outputs (in outdir, default ~/.hermes/cache/scratch):
  wxsph-<ID>.json         raw Firecrawl payload
  wxsph-<ID>-caption.txt  extracted caption/metadata text
  wxsph-<ID>-cover.jpg    downloaded cover
  wxsph-<ID>-ocr.txt      ilmu vision transcription (unless --skip-ocr)

Requires FIRECRAWL_API_KEY and ILMU_API_KEY in ~/.hermes/.env.
Public posts only — see SKILL.md red lines.
"""
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request

ENV_PATH = os.path.expanduser("~/.hermes/.env")
SCRATCH = os.path.expanduser("~/.hermes/cache/scratch")
ILMU_MODEL = "ilmu-glm-5.3-flash"

PROMPT = (
    "Extract ALL on-image text, structure-preserving: keep the layout hierarchy "
    "(titles, numbered items/sections, color blocks, arrows, captions). Transcribe "
    "in the original language exactly as written - do not summarize or translate. "
    "If the image contains no numbered list / no expected content, say so explicitly."
)


def load_env():
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k, v)


def scrape(sph_id):
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/scrape",
        data=json.dumps(
            {
                "url": f"https://weixin.qq.com/sph/{sph_id}",
                "formats": ["markdown"],
                "waitFor": 10000,
            }
        ).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['FIRECRAWL_API_KEY']}",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


def extract(data, out_prefix):
    md = data["data"]["markdown"]
    m = re.search(r"!\[\]\((https?://[^)]+)\)", md)
    img_url = m.group(1) if m else None
    # caption block: strip image markdown and the trailing QR boilerplate
    caption = md.replace("![二维码](<Base64-Image-Removed>)", "").strip()
    with open(f"{out_prefix}-caption.txt", "w") as f:
        f.write(caption)
    return img_url, caption


def download_image(url, path):
    subprocess.run(["curl", "-s", url, "-o", path], check=True)
    return path


def ocr_image(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {
        "model": ILMU_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                    },
                ],
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.1,
    }
    req = urllib.request.Request(
        "https://api.ilmu.ai/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['ILMU_API_KEY']}",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        out = json.load(resp)
    return out["choices"][0]["message"]["content"]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    skip_ocr = "--skip-ocr" in sys.argv
    outdir = None
    if "--outdir" in sys.argv:
        outdir = sys.argv[sys.argv.index("--outdir") + 1]
    if not args:
        print(__doc__)
        sys.exit(1)
    src = args[0]
    sph_id = src.split("/sph/")[-1].split("?")[0].strip("/")
    if not re.fullmatch(r"[A-Za-z0-9]+", sph_id):
        print(f"Invalid sph id: {sph_id}", file=sys.stderr)
        sys.exit(1)

    load_env()
    outdir = outdir or SCRATCH
    os.makedirs(outdir, exist_ok=True)
    prefix = os.path.join(outdir, f"wxsph-{sph_id}")

    print(f"1/4 scraping sph/{sph_id} ...")
    raw = scrape(sph_id)
    if not raw.get("success"):
        print(f"Scrape failed: {raw}", file=sys.stderr)
        sys.exit(1)
    with open(f"{prefix}.json", "w") as f:
        json.dump(raw, f, ensure_ascii=False, indent=1)

    print("2/4 extracting caption ...")
    img_url, caption = extract(raw, prefix)
    print(f"   author/date/stats: see {prefix}-caption.txt")
    print(caption[:400] + ("..." if len(caption) > 400 else ""))

    if not img_url:
        print("No cover image found in payload — done (caption-only source).")
        return
    print("3/4 downloading cover ...")
    cover = download_image(img_url, f"{prefix}-cover.jpg")
    if skip_ocr:
        print(f"   cover saved: {cover} (--skip-ocr)")
        return

    print("4/4 ilmu vision OCR ...")
    text = ocr_image(cover)
    with open(f"{prefix}-ocr.txt", "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
