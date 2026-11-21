# Before Production Conditional Hardening Checklis

R — Source anchor
Before production: conditional hardening checklist. Verified in Firecrawl @ 41b36df at SELF_HOST.md:52-71. verified under V1/V2/V3.

I — Interpretation
|

A1 — Source example
> "## Before production
> - **If the API will leave a trusted network,** add a complete authentication design, TLS termination, and network policy first. The default API is unauthenticated.

A2 — Operational rule
Apply this capability when its trigger matches; follow the source-defined order; record the evidence for each decision. Do NOT extend it to cases the source does not cover.

E — Execution
Input: a task matching the capability's trigger. Steps: (1) restate the trigger check, (2) apply the source-defined rule in order, (3) record evidence and outcome. Output: a decision with its evidence reference. Completion: every step traced to a source line; gaps marked explicitly.

B — Boundary
Not for tasks outside the cited source's scope. Static/walkthrough verification only — this bundle has not run the Firecrawl service. T1 (first scrape) and T6 (agent/MCP full onboarding) are explicit external-doc gaps and are NOT covered here.
