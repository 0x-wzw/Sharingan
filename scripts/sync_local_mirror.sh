#!/usr/bin/env bash
# Sharingan <-> local bidirectional sync (run after skills self-improve, or by cron)
# Policy (hermes/INDEX.md): mirror process/infrastructure skills; outputs stay canonical in the vault.
set -euo pipefail
REPO="$HOME/Projects/sharingan"
PROFILE_SKILLS="$HOME/.hermes/profiles/kakashi/skills"
DEFAULT_SKILLS="$HOME/.hermes/skills"
# skills mirrored into the repo (process/infrastructure/operators — NOT vault-canonical outputs)
MIRROR_SKILLS=(mediacrawler-cangjie youtube-crawler wechat-video-ingest skillevaluator-harness venture-validation-machine)
# skills that live in the default profile instead
DEFAULT_MIRROR=(venture-machine parallel-venture-validation poteto-swarm-method venture-validation-machine)

cd "$REPO"
echo "[1/4] pull GitHub"
git pull --ff-only origin main || { echo "pull failed — resolve manually"; exit 1; }

echo "[2/4] mirror locally improved skills -> repo"
changed=0
for s in "${MIRROR_SKILLS[@]}"; do
  src="$PROFILE_SKILLS/$s/SKILL.md"
  dst="hermes/skills/$s/SKILL.md"
  if [ -f "$src" ] && ! diff -q "$src" "$dst" >/dev/null 2>&1; then
    mkdir -p "hermes/skills/$s"
    cp "$src" "$dst"
    [ -d "$PROFILE_SKILLS/$s/references" ] && rm -rf "hermes/skills/$s/references" && cp -R "$PROFILE_SKILLS/$s/references" "hermes/skills/$s/"
    echo "  updated: $s"; changed=1
  fi
done
for s in "${DEFAULT_MIRROR[@]}"; do
  src="$DEFAULT_SKILLS/$s/SKILL.md"
  dst="hermes/skills/$s/SKILL.md"
  if [ -f "$src" ] && ! diff -q "$src" "$dst" >/dev/null 2>&1; then
    cp "$src" "$dst"; echo "  updated: $s (default profile)"; changed=1
  fi
done

echo "[3/4] compiler <-> profile linkage"
# profile toolchain is a symlink to this repo — always synced; verify:
diff -q scripts/compile_single.py "$HOME/.hermes/profiles/kakashi/skills-src/cangjie-skill/scripts/compile_single.py" >/dev/null \
  && echo "  compiler symlink: OK" || echo "  WARN: profile toolchain diverged from repo"

echo "[4/4] push"
if [ "$changed" = "1" ] || [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "hermes: skills self-improvement sync $(date +%F-%H%M)"
  git push -q origin main
  echo "  pushed"
else
  echo "  nothing to push"
fi
echo "sync complete"
