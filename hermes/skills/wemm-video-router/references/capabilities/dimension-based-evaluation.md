## R — Reading (source)

"The evaluation is organized around five critical dimensions... incorporates 33 representative benchmarks... For existing models, we report official results where available and our own evaluations otherwise." (paper pp.6–7 §5.1, Table 1 footnotes)

## I — Interpretation

Benchmark comparison fails when metric conventions are mixed or vendor numbers are treated as locally reproduced. Fix dimensions first, select benchmarks per dimension, then apply each benchmark's footnoted metric convention (judge, subset order, lower-is-better). Mark every number as official-reported or locally reproduced, and report both inference modes for a flagship so reasoning gains are visible against non-thinking baselines. Every number carries its metric and provenance.

## A1 — Application Example

Source case (paper pp.6–13): 33 AV benchmarks over five dimensions, 32 silent-video over seven, with footnotes defining judges (GPT-4o, GPT-6-Luna), subset ordering and WER/CER. Some rows official, others the authors' own evaluations.

## A2 — Future Trigger

Use when comparing models or evaluating a new system across benchmarks, or when two reported scores conflict. Signals: 'which benchmark', 'compare models', 'metric definition', 'fair evaluation'. Distinct from honest-validation-records (completion status) and reward-routing-by-verifiability (training rewards).

## E — Execution

1. Declare dimensions for the modality — completion: list with rationale. 2. Map benchmarks to dimensions with metric/judge — completion: benchmark registry. 3. Mark each number official vs local — completion: provenance column filled. 4. Report both modes where a switch exists — completion: mode-labeled results. 5. Compare only within identical conventions — completion: no cross-convention ranking.

## B — Boundary

Not for a single-task sanity check and not a license to accept vendor numbers as neutral. Source-specific judges are not universal defaults. Benchmark deltas do not establish causal attribution.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
