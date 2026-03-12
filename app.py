import streamlit as st
import sqlite3
from pathlib import Path
from passlib.hash import bcrypt
# Local imports – wrappers
from database import get_conn, ensure_schema, seed_default_role, seed_default_user
from utils import init_session_state, apply_dark_mode
from auth import has_permission
from admin_panel import show_admin_panel

# Page configuration
st.set_page_config(page_title="Drug Prescription App", page_icon="💊", layout="wide")

# Import page components
from predict_page import show_predict_page
from explore_page import show_explore_page
from records import records
from add_medicine_page import show_add_medicine_page
from add_user_page import add_user_page

# Constants
from config import DB_PATH_USERS, DB_PATH_MEDICINE

# ---------- Core helpers ----------
def main() -> None:
    st.title("💊 Drug Prescription and Disease Dataset Analysis")
    apply_dark_mode()
    hide_streamlit_elements()

    # Load/seed databases
    conn = get_conn()                    # users database
    medicine_conn = get_conn(DB_PATH_MEDICINE)  # medicines database

    if conn:
        ensure_schema(conn)
        seed_default_role(conn)
        seed_default_user(conn)

    init_session_state()

    if not st.session_state["authenticated"]:
        login_ui(conn)
    else:
        app_ui(conn, medicine_conn)

# (rest of the file unchanged – keep the functions that call login_ui and app_ui, etc.)



def hide_streamlit_elements() -> None:
    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def login_ui(conn: sqlite3.Connection) -> None:
    IMAGE_PATH = Path("assets/login_image.png")
    if IMAGE_PATH.exists():
        st.image(IMAGE_PATH, use_container_width=True)

    st.sidebar.title("🔐 Login")
    with st.sidebar.form("login_form"):
        username_input = st.text_input("Username", key="username_input")
        password_input = st.text_input("Password", type="password", key="password_input")

        if st.form_submit_button("Login"):
            if authenticate_user(username_input, password_input, conn):
                st.rerun()

    if st.session_state["login_error"]:
        st.sidebar.error(st.session_state["login_error"])


def authenticate_user(username: str, password: str, conn: sqlite3.Connection) -> bool:
    if conn is None:
        return False
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT u.username, u.password, r.role_name
        FROM users u
        JOIN roles r ON u.role_id = r.id
        WHERE u.username=?
        """,
        (username,),
    )
    user = cursor.fetchone()
    if user and bcrypt.verify(password, user[1]):
        st.session_state.update(
            authenticated=True, user=username, role=user[2], login_error=""
        )
        return True

    st.session_state.update(authenticated=False, login_error="Invalid username or password.")
    return False

def app_ui(conn: sqlite3.Connection, medicine_conn: sqlite3.Connection) -> None:
    st.sidebar.title(f"👤 Welcome, {st.session_state['user']} ({st.session_state['role']})")

    # Ensure Medicines table exists
    cursor = medicine_conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            "Patient Name" TEXT NOT NULL,
            "Medicine" TEXT,
            "Disease" TEXT,
            "Variety" TEXT,
            "Quantity(Packets)" INTEGER NOT NULL,
            "Date" DATE NOT NULL,
            "Season" TEXT
        )
        """
    )
    medicine_conn.commit()

    sections = ["General", "Records"]
    if st.session_state["role"] == "Admin":
        sections.append("Admin Panel")
    section_selection = st.sidebar.selectbox("📂 Select Section", sections, key="section_selectbox")
    st.session_state["section"] = section_selection

    if section_selection == "General":
        page_selection = st.sidebar.selectbox("📄 Select Page", ["Predict", "Explore"], key="page_selectbox")
        st.session_state["page"] = page_selection
        if page_selection == "Predict":
            show_predict_page()
        else:
            show_explore_page()

    elif section_selection == "Records":
        records_menu = st.sidebar.selectbox("📋 Records Menu", ["View Records", "Add New Medicine", "Add Users"], key="records_menu_selectbox")
        st.session_state["records_page"] = records_menu
        if records_menu == "View Records":
            records(medicine_conn)
        elif records_menu == "Add New Medicine":
            show_add_medicine_page(medicine_conn)
        elif records_menu == "Add Users":
            add_user_page()   # <‑‑ no conn argument

    elif section_selection == "Admin Panel":
        show_admin_panel()   # <‑‑ new panel

    if st.sidebar.button("🚪 Log Out", key="logout_button"):
        logout()
        st.rerun()


def logout() -> None:
    st.session_state.update(
        authenticated=False,
        user="",
        role="",
        section="General",
        page="Predict",
        records_page="View Records",
    )
if __name__ == "__main__":
    main()