# Verification Done Criteria

R — Source anchor
Verification done-criteria：编译不算，需真实请求. Verified in Firecrawl @ 41b36df at skills/firecrawl-build/references/verification.md. verified under V1/V2/V3.

I — Interpretation
|

A1 — Source example
> "Do not stop at \"the code compiles.\" Verify that a real Firecrawl request works... What Counts As Done: credentials are loaded from .env or the deployment secret store; the chosen endpoint succeeds once with real data; the result reaches the intended application path; obvious auth or base-URL mist
> summary: |

A2 — Operational rule
Apply this capability when its trigger matches; follow the source-defined order; record the evidence for each decision. Do NOT extend it to cases the source does not cover.

E — Execution
Input: a task matching the capability's trigger. Steps: (1) restate the trigger check, (2) apply the source-defined rule in order, (3) record evidence and outcome. Output: a decision with its evidence reference. Completion: every step traced to a source line; gaps marked explicitly.

B — Boundary
Not for tasks outside the cited source's scope. Static/walkthrough verification only — this bundle has not run the Firecrawl service. T1 (first scrape) and T6 (agent/MCP full onboarding) are explicit external-doc gaps and are NOT covered here.
