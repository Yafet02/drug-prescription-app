import streamlit as st
import pandas as pd
from database import get_conn
from utils import apply_dark_mode
import sqlite3

# ---------- Admin Panel ----------
def show_admin_panel() -> None:
    """Admin‑only page for managing users."""
    if st.session_state.get("role") != "Admin":
        st.error("You do not have permission to access the Admin Panel.")
        return

    apply_dark_mode()
    st.title("Admin Panel")

    conn = get_conn()  # users database
    cursor = conn.cursor()

    # Fetch users
    cursor.execute(
        """
        SELECT u.id, u.username, r.role_name
        FROM users u
        JOIN roles r ON u.role_id = r.id
        """
    )
    users = cursor.fetchall()
    df_users = pd.DataFrame(users, columns=["ID", "Username", "Role"])
    st.dataframe(df_users)

    # Deletion
    delete_id = st.number_input("Delete User by ID", min_value=1, step=1, key="delete_user_id")
    if st.button("Delete User"):
        try:
            cursor.execute("DELETE FROM users WHERE id=?", (delete_id,))
            conn.commit()
            st.success(f"Deleted user with ID {delete_id}.")
        except sqlite3.Error as e:
            st.error(f"Error deleting user: {e}")

    conn.close()