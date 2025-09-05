# pages/2_Adaptive_Feedback_Agent.py
import streamlit as st
import pandas as pd
from adaptive_agent.suggestion_engine import choose_suggestion
from adaptive_agent.tuner import update_weight
from adaptive_agent.storage import load_weights, load_feedback, load_improvements, log_feedback
from data_manager import DataManager  # Integrate with main data for context

st.set_page_config(page_title="Adaptive Feedback Agent", page_icon="⚙️", layout="wide")
st.title("⚙️ Adaptive Feedback Agent")

st.markdown("Describe your project progress. I'll suggest improvements based on RL-adapted feedback.")

# Get context from main system (e.g., team progress)
data_manager = DataManager()
stats = data_manager.get_statistics()
context = {"submission_rate": stats["submission_rate"], "team_count": stats["total_teams"]}  # Example context

user_text = st.text_area("Project Update (e.g., 'Submitted MVP, low on creativity')", height=150)

if "current" not in st.session_state:
    st.session_state.current = None
    st.session_state.last_context = None

col1, col2 = st.columns(2)
if col1.button("Get Suggestion") and user_text:  # Validate input
    try:
        st.session_state.last_context = {"user_text": user_text, **context}
        st.session_state.current = choose_suggestion(st.session_state.last_context)
    except Exception as e:
        st.error(f"Error generating suggestion: {e}")

if st.session_state.current:
    s = st.session_state.current
    st.success(f"**Suggestion**: {s['text']}  \n*(ID: {s['suggestion_id']}, Weight: {s['weight']:.2f})*")

    a, b = st.columns(2)
    if a.button("✅ Accept"):
        log_feedback(s["suggestion_id"], user_text, s["text"], +1)
        update_weight(s["suggestion_id"], +1, st.session_state.last_context, context)  # Pass next_state
        st.toast("Thanks! Adapting...")
        st.session_state.current = None
    if b.button("❌ Reject"):
        log_feedback(s["suggestion_id"], user_text, s["text"], -1)
        update_weight(s["suggestion_id"], -1, st.session_state.last_context, context)
        st.toast("Noted. Improving...")
        st.session_state.current = None

# Stats and History
st.divider()
st.subheader("📈 Stats")
try:
    w = load_weights()
    st.metric("Templates", len(w))
    st.dataframe(w, width="stretch")
except:
    st.info("No weights yet.")

with st.expander("Feedback & Improvements"):
    st.caption("Recent Feedback")
    st.dataframe(load_feedback().tail(10), width="stretch")
    st.caption("Weight Updates")
    st.dataframe(load_improvements().tail(10), width="stretch")