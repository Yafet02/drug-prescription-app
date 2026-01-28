import streamlit as st
st.set_page_config(page_title="Drug Prescription App", page_icon="💊", layout="wide")
import sqlite3
from pathlib import Path
from passlib.hash import bcrypt

# Now import modules that use Streamlit
from predict_page import show_predict_page
from explore_page import show_explore_page
from records import records
from add_medicine_page import show_add_medicine_page, apply_dark_mode
from add_user_page import add_user_page

# Constants
DB_PATH_USERS = "users.db"
DB_PATH_MEDICINE = "Historical_Data_Medicine.db"
IMAGE_PATH = "assets/login_image.png"  # Use a relative path for web hosting
STYLES_PATH = "styles.css"

@st.cache_resource
def create_connection(db_file):
    """Create a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

def create_medicines_table(conn):
    """Create the medicines table if it doesn't exist."""
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Medicines (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          "Patient Name" TEXT NOT NULL,
                          "Medicine" TEXT,
                          "Disease" TEXT,
                          "Variety" TEXT,
                          "Quantity(Packets)" INTEGER NOT NULL,
                          "Date" DATE NOT NULL,
                          "Season" TEXT
                          )''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error creating Medicine table: {e}")

def load_css():
    """Load and apply custom CSS styles."""
    try:
        with open(STYLES_PATH, "r") as css_file:
            st.markdown(f"""<style>{css_file.read()}</style>""", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file not found at {STYLES_PATH}")

def hide_streamlit_elements():
    """Hide default Streamlit UI elements."""
    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def authenticate_user(username, password, conn):
    """Authenticate user credentials against database."""
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT u.username, u.password, r.role_name
                          FROM users u
                          JOIN roles r ON u.role_id = r.id
                          WHERE u.username=?''', (username,))
        user = cursor.fetchone()
        if user:
            hashed_password = user[1]
            role = user[2]
            if bcrypt.verify(password, hashed_password):
                st.session_state["authenticated"] = True
                st.session_state["user"] = username
                st.session_state["role"] = role
                st.session_state["login_error"] = ""
                return True
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")

    st.session_state["authenticated"] = False
    st.session_state["login_error"] = "Invalid username or password."
    return False

def logout():
    """Handle user logout."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = ""
    st.session_state.pop("page", None)
    st.session_state.pop("records_page", None)
    st.session_state.pop("section", None)

def create_roles_table(conn):
    """Create the roles table if it doesn't exist."""
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE
        )''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error creating roles table: {e}")

def seed_roles(conn):
    """Seed the roles table with default roles."""
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        roles = ["Admin", "Healthcare Staff"]
        for role in roles:
            cursor.execute("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", (role,))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error seeding roles: {e}")

def create_users_table(conn):
    """Create the users table if it doesn't exist."""
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles (id)
        )''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error creating users table: {e}")

def seed_default_user(conn):
    """Seed the users table with a default user if not present."""
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", ("Tedros",))
        if cursor.fetchone() is None:
            from passlib.hash import bcrypt
            hashed_password = bcrypt.hash("pass123")
            cursor.execute("INSERT INTO users (username, password, role_id) VALUES (?, ?, ?)", ("Tedros", hashed_password, 1))
            conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error seeding default user: {e}")

def main():
    """Main application entry point."""
    st.title('💊 Drug Prescription and Disease Dataset Analysis')

    # Load styles and hide elements
    load_css()
    hide_streamlit_elements()

    # Connect to databases
    conn = create_connection(DB_PATH_USERS)
    medicine_conn = create_connection(DB_PATH_MEDICINE)

    # Ensure roles and users tables exist and seed default data
    if conn is not None:
        create_roles_table(conn)
        seed_roles(conn)
        create_users_table(conn)
        seed_default_user(conn)

    # Initialize session state variables
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["user"] = ""
        st.session_state["role"] = ""
        st.session_state["login_error"] = ""
        st.session_state["section"] = "General"
        st.session_state["page"] = "Predict"
        st.session_state["records_page"] = "View Records"

    if not st.session_state["authenticated"]:
        # Login page
        try:
            if Path(IMAGE_PATH).exists():
                st.image(IMAGE_PATH, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not load image: {e}")

        st.sidebar.title("🔐 Login")

        with st.sidebar.form(key='login_form'):
            username_input = st.text_input("Username", key="username_input")
            password_input = st.text_input("Password", type="password", key="password_input")

            if st.form_submit_button("Login"):
                if authenticate_user(username_input, password_input, conn):
                    st.rerun()

        if st.session_state["login_error"]:
            st.sidebar.error(st.session_state["login_error"])

    else:
        # Main application
        st.sidebar.title(f"👤 Welcome, {st.session_state['user']} ({st.session_state['role']})!")

        if medicine_conn is not None:
            create_medicines_table(medicine_conn)
        else:
            st.error("Failed to connect to the Medicine database.")
            return

        # Sidebar navigation based on role
        if st.session_state["role"] == "Admin":
            section_selection = st.sidebar.selectbox(
                "📂 Select Section",
                ["General", "Records", "Admin Panel"],
                key="section_selectbox"
            )
        else:
            section_selection = st.sidebar.selectbox(
                "📂 Select Section",
                ["General", "Records"],
                key="section_selectbox"
            )

        st.session_state["section"] = section_selection

        if section_selection == "General":
            page_selection = st.sidebar.selectbox(
                "📄 Select Page",
                ["Predict", "Explore"],
                key="page_selectbox"
            )
            st.session_state["page"] = page_selection
            st.session_state["records_page"] = None

            # Display the selected page
            if st.session_state["page"] == "Predict":
                show_predict_page()
            elif st.session_state["page"] == "Explore":
                show_explore_page()

        elif section_selection == "Records":
            # Records Menu
            records_menu = st.sidebar.selectbox(
                "📋 Records Menu",
                ["View Records", "Add New Medicine", "Add Users"],
                key="records_menu_selectbox"
            )
            st.session_state["page"] = "Records"
            st.session_state["records_page"] = records_menu

            # Handle records menu
            if st.session_state["records_page"] == "View Records":
                records(medicine_conn)
            elif st.session_state["records_page"] == "Add New Medicine":
                show_add_medicine_page(medicine_conn)
            elif st.session_state["records_page"] == "Add Users":
                add_user_page(conn)

        elif section_selection == "Admin Panel":
            st.write("For future admin panel functionality.")

        # Logout button
        if st.sidebar.button("🚪 Log Out", key="logout_button"):
            logout()
            st.rerun()

if __name__ == '__main__':
    main()
