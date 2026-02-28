import streamlit as st
import pickle
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ceylon Forecast",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# GLOBAL CSS (Simplified for stability)
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg: #080b12; --bg1: #0d1018; --bg2: #111520; --bg3: #161a28;
  --border: #1c2030; --border2: #242840; --gold: #c9aa71; --gold2: #e8c980;
  --gold-dim: rgba(201,170,113,0.12); --text: #ddd8ce; --text2: #8a8fa0;
  --text3: #45495a; --teal: #38c4b4; --rose: #e06b6b; --radius: 10px;
}

[data-testid="stAppViewContainer"] { background: var(--bg) !important; color: var(--text) !important; font-family: 'DM Sans', sans-serif !important; }
.hero-banner { background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 60%, #0d1520 100%); border-bottom: 1px solid var(--border); padding: 3rem 2.5rem 2.5rem; position: relative; }
.hero-title { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; color: #f2ece0; line-height: 1.05; }
.hero-title em { color: var(--gold); font-style: italic; }
.result-mega { text-align: center; padding: 2.8rem 1.5rem; background: var(--bg3); border-top: 3px solid var(--gold); border-radius: var(--radius); }
.result-mega-num { font-family: 'Playfair Display', serif; font-size: 4rem; color: var(--gold); }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# LOAD MODEL & ENCODERS
# ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    try:
        with open("tourist_model.pickle", "rb") as f:
            model = pickle.load(f)
        with open("encoders.pickle", "rb") as f:
            encoders = pickle.load(f)
        return model, encoders
    except FileNotFoundError as e:
        st.error(f"❌ Required file missing: {e.filename}")
        return None, None

assets = load_assets()
if not assets[0]: st.stop()
model, encoders = assets
le_country = encoders["le_country"]

MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
MONTH_MAP = {m: i+1 for i, m in enumerate(MONTHS)}

def predict_arrivals(year, month_num, country_name, dollar, cpi):
    # Encode country name to match training data
    try:
        country_enc = le_country.transform([country_name])[0]
    except ValueError:
        # Fallback if country is not in the encoder (e.g., grouped as 'Other' during training)
        country_enc = le_country.transform(['Other'])[0]
    
    # Feature order MUST match the order used during model.fit()
    features = np.array([[year, month_num, country_enc, dollar, cpi]])
    prediction = model.predict(features)[0]
    return max(0, int(prediction))

# ──────────────────────────────────────────────────────────────
# UI SECTIONS
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div style="font-size: 0.65rem; letter-spacing: 0.3em; color: var(--gold);">Sri Lanka · Arrivals Intelligence</div>
    <h1 class="hero-title">Tourist <em>Forecast</em><br>Engine</h1>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Forecast", "Analysis"])

with tab1:
    with st.form("main_form"):
        c1, c2, c3 = st.columns(3)
        with c1: country = st.selectbox("Origin Market", le_country.classes_)
        with c2: month = st.selectbox("Arrival Month", MONTHS)
        with c3: year = st.number_input("Target Year", 2018, 2040, 2026)
        
        c4, c5 = st.columns(2)
        with c4: dollar = st.slider("LKR/USD Rate", 150.0, 600.0, 310.0)
        with c5: cpi = st.slider("Consumer Price Index", 80.0, 450.0, 210.0)
        
        submit = st.form_submit_button("Run AI Projection")

    if submit:
        val = predict_arrivals(year, MONTH_MAP[month], country, dollar, cpi)
        
        st.markdown(f"""
        <div class="result-mega">
            <div style="font-size: 0.7rem; letter-spacing: 0.2em; color: #8a8fa0; text-transform: uppercase;">Estimated Monthly Arrivals</div>
            <div class="result-mega-num">{val:,}</div>
            <div style="color: #45495a;">Visitors from {country} in {month} {year}</div>
        </div>
        """, unsafe_allow_html=True)



