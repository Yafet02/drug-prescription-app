import sqlite3
from passlib.hash import bcrypt

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return conn

def create_roles_table(conn):
    """Create the roles table if it doesn't exist."""
    create_roles_table_sql = """
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_roles_table_sql)
        print("Table 'roles' created successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while creating the roles table")

def seed_roles(conn):
    """Seed the roles table with default roles."""
    roles = ["Admin", "Healthcare Staff"]
    try:
        c = conn.cursor()
        for role in roles:
            c.execute("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", (role,))
        conn.commit()
        print("Default roles seeded successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while seeding roles")

def create_users_table(conn):
    """Create the users table with role_id as a foreign key."""
    create_users_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role_id INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles (id)
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_users_table_sql)
        print("Table 'users' created successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while creating the users table")

def add_user(conn, username, password, role):
    """Add a new user with a specific role."""
    try:
        hashed_password = bcrypt.hash(password)
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, password, role_id) VALUES (?, ?, (SELECT id FROM roles WHERE role_name=?))",
            (username, hashed_password, role)
        )
        conn.commit()
        print(f"User '{username}' with role '{role}' added successfully")
    except sqlite3.IntegrityError:
        print(f"The username '{username}' is already taken")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while adding the user")

def setup_database():
    """Setup database, create tables, and seed default data."""
    conn = create_connection("users.db")
    if conn is not None:
        create_roles_table(conn)
        seed_roles(conn)
        create_users_table(conn)
        add_user(conn, "Admin", "pass123", "Admin")
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    setup_database()
