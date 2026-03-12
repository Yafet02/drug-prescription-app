import streamlit as st
from utils import apply_dark_mode
from database import get_conn
from passlib.hash import bcrypt
import sqlite3

# ---------- Add User Page ----------
def add_user_page() -> None:
    """Page for adding new users – only accessible by Admin."""
    st.header("Add New User")
    apply_dark_mode()

    # Permission check
    if st.session_state.get("role") != "Admin":
        st.error("Only Admin users can add new users.")
        return

    with st.form("add_user_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Role", ["Admin", "Healthcare Staff"])

        if st.form_submit_button("Add User"):
            if password != confirm_password:
                st.error("Passwords do not match.")
            elif not username or not password:
                st.error("Username and password cannot be empty.")
            else:
                add_user(username, password, role)

def add_user(username: str, password: str, role: str) -> None:
    """Insert a new user into the database."""
    conn = get_conn()  # users database
    cursor = conn.cursor()
    hashed_pw = bcrypt.hash(password)
    try:
        cursor.execute(
            """
            INSERT INTO users (username, password, role_id)
            VALUES (?, ?, (SELECT id FROM roles WHERE role_name=?))
            """,
            (username, hashed_pw, role),
        )
        conn.commit()
        st.success(f"User {username} added successfully!")
    except sqlite3.IntegrityError:
        st.error(f"Username {username} is already taken. Please choose a different one.")
    except sqlite3.Error as e:
        st.error(f"Error adding user: {e}")
    finally:
        conn.close()