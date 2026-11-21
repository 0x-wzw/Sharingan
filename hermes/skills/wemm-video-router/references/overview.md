# BOOK_OVERVIEW — WeMM-Video (Sharingan Stage 0)

Source: https://github.com/Tencent/WeMM-Video (13 commits, 2026-11-19/20), paper
arXiv:2611.26409 (21 pp, submitted 2026-11-19), README/README_zh, docs/serving.md,
patch/README.md, native/README.md, examples/README.md. Local mirror:
`$HOME/.hermes/cache/scratch/wemm-video-eval/`. License: Apache-2.0 code;
separate model license. Attribution: WeChat Vision, Tencent Inc. + Tsinghua.

## Structure (Adler step 1)
1. Problem framing (pp.1–2): open-source omni-modal video models brittle on
   fine-grained AV detail, cross-modal temporal alignment, cross-modal hallucination.
2. Architecture (pp.2–3): Qwen3.5/Qwen3.6 LLM backbone + native vision encoder +
   Whisper audio encoder + window-level Q-Former; audio → 10 tokens/sec (0.1 s
   windows); visual/audio tokens interleaved chronologically with explicit text
   timestamps. Sizes 2B/4B/9B dense, 35B-A3B MoE. Hybrid thinking: instruct vs
   thinking mode.
3. Data (pp.3–4): ~1.2T tokens; modality mix AV 45.4% / visual 28.4% / audio 23.6% /
   text 2.6%; task mix captioning 37.7%, knowledge&reasoning QA 17.5%, grounding
   12.6%, ASR 8.1%, music 6.6%, dialogue 5.4%, summarization 4.9%, cross-media 3.3%,
   OCR 1.9%, counting 1.6%, agent/tool 0.4%. Quality pipeline: automated scoring,
   semantic dedup, toxicity filtering.
4. Training (pp.4–5): progressive 3-stage pre-training (acoustic alignment with
   aligner only → full omni-modal knowledge injection keeping visual encoder frozen →
   long-context scaling) then 3-stage post-training (multi-teacher OPD;
   anti-repetition MrDPO with offline-mined hard negatives + LoRA-only rounds that
   are merged/reinitialized; specialist RL with rule/rubric/teacher-consistency
   rewards routed dynamically, joint instruct+thinking sampling, long-context RL).
5. Evaluation (pp.5–13): >120 benchmarks; 33 AV benchmarks, 32 silent-video;
   comparisons vs Gemini-3.0-Flash, Seed2.0-Mini-0428, Qwen3.5-Omni-Flash, etc.
6. Reproduction artifacts: 4 quantized formats per size (FP8 Block128, AWQ W4A16,
   GGUF Q4_K_M, NVFP4 W4A16), patched vLLM 0.18/0.31 and SGLang 0.5.16/0.5.19
   overlays with SHA-256 manifests, Docker profiles, native GGUF runtime,
   OpenAI-compatible serving. Validation table openly marks GPU generation pending.

## Interpretation (Adler step 2)
The transferable thesis: **omni-modal competence is an alignment-and-curriculum
engineering problem, not just a scale problem.** Three reusable ideas stand out:
(a) interleave modality tokens in chronological order with explicit timestamps so
    cross-modal temporal alignment is learnable;
(b) freeze the already-good encoder and unfreeze progressively (aligner → all-but-
    visual → long context) to bridge modality gaps without destroying priors;
(c) post-training is *staged by failure mode* — general capability (OPD), generation
    degeneration (MrDPO), then specialized skill (RL) — with teacher choice matched
    to the capability being protected (same-family teachers preserve AV ability).

## Critique (Adler step 3)
- Training data recipe is described at mixture level, not reproducible: no dataset
  manifest, dedup thresholds, quality-scorer spec, or caption-synthesis prompts.
- No ablation isolating OPD vs MrDPO vs RL; claims of "substantial gains" for
  thinking mode are from benchmark deltas, not controlled studies.
- Model license is separate from Apache-2.0 code; checkpoints require HF terms review.
- The repo is 2 days old with no releases, 0 forks; validation explicitly says GPU
  generation after checkpoint download is pending — reproduction is not yet proven.
- Serving relies on version-pinned source overlays into vLLM/SGLang; hashes are
  provided, but long-term maintainability across engine upgrades is unproven.

## Application (Adler step 4)
Most useful to an agent operator: a *staged capability-injection* pattern (align one
new modality at a time, freeze what already works, then fix degeneration before
adding specialist skills), a *failure-mode-ordered post-training* checklist, and a
*reproducibility discipline* pattern (version-pinned overlays + hash manifests +
explicit "pending" validation rows). The model weights themselves are not a skill.

## Critical tasks for coverage audit
1. How to add a new modality without destroying an existing encoder's priors.
2. How to make cross-modal temporal alignment learnable.
3. How to stop repetition/degeneration before RL.
4. How to allocate teachers across capabilities during distillation.
5. How to route rewards for verifiable vs open-ended tasks.
6. How to ship a reproducible multi-engine serving stack with honest validation.
