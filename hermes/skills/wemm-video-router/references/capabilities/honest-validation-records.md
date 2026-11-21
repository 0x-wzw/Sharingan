## R — Reading (source)

"A completed source build is pending." / "GPU generation after downloading a checkpoint from the Hub is pending." (docs/serving.md Validation, lines 148–158)

## I — Interpretation

A validation report that omits unfinished checks reads as success and misleads the next operator. Every validation scope must carry an explicit status, with uncompleted work marked pending rather than promoted to pass or dropped. Bundle components (GGUF runtime, tokenizer, processor) must come from the same repository and revision so a pass refers to a coherent artifact set.

## A1 — Application Example

Source case (docs/serving.md Validation): offline rebuild, hash checks, loopback HTTP checks and GGUF CPU smoke test recorded as passed; a completed source build and GPU generation explicitly pending.

## A2 — Future Trigger

Use when asked whether a system is verified, or when writing a test report that must not overclaim. Signals: 'is it verified', 'validation status', 'what has not been tested'. Distinct from dimension-based-evaluation and weight-format-runtime-matrix.

## E — Execution

1. List validation scopes — completion: table with no implicit scopes. 2. Record pass/fail/pending with exact check — completion: every row has status and evidence. 3. Mark uncompleted as pending, never inferred — completion: no silent rows. 4. Record artifact revision per component — completion: same-revision proof. 5. Publish with pending rows intact — completion: reader sees what is unproven.

## B — Boundary

Pending is not a pass and not a substitute for running the check. Do not soften a genuine failure. Router card.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
