# CLAUDE.md — Project Memory

This file is read by Claude Code at the start of every session. It preserves key decisions,
file locations, design conventions, and research context so they survive context resets.

---

## What CLAUDE.md Is

A persistent memory file checked into the repo. Claude reads it automatically on session start,
so anything here does not need to be re-explained. Update it whenever a significant decision
is made or a new artifact is added.

---

## Repository Contents

| File | Description |
|---|---|
| `AI_Implementation_Strategy_SE_Workshop.pptx` | 28-slide workshop deck on AI in practice |
| `MBSE_AI_Transformation_Pitch.pptx` | 3-slide pitch deck for MBSE AI transformation engagement |
| `ai_experimentation_report.html` | Source HTML for workshop S22-S26 content (Excel, PowerPoint, Cowork, NotebookLM, Gemini) |
| `ai_product_research_playbook.html` | Predecessor HTML, same design system |
| `monthly_ai_report_may2026.html` | Monthly AI report (May 2026) |
| `ECSE_WP11_Strategic_AI_Integration_v2.0.docx` | Strategic AI integration working paper |
| `app.py` | Flask/Streamlit app entry point |
| `requirements.txt` | Python dependencies |

---

## Slide Deck — Design System

### Palette (python-pptx hex values)
```
NAVY  = #002060    BLUE  = #0070C0    TEAL  = #006B6B
AMBER = #7B4F00    GREEN = #1A5E38    CORAL = #8B1A1A
INK   = #1A1C22    MID   = #52586A    LBLUE = #E6EEF7
LGRN  = #E6F4EC    OFFW  = #F7F8FA    DARK  = #090D18
SUBT  = #8A93A8
```

### Key Helpers (build scripts in /tmp)
- `rect(slide, l,t,w,h, fill, line)` — basic rectangle
- `tbox(slide, text, l,t,w,h, size, bold, color, align, wrap)` — text box
- `run(para, text, size, bold, color)` — inline run with mixed formatting
- `accent_rows(slide, rows, top, left, w, row_h)` — bullet rows with teal dot accent
- `card_box(slide, title, bullets, l,t,w,h, accent)` — card with colored header
- `section_divider(slide, num, title, subtitle)` — full-bleed section break slide
- `content_base(slide, title, subtitle)` — standard content slide base
- `footer(slide, text)` — bottom footer band

### ASCII Safety Rule
**Always use ASCII in python-pptx build scripts.** Use `--` not em-dash, `->` not arrow,
straight quotes only. The Python source must be ASCII-clean; the PPTX rendering layer
handles Unicode fine but the edit tool introduces curly quotes that break the parser.

### Workshop Deck Structure
- S01-S03: Opening / agenda / positioning
- S04-S08: AI landscape and market context
- S09-S12: SaaS defensibility and enterprise AI
- S13-S16: Workflow integration patterns
- S17: Fixed — removed unresolvable "OpenClaw" tool reference
- S18-S20: RAG and Ollama chatbot
- S21: Section 04 divider
- S22: Claude in Excel (5 steps)
- S23: Claude in PowerPoint (5 steps)
- S24: Cowork and Reusable Skills (CLAUDE.md + slash commands)
- S25: NotebookLM (TEAL) + Notion AI (AMBER) side-by-side
- S26: Gemini vs Claude comparison (Claude panel highlighted BLUE)
- S27: Section 05 divider — The Research Project
- S28: Timeline visual

---

## MBSE Pitch Deck — Design Notes

3-slide vision-forward structure. Each slide: bold vision band at top, supporting cards below.

- Slide 1 (WS1): AI implementation in SE — light due diligence of existing processes, workshop-style
- Slide 2 (WS2): Products that read large document volumes at scale (proof case: Arcadia vs SysML v2)
- Slide 3 (WS3): Investment question — direct cost vs strategic direction vs opportunity cost

Helpers: `vision_band()`, `seclabel()`, `card()`, `strip()`, `deck_footer()`
Build script: `/tmp/build_pitch.py` (ephemeral — recreate from CLAUDE.md if lost)

---

## Domain Knowledge — Systems Engineering

- **SysML v2**: Adopted by OMG July 2025. KerML-based metamodel. Textual + graphical notation.
  Native API & Services layer (third pillar). Rev Task Forces for KerML 1.1 and SysML 2.1 established.
- **Arcadia**: MBSE *method* (not a language). Prescriptive, paired with Capella tool.
  Developed because SysML v1 was too software-engineering-centric for SE users.
  **Critical distinction: Arcadia = method, SysML = language.**
- **WS2 framing**: Arcadia/SysML v2 comparison is the proof case for the document-reading
  product capability, not the end goal in itself.

---

## Research Framework — AI Knowledge Domains

Four categories (non-MECE by design — overlaps are the most fertile research areas):

1. **Engineering AI Systems** — Design and build of AI-native capabilities: agents, pipelines, and AI products.
2. **Enterprise AI** — Organizational deployment and institutionalization of AI across business functions and workflows.
3. **Eval Sets** — Methods and frameworks for measuring AI system performance and the quality of AI-assisted processes.
4. **Engineering Systems through AI** — Using AI as instrument to architect, verify, and develop systems whose artifact is not itself AI-dependent.

Key insight: "Engineering Systems through AI where the solution does not contain AI" is the most
counterintuitive and therefore most valuable framing for the SE community. Separates AI capability
from AI outcome -- the artifact stays clean, the process is AI-augmented.

---

## Key Concepts

- **MCP (Model Context Protocol)**: Standard connector giving Claude access to external tools/systems
  (GitHub, Drive, web search, etc.). What the user was calling "the interface layer."
- **RAG**: Vector DB + LLM for document Q&A. Used in Ollama chatbot and proposed for WS2.
- **Feasibility x Impact matrix**: Core consulting framework for sequencing AI transformation.
  Appears in WS1 and WS3 of pitch deck.
- **SaaS defensibility claims**: Sourced from Bain PE/Digital reports and Tech Due Diligence practice.

---

## Git

- Active branch: `claude/monthly-ai-work-report-xjbyL`
- Remote: `betodon96-svg/sai-workflow-app`
- Always push with: `git push -u origin claude/monthly-ai-work-report-xjbyL`
