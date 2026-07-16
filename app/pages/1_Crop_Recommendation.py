import streamlit as st
import joblib
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Crop Recommendation",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Crop Recommendation")

st.write(
    "Enter the soil and environmental parameters to receive the most suitable crop recommendation."
)

# --------------------------------------------------
# Load Models
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "models"

crop_model = joblib.load(MODEL_DIR / "crop_random_forest.pkl")

crop_scaler = joblib.load(MODEL_DIR / "crop_scaler.pkl")

crop_label_encoder = joblib.load(MODEL_DIR / "crop_label_encoder.pkl")

st.success("✅ Crop Recommendation model loaded successfully.")

# --------------------------------------------------
# User Input Form
# --------------------------------------------------

st.markdown("---")
st.header("📝 Enter Agricultural Parameters")

col1, col2 = st.columns(2)

with col1:

    nitrogen = st.number_input(
        "Nitrogen (N)",
        min_value=0.0,
        max_value=150.0,
        value=50.0
    )

    phosphorus = st.number_input(
        "Phosphorus (P)",
        min_value=0.0,
        max_value=150.0,
        value=50.0
    )

    potassium = st.number_input(
        "Potassium (K)",
        min_value=0.0,
        max_value=250.0,
        value=50.0
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        max_value=50.0,
        value=25.0
    )

with col2:

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=60.0
    )

    ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        max_value=500.0,
        value=100.0
    )

st.markdown("")

predict_crop = st.button(
    "🌾 Recommend Crop",
    use_container_width=True,
    type="primary"
)

# --------------------------------------------------
# Crop Prediction
# --------------------------------------------------

if predict_crop:

    # Create DataFrame
    input_data = pd.DataFrame(
        [[
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall
        ]],
        columns=[
            "N",
            "P",
            "K",
            "temperature",
            "humidity",
            "ph",
            "rainfall"
        ]
    )

    # Scale input
    input_scaled = crop_scaler.transform(input_data)

    # Prediction
    prediction = crop_model.predict(input_scaled)

    predicted_crop = crop_label_encoder.inverse_transform(prediction)[0]

    # Prediction probabilities
    probabilities = crop_model.predict_proba(input_scaled)[0]

    confidence = probabilities.max() * 100

    st.markdown("---")

    st.success("### 🌾 Recommended Crop")

    st.markdown(
        f"""
        ## 🌱 **{predicted_crop.upper()}**

        **Prediction Confidence:** **{confidence:.2f}%**

        Based on the provided soil and environmental conditions,
        this crop is the most suitable for cultivation.
        """
    )

    # ----------------------------------------
    # Top 5 Predictions
    # ----------------------------------------

    st.subheader("📊 Top 5 Crop Recommendations")

    top5_indices = probabilities.argsort()[-5:][::-1]

    top5_crops = crop_label_encoder.inverse_transform(top5_indices)

    top5_probs = probabilities[top5_indices] * 100

    top5_df = pd.DataFrame({
        "Crop": top5_crops,
        "Confidence (%)": top5_probs
    })

    st.dataframe(
        top5_df,
        use_container_width=True,
        hide_index=True
    )

    # ----------------------------------------
    # Probability Chart
    # ----------------------------------------

    fig, ax = plt.subplots(figsize=(8,4))

    ax.barh(
        top5_df["Crop"][::-1],
        top5_df["Confidence (%)"][::-1]
    )

    ax.set_xlabel("Confidence (%)")
    ax.set_title("Top 5 Predicted Crops")

    st.pyplot(fig)