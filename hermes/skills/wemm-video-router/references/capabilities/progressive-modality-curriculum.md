## R — Reading (source)

"only the audio aligner is optimized, while the backbone LLM and modality encoders remain frozen... we unfreeze all model parameters except the visual encoder... In the final pre-training stage, we maintain the same trainable parameter configuration while further scaling the context window." (paper pp.4–5 §4.1)

## I — Interpretation

Adding a new modality to a strong pretrained model fails when you fine-tune everything at once: the new signal is weak and the old encoder's priors get overwritten. Stage 1 trains only the new modality's aligner on simple paired data under a short context while the backbone and existing encoders are frozen. Stage 2 widens context and unfreezes everything except the encoder that is already good enough — that encoder stays as a fixed anchor. Stage 3 keeps the same trainable set and only lengthens sequences, so long-range dependencies are learned without another parameter change. Rule: align first, unfreeze progressively, scale context last.

## A1 — Application Example

Source case (paper pp.4–5): WeMM-Video Stage 1 trains only the window-level Q-Former on audio-text pairs; Stage 2 unfreezes all but the native visual encoder on mixed text/visual/audio/AV data; Stage 3 scales to long videos and multi-video inputs. Preserved visual competence plus omni-modal comprehension is reported; no ablation isolates each stage.

## A2 — Future Trigger

Use when adding a new input modality (audio, sensor, time series) to an existing model without losing current capability, or when a fine-tune degraded an existing benchmark. Signals: 'add modality without breaking', 'catastrophic forgetting', 'which layers to freeze', 'curriculum for fine-tuning'. Distinct from anti-repetition-loop (generation degeneration) and scarce-modality-data-transfer (data strategy).

## E — Execution

1. Inventory encoders and name the one whose priors must survive — completion: frozen-encoder list. 2. Stage 1: train only the new aligner on paired data with compact context — completion: new modality works, frozen benchmarks unchanged. 3. Stage 2: expand context, unfreeze all except the marked encoder — completion: joint-modality task passes. 4. Stage 3: hold trainable set, scale sequence length — completion: long-input task passes with no regression. Stop: if frozen-encoder benchmark drops, return to Stage 2.

## B — Boundary

Not for training from scratch or for a new task format on an existing modality. Exact context sizes, token counts and per-stage mixture ratios are undisclosed — do not invent them. Benchmark deltas are source-reported, not causally attributed.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
