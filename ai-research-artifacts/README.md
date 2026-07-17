# AI Research Artifacts — July 2026

Three HTML documents produced in a single Claude Code session exploring the AI knowledge landscape.

| File | What it is |
|---|---|
| `ai-taxonomy-2026.html` | Standard field taxonomy: AI branches, subfields, and application domains with maturity signals and business relevance — sourced from Stanford HAI, NVIDIA, McKinsey, Gartner, and Deloitte 2026 reports. |
| `personal-taxonomy-2026.html` | Personal practitioner taxonomy (betodon96): 4 domains (Engineering AI Systems, Enterprise AI, Eval Sets, Engineering Systems through AI) with sub-domains, overlap zones, and design rationale. |
| `taxonomy-comparison.html` | Side-by-side analysis of both taxonomies across 11 criteria — relevance, comprehensiveness, practitioner utility — with a synthesis conclusion and 5 proposed research sprint targets. |
| `research-process-log.html` | Objective log of how the standard taxonomy was produced — the intended multi-agent pipeline, what failed (proxy blocked full-page fetching), how the artifact was recovered from search snippets, and an honest quality risk assessment. |
| `agent-architecture.html` | Systems-level architecture of the deep-research workflow — orchestrator/agent distinction, component specs, interface schemas, design decisions, and failure analysis with a visual pipeline diagram. |
| `fetch-layer-architecture.html` | Architecture alternatives for the fetch layer — root cause analysis of the 403 egress policy constraint, 5 option cards (FastAPI MCP microservice, GitHub Actions runner, third-party API, Drive corpus, snippet-first hybrid), decision matrix, and a recommendation to build Option B (GitHub Actions) now and migrate to Option A at scale. |

All files are self-contained HTML — open in any browser, support light and dark themes.
