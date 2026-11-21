# Glossary — WeMM-Video (Sharingan RIA-TV++ Stage 1)

Shared concept dictionary for downstream WeMM-Video skills. Definitions are grounded
in the local source (paper `paper.txt`, `README.md`, `docs/serving.md`,
`patch/README.md`, `native/README.md`, `BOOK_OVERVIEW.md`). Source references give
the paper page (`p.N`) or file section where the term is used/defined.

> Terms marked **[UNDEFINED IN SOURCE]** are used by the source but never properly
> defined there; an agent operator must not assume the dictionary meaning.

```yaml
- id: g01
  term: omni-modal (omni-modal video understanding)
  type: core-concept
  source_chapter: Abstract/p.1–2; "Omni-Modal Understanding" Fig.1
  author_definition: |
    A foundation model that unifies text, image, audio, and video processing in one
    model; for video it jointly perceives frames and the original soundtrack, producing
    text responses. "Omni-modal video understanding" is the joint comprehension of
    continuous visual scenes AND acoustic signals in real-world video.
  key_distinction: |
    ≠ "multimodal" in the loose sense (any 2 modalities) — here it specifically means
      native joint audio-visual-temporal understanding, not image+text only.
    ≠ "omni" as "all tasks" — it is a modality claim (text/image/audio/video), not a
      task-coverage claim.
  why_it_matters: |
    Downstream skills must treat audio as a first-class input, not an optional add-on;
    "video" in this project defaults to frames + soundtrack (video_audio), and evaluation
    is dominated by joint audio-visual (AV) benchmarks.
  tags: [term, core-concept]

- id: g02
  term: hybrid-thinking paradigm
  type: core-concept
  source_chapter: Abstract/p.1; Intro/p.2
  author_definition: |
    A single model that supports two inference behaviours: a non-thinking "instruct"
    mode for fast, direct responses and a "thinking" mode for explicit step-by-step /
    extended chain-of-thought reasoning over visual and audio-visual inputs.
  key_distinction: |
    ≠ "two separate models" — it is one set of weights with a mode switch.
    ≠ "chain-of-thought always on" — the mode is selected at inference via
      enable_thinking / chat_template_kwargs.enable_thinking.
  why_it_matters: |
    Mode choice is an operator decision: thinking mode mitigates cross-modal
    hallucination and raises complex-video scores but costs latency; instruct mode is
    the default for direct perception tasks.
  tags: [term, core-concept]

- id: g03
  term: instruct mode (non-thinking mode)
  type: term
  source_chapter: README "Inference modes"; p.1–2; serving.md
  author_definition: |
    The default inference mode giving low-latency, direct answers without emitting a
    reasoning trace. Enabled with enable_thinking=False in apply_chat_template or
    chat_template_kwargs.enable_thinking=false.
  key_distinction: |
    ≠ "simpler model" — same weights; only generation behaviour differs.
    ≠ always appropriate — the paper reports weaker complex-video reasoning here.
  why_it_matters: |
    Operators must set the flag explicitly; the serving/Transformers examples default
    to instruct mode.
  tags: [term]

- id: g04
  term: thinking mode
  type: term
  source_chapter: Abstract/p.1; Intro/p.2; p.5 (Specialist RL); serving.md
  author_definition: |
    The inference mode that produces explicit multi-step reasoning traces grounded in
    visual and audio-visual input, mitigating cross-modal hallucinations and boosting
    performance on complex video tasks. Enabled with enable_thinking=True.
  key_distinction: |
    ≠ generic "longer output" — the trace is grounded reasoning meant to reduce hallucination.
    It is jointly optimized with instruct mode via stochastic sampling during specialist RL.
  why_it_matters: |
    Use for complex AV reasoning; it is the mode behind most headline benchmark gains.
  tags: [term, core-concept]

- id: g05
  term: window-level Q-Former (audio aligner)
  type: term
  source_chapter: p.3 Architecture; p.4 Stage 1 pre-training
  author_definition: |
    A learned aligner that compresses Whisper acoustic features within local temporal
    windows of 0.1 s, mapping each window to a single audio token in the LLM input
    space, yielding 10 audio tokens per second. It is the ONLY trainable component in
    pre-training Stage 1 (acoustic alignment).
  key_distinction: |
    ≠ the audio encoder itself — the Whisper-based encoder extracts features; the
      Q-Former aligns/compresses them into the LLM token space.
    ≠ a global pooling layer — compression is local per 0.1 s window.
  why_it_matters: |
    It is the bridge that makes a text-only LLM acoustic; freezing it vs. unfreezing is
    the central lever in the staged curriculum (see g09/g10).
  tags: [term, architecture]

- id: g06
  term: Whisper-based audio encoder
  type: term
  source_chapter: p.3 Architecture
  author_definition: |
    The dedicated audio encoder (initialized from Qwen2.5-Omni) that extracts acoustic
    features from audio sampled at 16,000 Hz and segmented into 30-second chunks, which
    the window-level Q-Former then compresses.
  key_distinction: |
    ≠ a generic speech-to-text module — it produces continuous features for an LLM,
      not text transcripts directly.
    The vision encoder is kept native to the backbone; only the audio path is added.
  why_it_matters: |
    Tells the operator the audio input contract: 16 kHz, 30 s chunking, and that audio
    capability comes from a separate encoder, not the LLM backbone.
  tags: [term, architecture]

- id: g07
  term: timestamped token interleaving (cross-modal temporal alignment)
  type: core-concept
  source_chapter: p.3 Architecture; Fig.2; BOOK_OVERVIEW interpretation (a)
  author_definition: |
    For video with audio, visual and audio tokens are interleaved in chronological
    order and supplemented with explicit textual timestamps (e.g. "<0.0 sec>",
    "<1.0 sec>") to facilitate fine-grained cross-modal temporal alignment.
  key_distinction: |
    ≠ concatenating modalities (all video, then all audio) — order is by time.
    ≠ implicit positional encoding — timestamps are literal text tokens the model reads.
  why_it_matters: |
    This is the paper's key transferable idea for teaching a model "what was said when",
    directly addressing the failure to align acoustic cues to visual events.
  tags: [term, core-concept, transferable-pattern]

- id: g08
  term: progressive pre-training (progressive three-stage curriculum)
  type: core-concept
  source_chapter: p.4–5 §4.1; BOOK_OVERVIEW §4
  author_definition: |
    A three-stage curriculum that systematically expands the context window while
    enriching cross-modal representations: Stage 1 acoustic modality alignment →
    Stage 2 omni-modal knowledge injection → Stage 3 long-context capability scaling.
    It smoothly bridges modality gaps and scales long-horizon comprehension.
  key_distinction: |
    ≠ "train on everything at once" — stages change both data mix and trainable
      parameters; already-good encoders are frozen and unfrozen progressively.
  why_it_matters: |
    Encodes the reusable principle "add one modality at a time, freeze what already
    works" — the transferable staged capability-injection pattern.
  tags: [term, core-concept, transferable-pattern]

- id: g09
  term: acoustic modality alignment (pre-training Stage 1)
  type: term
  source_chapter: p.4 §4.1 Stage 1
  author_definition: |
    Initial pre-training stage: under a compact context window, only the audio aligner
    (window-level Q-Former) is optimized; the backbone LLM and modality encoders stay
    frozen. Training on audio-text pairs yields ASR and general audio-captioning ability.
  key_distinction: |
    ≠ full fine-tuning — deliberately minimal trainable set to avoid damaging priors.
  why_it_matters: |
    Concrete instantiation of "bridge a new modality without destroying the backbone".
  tags: [term, training-stage]

- id: g10
  term: omni-modal knowledge injection (pre-training Stage 2)
  type: term
  source_chapter: p.5 §4.1 Stage 2
  author_definition: |
    Core pre-training phase with expanded context window: all parameters are unfrozen
    EXCEPT the visual encoder (whose inherited representations are already strong),
    training on textual, visual, auditory, and joint AV data to form a unified
    cross-modal representation space.
  key_distinction: |
    ≠ Stage 1 — here almost everything is trainable; the visual encoder specifically
      stays frozen as the preserved prior.
  why_it_matters: |
    Shows which component is treated as "sacred" and why — a decision rule for staged
    modality addition.
  tags: [term, training-stage]

- id: g11
  term: long-context capability scaling (pre-training Stage 3)
  type: term
  source_chapter: p.5 §4.1 Stage 3
  author_definition: |
    Final pre-training stage: same trainable configuration as Stage 2 but a further
    scaled context window; trained on long videos, extended audio, and multi-video
    inputs to capture long-range cross-modal temporal dependencies.
  key_distinction: |
    ≠ a new parameter regime — only sequence length / context window changes.
  why_it_matters: |
    Explains why serving examples expose fps/max_frames/total_pixels and long-context
    RL — operators control how much of this capability is exercised.
  tags: [term, training-stage]

- id: g12
  term: multi-teacher OPD (on-policy distillation)
  type: core-concept
  source_chapter: Abstract/p.1; Intro/p.2; p.5 §4.2
  author_definition: |
    First post-training stage: a multi-teacher distillation strategy that strengthens
    general language and vision-language capabilities while preserving omni-modal
    understanding. Stronger EXTERNAL teachers supervise text / vision-language tasks;
    same-model-family teachers retain audio and AV abilities; cross-modal distillation
    transfers text knowledge to audio tasks.
  key_distinction: |
    ≠ single-teacher distillation — teacher is chosen per capability, and "on-policy"
      means it distills the model's own current outputs.
    ≠ generic knowledge boost — explicitly structured to avoid degrading AV ability.
  why_it_matters: |
    The transferable rule "match teacher choice to the capability you are protecting"
    (same-family teachers preserve AV) is directly reusable by an operator.
  tags: [term, core-concept, transferable-pattern]

- id: g13
  term: anti-repetition MrDPO (multi-round direct preference optimization)
  type: core-concept
  source_chapter: Abstract/p.1; Intro/p.2; p.5 §4.2
  author_definition: |
    Second post-training stage: iteratively optimizes the model against offline-mined
    hard-negative samples exhibiting repetitive/endless decoding across video, audio,
    and vision-language tasks. Offline mining is used because these degeneration cases
    are rare and online methods capture them inefficiently.
  key_distinction: |
    ≠ general alignment DPO — narrowly targets generation degeneration (repetition,
    over-long traces) that survives pre-training and OPD and would obstruct RL.
    Uses OFFLINE mining, not online.
  why_it_matters: |
    Encodes the principle "fix degeneration before RL" — a failure-mode-ordered
    post-training checklist item.
  tags: [term, core-concept, transferable-pattern]

- id: g14
  term: LoRA adapter merge/reinit
  type: term
  source_chapter: p.5 §4.2 (Anti-Repetition MrDPO)
  author_definition: |
    Stability mechanism in MrDPO: only LoRA adapters are updated in each round, then
    merged into the model and reinitialized between successive rounds.
  key_distinction: |
    ≠ full-weight fine-tuning — low-rank updates keep each round stable;
    ≠ a single continuous LoRA — adapters are merged then reinitialized per round.
  why_it_matters: |
    A concrete technique an operator can reuse to run many optimization rounds without
    drift or catastrophic forgetting.
  tags: [term, technique]

- id: g15
  term: specialist RL
  type: core-concept
  source_chapter: Abstract/p.1; p.5 §4.2; BOOK_OVERVIEW §4
  author_definition: |
    Final post-training stage: reinforcement learning to boost challenging downstream
    abilities (audio-visual speaker ID, video-soundtrack matching, structured music
    understanding, complex AV reasoning). Training instances are curated by offline
    inference/evaluation, discarding samples the model already solves reliably.
  key_distinction: |
    ≠ generic RLHF — targeted at hard, filtered tasks and extended with long-context
    training (more video frames / longer sequences).
  why_it_matters: |
    Third link in the failure-mode-ordered chain: general capability (OPD) →
    generation stability (MrDPO) → specialized skill (RL).
  tags: [term, core-concept, transferable-pattern]

- id: g16
  term: dynamic reward router
  type: term
  source_chapter: p.5 §4.2 (Specialist RL)
  author_definition: |
    Component that assigns task-specific rewards during specialist RL, selecting the
    appropriate reward type according to whether the task is verifiable/deterministic
    or open-ended.
  key_distinction: |
    ≠ a single fixed reward function — routing is by task verifiability.
  why_it_matters: |
    Operational rule for reward design: match reward signal to task nature rather than
    applying one objective everywhere.
  tags: [term, technique, transferable-pattern]

- id: g17
  term: rule-based / rubric-based / teacher-consistency rewards
  type: term
  source_chapter: p.5 §4.2 (Specialist RL)
  author_definition: |
    Reward types combined in specialist RL: rule-based rewards for deterministic
    (verifiable) tasks; rubric-based and teacher-consistency rewards for open-ended
    tasks (the latter scored against teacher outputs).
  key_distinction: |
    ≠ interchangeable — rule for verifiable, rubric/teacher-consistency for open-ended.
  why_it_matters: |
    Directly answers "how to route rewards for verifiable vs open-ended tasks".
  tags: [term, technique]

- id: g18
  term: 35B-A3B MoE  **[UNDEFINED IN SOURCE]**
  type: model-variant
  source_chapter: README Model Zoo/Overview; p.1–2; BOOK_OVERVIEW §2
  author_definition: |
    The flagship variant — a Mixture-of-Experts model ("35B-A3B"), built on
    Qwen3.6-35B-A3B, described in the README as a mixture-of-experts model with 2B/4B/9B
    dense siblings. Conventional reading: 35B total parameters, ~3B activated per token.
  key_distinction: |
    The source uses "35B-A3B" and "mixture-of-experts" but NEVER defines the naming
    convention (total vs. active params) or the routing architecture. Do not assert the
    35B/3B split as a sourced fact — treat it as industry-standard inference only.
  why_it_matters: |
    Serving implication (sourced): for 35B-A3B BF16, plan memory for the FULL expert
    weights and set --tensor-parallel-size; activation size ≠ memory footprint.
  tags: [term, model-variant, flagged-undefined]

- id: g19
  term: FP8 Block128 / AWQ W4A16 / GGUF Q4_K_M / NVFP4 W4A16  **[UNDEFINED IN SOURCE]**
  type: quantization-format
  source_chapter: README Model Zoo & "Choose a runtime"; docs/serving.md "Runtime profiles"
  author_definition: |
    The four released quantization formats per model size, each bound to a serving
    runtime: BF16 (Transformers / patched vLLM / patched SGLang); FP8 Block128 (patched
    vLLM 0.18 on FP8-capable GPU); AWQ W4A16 (patched vLLM 0.18 with compressed-tensors);
    GGUF Q4_K_M (native llama.cpp runtime, CPU/CUDA); NVFP4 W4A16 (patched vLLM 0.31
    with ModelOpt Mixed Precision + Marlin).
  key_distinction: |
    These are named and mapped to runtimes but NEVER actually defined in any source
    (no bit-width/block-size/accuracy explanation). "W4A16"/"W4A16 NVFP4" etc. should not
    be glossed with invented detail.
  why_it_matters: |
    The operator's first decision is checkpoint format → runtime pairing; picking the
    wrong engine (e.g. GGUF on vLLM) will not work.
  tags: [term, quantization, flagged-undefined]
```

## Coverage / self-check
- 19 terms: all core concepts + training stages + architecture + serving formats.
- `author_definition` uses near-verbatim source phrasing (paper pp.1–5).
- `key_distinction` states the common-sense/dictionary trap for each (highest-value field).
- `why_it_matters` ties each term to a downstream operator/skill decision.
- Flagged as used-but-never-defined: **35B-A3B MoE** (g18) and the four quantization
  format names (g19). The paper also uses "omni-modal" and "hybrid-thinking" as
  framing labels without a formal one-sentence definition; definitions here are
  synthesized from their contextual use and marked accordingly.
