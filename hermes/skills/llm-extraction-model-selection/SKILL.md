---
name: llm-extraction-model-selection
description: |
  Use when schema-driven model selection for llm extraction. Source-grounded from Firecrawl @ 41b36df.
version: 1.0.0
license: MIT
metadata:
  author: Cangjie Distillation <agent@example.com>  # source: Firecrawl contributors
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.capability-id: cap.firecrawl.f07
  cangjie.capability-revision: 1
  cangjie.bundle-id: bundle.firecrawl
  cangjie.source-title: "Firecrawl repository @ 41b36df"
  cangjie.tags: firecrawl, distilled, stage-1.5
---
# Schema Driven Model Selection For Llm Extraction

R — Source anchor
Schema-driven model selection for LLM extraction. Verified in Firecrawl @ 41b36df at apps/api/src/scraper/scrapeURL/transformers/llmExtract.ts:38-75. verified under V1/V2/V3.

I — Interpretation


A1 — Source example
> import { aiTelemetry } from "../../../lib/ai-telemetry";
> // Smart model selection based on schema

A2 — Operational rule
Apply this capability when its trigger matches; follow the source-defined order; record the evidence for each decision. Do NOT extend it to cases the source does not cover.

E — Execution
Input: a task matching the capability's trigger. Steps: (1) restate the trigger check, (2) apply the source-defined rule in order, (3) record evidence and outcome. Output: a decision with its evidence reference. Completion: every step traced to a source line; gaps marked explicitly.

B — Boundary
Not for tasks outside the cited source's scope. Static/walkthrough verification only — this bundle has not run the Firecrawl service. T1 (first scrape) and T6 (agent/MCP full onboarding) are explicit external-doc gaps and are NOT covered here.
