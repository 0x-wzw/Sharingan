## R — Reading (source)

"we apply MrDPO... using offline-mined hard-negative samples exhibiting repetitive decoding... we only update LoRA adapters during each round, merging and reinitializing them between successive rounds." (paper p.5 §4.2)

## I — Interpretation

Repetitive, endless decoding is rare in normal samples, so online preference optimization seldom sees it, and it blocks later RL. Mine degenerate generations offline first, then run rounds of DPO on those hard negatives. Each round updates only LoRA adapters; between rounds the adapters are merged and reinitialized, keeping repeated rounds stable instead of drifting. General pattern: mine rare failures offline, isolate each correction round.

## A1 — Application Example

Source case (paper p.5): offline hard negatives from video, audio and vision-language tasks; LoRA-only MrDPO rounds merged/reinitialized. Repetition persisting after pre-training and OPD is stated; no numeric before/after repetition rate is reported.

## A2 — Future Trigger

Use when outputs loop or repeat after fine-tuning, or when asked how to fix degeneration before RL. Signals: 'keeps repeating itself', 'endless generation', 'DPO made it worse', 'before RL'. Distinct from failure-mode-ordered-post-training (stage placement) and reward-routing-by-verifiability (RL rewards).

## E — Execution

1. Flag repetition/endless decoding in sampled generations — completion: hard-negative set with counts. 2. Build pairs from flagged vs normal outputs on the same prompt — completion: pairs verified by rule or human. 3. Run one MrDPO round updating only LoRA — completion: repetition probe improves. 4. Merge adapter, reinitialize — completion: merge hash recorded. 5. Repeat until probe passes, then proceed to RL.

## B — Boundary

Not for generic helpfulness alignment or intentional repetition. Detector, pair rule and round count are undisclosed; declare locally. Offline mining requires observable failures.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
