"""
SAI Workflow Runner — Streamlit app
Calls SAI API: POST /workflows/{name}/run
"""
import json
import csv
import os
from datetime import datetime
import httpx
import streamlit as st

st.set_page_config(page_title="SAI Workflow Runner", page_icon="🤖", layout="centered")

# ── Config ────────────────────────────────────────────────────────────────────
SAI_BASE_URL = st.secrets.get("SAI_BASE_URL", os.environ.get("SAI_BASE_URL", "https://api.sai.example.com"))
SAI_API_KEY  = st.secrets.get("SAI_API_KEY",  os.environ.get("SAI_API_KEY",  ""))

WORKFLOWS = [
    "summarize",
    "classify",
    "extract_entities",
    "translate",
    "qa",
]

FEEDBACK_FILE = "feedback_log.csv"

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .output-box { background:#1e293b; border:1px solid #334155; border-radius:10px;
                padding:18px; font-size:0.95rem; line-height:1.6; color:#e2e8f0; }
  .feedback-row { display:flex; gap:12px; margin-top:12px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🤖 SAI Workflow Runner")
st.markdown("Submit a task to an SAI workflow and rate the output.")
st.divider()

# ── Inputs ────────────────────────────────────────────────────────────────────
workflow = st.selectbox(
    "Select workflow",
    WORKFLOWS,
    help="Each workflow specialises in a different task type.",
)

task = st.text_area(
    "Your task",
    placeholder="e.g. Summarize the following paragraph: ...",
    height=140,
)

run_btn = st.button("▶ Run workflow", type="primary", use_container_width=True)

# ── API call ──────────────────────────────────────────────────────────────────
if run_btn:
    if not task.strip():
        st.warning("Please enter a task before running.")
        st.stop()

    with st.spinner(f"Running **{workflow}** workflow…"):
        try:
            headers = {"Content-Type": "application/json"}
            if SAI_API_KEY:
                headers["Authorization"] = f"Bearer {SAI_API_KEY}"

            resp = httpx.post(
                f"{SAI_BASE_URL}/workflows/{workflow}/run",
                json={"task": task},
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            output = (
                data.get("output")
                or data.get("result")
                or data.get("response")
                or json.dumps(data, indent=2, ensure_ascii=False)
            )
            st.session_state["last_output"]   = output
            st.session_state["last_workflow"]  = workflow
            st.session_state["last_task"]      = task
            st.session_state["feedback_given"] = False

        except httpx.HTTPStatusError as e:
            st.error(f"API error {e.response.status_code}: {e.response.text[:300]}")
            st.stop()
        except Exception as e:
            st.error(f"Request failed: {e}")
            st.stop()

# ── Output display ────────────────────────────────────────────────────────────
if "last_output" in st.session_state:
    st.markdown("### Output")
    st.markdown(
        f'<div class="output-box">{st.session_state["last_output"]}</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Workflow: `{st.session_state['last_workflow']}`")

    # ── Feedback ──────────────────────────────────────────────────────────────
    if not st.session_state.get("feedback_given"):
        st.markdown("**Was this output helpful?**")
        col1, col2 = st.columns([1, 1])
        thumbs_up   = col1.button("👍  Yes", use_container_width=True)
        thumbs_down = col2.button("👎  No",  use_container_width=True)

        if thumbs_up or thumbs_down:
            rating = "up" if thumbs_up else "down"
            row = {
                "timestamp": datetime.now().isoformat(),
                "workflow":  st.session_state["last_workflow"],
                "task":      st.session_state["last_task"][:200],
                "rating":    rating,
            }
            file_exists = os.path.exists(FEEDBACK_FILE)
            with open(FEEDBACK_FILE, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=row.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)

            st.session_state["feedback_given"] = True
            st.success("Thanks for your feedback! 🎉")
            st.rerun()
    else:
        st.success("Feedback recorded ✓")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("SAI Workflow Runner · Built with Streamlit")
