# Engine Forcing 3

R — Source anchor
Engine forcing：模式语义与 3 步优先级. Verified in Firecrawl @ 41b36df at apps/api/src/scraper/WebScraper/utils/ENGINE_FORCING.md. verified under V1/V2/V3.

I — Interpretation


A1 — Source example
> 1. **Exact domain match**: `"example.com"` matches `example.com` and all its subdomains (`www.example.com`, `api.example.com`, etc.)
> 2. **Wildcard pattern**: `"*.subdomain.com"` matches only subdomains of `subdomain.com` (e.g., `api.subdomain.com`, `www.subdomain.com`) but NOT the base domain itself

A2 — Operational rule
Apply this capability when its trigger matches; follow the source-defined order; record the evidence for each decision. Do NOT extend it to cases the source does not cover.

E — Execution
Input: a task matching the capability's trigger. Steps: (1) restate the trigger check, (2) apply the source-defined rule in order, (3) record evidence and outcome. Output: a decision with its evidence reference. Completion: every step traced to a source line; gaps marked explicitly.

B — Boundary
Not for tasks outside the cited source's scope. Static/walkthrough verification only — this bundle has not run the Firecrawl service. T1 (first scrape) and T6 (agent/MCP full onboarding) are explicit external-doc gaps and are NOT covered here.
