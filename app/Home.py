import streamlit as st
import plotly.graph_objects as go

from style import (
    COLORS,
    inject_base_css,
    render_sidebar,
    render_hero,
    render_footer,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI-Based Precision Farming",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_base_css()
render_sidebar(active="home")

# --------------------------------------------------
# Hero Section
# --------------------------------------------------

render_hero(
    eyebrow="AI-Based Precision Farming",
    title="🌱 Precision Farming Recommendation Engine",
    subtitle=(
        "Empowering smarter agriculture with machine learning — instant, "
        "data-driven crop and fertilizer recommendations built on real "
        "soil and environmental data."
    ),
)

# --------------------------------------------------
# Key Metrics
# --------------------------------------------------

m1, m2, m3, m4 = st.columns(4)

metric_cards = [
    ("99.55%", "Crop Model Accuracy"),
    ("87.50%", "Fertilizer Model Accuracy"),
    ("5", "ML Algorithms Compared"),
    ("12,200+", "Records Analyzed"),
]

for col, (value, label) in zip([m1, m2, m3, m4], metric_cards):
    with col:
        st.markdown(
            f"""
            <div class="pf-metric">
                <div class="pf-metric-value">{value}</div>
                <div class="pf-metric-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
st.divider()

# --------------------------------------------------
# What This System Can Do
# --------------------------------------------------

st.markdown('<div class="pf-section-title">🚀 What This System Can Do</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="pf-section-sub">Two Random Forest models, trained on real agricultural data, working together end-to-end</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2)

with c1:
    st.markdown(
        f"""
        <div class="pf-card pf-card-accent">
            <div style="font-size:26px;">🌾</div>
            <div style="font-family:'Poppins',sans-serif; font-weight:600; font-size:16px; margin:10px 0 6px 0;">Crop Recommendation</div>
            <div style="color:{COLORS['muted']}; font-size:13.5px; line-height:1.55;">
                Recommends the most suitable crop from 22 possible types based on soil nutrients
                (N, P, K), temperature, humidity, pH and rainfall.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        f"""
        <div class="pf-card pf-card-accent">
            <div style="font-size:26px;">📈</div>
            <div style="font-family:'Poppins',sans-serif; font-weight:600; font-size:16px; margin:10px 0 6px 0;">Prediction Confidence</div>
            <div style="color:{COLORS['muted']}; font-size:13.5px; line-height:1.55;">
                Every recommendation comes with a confidence gauge and a ranked Top-5 view,
                so you see how sure the model is — not just its single best guess.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="pf-card pf-card-accent">
            <div style="font-size:26px;">🌱</div>
            <div style="font-family:'Poppins',sans-serif; font-weight:600; font-size:16px; margin:10px 0 6px 0;">Fertilizer Recommendation</div>
            <div style="color:{COLORS['muted']}; font-size:13.5px; line-height:1.55;">
                Suggests the optimal fertilizer from 7 classes using soil, crop, seasonal,
                irrigation and regional agricultural factors.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        f"""
        <div class="pf-card pf-card-accent">
            <div style="font-size:26px;">⚡</div>
            <div style="font-family:'Poppins',sans-serif; font-weight:600; font-size:16px; margin:10px 0 6px 0;">Instant Prediction</div>
            <div style="color:{COLORS['muted']}; font-size:13.5px; line-height:1.55;">
                Trained Random Forest models generate intelligent recommendations
                in a fraction of a second — no lab test required to get started.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.divider()

# --------------------------------------------------
# Model Performance
# --------------------------------------------------

st.markdown('<div class="pf-section-title">📊 Final Model Performance</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="pf-section-sub">Random Forest was selected for both tasks after comparing 5 algorithms on accuracy, precision, recall and F1-score</div>',
    unsafe_allow_html=True,
)

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=["Crop Model", "Fertilizer Model"],
        y=[99.55, 87.50],
        text=["99.55%", "87.50%"],
        textposition="outside",
        marker_color=[COLORS["forest"], COLORS["moss"]],
        width=[0.42, 0.42],
    )
)
fig.update_layout(
    template="plotly_white",
    height=380,
    yaxis=dict(range=[0, 110], title="Accuracy (%)", gridcolor="#EDF1E8"),
    xaxis_title="Deployed Random Forest Models",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font={"family": "Inter, sans-serif", "color": COLORS["text"]},
    margin=dict(t=20, b=10),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Workflow
# --------------------------------------------------

st.markdown('<div class="pf-section-title">🌾 How It Works</div>', unsafe_allow_html=True)
st.write("")

steps = [
    ("1", "Enter Parameters", "Provide soil & environmental readings"),
    ("2", "Choose a Module", "Crop or fertilizer recommendation"),
    ("3", "Model Predicts", "Random Forest scores every class"),
    ("4", "View Results", "Confidence gauge + Top-5 ranking"),
]
cols = st.columns(4)
for col, (num, title, desc) in zip(cols, steps):
    with col:
        st.markdown(
            f"""
            <div class="pf-card" style="text-align:center;">
                <div style="width:38px;height:38px;border-radius:50%;background:{COLORS['forest']};
                            color:white;font-family:'Poppins',sans-serif;font-weight:700;
                            display:flex;align-items:center;justify-content:center;margin:0 auto 12px auto;">
                    {num}
                </div>
                <div style="font-weight:600; font-size:14px; margin-bottom:4px;">{title}</div>
                <div style="color:{COLORS['muted']}; font-size:12px;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
st.divider()

# --------------------------------------------------
# Technologies
# --------------------------------------------------

st.markdown('<div class="pf-section-title">🛠️ Technologies Used</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="margin-top:8px;">
        <span class="pf-badge">Python</span>
        <span class="pf-badge">Pandas</span>
        <span class="pf-badge">NumPy</span>
        <span class="pf-badge">Scikit-learn</span>
        <span class="pf-badge">Random Forest</span>
        <span class="pf-badge">Plotly</span>
        <span class="pf-badge">Streamlit</span>
        <span class="pf-badge">Joblib</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.divider()

render_footer()
