# Donoso Deep Research (DDP) — /ddp

Deep research workflow for Claude Code environments with restricted HTTPS egress.
Replaces Claude's built-in WebFetch (blocked by proxy) with a GitHub Actions fetch
module running on an unrestricted Ubuntu runner.

## Architecture

```
Research Question
    → [Phase 1] Search:    web search → verified URL list (12–20 sources)
    → [Phase 2] Fetch:     GitHub Actions runner → HTML/PDF extraction → branch commit
    → [Phase 3] Synthesize: read local .txt files → adversarial verify → cited report
```

UI layer: Claude Code itself (no additional interface needed)

## Repo Config (update when deploying to a new repo)

```
REPO:            betodon96-svg/sai-workflow-app
FETCH_WORKFLOW:  fetch-research-urls.yml
OUTPUT_BRANCH:   claude/monthly-ai-work-report-xjbyL
CONTENT_DIR:     fetched-content/
FETCH_LOG:       research-logs/fetch-log.xlsx
SCRIPTS:         scripts/fetch_urls.py, scripts/requirements-fetch.txt
```

---

## Phase 1 — Search (source discovery)

Run 6–10 targeted web searches on the research question. For each result:
- Extract the real URL from the search result (never generate URLs from memory — this produces hallucinated 404s)
- Target: 12–20 high-quality, diverse sources (academic papers, primary reports, institutional sources, practitioner publications)
- Exclude: social media, wikis, opinion blogs, known paywall sites (McKinsey, Gartner)
- Deduplicate: if the same paper appears as both /abs/ and /pdf/ on arXiv, keep only /abs/ (the fetch layer rewrites it)

Produce a clean, deduplicated list of real URLs before moving to Phase 2.

---

## Phase 2 — Fetch (GitHub Actions)

1. Generate a session_id from the research question:
   - Lowercase, underscores, max 25 chars
   - Example: question "World models for robotics 2026" → session_id `world_models_robotics`

2. Format the URL list as a JSON array string:
   `["https://url1.com", "https://url2.com", ...]`

3. Trigger the fetch workflow using mcp__github__actions_run_trigger:
   - method: run_workflow
   - workflow_id: fetch-research-urls.yml
   - ref: main
   - inputs:
     - urls_json: the JSON array string
     - session_id: the generated session_id
     - output_branch: claude/monthly-ai-work-report-xjbyL

4. Poll for completion using mcp__github__actions_get:
   - method: get_workflow_run (use the run ID returned from the trigger)
   - Check every ~30s until status = "completed"
   - On conclusion "failure": note the error but continue with any partial results
   - Typical runtime: 1–2 min for HTML-only, 3–5 min for runs with large PDFs

5. Pull committed results:
   - Run: git pull origin claude/monthly-ai-work-report-xjbyL

6. Confirm extraction: ls fetched-content/{session_id}/
   - Files present = successful extractions
   - Count of files vs URL count = rough success rate

---

## Phase 3 — Synthesize

1. Read each .txt file in fetched-content/{session_id}/ using the Read tool
2. Note word counts: files under 100 words were blocked, JS-rendered, or partial — note but do not cite
3. Check research-logs/fetch-log.xlsx for HTTP codes and status of failed sources

Produce a cited report structured as:

**Executive Summary**
3–5 key findings, each a bold claim with inline citation.

**Findings by Theme**
Group sources thematically. Cite inline as [Source Name, Year].
Minimum 3 themes. Each theme synthesizes across multiple sources.

**Source Quality Table**
| Document | Words Extracted | Status | Key Contribution |
Rows for all attempted sources, including failures.

**Gaps and Limitations**
Failed sources noted by name. JS-blocked pages flagged.
Paywall sites listed. Claims that couldn't be verified noted.

Rules:
- Only cite sources that were successfully fetched (>100 words)
- Never fabricate a quote or finding from a failed source
- Flag uncertainty explicitly: "based on abstract only" if a PDF failed

---

## Known Limitations

| Constraint | Cause | Status |
|---|---|---|
| JS-rendered pages return <100 words | httpx cannot execute JavaScript | Accepted limitation |
| McKinsey, Gartner always fail | Login/paywall required | Use alternative open sources |
| GitHub Actions cold start ~45s | Runner provisioning overhead | Expected, not an error |
| arXiv abs+pdf = duplicate content | Both URLs resolve to same PDF | Deduplicate in Phase 1 |
| Large PDFs capped at 15–60 pages | Size-aware pdfplumber limit | Configurable in fetch_urls.py |

---

## Setup for a New Repo

To deploy DDP to a new repo:

1. Copy `.github/workflows/fetch-research-urls.yml` to the target repo
2. Copy `scripts/fetch_urls.py` and `scripts/requirements-fetch.txt`
3. Create `research-logs/` directory with a `.gitkeep`
4. Push the workflow to the default branch (required for workflow_dispatch)
5. Update the Repo Config section above with the new repo details
6. Optional: run `scripts/seed_fetch_log.py` to pre-populate the log with historical attempts

The workflow needs `contents: write` permission (already set in the YAML).
