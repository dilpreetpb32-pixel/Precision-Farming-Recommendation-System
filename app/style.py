"""
Shared design system for the AI-Based Precision Farming Recommendation Engine.

This module centralizes the color palette, typography, CSS injection and a
handful of reusable UI components (hero header, sidebar, metric cards,
confidence gauge, top-5 bar chart) so that Home.py and every page under
app/pages/ look and feel like one cohesive, professionally designed product
rather than three separate Streamlit scripts.
"""

import re

import streamlit as st
import plotly.graph_objects as go

# --------------------------------------------------------------------------
# Brand palette — kept in one place so every page stays visually consistent
# --------------------------------------------------------------------------

COLORS = {
    "forest": "#2C5F2D",
    "forest_dark": "#1D3F1E",
    "moss": "#97BC62",
    "moss_light": "#E4EFD6",
    "gold": "#E9A23B",
    "cream": "#F5F7F2",
    "white": "#FFFFFF",
    "text": "#1F2D1F",
    "muted": "#5A6B5A",
    "danger": "#C0392B",
}

FONT_IMPORT_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600&display=swap"
)


def inject_base_css():
    """Injects global CSS shared by every page: fonts, layout, cards,
    buttons, inputs, tables, sidebar and footer."""

    css = f"""
        <link href="{FONT_IMPORT_URL}" rel="stylesheet">
        <style>
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        h1, h2, h3, h4 {{
            font-family: 'Poppins', sans-serif !important;
            color: {COLORS['text']};
        }}

        .block-container {{
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }}

        /* ---------- Hero banner ---------- */
        .pf-hero {{
            background: linear-gradient(135deg, {COLORS['forest']} 0%, {COLORS['forest_dark']} 100%);
            border-radius: 18px;
            padding: 44px 48px;
            color: white;
            margin-bottom: 28px;
            position: relative;
            overflow: hidden;
        }}
        .pf-hero::after {{
            content: "";
            position: absolute;
            top: -60px; right: -60px;
            width: 220px; height: 220px;
            background: rgba(151, 188, 98, 0.25);
            border-radius: 50%;
        }}
        .pf-hero-eyebrow {{
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 2.5px;
            color: {COLORS['gold']};
            text-transform: uppercase;
            margin-bottom: 6px;
        }}
        .pf-hero h1 {{
            color: white !important;
            font-size: 34px;
            font-weight: 700;
            margin: 0 0 10px 0;
        }}
        .pf-hero p {{
            color: #DCE9CE;
            font-size: 16px;
            max-width: 720px;
            margin: 0;
            line-height: 1.5;
        }}

        /* ---------- Section headers ---------- */
        .pf-section-title {{
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 21px;
            color: {COLORS['text']};
            margin: 6px 0 2px 0;
        }}
        .pf-section-sub {{
            color: {COLORS['muted']};
            font-size: 13.5px;
            margin-bottom: 18px;
        }}

        /* ---------- Cards ---------- */
        .pf-card {{
            background: {COLORS['white']};
            border: 1px solid #E7ECE2;
            border-radius: 14px;
            padding: 22px 24px;
            box-shadow: 0 2px 10px rgba(31, 45, 31, 0.04);
            height: 100%;
        }}
        .pf-card-accent {{
            border-top: 4px solid {COLORS['forest']};
        }}

        /* ---------- Metric tiles ---------- */
        .pf-metric {{
            background: {COLORS['white']};
            border: 1px solid #E7ECE2;
            border-radius: 14px;
            padding: 18px 20px;
            text-align: left;
            box-shadow: 0 2px 10px rgba(31, 45, 31, 0.04);
        }}
        .pf-metric-value {{
            font-family: 'Poppins', sans-serif;
            font-size: 30px;
            font-weight: 700;
            color: {COLORS['forest']};
            line-height: 1.1;
        }}
        .pf-metric-label {{
            color: {COLORS['muted']};
            font-size: 12.5px;
            font-weight: 500;
            margin-top: 4px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }}

        /* ---------- Result banner ---------- */
        .pf-result {{
            background: linear-gradient(135deg, {COLORS['forest']} 0%, {COLORS['forest_dark']} 100%);
            border-radius: 16px;
            padding: 30px 34px;
            color: white;
            margin: 10px 0 22px 0;
        }}
        .pf-result-eyebrow {{
            font-size: 12.5px;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: {COLORS['gold']};
            margin-bottom: 8px;
        }}
        .pf-result-value {{
            font-family: 'Poppins', sans-serif;
            font-size: 36px;
            font-weight: 700;
            margin: 0 0 6px 0;
        }}
        .pf-result-desc {{
            color: #DCE9CE;
            font-size: 14px;
            max-width: 640px;
        }}

        /* ---------- Badges / pills ---------- */
        .pf-badge {{
            display: inline-block;
            background: {COLORS['moss_light']};
            color: {COLORS['forest_dark']};
            padding: 5px 14px;
            border-radius: 999px;
            font-size: 12.5px;
            font-weight: 600;
            margin: 3px 6px 3px 0;
        }}

        /* ---------- Buttons ---------- */
        div.stButton > button {{
            background: {COLORS['forest']};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 1.2rem;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.15s ease;
        }}
        div.stButton > button:hover {{
            background: {COLORS['forest_dark']};
            color: white;
            transform: translateY(-1px);
        }}

        /* ---------- Inputs ---------- */
        div[data-baseweb="input"], div[data-baseweb="select"] > div {{
            border-radius: 8px !important;
        }}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{
            background: {COLORS['forest_dark']};
        }}
        section[data-testid="stSidebar"] * {{
            color: #E4EFD6 !important;
        }}
        section[data-testid="stSidebar"] .pf-sidebar-title {{
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 19px;
            color: white !important;
            margin-bottom: 2px;
        }}
        section[data-testid="stSidebar"] .pf-sidebar-sub {{
            font-size: 12px;
            color: #9CB78A !important;
            margin-bottom: 18px;
        }}
        section[data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,0.12);
        }}
        .pf-nav-link {{
            display: block;
            padding: 9px 12px;
            border-radius: 8px;
            margin-bottom: 4px;
            font-size: 14.5px;
            font-weight: 500;
            text-decoration: none !important;
        }}
        .pf-nav-active {{
            background: {COLORS['moss']};
            color: {COLORS['forest_dark']} !important;
            font-weight: 700;
        }}
        .pf-nav-inactive {{
            background: rgba(255,255,255,0.06);
        }}

        /* ---------- Footer ---------- */
        .pf-footer {{
            text-align: center;
            color: {COLORS['muted']};
            font-size: 12.5px;
            padding: 26px 0 6px 0;
        }}

        /* ---------- Dataframe polish ---------- */
        div[data-testid="stDataFrame"] {{
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #E7ECE2;
        }}

        /* Hide default streamlit chrome we don't want */
        #MainMenu {{visibility: hidden;}}
        div[data-testid="stSidebarNav"] {{display: none;}}
        footer {{visibility: hidden;}}
        </style>
        """

    css = "\n".join(line for line in css.splitlines() if line.strip() != "")
    st.markdown(css, unsafe_allow_html=True)


def render_sidebar(active: str):
    """Renders the shared branded sidebar navigation.

    active: one of "home", "crop", "fertilizer" — used to highlight the
    current page in the nav list.
    """

    def link_class(key):
        return "pf-nav-link pf-nav-active" if key == active else "pf-nav-link pf-nav-inactive"

    st.sidebar.markdown(
        f"""
        <div class="pf-sidebar-title">🌾 Precision Farming</div>
        <div class="pf-sidebar-sub">AI Recommendation Engine</div>
        <a class="{link_class('home')}" href="/" target="_self">🏠&nbsp;&nbsp;Home</a>
        <a class="{link_class('crop')}" href="/Crop_Recommendation" target="_self">🌾&nbsp;&nbsp;Crop Recommendation</a>
        <a class="{link_class('fertilizer')}" href="/Fertilizer_Recommendation" target="_self">🌱&nbsp;&nbsp;Fertilizer Recommendation</a>
        <hr>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("**📌 Project Highlights**")
    st.sidebar.markdown(
        """
        <div style="font-size: 13px; line-height: 2;">
        🤖 Random Forest Models<br>
        🌾 22 Crop Types Supported<br>
        🌱 7 Fertilizer Classes<br>
        📈 Confidence-Scored Predictions<br>
        📊 Top-5 Ranked Recommendations
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.caption("AI-Based Precision Farming Recommendation System")
    st.sidebar.caption("Developed by Dilpreet Kaur · B.Sc. IT, LPU")


def render_hero(eyebrow: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="pf-hero">
            <div class="pf-hero-eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_row(metrics):
    """metrics: list of (value, label) tuples."""
    cols = st.columns(len(metrics))
    for col, (value, label) in zip(cols, metrics):
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


def render_result_banner(eyebrow: str, value: str, description: str):
    st.markdown(
        f"""
        <div class="pf-result">
            <div class="pf-result-eyebrow">{eyebrow}</div>
            <div class="pf-result-value">{value}</div>
            <div class="pf-result-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def confidence_gauge(confidence: float, label: str = "Prediction Confidence"):
    """Returns a Plotly gauge figure styled to match the brand palette."""

    if confidence >= 80:
        bar_color = COLORS["forest"]
    elif confidence >= 50:
        bar_color = COLORS["gold"]
    else:
        bar_color = COLORS["danger"]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=confidence,
            number={"suffix": "%", "font": {"size": 34, "family": "Poppins, sans-serif", "color": COLORS["text"]}},
            title={"text": label, "font": {"size": 14, "family": "Inter, sans-serif", "color": COLORS["muted"]}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": COLORS["muted"]},
                "bar": {"color": bar_color, "thickness": 0.28},
                "bgcolor": "white",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "#F3F5EF"},
                    {"range": [50, 80], "color": "#EAF0DE"},
                    {"range": [80, 100], "color": "#DCEACB"},
                ],
            },
        )
    )
    fig.update_layout(
        height=230,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif"},
    )
    return fig


def top5_bar_chart(labels, values, title: str, unit_label: str = "Confidence (%)"):
    """Horizontal bar chart for top-5 style ranked predictions, styled to
    match the brand palette, with the top prediction highlighted."""

    labels = list(labels)[::-1]
    values = list(values)[::-1]
    colors = [COLORS["moss"]] * len(values)
    colors[-1] = COLORS["forest"]  # top prediction (last after reversal)

    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=colors,
            text=[f"{v:.1f}%" for v in values],
            textposition="outside",
            cliponaxis=False,
        )
    )
    fig.update_layout(
        title={"text": title, "font": {"size": 15, "family": "Poppins, sans-serif", "color": COLORS["text"]}},
        xaxis_title=unit_label,
        height=300,
        margin=dict(l=10, r=30, t=50, b=30),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif", "color": COLORS["text"]},
        xaxis=dict(range=[0, max(values) * 1.18 if values else 100], gridcolor="#EDF1E8"),
    )
    return fig


def render_footer():
    st.markdown(
        """
        <div class="pf-footer">
            <b>AI-Based Precision Farming Recommendation Engine</b><br>
            Developed by Dilpreet Kaur · B.Sc. IT, Lovely Professional University
        </div>
        """,
        unsafe_allow_html=True,
    )
