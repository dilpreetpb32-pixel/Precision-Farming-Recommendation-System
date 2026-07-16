import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Fertilizer Recommendation",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Fertilizer Recommendation")

st.write(
    "Enter the soil, crop, and environmental parameters to receive the most suitable fertilizer recommendation."
)

# --------------------------------------------------
# Load Saved Models
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "models"

fertilizer_model = joblib.load(
    MODEL_DIR / "fertilizer_random_forest.pkl"
)

fertilizer_scaler = joblib.load(
    MODEL_DIR / "fertilizer_scaler.pkl"
)

fertilizer_label_encoder = joblib.load(
    MODEL_DIR / "fertilizer_label_encoder.pkl"
)

feature_encoders = joblib.load(
    MODEL_DIR / "fertilizer_feature_encoders.pkl"
)

st.success("✅ Fertilizer Recommendation model loaded successfully.")

# --------------------------------------------------
# User Input Form
# --------------------------------------------------

st.markdown("---")
st.header("📝 Enter Agricultural Parameters")

col1, col2 = st.columns(2)

with col1:

    soil_ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )

    soil_moisture = st.number_input(
        "Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=45.0
    )

    organic_carbon = st.number_input(
        "Organic Carbon (%)",
        min_value=0.0,
        max_value=10.0,
        value=1.0
    )

    electrical_conductivity = st.number_input(
        "Electrical Conductivity",
        min_value=0.0,
        value=0.5
    )

    nitrogen = st.number_input(
        "Nitrogen Level",
        min_value=0.0,
        max_value=300.0,
        value=60.0
    )

    phosphorus = st.number_input(
        "Phosphorus Level",
        min_value=0.0,
        max_value=300.0,
        value=40.0
    )

    potassium = st.number_input(
        "Potassium Level",
        min_value=0.0,
        max_value=300.0,
        value=40.0
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        max_value=60.0,
        value=28.0
    )

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=65.0
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        max_value=500.0,
        value=120.0
    )

with col2:

    soil_type = st.selectbox(
        "Soil Type",
        feature_encoders["Soil_Type"].classes_
    )

    crop_type = st.selectbox(
        "Crop Type",
        feature_encoders["Crop_Type"].classes_
    )

    crop_growth_stage = st.selectbox(
        "Crop Growth Stage",
        feature_encoders["Crop_Growth_Stage"].classes_
    )

    season = st.selectbox(
        "Season",
        feature_encoders["Season"].classes_
    )

    irrigation_type = st.selectbox(
        "Irrigation Type",
        feature_encoders["Irrigation_Type"].classes_
    )

    previous_crop = st.selectbox(
        "Previous Crop",
        feature_encoders["Previous_Crop"].classes_
    )

    region = st.selectbox(
        "Region",
        feature_encoders["Region"].classes_
    )

    fertilizer_used_last_season = st.number_input(
        "Fertilizer Used Last Season",
        min_value=0.0,
        value=50.0,
        step=1.0
    )

    yield_last_season = st.number_input(
        "Yield Last Season (tons/hectare)",
        min_value=0.0,
        value=3.0
    )

st.markdown("")

predict_fertilizer = st.button(
    "🌱 Recommend Fertilizer",
    use_container_width=True,
    type="primary"
)

# --------------------------------------------------
# Fertilizer Prediction
# --------------------------------------------------
if predict_fertilizer:
    
    # --------------------------------------------------
    # Encode categorical features
    # --------------------------------------------------

    soil_type_encoded = feature_encoders["Soil_Type"].transform([soil_type])[0]
    crop_type_encoded = feature_encoders["Crop_Type"].transform([crop_type])[0]
    crop_growth_stage_encoded = feature_encoders["Crop_Growth_Stage"].transform([crop_growth_stage])[0]
    season_encoded = feature_encoders["Season"].transform([season])[0]
    irrigation_type_encoded = feature_encoders["Irrigation_Type"].transform([irrigation_type])[0]
    previous_crop_encoded = feature_encoders["Previous_Crop"].transform([previous_crop])[0]
    region_encoded = feature_encoders["Region"].transform([region])[0]

    # --------------------------------------------------
    # Create input dataframe (same order as training)
    # --------------------------------------------------

    input_data = pd.DataFrame({
        "Soil_Type": [soil_type_encoded],
        "Soil_pH": [soil_ph],
        "Soil_Moisture": [soil_moisture],
        "Organic_Carbon": [organic_carbon],
        "Electrical_Conductivity": [electrical_conductivity],
        "Nitrogen_Level": [nitrogen],
        "Phosphorus_Level": [phosphorus],
        "Potassium_Level": [potassium],
        "Temperature": [temperature],
        "Humidity": [humidity],
        "Rainfall": [rainfall],
        "Crop_Type": [crop_type_encoded],
        "Crop_Growth_Stage": [crop_growth_stage_encoded],
        "Season": [season_encoded],
        "Irrigation_Type": [irrigation_type_encoded],
        "Previous_Crop": [previous_crop_encoded],
        "Region": [region_encoded],
        "Fertilizer_Used_Last_Season": [fertilizer_used_last_season],
        "Yield_Last_Season": [yield_last_season]
    })

    # --------------------------------------------------
    # Scale ONLY numerical columns
    # --------------------------------------------------

    numerical_columns = [
        "Soil_pH",
        "Soil_Moisture",
        "Organic_Carbon",
        "Electrical_Conductivity",
        "Nitrogen_Level",
        "Phosphorus_Level",
        "Potassium_Level",
        "Temperature",
        "Humidity",
        "Rainfall",
        "Fertilizer_Used_Last_Season",
        "Yield_Last_Season"
    ]

    input_data[numerical_columns] = fertilizer_scaler.transform(
        input_data[numerical_columns]
    )

    # --------------------------------------------------
    # Predict
    # --------------------------------------------------

    prediction = fertilizer_model.predict(input_data)

    predicted_fertilizer = fertilizer_label_encoder.inverse_transform(prediction)[0]

    probabilities = fertilizer_model.predict_proba(input_data)[0]

    confidence = probabilities.max() * 100

    # --------------------------------------------------
    # Display Result
    # --------------------------------------------------

    st.markdown("---")

    st.success("### 🌱 Recommended Fertilizer")

    st.markdown(f"""
    
    ## 🧪 {predicted_fertilizer.upper()}

    **Prediction Confidence:** {confidence:.2f}%

    Based on the provided agricultural parameters, this fertilizer is the most suitable recommendation.
    """)

    # --------------------------------------------------
    # Top 5 Recommendations
    # --------------------------------------------------

    st.subheader("📊 Top 5 Fertilizer Recommendations")

    top5_indices = probabilities.argsort()[-5:][::-1]

    top5_labels = fertilizer_label_encoder.inverse_transform(top5_indices)

    top5_probs = probabilities[top5_indices] * 100

    top5_df = pd.DataFrame({
        "Fertilizer": top5_labels,
        "Confidence (%)": top5_probs
    })

    st.dataframe(
        top5_df,
        use_container_width=True,
        hide_index=True
    )

    fig, ax = plt.subplots(figsize=(8,4))

    ax.barh(
        top5_df["Fertilizer"][::-1],
        top5_df["Confidence (%)"][::-1]
    )

    ax.set_xlabel("Confidence (%)")
    ax.set_title("Top 5 Predicted Fertilizers")

    st.pyplot(fig)