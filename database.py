import sqlite3
from pathlib import Path
from config import DB_PATH_USERS
from passlib.hash import bcrypt

# ---------- Connection helpers ----------
def get_conn(db_path: Path | None = None) -> sqlite3.Connection:
    """Return a new SQLite connection.
    If *db_path* is ``None`` the function uses :data:`config.DB_PATH_USERS`."""
    path = db_path or DB_PATH_USERS
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn

# ---------- Schema creation ----------
def ensure_schema(conn: sqlite3.Connection) -> None:
    """Create the required tables if they do not already exist.
    The users table is dropped and recreated every time to guarantee the
    presence of the `id` primary‑key column."""
    cursor = conn.cursor()

    # Roles table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE
        )
        """
    )

    # Users table – always recreate to ensure id column exists
    cursor.execute("DROP TABLE IF EXISTS users;")
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
        """
    )

    # Medicines table
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
    conn.commit()

# ---------- Seeding ----------
def seed_default_role(conn: sqlite3.Connection) -> None:
    """Insert default roles if they are missing."""
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", ("Admin",))
    cursor.execute("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", ("Healthcare Staff",))
    conn.commit()

def seed_default_user(conn: sqlite3.Connection) -> None:
    """Create a default admin user (username `Tedros`, password `pass123`).
    The function ignores the insert if the user already exists."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role_id) VALUES (?, ?, (SELECT id FROM roles WHERE role_name=?))",
            ("Tedros", bcrypt.hash("pass123"), "Admin"),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # The user already exists – ignore the error.
        pass