import streamlit as st
from config import SESSION_KEYS

# ------------------------------------------------------------------
# Session state helpers
# ------------------------------------------------------------------
def init_session_state() -> None:
    """Ensure all required session state keys exist."""
    for key, default in SESSION_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = default


# ------------------------------------------------------------------
# Dark‑mode CSS
# ------------------------------------------------------------------
def apply_dark_mode() -> None:
    st.markdown(
        """
        <style>
        .stApp {background:#0E1117;color:#FAFAFA;}
        .stTextInput>div>input, .stNumberInput>div>input,
        .stDateInput>div>input, .stSelectbox>div>div {
            background:#262730 !important;color:#FAFAFA !important;
            border-radius:8px;border:1px solid #00BFFF;
        }
        .stButton>button {background:#00BFFF;color:#FAFAFA;
            border-radius:8px;border:none;font-weight:bold;}
        </style>
        """,
        unsafe_allow_html=True,
    )
