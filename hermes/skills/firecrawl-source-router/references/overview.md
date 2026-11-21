# BOOK_OVERVIEW — firecrawl (source-code corpus)

> "Book" here means the checked-out repository at HEAD `41b36df`. Every claim below is anchored to a file in the source manifest.

## 1. Structure (Adler: what is in it)

The repo is a monorepo with four functional regions:

- **`apps/api`** — the actual API and workers; the operational core. `AGENTS.md:1-4` says so explicitly: "Firecrawl is a web scraper API. The directory you have access to is a monorepo: `apps/api` has the actual API and worker code / `apps/*-sdk` are various SDKs."
- **`apps/*-sdk`** — Python, JS, Go, Java, PHP, Rust, .NET, Ruby clients. Their READMEs are the largest markdown files after the root README, and encode the public API contract.
- **`skills/` and `firecrawl-*-skills/`** — agent-facing capabilities (`firecrawl-build`, `-scrape`, `-search`, `-interact`, `-onboarding`) with `references/` for deeper mechanics.
- **`examples/`, `apps/test-site/src/content/blog/`, `firecrawl-workflows/`** — worked recipes, launch-week announcements, and workflow patterns.

The top-level documents divide authority deliberately:
- `README.md` = product surface + quick start.
- `SELF_HOST.md:7-8` states its own scope: "Use this file when you are changing the baseline. It stays with the source, so the services and configuration match the revision you checked out." It points to external docs for first-run and product changes.
- `AGENTS.md` = contributor workflow contract (E2E `snips` first, `pnpm harness`, targeted tests, CI on PR).

## 2. Interpretation (what it argues)

Three coherent theses emerge:

**A. Source-aligned baseline over floating instructions.**
`SELF_HOST.md:22-24`: "Release: an exact tag. Review the target release's Compose file before changing it. A checkout of `main` and floating image tags can change independently." The repo treats documentation as revision-pinned, not evergreen. `SELF_HOST.md:40-41` adds a precise boundary: "The root `.env` overrides only variables referenced by `docker-compose.yaml`. Do not use `apps/api/.env.example` as a drop-in Compose contract."

**B. Simplicity first, complexity by evidence.**
`SELF_HOST.md:20-38` defines a six-item minimal baseline — exact tag, `USE_DB_AUTHENTICATION=false`, NuQ PostgreSQL, bundled Playwright with basic-fetch fallback, no model provider, queue UI off — and closes with "Get this baseline working before swapping backends or adding providers." `SELF_HOST.md:49-50` names the trade: "Self-hosting gives you source and infrastructure control. You also own security, availability, capacity, upgrades, data retention, and compliance."

**C. Expose the capability, gate the danger.**
The product surface (README) presents scrape / search / crawl / map / agent / batch as composable calls. The self-hosting doc draws hard operational boundaries: `SELF_HOST.md:54-56` "The default API is unauthenticated"; `SELF_HOST.md:57-59` no persistent volumes for NuQ PostgreSQL, Redis, RabbitMQ; `SELF_HOST.md:75-79` admin routes exist only under `BULL_AUTH_KEY`, while the internal listener needs no key and "Never publish this port."

## 3. Critique (tensions and gaps)

- **Two public docs, different jobs.** `SELF_HOST.md` explicitly delegates first-run guidance to an external URL (`docs.firecrawl.dev/contributing/self-host`). A distillation from this repo alone cannot claim a complete first-scrape procedure — that text is not in the corpus. This is a source gap, not an inference opportunity.
- **Fast-moving HEAD.** The checkout is dated 2026-11-20 and includes a commit adding `HOSTED_MCP_PROXY_SECRET`. Any claim about MCP auth must be pinned to this revision.
- **Production readiness is explicitly disclaimed.** `SELF_HOST.md:66-68`: "The checked-in Compose file is a source-aligned starting point, not a production architecture." Kubernetes and Helm examples are "versioned starting points, not as evidence that these production decisions have been made for you" (`SELF_HOST.md:70-71`).
- **Theme asymmetry.** Operational/self-host material is dense, self-critical, and revision-pinned. Agent/MCP material is thinner here — much of it lives in skills plus an external docs site. Evidence ranking must reflect this rather than flattening all three themes.

## 4. Application (what a user does with it)

Highest-value extractable methodology:
1. A **self-host baseline decision procedure** — what to keep minimal, what to add only with a named prerequisite, and which defaults are unsafe outside a trusted network.
2. A **source-vs-deployment reconciliation habit** — check the checked-out Compose/env against the docs before changing anything; treat SDK READMEs as API contract.
3. A **contributor verification loop** — E2E snips, `pnpm harness`, targeted vitest, CI.
4. **Scrape/crawl/extract mechanics** from `skills/firecrawl-build-scrape` and the LLM-extraction examples (subject to extractor evidence).
5. **Agent/MCP integration patterns** from the skills tree and MCP blog post (weakest in-repo evidence; needs external verification before promotion).

## Key tasks for coverage audit (Stage 1.5)

| ID | Key task | Expected destination |
|---|---|---|
| T1 | Decide if self-hosting fits and get a first successful scrape | external-doc gap; partial only |
| T2 | Choose and verify a revision-pinned baseline | candidate: operational framework |
| T3 | Recognize which defaults are unsafe in production | candidate: counter-examples |
| T4 | Reconcile `.env` / Compose at a given revision | candidate: principle |
| T5 | Run scrape / crawl / extract with correct parameters | candidate: framework + cases |
| T6 | Connect an agent or MCP client | candidate: cases + gap note |
| T7 | Verify a change before PR (E2E-first) | candidate: principle from AGENTS.md |
| T8 | Operate admin routes without exposing them | candidate: counter-example + principle |

## Provenance

All quotes reproduced verbatim from `$HOME/firecrawl` at HEAD `41b36dfd28ad69df7da221d1d51f3d5fb4838be3`, pinned in `source-manifest.json`.
