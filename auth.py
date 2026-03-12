import streamlit as st
from utils import SESSION_KEYS

# Map each page to the set of roles that can access it.
PERMISSIONS = {
    "Predict": {"Admin", "Healthcare Staff"},
    "Explore": {"Admin", "Healthcare Staff"},
    "Records": {"Admin", "Healthcare Staff"},
    "Add Medicine": {"Admin", "Healthcare Staff"},
    "Add User": {"Admin"},
}

def has_permission(page: str) -> bool:
    """Return True if the current user role can access *page*."""
    role = st.session_state.get("role")
    return role in PERMISSIONS.get(page, set())
