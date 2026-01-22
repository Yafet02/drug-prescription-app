import streamlit as st
from config import MEDICINE_DISEASE_MAP

def about_page():
    """About and help page."""
    st.title("❓ About & Help")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("How to Use")
        st.markdown("""
        ### Prediction Page
        1. Select a medicine from the dropdown
        2. Choose the disease type
        3. Set the current quantity
        4. Choose dosage level and frequency
        5. Click "Generate Prediction"
        6. Download results as CSV
        
        ### Explore Page
        1. View statistics about the dataset
        2. Filter medicines to analyze
        3. Choose different visualization types
        4. View the raw data table
        """)
    
    with col2:
        st.header("Features")
        st.markdown("""
        ✅ **ML-Powered Predictions** - AI models trained on historical data
        
        📊 **Interactive Visualizations** - Multiple chart types
        
        📥 **CSV Export** - Download predictions
        
        🔒 **Secure Authentication** - User accounts and login
        
        📈 **Data Analytics** - Statistical summaries
        
        💾 **Data Persistence** - Track all predictions
        """)
    
    st.divider()
    
    st.header("Medicines & Diseases")
    st.markdown("Supported medicine-disease mappings:")
    
    # Create table
    mapping_data = []
    for medicine, disease in MEDICINE_DISEASE_MAP.items():
        mapping_data.append({"Medicine": medicine, "Primary Use": disease})
    
    mapping_df = st.dataframe(
        mapping_data,
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    st.header("Tips & Best Practices")
    col_tips1, col_tips2 = st.columns(2)
    
    with col_tips1:
        st.info("""
        **📌 Prediction Tips:**
        - Use historical dosage patterns for accuracy
        - Medium dosage is the baseline
        - Twice daily frequency is standard
        """)
    
    with col_tips2:
        st.warning("""
        **⚠️ Important:**
        - Always consult with healthcare professionals
        - These are AI predictions, not medical advice
        - Verify recommendations with licensed doctors
        """)
    
    st.divider()
    
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "Drug Prescription Analysis System | Version 1.0"
        "</div>",
        unsafe_allow_html=True
    )
