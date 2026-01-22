import streamlit as st
import sqlite3

def show_add_medicine_page(medicine_conn):

    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTextInput>div>input, .stNumberInput>div>input, .stDateInput>div>input, .stSelectbox>div>div {
        background-color: #262730 !important;
        color: #FAFAFA !important;
        border-radius: 8px;
        border: 1px solid #00BFFF;
    }
    .stButton>button {
        background-color: #00BFFF !important;
        color: #FAFAFA !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Add New Medicine")
    with st.form(key='add_medicine_form'):
        patient_name = st.text_input("Patient Name")
        medicine_name = st.text_input("Medicine")
        disease = st.text_input("Disease")
        variety = st.text_input("Variety")
        quantity = st.number_input("Quantity (Packets)", min_value=1, step=1)
        date = st.date_input("Date")
        season = st.selectbox("Season", ["Wet", "Dry"])

        submit_button = st.form_submit_button(label="Add Medicine")

        if submit_button:
            if patient_name and medicine_name and disease and variety:
                try:
                    cursor = medicine_conn.cursor()
                    cursor.execute('''
                        INSERT INTO Medicines ("Patient Name", "Medicine", "Disease", "Variety", "Quantity(Packets)", "Date", "Season")
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (patient_name, medicine_name, disease, variety, quantity, date, season))
                    medicine_conn.commit()
                    st.success("Medicine added successfully!")
                    st.rerun()
                except sqlite3.Error as e:
                    st.error(f"Failed to add medicine: {e}")
            else:
                st.error("Please fill out all fields.")
