import streamlit as st
import pandas as pd
from utils import apply_dark_mode

apply_dark_mode()

def handle_action(action: str, row_id: int, conn) -> None:
    if action == "Edit":
        st.session_state.update(page="Edit Medicine", edit_id=row_id)
        st.rerun()
    elif action == "Delete":
        if st.session_state.get("role") == "Admin":
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Medicines WHERE rowid=?", (row_id,))
            conn.commit()
            st.success(f"Deleted successfully! (ID: {row_id})")
            st.session_state.update(page="Records")
            st.rerun()
        else:
            st.error("You do not have permission to delete records.")

def records(conn):
    st.title("Records")
    if not conn:
        st.error("Failed to connect to the database.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT rowid, * FROM Medicines")
    medicines = cursor.fetchall()
    columns = ["ID"] + [desc[0] for desc in cursor.description[1:]]

    if medicines:
        df = pd.DataFrame(medicines, columns=columns)
        max_entries = len(df)
        entries_to_show = st.number_input(
            "Entries to show",
            min_value=1,
            max_value=max_entries,
            value=min(10, max_entries),
        )
        st.dataframe(df.head(entries_to_show))
    else:
        st.write("No records found.")