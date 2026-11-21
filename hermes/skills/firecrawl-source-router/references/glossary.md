# Firecrawl 术语表 — 源 @ 41b36df

### Firecrawl Local (g01)

"scrapes, crawls and maps from your own machine without a database, queue or container, and it reaches Firecrawl Cloud when your AI agents need search or Alexandria." gloss: A single Rust binary that does scraping/crawling/mapping on your machine with no infrastructure, delegating search and Alexandria to the cloud. key_distinction: | ≠ "the full server self-hosted" — no DB, queue or container ≠ "cloud-only" — scrape/crawl/map run locally; only search/Alexandria go to Cloud why_it_matters: Skills must route "run it myself" to the Local binary, not the Compose server stack, and know which features need Cloud or login.

- 释义：A single Rust binary that does scraping/crawling/mapping on your machine with no infrastructure, delegating search and Alexandria to the cloud.
- 主题：operational
- 来源：`README.md:58`

### Firecrawl Cloud (g02)

"runs everything Firecrawl Local does at scale, with no browser or machine of your own to look after. It also gives your AI agents access to far more knowledge than scraping alone, with search, Alexandria, Interact and Agent all through a single API." gloss: The hosted service that runs all features at scale with no local machine to manage, adding search, Alexandria, Interact and Agent. key_distinction: | ≠ "just a hosted scraper" — a superset of Local plus search, Alexandria, Interact, Agent ≠ "requires signup for everything" — keyless tier gives 1,000 free credits/month (README.md:144) why_it_matters: Attributes agent/scale/search features to Cloud, and notes that Local reads may silently fall back to it.

- 释义：The hosted service that runs all features at scale with no local machine to manage, adding search, Alexandria, Interact and Agent.
- 主题：operational
- 来源：`README.md:138`

### LLM-ready output (g03)

"LLM-ready output. Clean markdown, structured JSON, screenshots and more, so your AI agents spend fewer tokens." gloss: Firecrawl's clean, model-friendly result formats (markdown, structured JSON, screenshots) that minimize tokens consumed by agents. key_distinction: | ≠ "raw HTML" — the point is cleaned, concise content = the stated reason markdown is the default return format why_it_matters: Justifies the build-scrape default "Return markdown unless the feature truly needs another format" (scrape/SKILL.md:33).

- 释义：Firecrawl's clean, model-friendly result formats (markdown, structured JSON, screenshots) that minimize tokens consumed by agents.
- 主题：scraping-extraction
- 来源：`README.md:142`

### /scrape (g04)

"| `/scrape` | You already have the URL and need one page | The feature starts with a query |" gloss: The single-page extraction endpoint for a known URL; the default first choice for product integrations. key_distinction: | ≠ "/search" — search starts from a query, scrape from a known URL ≠ "/interact" — clicks/forms/navigation after scraping (endpoint-selection.md:13) = "the default extraction primitive before considering /interact" (scrape/SKILL.md:29) why_it_matters: Endpoint selection is the first routing decision in every build skill; misrouting wastes cost and complexity.

- 释义：The single-page extraction endpoint for a known URL; the default first choice for product integrations.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build/references/endpoint-selection.md:11`

### /search (g05)

"| `/search` | The feature starts with a query and must discover sources | The target URL is already known |" gloss: Query-first discovery endpoint that finds web pages and can return their full content; second in the default priority order. key_distinction: | ≠ "queries the research or developer indexes" — neither index is queried by /search (endpoint-selection.md:28) = "Treat /search as discovery, ranking, and source selection" (search/SKILL.md:55) why_it_matters: Skills must not promise paper/issue search via /search; `categories: ["research"]` is only a website filter.

- 释义：Query-first discovery endpoint that finds web pages and can return their full content; second in the default priority order.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build/references/endpoint-selection.md:12`

### /interact (g06)

"| `/interact` | The page must be clicked, typed into, or navigated after scrape | Plain `/scrape` already returns the data |" gloss: Browser-action endpoint for pages needing clicks, typing, forms or navigation after the scrape; last in the escalation chain. key_distinction: | ≠ "default" — "Start with /scrape before /interact" (endpoint-selection.md:23) = "the right tool when the page must be manipulated, not just read" (interact/SKILL.md:44) why_it_matters: Prevents reaching for browser automation when a plain read suffices; keeps integrations cheap.

- 释义：Browser-action endpoint for pages needing clicks, typing, forms or navigation after the scrape; last in the escalation chain.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build/references/endpoint-selection.md:13`

### research paper index (g07)

"Research paper index | The query is for published research papers — biomedical, clinical, and life-science literature (PubMed, bioRxiv, medRxiv) or arXiv preprints — rather than web pages | MCP `firecrawl_research_*`, CLI `firecrawl research <subcommand>`." gloss: A dedicated index for published papers (PubMed/bioRxiv/medRxiv/arXiv) reached via MCP or CLI, not ordinary /search. key_distinction: | ≠ "`categories: ["research"]` on /search" — that only filters web search to research sites (endpoint-selection.md:35) = a separate surface with abstract search and related-paper expansion why_it_matters: A confusion the corpus explicitly warns about; paper queries must go to the index, not a filtered web search.

- 释义：A dedicated index for published papers (PubMed/bioRxiv/medRxiv/arXiv) reached via MCP or CLI, not ordinary /search.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build/references/endpoint-selection.md:32`

### developer index (g08)

"Developer index | The answer belongs in an issue, merged pull request, README, or documentation page: code behavior, an API contract, an error string, a known bug | `GET` or `POST /v2/search/developer`, MCP `firecrawl_developer_search`, CLI `firecrawl developer`." gloss: A dedicated index over issues, PRs, READMEs and docs for code behavior, API contracts, error strings and bugs. key_distinction: | ≠ "`categories: ["developer"]` on /search" — a domain filter, not index access (search/SKILL.md:51) ≠ "generic web search" — targets developer artifacts specifically why_it_matters: Code-question skills must pick this index to get issue/PR-level evidence.

- 释义：A dedicated index over issues, PRs, READMEs and docs for code behavior, API contracts, error strings and bugs.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build/references/endpoint-selection.md:33`

### freshness (g09)

"**Freshness** — how old is this content? Controlled by `maxAge`." gloss: How old the returned content is; governed by maxAge and reported in response metadata. key_distinction: | ≠ "liveness" — whether the described thing is still active, a source-specific judgment (freshness-and-liveness.md:6-7) = a property of the cached copy, not the real-world entity why_it_matters: The corpus insists the two questions stay separate in code; conflating them misleads downstream decisions.

- 释义：How old the returned content is; governed by maxAge and reported in response metadata.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build-scrape/references/freshness-and-liveness.md:5`

### liveness (g10)

"**Liveness** — is the thing the page describes still active? A source-specific judgment your application makes from the content." gloss: Whether the real-world item a page describes is still active; the application decides from page evidence. key_distinction: | ≠ "a successful fetch" — "200 plus non-empty content means the fetch succeeded, not that the item described by the page is still active" (freshness-and-liveness.md:43-45) ≠ freshness — that is about content age = keep state `unknown` when evidence is inconclusive (freshness-and-liveness.md:50) why_it_matters: Stops skills treating a 200 as proof an entity is live; the correct fallback is `unknown`.

- 释义：Whether the real-world item a page describes is still active; the application decides from page evidence.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build-scrape/references/freshness-and-liveness.md:6`

### maxAge (g11)

"`maxAge` is the maximum age, in milliseconds, of an indexed copy that `/scrape` may return." gloss: A millisecond bound on how old a reused indexed copy may be; omit for Firecrawl's per-domain default, set 0 to force a live scrape. key_distinction: | ≠ "a cache TTL you configure" — a maximum acceptable age of reuse = `maxAge: 0` skips reuse and takes the live path, costing latency (freshness-and-liveness.md:18-21) = `/parse` ignores it and is always uncached (freshness-and-liveness.md:23-24) why_it_matters: Skills tuning reads need the exact 0 semantics and the /parse exception.

- 释义：A millisecond bound on how old a reused indexed copy may be; omit for Firecrawl's per-domain default, set 0 to force a live scrape.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build-scrape/references/freshness-and-liveness.md:12`

### cacheState (g12)

"`cacheState` — `"hit"` or `"miss"`, present only when index reuse was eligible. With `maxAge: 0` the field is absent, which is itself the confirmation that no indexed copy was used." gloss: Response metadata saying whether a reused copy was served; absence under maxAge:0 confirms a live fetch. key_distinction: | ≠ "always present" — absent when index reuse was not eligible ≠ a liveness signal — says nothing about whether the entity is active why_it_matters: Gives code a concrete way to verify what it actually got, a recurring scrape-skill instruction.

- 释义：Response metadata saying whether a reused copy was served; absence under maxAge:0 confirms a live fetch.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build-scrape/references/freshness-and-liveness.md:30`

### Change Tracking (g13)

"Change Tracking allows you to monitor website changes by comparing the current scrapes and crawls to previous versions, clearly indicating if content is new, unchanged, modified, or removed." gloss: A feature that diffs current scrapes/crawls against previous versions and labels content new, same, changed or removed. key_distinction: | ≠ "generic diffing" — scoped by URL, team ID and markdown format (change-tracking.md:154) = resilient to whitespace/order changes; ignores iframe source URLs (change-tracking.md:156-157) = requires the `markdown` format in addition to `changeTracking` (change-tracking.md:27) why_it_matters: A distinctive capability with non-obvious setup constraints skills must convey.

- 释义：A feature that diffs current scrapes/crawls against previous versions and labels content new, same, changed or removed.
- 主题：scraping-extraction
- 来源：`apps/test-site/src/content/blog/launch-week-iii-day-1-introducing-change-tracking.md:13`

### FIRE-1 (g14)

"FIRE-1 brings a new level of intelligence to Firecrawl, enhancing your scraping tasks by navigating complex website structures, interacting with dynamic content, and more. This powerful AI agent ensures comprehensive data extraction beyond traditional scraping methods." gloss: Firecrawl's web action agent that navigates and clicks to reach data hidden behind logins, buttons, modals or pagination. key_distinction: | ≠ "plain scraper" — "This agent doesn't just scrape — it takes actions" (fire-1.md:15) ≠ "zero-config" — for scrape requests the `prompt` field is required (fire-1.md:35) = may consume more credits with task complexity (fire-1.md:59) why_it_matters: Powers /extract v2 and MCP agent support; enable only when interaction is needed and warn about prompt/credit costs.

- 释义：Firecrawl's web action agent that navigates and clicks to reach data hidden behind logins, buttons, modals or pagination.
- 主题：agent-MCP
- 来源：`apps/test-site/src/content/blog/launch-week-iii-day-2-announcing-fire-1.md:13`

### firecrawl-build (build skill) (g15)

"Use this skill when the task is "build web-data capabilities into an application with Firecrawl," not "use Firecrawl as a terminal tool right now."" gloss: The parent agent skill for integrating Firecrawl into application code, as opposed to one-off live web work via the CLI. key_distinction: | ≠ "firecrawl/cli" — CLI is for one-off research/terminal work (firecrawl-build/SKILL.md:43,131-133) = triggers even when the user never names Firecrawl but describes app-level web-data needs (SKILL.md:30) why_it_matters: The build-vs-CLI boundary is the primary routing rule of the skills catalog.

- 释义：The parent agent skill for integrating Firecrawl into application code, as opposed to one-off live web work via the CLI.
- 主题：operational
- 来源：`skills/firecrawl-build/SKILL.md:28`

### narrowest endpoint (g16)

"Route from that answer to the narrowest endpoint that fits:" gloss: Choose the least powerful endpoint that does the job; default order /scrape, /search, /interact. key_distinction: | ≠ "use the most capable endpoint" — escalation is one-way and deliberate (endpoint-selection.md:15-24) = "Default priority for most product integrations" (endpoint-selection.md:15) why_it_matters: Central selection doctrine reused across firecrawl-build, -scrape, -search and -interact skills.

- 释义：Choose the least powerful endpoint that does the job; default order /scrape, /search, /interact.
- 主题：scraping-extraction
- 来源：`skills/firecrawl-build/SKILL.md:58`

### source-of-truth pages (g17)

"are the canonical source of truth for SDK usage, request/response schemas, parameters, and endpoint behavior. Read the page that matches the project language before writing integration code:" gloss: Per-language docs pages at docs.firecrawl.dev/agent-source-of-truth/* that are authoritative for schemas and call details; skills cover when/why, not how. key_distinction: | ≠ "the SKILL.md itself" — "These skills describe when and why to use each endpoint. For how to call them, read the source-of-truth page" (SKILL.md:109-110) = a distinct URL per language (node, python, rust, java, elixir, curl) why_it_matters: Prevents skills from hallucinating SDK call syntax; defer to these pages for request/response details.

- 释义：Per-language docs pages at docs.firecrawl.dev/agent-source-of-truth/* that are authoritative for schemas and call details; skills cover when/why, not how.
- 主题：operational
- 来源：`skills/firecrawl-build/SKILL.md:98`

### smoke test (g18)

"Do not stop at "the code compiles." Verify that a real Firecrawl request works." gloss: A minimal real Firecrawl call proving auth, networking and SDK wiring; the final step of the default integration order. key_distinction: | ≠ "build/compile success" — explicitly not enough = "Run a smoke test that proves a real Firecrawl request succeeds" (firecrawl-build/SKILL.md:121) why_it_matters: Encodes the verification bar every integration skill must enforce before declaring done.

- 释义：A minimal real Firecrawl call proving auth, networking and SDK wiring; the final step of the default integration order.
- 主题：operational
- 来源：`skills/firecrawl-build/references/verification.md:3`

### fresh project vs existing project (g19)

"Before implementing Firecrawl in product code, classify the task:" gloss: Mandatory first intake split: greenfield picks stack/SDK/env; brownfield inspects repo conventions first and integrates in place. key_distinction: | ≠ "skip classification" — step 1 of Required Intake (firecrawl-build/SKILL.md:73) = existing projects must match "existing project conventions, not wherever is easiest in the moment" (project-intake.md:41) why_it_matters: Stops skills imposing greenfield defaults on established codebases.

- 释义：Mandatory first intake split: greenfield picks stack/SDK/env; brownfield inspects repo conventions first and integrates in place.
- 主题：operational
- 来源：`skills/firecrawl-build/references/project-intake.md:3`

### Alexandria (g20)

"gives your AI agents 550+ data providers in one library (250M+ people, 75M+ companies, 41M+ research papers), plus specialized indexes and the live web, through one API, MCP or CLI. AI agents discover a tool alongside their web results, inspect its inputs and pricing, then run it to get structured data. Discovery is free, and running a tool uses the credits listed on it." gloss: A cloud library of 550+ data providers that agents discover and run through one API/MCP/CLI, with free discovery and paid execution. key_distinction: | ≠ "scraping" — structured data from providers = Cloud-only; "the self-hosted server does not include it" (README.md:579) = discovery free and not counted toward creditsUsed (alexandria/README.md:16-17) why_it_matters: Distinguishes provider-tool workflows from scraping and sets cloud-only/free-discovery expectations.

- 释义：A cloud library of 550+ data providers that agents discover and run through one API/MCP/CLI, with free discovery and paid execution.
- 主题：agent-MCP
- 来源：`README.md:431`

### MCP server (Firecrawl) (g21)

"Today, we're rolling out a major set of updates to our Firecrawl MCP server — our implementation of the Model Context Protocol (MCP) that powers scraping workflows with LLMs and web data." gloss: Firecrawl's Model Context Protocol implementation exposing scraping/extraction tools to LLM agents and MCP clients. key_distinction: | ≠ "the CLI build skills" — MCP connects external agents (Claude, Gemini, OpenAI) (README.md:443-457) = Local's `init` registers it with local agents (README.md:92-98); supports SSE and FIRE-1 (mcp blog:13-26) why_it_matters: Primary delivery path to agents; route agent-MCP requests here, not to app-code integration.

- 释义：Firecrawl's Model Context Protocol implementation exposing scraping/extraction tools to LLM agents and MCP clients.
- 主题：agent-MCP
- 来源：`apps/test-site/src/content/blog/launch-week-iii-day-6-firecrawl-mcp.md:11`

### Agent (Firecrawl agent endpoint) (g22)

"Describe what you need, and our AI agent searches, navigates and retrieves it with no URLs required." gloss: A prompt-driven endpoint where an AI agent autonomously searches, navigates and returns an answer with sources, optionally structured via a schema. key_distinction: | ≠ "/search" — no URL needed; returns a result plus sources, not a page list = "the `spark-2` model" and effort levels are documented separately (README.md:368) why_it_matters: Distinct autonomous retrieval surface; must not be conflated with /search or /scrape.

- 释义：A prompt-driven endpoint where an AI agent autonomously searches, navigates and returns an answer with sources, optionally structured via a schema.
- 主题：agent-MCP
- 来源：`README.md:323`

### NuQ PostgreSQL (g23)

"**Queue: NuQ PostgreSQL.** Keep it unless you intentionally set `NUQ_BACKEND=fdb` and are prepared to operate FoundationDB." gloss: The default PostgreSQL-backed queue in the self-hosted stack; the safe baseline unless you deliberately switch to FoundationDB. key_distinction: | ≠ "an optional add-on" — the recommended default queue backend (SELF_HOST.md:29-30) = switching to `fdb` means operating FoundationDB yourself why_it_matters: Self-hosting advice must preserve the baseline queue choice and flag the operational cost of changing it.

- 释义：The default PostgreSQL-backed queue in the self-hosted stack; the safe baseline unless you deliberately switch to FoundationDB.
- 主题：operational
- 来源：`SELF_HOST.md:29`

### baseline (self-hosting) (g24)

"Get this baseline working before swapping backends or adding providers." gloss: The minimal supported self-hosted setup (exact tag, auth off, NuQ PostgreSQL, bundled Playwright, no AI provider) that must work before customization. key_distinction: | ≠ "production-ready" — "The checked-in Compose file is a source-aligned starting point, not a production architecture" (SELF_HOST.md:67-68) = deliberately unauthenticated by default; adding auth is a separate design task (SELF_HOST.md:25-28,55-56) why_it_matters: Frames self-hosting guidance: stabilize the simple baseline first, never imply the default Compose file is secure or production complete.

- 释义：The minimal supported self-hosted setup (exact tag, auth off, NuQ PostgreSQL, bundled Playwright, no AI provider) that must work before customization.
- 主题：operational
- 来源：`SELF_HOST.md:38`
