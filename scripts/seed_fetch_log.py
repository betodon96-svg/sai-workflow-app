#!/usr/bin/env python3
"""
One-time script — seeds research-logs/fetch-log.xlsx with the 24 fetch
attempts made in the July 2026 deep-research session (all failed due to
egress policy 403-CONNECT rejection in the Claude Code environment).
Run once; the ongoing fetch_urls.py script appends to the same file.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY  = "002060"
BLUE  = "0070C0"
WHITE = "FFFFFF"
INK   = "1A1C22"

STATUS_STYLE = {
    "Success": ("C6EFCE", "1A5E38"),
    "Partial": ("FFEB9C", "7B4F00"),
    "Failed":  ("FFC7CE", "9C0006"),
    "Timeout": ("FFD9B0", "7B3200"),
    "Error":   ("FFC7CE", "9C0006"),
}

COLUMNS = [
    ("Timestamp (UTC)",  22),
    ("Session",          18),
    ("Document Name",    40),
    ("URL",              55),
    ("Status",           12),
    ("HTTP Code",        10),
    ("Content Type",     14),
    ("Words Extracted",  16),
    ("Summary",          65),
    ("Duration (s)",     12),
]

LOG_PATH = Path("research-logs/fetch-log.xlsx")

# ── Historical fetch attempts ─────────────────────────────────────────────────
# All 24 attempted on 2026-07-15 during the ai-taxonomy-2026 research session.
# All failed: HTTPS proxy (127.0.0.1:37317) rejected all CONNECT tunnels (403).
SESSION = "ai-taxonomy-2026"
TS      = "2026-07-15 14:22:00 UTC"
REASON  = "403 CONNECT rejected by egress proxy — outbound HTTPS blocked by session policy"

ATTEMPTS = [
    # (document_name, url, content_type, snippet_comment)
    (
        "Stanford HAI — AI Index Report 2026",
        "https://hai.stanford.edu/assets/files/ai_index_report_2026.pdf",
        "PDF",
        "Primary report; $581.7B global corporate AI investment figure sourced from snippet"
    ),
    (
        "Stanford HAI — AI Index 2026 Overview Page",
        "https://hai.stanford.edu/ai-index/2026",
        "HTML",
        "Landing page; redirects to PDF; snippet confirmed key stats"
    ),
    (
        "NVIDIA — State of AI 2026",
        "https://resources.nvidia.com/en-zz-ai-strategy/state-of-ai-2026",
        "HTML",
        "280x inference cost reduction figure sourced from snippet; physical AI section"
    ),
    (
        "NVIDIA — Cosmos 3 Technical Report (Jun 2026)",
        "https://research.nvidia.com/publication/2026-06_cosmos-3-world-foundation-model",
        "HTML",
        "World foundation model for robotics; snippet mentioned simulation-to-real transfer"
    ),
    (
        "Google DeepMind — Genie 3",
        "https://deepmind.google/research/publications/genie-3/",
        "HTML",
        "Interactive 3D world generation from text/image; snippet only"
    ),
    (
        "McKinsey — State of AI Trust 2026",
        "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
        "HTML",
        "Agentic era framing; 10% of enterprise functions using agents per snippet"
    ),
    (
        "McKinsey — Agentic AI Era Report (Mar 2026)",
        "https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/the-state-of-ai-shifting-to-the-agentic-era",
        "HTML",
        "Detailed survey data; snippet confirmed enterprise adoption figures"
    ),
    (
        "Gartner — Hype Cycle for Agentic AI 2026",
        "https://www.gartner.com/en/articles/hype-cycle-for-agentic-ai-2026",
        "HTML",
        "Positioned agentic AI near Peak; 40% of enterprise apps forecast in snippet"
    ),
    (
        "Gartner — Predicts 2026: AI Agents Reshape Infrastructure",
        "https://www.gartner.com/en/documents/ai-agents-reshape-enterprise-infrastructure-2026",
        "HTML",
        "Infrastructure impact analysis; IT operations agent use case"
    ),
    (
        "Deloitte — Tech Trends 2026: AI Infrastructure Reckoning",
        "https://www2.deloitte.com/us/en/insights/focus/tech-trends/2026/ai-infrastructure.html",
        "HTML",
        "Inference economics; cloud vs on-prem GPU cost analysis in snippet"
    ),
    (
        "Oxford Economics — The Economics of AI",
        "https://www.oxfordeconomics.com/resource/the-economics-of-ai/",
        "HTML",
        "Labor market and productivity impact analysis"
    ),
    (
        "European Commission — EU AI Act (High-Risk Obligations)",
        "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai",
        "HTML",
        "High-risk obligations activate August 2026; compliance timeline in snippet"
    ),
    (
        "Frontiers in Robotics & AI — Embodied Intelligence Systems",
        "https://www.frontiersin.org/articles/10.3389/frobt.2025.1563482/full",
        "HTML",
        "Three-layer framework for embodied AI; sensor-motor-cognition architecture"
    ),
    (
        "arXiv:2606.00133 — World Models: Comprehensive Survey",
        "https://arxiv.org/abs/2606.00133",
        "HTML",
        "Jun 2026 survey; coverage of Dreamer, RSSM, Genie, Sora architectures"
    ),
    (
        "arXiv:2606.00133 — PDF",
        "https://arxiv.org/pdf/2606.00133",
        "PDF",
        "Same paper; direct PDF fetch attempted separately"
    ),
    (
        "MDPI Computers — Deep RL in Era of Foundation Models",
        "https://www.mdpi.com/2073-431X/14/7/214",
        "HTML",
        "Peer-reviewed survey; integration of RL with LLM policies"
    ),
    (
        "Adaline Labs — AI Research Landscape 2026",
        "https://adaline.ai/blog/ai-research-landscape-2026",
        "HTML",
        "Practitioner survey; field taxonomy for applied AI researchers"
    ),
    (
        "Sema4.ai — AI Maturity Model 2026",
        "https://sema4.ai/resources/ai-maturity-model-2026",
        "HTML",
        "5-level maturity framework for enterprise AI adoption"
    ),
    (
        "Vista Equity Partners — AI Inference Economics",
        "https://vistaequitypartners.com/insights/ai-inference-economics-framework-investors/",
        "HTML",
        "Investor-grade cost model for inference; GPU cluster economics"
    ),
    (
        "Chambers & Partners — Artificial Intelligence 2026",
        "https://chambers.com/guides/artificial-intelligence-2026",
        "HTML",
        "Jurisdiction-by-jurisdiction AI regulation landscape"
    ),
    (
        "Anthropic — Model Card: Claude 3.7 Series",
        "https://www.anthropic.com/model-card/claude-3-7",
        "HTML",
        "Reasoning capabilities and safety mitigations; thinking tokens"
    ),
    (
        "Google Research — Agent-Computer Interaction Survey",
        "https://research.google/pubs/agent-computer-interaction-survey-2026/",
        "HTML",
        "Grounding, tool use, and action spaces for LLM agents"
    ),
    (
        "World Economic Forum — AI 2030 Scenarios",
        "https://www.weforum.org/publications/shaping-the-future-of-ai/",
        "HTML",
        "Four scenarios for AI governance and economic impact through 2030"
    ),
    (
        "Hugging Face — Open LLM Leaderboard 2026 Analysis",
        "https://huggingface.co/blog/open-llm-leaderboard-2026-analysis",
        "HTML",
        "Benchmark saturation analysis; new evaluation dimensions proposed"
    ),
]


# ── Excel builder ─────────────────────────────────────────────────────────────

def _border(color="DDDDDD"):
    s = Side(style="thin", color=color)
    return Border(left=s, right=s, top=s, bottom=s)


def build_workbook():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fetch Log"

    hdr_fill   = PatternFill("solid", fgColor=NAVY)
    hdr_font   = Font(name="Arial", bold=True, size=10, color=WHITE)
    hdr_align  = Alignment(horizontal="center", vertical="center", wrap_text=True)
    hdr_border = _border("888888")

    for col, (label, width) in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=1, column=col, value=label)
        cell.font      = hdr_font
        cell.fill      = hdr_fill
        cell.alignment = hdr_align
        cell.border    = hdr_border
        ws.column_dimensions[get_column_letter(col)].width = width

    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"
    return wb, ws


def write_row(ws, ts, session, name, url, status, http_code, content_type, words, summary, duration):
    fill_hex, font_hex = STATUS_STYLE.get(status, ("F7F8FA", INK))
    row_fill = PatternFill("solid", fgColor=fill_hex)
    row_n    = ws.max_row + 1

    CENTER = Alignment(horizontal="center", vertical="top")
    WRAP   = Alignment(horizontal="left",   vertical="top", wrap_text=True)
    wrap_cols   = {3, 4, 9}
    center_cols = {1, 2, 5, 6, 7, 8, 10}

    values = [ts, session, name, url, status, str(http_code), content_type, words, summary, duration]

    for col, value in enumerate(values, start=1):
        cell           = ws.cell(row=row_n, column=col, value=value)
        cell.fill      = row_fill
        cell.border    = _border()
        cell.alignment = WRAP if col in wrap_cols else CENTER

        if col == 4:
            cell.font      = Font(name="Arial", size=9, color=BLUE, underline="single")
            cell.hyperlink = url
        else:
            cell.font = Font(name="Arial", size=9, color=font_hex)

    ws.row_dimensions[row_n].height = 55


def main():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if LOG_PATH.exists():
        print(f"{LOG_PATH} already exists — aborting to avoid overwrite.")
        print("Delete it first if you want to re-seed.")
        sys.exit(1)

    wb, ws = build_workbook()

    for name, url, content_type, snippet in ATTEMPTS:
        write_row(
            ws,
            ts           = TS,
            session      = SESSION,
            name         = name,
            url          = url,
            status       = "Failed",
            http_code    = "000",
            content_type = content_type,
            words        = 0,
            summary      = REASON + " | Snippet available: " + snippet,
            duration     = 0.0,
        )

    wb.save(LOG_PATH)
    print(f"Seeded {LOG_PATH} with {len(ATTEMPTS)} historical fetch attempts.")


if __name__ == "__main__":
    main()
