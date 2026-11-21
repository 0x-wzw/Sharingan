## R — Reading (source)

"BF16 | Transformers, patched vLLM 0.18.0 or 0.31.0, or patched SGLang 0.5.16 or 0.5.19"; "FP8 Block128 | patched vLLM 0.18.0"; "GGUF Q4_K_M | native runtime on CPU or CUDA"; "NVFP4 W4A16 | patched vLLM 0.31.0..." (docs/serving.md lines 11–17)

## I — Interpretation

Serving failures often come from pairing a checkpoint format with an engine that cannot read it. Keep an explicit format→runtime→engine-version mapping plus a fixed procedure: one version per environment, dry-run the overlay, apply, verify GPU/media decoders, serve. Hash manifests and revision pinning make the mapping reproducible.

## A1 — Application Example

Source case (docs/serving.md, patch/README.md): four formats × four sizes, pinned overlays with SHA-256 manifests, Docker profiles, and a validation table that marks source builds and GPU generation pending.

## A2 — Future Trigger

Use when asked which runtime fits a quantized checkpoint or when a serving container fails. Signals: 'which runtime', 'GGUF vs AWQ', 'vLLM version', 'serving fails'. Distinct from honest-validation-records and dimension-based-evaluation.

## E — Execution

1. Read checkpoint format from config — completion: format named. 2. Select matching runtime and pinned engine version — completion: profile chosen. 3. Dry-run overlay and compare hashes — completion: version/hashes match. 4. Verify ffmpeg/ffprobe, GPU, shared libraries — completion: preflight passes. 5. Start server, hit /health — completion: healthy response.

## B — Boundary

Not a universal table; specific to pinned versions and these checkpoints. Version-pinned overlays are a maintenance liability. Router card.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
