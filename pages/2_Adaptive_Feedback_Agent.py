import streamlit as st
import pandas as pd
from adaptive_agent.suggestion_engine import choose_suggestion
from adaptive_agent.tuner import update_weight
from adaptive_agent.storage import load_weights, load_feedback, load_improvements, log_feedback

st.set_page_config(page_title="Adaptive Feedback Agent", page_icon="⚙️", layout="centered")
st.title("⚙️ Adaptive Feedback Agent")

st.markdown("Type what you just did or plan to do. I’ll suggest a next step. Accept/Reject teaches me to improve.")

user_text = st.text_area("Recent activity (free text)", height=100, placeholder="e.g., Studied 20 mins, feeling sleepy…")

if "current" not in st.session_state:
    st.session_state.current = None  # holds the last suggestion dict

col1, col2 = st.columns(2)
if col1.button("Get suggestion"):
    st.session_state.current = choose_suggestion(epsilon=0.1)

if st.session_state.current:
    s = st.session_state.current
    st.success(f"**Suggestion**: {s['text']}  \n*(id: {s['suggestion_id']}, weight: {s['weight']:.2f})*")

    a, b = st.columns(2)
    if a.button("✅ Accept"):
        log_feedback(s["suggestion_id"], user_text, s["text"], +1)
        update_weight(s["suggestion_id"], +1)
        st.toast("Thanks! I’ll show more of good ones.")
        st.session_state.current = None
    if b.button("❌ Reject"):
        log_feedback(s["suggestion_id"], user_text, s["text"], -1)
        update_weight(s["suggestion_id"], -1)
        st.toast("Got it. I’ll show that less.")
        st.session_state.current = None

st.divider()
st.subheader("📈 Quick stats (updates as you click)")
try:
    w = load_weights()
    st.metric("Templates", len(w))
    st.dataframe(w, use_container_width=True)
except Exception:
    st.info("Weights not ready yet.")

with st.expander("See feedback & improvements"):
    try:
        st.caption("Recent feedback")
        st.dataframe(load_feedback().tail(10), use_container_width=True)
    except Exception:
        st.write("No feedback yet.")
    try:
        st.caption("Weight update history")
        st.dataframe(load_improvements().tail(10), use_container_width=True)
    except Exception:
        st.write("No improvements yet.")
