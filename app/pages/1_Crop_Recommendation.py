import sys
from pathlib import Path

import streamlit as st
import joblib
import pandas as pd

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

st.set_page_config(page_title="Crop Recommendation", page_icon="🌾", layout="wide")

inject_base_css()
render_sidebar(active="crop")

render_hero(
    eyebrow="Module 01 · Crop Recommendation",
    title="🌾 Crop Recommendation",
    subtitle=(
        "Enter your soil nutrients and environmental readings below. "
        "The model scores all 22 supported crops and returns the best match "
        "with a full confidence breakdown."
    ),
)

# --------------------------------------------------
# Load Models
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "models"

try:
    crop_model = joblib.load(MODEL_DIR / "crop_random_forest.pkl")
    crop_scaler = joblib.load(MODEL_DIR / "crop_scaler.pkl")
    crop_label_encoder = joblib.load(MODEL_DIR / "crop_label_encoder.pkl")
    models_loaded = True
except Exception as e:
    models_loaded = False
    st.error(f"⚠️ Could not load the crop recommendation model: {e}")

if models_loaded:
    st.markdown(
        '<span class="pf-badge">✅ Random Forest model loaded · 99.55% test accuracy</span>',
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------
# User Input Form
# --------------------------------------------------

st.markdown('<div class="pf-section-title">📝 Soil & Environmental Parameters</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="pf-section-sub">All seven inputs come directly from a basic soil test and local weather data</div>',
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="pf-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🧪 Soil Nutrients**")
        nitrogen = st.slider("Nitrogen — N (kg/ha)", min_value=0.0, max_value=150.0, value=50.0, help="Nitrogen content in the soil")
        phosphorus = st.slider("Phosphorus — P (kg/ha)", min_value=0.0, max_value=150.0, value=50.0, help="Phosphorus content in the soil")
        potassium = st.slider("Potassium — K (kg/ha)", min_value=0.0, max_value=250.0, value=50.0, help="Potassium content in the soil")
        ph = st.slider("Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1, help="0 = highly acidic, 14 = highly alkaline, 7 = neutral")

    with col2:
        st.markdown("**🌤️ Environmental Conditions**")
        temperature = st.slider("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
        humidity = st.slider("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
        rainfall = st.slider("Rainfall (mm)", min_value=0.0, max_value=500.0, value=100.0)
        st.markdown(
            f"""
            <div style="margin-top:30px; padding:12px 14px; background:{COLORS['moss_light']};
                        border-radius:10px; font-size:12.5px; color:{COLORS['forest_dark']};">
            💡 Rainfall and humidity are the two strongest predictors of crop suitability
            in our trained model — adjust them to see how recommendations shift.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

predict_crop = st.button("🌾 Recommend Crop", use_container_width=True, type="primary", disabled=not models_loaded)

# --------------------------------------------------
# Crop Prediction
# --------------------------------------------------

if predict_crop and models_loaded:

    input_data = pd.DataFrame(
        [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]],
        columns=["N", "P", "K", "temperature", "humidity", "ph", "rainfall"],
    )

    input_scaled = crop_scaler.transform(input_data)
    prediction = crop_model.predict(input_scaled)
    predicted_crop = crop_label_encoder.inverse_transform(prediction)[0]

    probabilities = crop_model.predict_proba(input_scaled)[0]
    confidence = probabilities.max() * 100

    st.divider()

    render_result_banner(
        eyebrow="Recommended Crop",
        value=f"🌱 {predicted_crop.upper()}",
        description=(
            "Based on the soil and environmental conditions provided, this crop is the "
            "most suitable choice for cultivation according to the trained Random Forest model."
        ),
    )

    res_col1, res_col2 = st.columns([1, 1.4])

    with res_col1:
        st.plotly_chart(confidence_gauge(confidence), use_container_width=True)

    with res_col2:
        top5_idx = probabilities.argsort()[-5:][::-1]
        top5_crops = crop_label_encoder.inverse_transform(top5_idx)
        top5_probs = probabilities[top5_idx] * 100

        st.plotly_chart(
            top5_bar_chart(top5_crops, top5_probs, title="Top 5 Crop Recommendations"),
            use_container_width=True,
        )

    top5_df = pd.DataFrame({"Crop": top5_crops, "Confidence (%)": [f"{p:.2f}%" for p in top5_probs]})
    st.dataframe(top5_df, use_container_width=True, hide_index=True)

st.write("")
st.divider()
render_footer()
