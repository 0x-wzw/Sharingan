## R — Reading (source)

"For video inputs with accompanying audio, visual and audio tokens are interleaved in chronological order, supplemented with explicit textual timestamps to facilitate fine-grained cross-modal temporal alignment." (paper p.3 §2, Fig.2)

## I — Interpretation

Models fail to bind a sound to the frame that produced it when the two modalities arrive as separate blocks and time is left implicit. Give time an explicit representation in the token stream: assign each visual frame and audio window a wall-clock interval, then merge both into one sequence ordered by start time with literal timestamp tokens at boundaries. The model learns correspondence from order plus explicit time text instead of inferring alignment from juxtaposition. The transferable pattern is a shared explicit time axis before fusion.

## A1 — Application Example

Source case (paper p.3 Fig.2): 'Next is the video. <0.0 sec> <1.0 sec> ... Next is the audio.' with visual-frame and audio tokens interleaved chronologically, credited with fine-grained temporal alignment. No timestamp ablation is reported.

## A2 — Future Trigger

Use when a model misses the moment an event happens, conflates simultaneous audio and video, or when asked how to fuse two time-indexed streams. Signals: 'align audio with video', 'timestamp alignment', 'interleave streams', 'which frame matches this sound'. Distinct from fixed-rate-signal-tokenization (token budget) and progressive-modality-curriculum (training schedule).

## E — Execution

1. Assign every modality chunk a (start,end) interval — completion: all chunks timestamped. 2. Tokenize each chunk with its own encoder — completion: tokens carry source-chunk provenance. 3. Merge by start time with a declared tie-break; insert timestamp tokens at boundaries — completion: time recoverable from tokens alone. 4. Probe with a new clip asking which frame matches a sound — completion: correct match.

## B — Boundary

Not for non-temporal fusion (text+image) and not a substitute for a real audio encoder. Tie-break and sampling policy are unspecified; declare as local conventions. Do not claim hallucination reduction from this mechanism alone — the paper attributes that to thinking mode.

## Related capabilities (Stage 3 draft)

See also_read in verified.yaml.
