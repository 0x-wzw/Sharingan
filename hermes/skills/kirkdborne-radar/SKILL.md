---
name: kirkdborne-radar
approval_source: agent
description: Use when curating LLM and FDE signal into a daily digest.
version: 1.0.0
author: Hermes Agent
license: MIT
read_scope: profile
source: "Sharingan lightweight distill 2026-11-15 — @KirkDBorne's curation method (154-post corpus, Lurkbird mirror + fxtwitter probe)"
metadata:
  author: "Zehan Teoh <zehan@aised.net>"
  layer: operator
  stack-source: vault
  hermes:
    tags: [radar, curation, llm, fde, intelligence, sharingan]
    related_skills: [knowledge-base-builder, tetherline-doctrine, sample-and-garden]
---

# Kirk Borne Radar — LLM + FDE signal curation, his method

## Instructions

1. Scan the source list (below) for new items; dedupe against the last digest.
2. Frame each find Borne-style: **Title — subtitle**, then `Key Topics:` with 3-5
   🔶 bullets, then a one-line "why it matters for LLM/FDE practice".
3. Classify into the taxonomy and weight: LLM/GenAI, Agents/agentic, MLOps/infra,
   Data eng, Security/governance — FDE-relevant items jump the queue.
4. Pair at most one story/parable with a current event to land a principle.
5. Deliver the digest: top 5-10 finds, taxonomy-tagged, each with the link.

## When to Use

- The user asks for an AI/LLM/FDE signal scan, intel digest, or "what did Kirk Borne post"
- Building the weekly intelligence brief's LLM/FDE section
- Triaging which new resources deserve the estate's attention vs noise

## Source list (verified 2026-11-15)

- `https://lurkbird.com/KirkDBorne/` — mirror of @KirkDBorne's timeline (~154 recent posts,
  machine-parseable HTML); primary corpus
- `https://api.fxtwitter.com/KirkDBorne` — profile + identity probe (497k followers;
  "Founder of @LeadershipData … PhD Astrophysics @Caltech")
- `https://www.bytewoops.com/en/stories/…kirk-borne…` — per-post mirrors (full text + links)
- Anything Kirk surfaces is itself a source: publisher roundups (Packt et al.), book
  announcements, conference tracks

## The method being mirrored (from the 154-post corpus)

- **51% resource roundups**: "Title — subtitle: Key Topics: 🔶 … Get it here" — always
  a publisher or course, always a topics list, always a link
- **Topic mix**: LLM/GenAI 31 · Agents/agentic 25 · MLOps/infra 18 · Data eng 8 ·
  Security/governance 7 · Leadership/culture 4
- **Parable pairing**: one engineering story (the $1 chalk mark) matched to a current
  event (the Microsoft outage + "layoffs of senior engineers") to land a principle:
  expertise in reliability work is what fixes 3 AM production
- **Listicle pattern**: "20 Embedded Patterns Every Engineer Should Know" — number
  claims, cite the publisher

## FDE weighting rule

Forward-deployed relevance = the find changes what you'd DO at a customer site:
deployment patterns, RAG/fine-tuning tradeoffs, agent trust boundaries, delivery
automation, incident stories. Pure research papers rank below deployable patterns.

## Examples

Real digest entries produced by this method on 2026-11-15:

- 🔶 **Harness Engineering — Design Patterns for Securing Long-Horizon Multi-Agent AI
  Systems** (Packt): control plane for long-running agents; prompt-injection containment
  via enforceable trust boundaries; bounded autonomy, least-privilege identity, governed
  memory, runtime recovery. *FDE-relevant: direct input to Tetherline's verification
  suite design.* Source: @KirkDBorne, 2026-11-13.
- 🔶 **Agentic Coding with OpenAI Codex CLI** — agent workflows via agentic engineering,
  MCP, hooks, delivery automation. *FDE-relevant: the delivery-automation pattern maps
  to the venture machine's driver.* Source: @KirkDBorne, 2026-11-13.
- 🔶 **LLM Systems Engineering** — training/building LLMs: fine-tuning, continued
  pretraining. *LLM-relevant: the model-layer reference for PricingOracle decisions.*

## Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| 0 posts parsed from mirror | Lurkbird markup changed or blocked | Fall back to fxtwitter profile probe + Bytewoops per-post mirrors; report INCOMPLETE, never fabricate |
| Digest full of games/noise (#Sedecordle streaks) | Filters too loose | The taxonomy filter is mandatory; drop non-topical posts before framing |
| Same find repeats across digests | No dedupe baseline | Keep the last digest's link set; exclude previously delivered links |
| Gate complains about missing sections | Sections edited out | Re-run the fix batch pattern: Instructions + Examples + Troubleshooting are required |

## Sources (verified 2026-11-15)

- Corpus: Lurkbird mirror of @KirkDBorne (154 posts captured; 139,913 chars archived at
  `~/.hermes/cache/web/lurkbird.com-a2030ae0aa.md`)
- Identity: fxtwitter API probe (id 534563976, 496,757 followers, 199,354 tweets)
- Cross-check: Bytewoops per-post mirrors (Nov 11-13, 2026 posts confirmed)
