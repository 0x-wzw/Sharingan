## R — Reading (source)

"verifiable audio-visual reasoning data is naturally scarce in the wild. To bridge this gap, we curate... via a dual strategy: large-scale vision-language STEM and knowledge reasoning datasets augmented with high-quality thinking traces, alongside a curated set of native audio-visual reasoning tasks." (paper p.4 §3)

## I — Interpretation

When verifiable reasoning data is scarce in the target modality, synthesizing it from scratch gives shallow traces. Combine a large adjacent-domain corpus that already contains strong reasoning traces with a smaller set of genuinely native target-modality tasks: the adjacent corpus teaches reasoning shape, the native set grounds it. Transfer reasoning across modalities instead of manufacturing scarce native data.

## A1 — Application Example

Source case (paper p.4): VL STEM/knowledge QA with thinking traces plus curated native AV reasoning tasks, credited with transferring reasoning into omni-modal scenarios. Dataset names, sizes and trace criteria undisclosed.

## A2 — Future Trigger

Use when collecting training data for a new modality or when verifiable reasoning data is too scarce. Signals: 'not enough data', 'transfer reasoning', 'scarce labels', 'data strategy for new modality'. Distinct from progressive-modality-curriculum and from the needs-review caption pipeline.

## E — Execution

1. Identify a rich adjacent domain with traces — completion: named corpus. 2. Curate small verifiable native target set — completion: tasks with answers. 3. Mix with an explicit ratio — completion: ratio declared as local decision. 4. Check transfer on native held-out task — completion: improvement without adjacent-only overfitting.

## B — Boundary

Not when native verifiable data is plentiful; not a substitute for a real target encoder. No mixture ratio given. Router card.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
