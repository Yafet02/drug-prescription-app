import streamlit as st
from utils import apply_dark_mode

def show_add_medicine_page(medicine_conn):
    if st.session_state.get("role") not in ["Admin", "Healthcare Staff"]:
        st.error("You do not have permission to access this page.")
        return

    apply_dark_mode()
    st.title("Add New Medicine")

    with st.form("add_medicine_form"):
        patient_name = st.text_input("Patient Name")
        medicine_name = st.text_input("Medicine")
        disease = st.text_input("Disease")
        variety = st.text_input("Variety")
        quantity = st.number_input("Quantity (Packets)", min_value=1, step=1)
        date = st.date_input("Date")
        season = st.selectbox("Season", ["Wet", "Dry"])

        if st.form_submit_button("Add Medicine"):
            if all([patient_name, medicine_name, disease, variety]):
                cursor = medicine_conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO Medicines ("Patient Name", "Medicine", "Disease", "Variety",
                        "Quantity(Packets)", "Date", "Season")
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (patient_name, medicine_name, disease, variety, quantity, date, season),
                )
                medicine_conn.commit()
                st.success("Medicine added successfully!")
                st.rerun()
            else:
                st.error("Please fill out all fields.")