import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import joblib
import io
from utils import apply_dark_mode
from config import MODEL_PATH, FEATURES_PATH
from auth import has_permission

apply_dark_mode()

# ---------- Loading helpers – cached ----------
@st.cache_resource
def load_model() -> object | None:
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        st.error(f"Model file not found at: {MODEL_PATH}")
        return None


@st.cache_resource
def load_feature_columns() -> list | None:
    try:
        return joblib.load(FEATURES_PATH)
    except FileNotFoundError:
        st.error(f"Feature columns file not found at: {FEATURES_PATH}")
        return None


# ---------- Pre‑processing ----------
def preprocess_input(
    Year: int,
    Month: str,
    Medicines: list[str],
    Season: str,
    feature_columns: list[str],
    df: pd.DataFrame,
) -> np.ndarray:
    month_map = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    month_num = month_map.get(Month, 0)

    input_rows = []
    for medicine in Medicines:
        # Most recent quantity
        med_df = df[df["Medicine"] == medicine]
        prev_qty = med_df["Quantity(Packets)"].shift(1).fillna(0).iloc[-1]

        # Base features
        features = [Year, month_num, prev_qty]

        # One‑hot season
        season_cols = [c for c in feature_columns if c.startswith("Season_")]
        season_one_hot = [0] * len(season_cols)
        if f"Season_{Season}" in season_cols:
            season_one_hot[season_cols.index(f"Season_{Season}")] = 1
        features.extend(season_one_hot)

        # One‑hot medicine (if present)
        med_cols = [c for c in feature_columns if c.startswith("Medicine_")]
        med_one_hot = [0] * len(med_cols)
        if f"Medicine_{medicine}" in med_cols:
            med_one_hot[med_cols.index(f"Medicine_{medicine}")] = 1
        features.extend(med_one_hot)

        input_rows.append(features)

    return np.array(input_rows)


# ---------- Page ----------
def show_predict_page() -> None:
    if not has_permission("Predict"):
        st.error("You do not have permission to access this page.")
        return

    st.title("Medicine Quantity Prediction")
    st.write(
        "Please fill in the following details to predict the quantity of medicine needed."
    )

    # Load the dataset and feature columns
    df = pd.read_csv("Historical_Data_7_Aug_2024.csv")  # CSV, not DB
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    df["YearMonth"] = df["Date"].dt.to_period("M")

    feature_columns = load_feature_columns()
    if feature_columns is None:
        return
    model = load_model()
    if model is None:
        return

    col1, col2 = st.columns(2)
    with col1:
        Year = st.number_input("Year", min_value=2024)
    with col2:
        Month = st.selectbox(
            "Month",
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
        )

    Season = st.radio("Season", ("Wet", "Dry"))
    Medicines = st.multiselect("Select Medicines", df["Medicine"].unique())

    if st.button("Submit"):
        if not Medicines:
            st.warning("Please select at least one medicine before submitting.")
            return

        table_data = []
        for medicine in Medicines:
            diseases = df[df["Medicine"] == medicine]["Disease"].unique()
            for disease in diseases:
                inp = preprocess_input(Year, Month, [medicine], Season, feature_columns, df)
                pred = model.predict(inp)[0]
                table_data.append(
                    {
                        "Month": Month,
                        "Medicine": medicine,
                        "Disease": disease,
                        "Predicted Quantity": int(round(pred)),
                    }
                )

        result_df = pd.DataFrame(table_data)
        st.write("Predicted Quantities:")
        st.dataframe(result_df)

        # Export predictions as CSV
        csv = io.StringIO()
        result_df.to_csv(csv, index=False)
        st.download_button(
            label="Download Predictions as CSV",
            data=csv.getvalue(),
            file_name="predictions.csv",
            mime="text/csv",
        )

        # Seasonal trends
        st.subheader("Seasonal Trends for Selected Medicines")
        seasonal_data = df[df["Medicine"].isin(Medicines)]
        seasonal_chart = alt.Chart(seasonal_data).mark_line().encode(
            x="YearMonth:T",
            y="Quantity(Packets):Q",
            color="Medicine:N",
            tooltip=["YearMonth", "Medicine", "Quantity(Packets)"],
        ).properties(width=800, height=400)
        st.altair_chart(seasonal_chart, use_container_width=True)

        # Future month predictions
        future_months = np.arange(1, 13)
        future_df = pd.DataFrame({"Month": future_months})
        for medicine in Medicines:
            preds = []
            for month in future_months:
                month_name = {
                    1: "January",
                    2: "February",
                    3: "March",
                    4: "April",
                    5: "May",
                    6: "June",
                    7: "July",
                    8: "August",
                    9: "September",
                    10: "October",
                    11: "November",
                    12: "December",
                }[month]
                inp = preprocess_input(Year, month_name, [medicine], Season, feature_columns, df)
                preds.append(int(round(model.predict(inp)[0])))
            future_df[f"{medicine}_Predicted"] = preds

        future_long = future_df.melt(id_vars=["Month"], var_name="Medicine_Disease", value_name="Predicted Quantity")

        st.subheader("Predicted Trend for Selected Medicines in Future Months")
        line_chart = alt.Chart(future_long).mark_line().encode(
            x="Month:Q",
            y="Predicted Quantity:Q",
            color="Medicine_Disease:N",
            tooltip=["Month", "Medicine_Disease", "Predicted Quantity"],
        ).properties(width=800, height=400)
        st.altair_chart(line_chart, use_container_width=True)