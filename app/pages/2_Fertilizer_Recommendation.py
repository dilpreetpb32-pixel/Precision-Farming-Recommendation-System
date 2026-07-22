import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import joblib

sys.path.append(str(Path(__file__).resolve().parents[1]))
from style import (
    COLORS,
    inject_base_css,
    render_sidebar,
    render_hero,
    render_result_banner,
    confidence_gauge,
    top5_bar_chart,
    render_footer,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(page_title="Fertilizer Recommendation", page_icon="🌱", layout="wide")

inject_base_css()
render_sidebar(active="fertilizer")

render_hero(
    eyebrow="Module 02 · Fertilizer Recommendation",
    title="🌱 Fertilizer Recommendation",
    subtitle=(
        "Enter your soil, crop and field details below. The model scores all 7 "
        "supported fertilizers and returns the best match with a full confidence breakdown."
    ),
)

# --------------------------------------------------
# Load Saved Models
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "models"

try:
    fertilizer_model = joblib.load(MODEL_DIR / "fertilizer_random_forest.pkl")
    fertilizer_scaler = joblib.load(MODEL_DIR / "fertilizer_scaler.pkl")
    fertilizer_label_encoder = joblib.load(MODEL_DIR / "fertilizer_label_encoder.pkl")
    feature_encoders = joblib.load(MODEL_DIR / "fertilizer_feature_encoders.pkl")
    models_loaded = True
except Exception as e:
    models_loaded = False
    st.error(f"⚠️ Could not load the fertilizer recommendation model: {e}")

if models_loaded:
    st.markdown(
        '<span class="pf-badge">✅ Random Forest model loaded · 87.50% test accuracy</span>',
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------
# User Input Form — organized into logical tabs
# --------------------------------------------------

st.markdown('<div class="pf-section-title">📝 Agricultural Parameters</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="pf-section-sub">19 inputs grouped into four categories — fill in each tab before generating a recommendation</div>',
    unsafe_allow_html=True,
)

tab_soil, tab_crop, tab_env, tab_history = st.tabs(
    ["🧪 Soil Properties", "🌾 Crop & Field", "🌤️ Environmental", "📈 Historical Data"]
)

with tab_soil:
    st.markdown('<div class="pf-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        soil_ph = st.slider("Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
        soil_moisture = st.slider("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=45.0)
        organic_carbon = st.slider("Organic Carbon (%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
        electrical_conductivity = st.number_input("Electrical Conductivity (dS/m)", min_value=0.0, value=0.5)
    with c2:
        nitrogen = st.slider("Nitrogen Level", min_value=0.0, max_value=300.0, value=60.0)
        phosphorus = st.slider("Phosphorus Level", min_value=0.0, max_value=300.0, value=40.0)
        potassium = st.slider("Potassium Level", min_value=0.0, max_value=300.0, value=40.0)
        soil_type = st.selectbox("Soil Type", feature_encoders["Soil_Type"].classes_) if models_loaded else None
    st.markdown("</div>", unsafe_allow_html=True)

with tab_crop:
    st.markdown('<div class="pf-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        crop_type = st.selectbox("Crop Type", feature_encoders["Crop_Type"].classes_) if models_loaded else None
        crop_growth_stage = st.selectbox("Crop Growth Stage", feature_encoders["Crop_Growth_Stage"].classes_) if models_loaded else None
        previous_crop = st.selectbox("Previous Crop", feature_encoders["Previous_Crop"].classes_) if models_loaded else None
    with c2:
        irrigation_type = st.selectbox("Irrigation Type", feature_encoders["Irrigation_Type"].classes_) if models_loaded else None
        region = st.selectbox("Region", feature_encoders["Region"].classes_) if models_loaded else None
        season = st.selectbox("Season", feature_encoders["Season"].classes_) if models_loaded else None
    st.markdown("</div>", unsafe_allow_html=True)

with tab_env:
    st.markdown('<div class="pf-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        temperature = st.slider("Temperature (°C)", min_value=0.0, max_value=60.0, value=28.0)
        humidity = st.slider("Humidity (%)", min_value=0.0, max_value=100.0, value=65.0)
    with c2:
        rainfall = st.slider("Rainfall (mm)", min_value=0.0, max_value=500.0, value=120.0)
        st.markdown(
            f"""
            <div style="margin-top:8px; padding:12px 14px; background:{COLORS['moss_light']};
                        border-radius:10px; font-size:12.5px; color:{COLORS['forest_dark']};">
            💡 Nitrogen, Phosphorus and Potassium levels carry the most predictive weight
            in the trained model — get these three right first.
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with tab_history:
    st.markdown('<div class="pf-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fertilizer_used_last_season = st.number_input("Fertilizer Used Last Season (kg/ha)", min_value=0.0, value=50.0, step=1.0)
    with c2:
        yield_last_season = st.number_input("Yield Last Season (tons/hectare)", min_value=0.0, value=3.0)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

predict_fertilizer = st.button("🌱 Recommend Fertilizer", use_container_width=True, type="primary", disabled=not models_loaded)

# --------------------------------------------------
# Fertilizer Prediction
# --------------------------------------------------

if predict_fertilizer and models_loaded:

    soil_type_encoded = feature_encoders["Soil_Type"].transform([soil_type])[0]
    crop_type_encoded = feature_encoders["Crop_Type"].transform([crop_type])[0]
    crop_growth_stage_encoded = feature_encoders["Crop_Growth_Stage"].transform([crop_growth_stage])[0]
    season_encoded = feature_encoders["Season"].transform([season])[0]
    irrigation_type_encoded = feature_encoders["Irrigation_Type"].transform([irrigation_type])[0]
    previous_crop_encoded = feature_encoders["Previous_Crop"].transform([previous_crop])[0]
    region_encoded = feature_encoders["Region"].transform([region])[0]

    input_data = pd.DataFrame(
        {
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
            "Yield_Last_Season": [yield_last_season],
        }
    )

    numerical_columns = [
        "Soil_pH", "Soil_Moisture", "Organic_Carbon", "Electrical_Conductivity",
        "Nitrogen_Level", "Phosphorus_Level", "Potassium_Level", "Temperature",
        "Humidity", "Rainfall", "Fertilizer_Used_Last_Season", "Yield_Last_Season",
    ]
    input_data[numerical_columns] = fertilizer_scaler.transform(input_data[numerical_columns])

    prediction = fertilizer_model.predict(input_data)
    predicted_fertilizer = fertilizer_label_encoder.inverse_transform(prediction)[0]

    probabilities = fertilizer_model.predict_proba(input_data)[0]
    confidence = probabilities.max() * 100

    st.divider()

    render_result_banner(
        eyebrow="Recommended Fertilizer",
        value=f"🧪 {predicted_fertilizer.upper()}",
        description=(
            "Based on the soil, crop and environmental parameters provided, this fertilizer is "
            "the most suitable recommendation according to the trained Random Forest model."
        ),
    )

    res_col1, res_col2 = st.columns([1, 1.4])

    with res_col1:
        st.plotly_chart(confidence_gauge(confidence), use_container_width=True)
        if confidence < 50:
            st.caption("⚠️ Confidence is relatively low — this often happens for rarer fertilizer classes with fewer training examples (e.g. SSP). Consider these results as guidance rather than a definitive answer.")

    with res_col2:
        top5_idx = probabilities.argsort()[-5:][::-1]
        top5_labels = fertilizer_label_encoder.inverse_transform(top5_idx)
        top5_probs = probabilities[top5_idx] * 100

        st.plotly_chart(
            top5_bar_chart(top5_labels, top5_probs, title="Top 5 Fertilizer Recommendations"),
            use_container_width=True,
        )

    top5_df = pd.DataFrame({"Fertilizer": top5_labels, "Confidence (%)": [f"{p:.2f}%" for p in top5_probs]})
    st.dataframe(top5_df, use_container_width=True, hide_index=True)

st.write("")
st.divider()
render_footer()
