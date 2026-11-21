## R — Reading (source)

"audio inputs sampled at 16,000 Hz and segmented into 30-second chunks. The window-level Q-Former then compresses these features within local temporal windows of 0.1 seconds... yielding 10 audio tokens per second." (paper p.3 §2)

## I — Interpretation

A continuous signal has unbounded token cost unless you fix a sampling contract: resample to a fixed rate, chunk into fixed lengths, then compress within local windows to exactly one token per window, giving a constant tokens-per-second budget identical across model sizes. Predictable budgets make context planning and cross-modal interleaving tractable.

## A1 — Application Example

Source case (paper p.3): 16 kHz → 30 s chunks → 0.1 s Q-Former windows → 10 tokens/s across all variants; Q-Former is the Stage-1 aligner. No alternative window size ablated.

## A2 — Future Trigger

Use when feeding audio or another continuous signal into an LLM, or budgeting tokens for a streaming sensor. Signals: 'audio tokens', 'token rate', 'continuous signal to LLM', 'frame sampling budget'. Distinct from timestamped-token-interleaving (ordering) and progressive-modality-curriculum (schedule).

## E — Execution

1. Fix sample rate and chunk length — completion: both recorded. 2. Choose a local window mapped to one token — completion: tokens/second = 1/window. 3. Verify constant rate across sizes — completion: same rate everywhere. 4. Compute budget = seconds × rate — completion: budget for target clip length.

## B — Boundary

Not evidence that 0.1 s is optimal; no ablation. Do not extend the numbers to other signals without re-deriving. Router card.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
