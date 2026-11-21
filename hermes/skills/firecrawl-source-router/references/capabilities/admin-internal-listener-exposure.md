# Publishing The Unauthenticated Admin Internal Li

R — Source anchor
Publishing the unauthenticated admin internal listener. Verified in Firecrawl @ 41b36df at see candidates. verified under V1/V2/V3.

I — Interpretation
|

A1 — Source example
> "| `ADMIN_INTERNAL_PORT` | unset | Starts a second listener on this port that serves the routes below with no key. Never publish this port. |"
> — SELF_HOST.md:86

A2 — Operational rule
Apply this capability when its trigger matches; follow the source-defined order; record the evidence for each decision. Do NOT extend it to cases the source does not cover.

E — Execution
Input: a task matching the capability's trigger. Steps: (1) restate the trigger check, (2) apply the source-defined rule in order, (3) record evidence and outcome. Output: a decision with its evidence reference. Completion: every step traced to a source line; gaps marked explicitly.

B — Boundary
Not for tasks outside the cited source's scope. Static/walkthrough verification only — this bundle has not run the Firecrawl service. T1 (first scrape) and T6 (agent/MCP full onboarding) are explicit external-doc gaps and are NOT covered here.
