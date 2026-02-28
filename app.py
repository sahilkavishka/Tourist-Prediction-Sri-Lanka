import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Ceylon Forecast · Sri Lanka Tourism",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=Outfit:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --jungle:   #1a2e1a;
  --deep:     #0f1f10;
  --bark:     #2e1f0f;
  --leaf:     #2d5a27;
  --emerald:  #3a8c3a;
  --mint:     #7ec87e;
  --gold:     #d4a843;
  --amber:    #f0c060;
  --ivory:    #f5f0e8;
  --sand:     #e8d9b8;
  --mist:     #b8c8a8;
  --stone:    #8a9478;
  --text:     #f0ece4;
  --text2:    #b8b4a8;
  --text3:    #6a6860;
  --r:        12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] {
  background: var(--deep) !important;
  color: var(--text) !important;
  font-family: 'Outfit', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--jungle) !important; }
section[data-testid="stSidebar"] > div { background: var(--jungle) !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HERO ──────────────────────────────────────────────────── */
.hero {
  position: relative;
  min-height: 420px;
  background:
    linear-gradient(180deg, rgba(10,18,10,0.0) 0%, rgba(10,18,10,0.85) 70%, var(--deep) 100%),
    url('https://images.unsplash.com/photo-1586861635167-e5223aadc9fe?w=1600&q=80') center/cover no-repeat;
  display: flex;
  align-items: flex-end;
  padding: 3rem 3.5rem;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 30% 60%, rgba(42,90,35,0.3) 0%, transparent 60%);
  pointer-events: none;
}

.hero-eyebrow {
  font-family: 'DM Mono', monospace;
  font-size: 0.68rem;
  letter-spacing: 0.28em;
  color: var(--mint);
  text-transform: uppercase;
  margin-bottom: 0.75rem;
  opacity: 0.9;
}

.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2.8rem, 5vw, 4.5rem);
  font-weight: 300;
  color: var(--ivory);
  line-height: 1.05;
  margin-bottom: 0.5rem;
}

.hero-title strong {
  font-weight: 700;
  color: var(--amber);
  font-style: italic;
}

.hero-sub {
  font-size: 0.95rem;
  color: var(--mist);
  font-weight: 300;
  max-width: 500px;
  line-height: 1.6;
  margin-top: 0.75rem;
}

/* ── ATTRACTION STRIPS ───────────────────────────────────── */
.attraction-strip {
  display: flex;
  gap: 0;
  overflow: hidden;
  height: 120px;
}

.attr-card {
  flex: 1;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: flex 0.5s cubic-bezier(.4,0,.2,1);
}

.attr-card:hover { flex: 2; }

.attr-card img {
  width: 100%; height: 100%;
  object-fit: cover;
  filter: brightness(0.65) saturate(1.2);
  transition: filter 0.4s, transform 0.6s;
}

.attr-card:hover img {
  filter: brightness(0.85) saturate(1.4);
  transform: scale(1.05);
}

.attr-label {
  position: absolute;
  bottom: 8px; left: 10px;
  font-size: 0.62rem;
  letter-spacing: 0.15em;
  color: rgba(255,255,255,0.85);
  font-family: 'DM Mono', monospace;
  text-transform: uppercase;
  opacity: 0;
  transition: opacity 0.3s;
}

.attr-card:hover .attr-label { opacity: 1; }

/* ── MAIN CONTENT WRAPPER ────────────────────────────────── */
.main-wrap {
  padding: 2.5rem 3rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* ── SECTION HEADER ──────────────────────────────────────── */
.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.8rem;
}

.section-header .line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--leaf), transparent);
}

.section-header h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.4rem;
  font-weight: 400;
  color: var(--sand);
  white-space: nowrap;
}

.section-header .dot {
  width: 6px; height: 6px;
  background: var(--emerald);
  border-radius: 50%;
}

/* ── FORECAST PANEL ──────────────────────────────────────── */
.forecast-panel {
  background: linear-gradient(135deg, rgba(26,46,26,0.7) 0%, rgba(15,31,16,0.9) 100%);
  border: 1px solid rgba(58,140,58,0.2);
  border-radius: var(--r);
  padding: 2.2rem 2.5rem;
  backdrop-filter: blur(12px);
}

/* ── FORM LABELS ─────────────────────────────────────────── */
.stSelectbox label, .stSlider label, .stNumberInput label {
  font-family: 'DM Mono', monospace !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.18em !important;
  color: var(--mint) !important;
  text-transform: uppercase !important;
}

/* ── SELECT / INPUT ELEMENTS ─────────────────────────────── */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
  background: rgba(10,20,10,0.6) !important;
  border: 1px solid rgba(58,140,58,0.3) !important;
  border-radius: 8px !important;
  color: var(--ivory) !important;
}

.stSelectbox > div > div:hover,
.stNumberInput > div > div > input:hover {
  border-color: var(--emerald) !important;
}

/* ── SLIDER ──────────────────────────────────────────────── */
.stSlider > div > div > div > div {
  background: var(--emerald) !important;
}

/* ── SUBMIT BUTTON ───────────────────────────────────────── */
.stFormSubmitButton > button {
  width: 100% !important;
  background: linear-gradient(135deg, var(--leaf) 0%, var(--emerald) 100%) !important;
  color: var(--ivory) !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 0.9rem 2rem !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.08em !important;
  cursor: pointer !important;
  transition: all 0.3s !important;
  text-transform: uppercase !important;
  margin-top: 0.5rem !important;
}

.stFormSubmitButton > button:hover {
  background: linear-gradient(135deg, var(--emerald) 0%, #4fa84f 100%) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 24px rgba(58,140,58,0.35) !important;
}

/* ── RESULT CARD ─────────────────────────────────────────── */
.result-card {
  background: linear-gradient(135deg, rgba(26,46,26,0.95) 0%, rgba(20,38,15,0.98) 100%);
  border: 1px solid rgba(212,168,67,0.35);
  border-top: 3px solid var(--gold);
  border-radius: var(--r);
  padding: 2.5rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.result-card::before {
  content: '';
  position: absolute;
  top: -40%; left: 50%;
  transform: translateX(-50%);
  width: 300px; height: 300px;
  background: radial-gradient(ellipse, rgba(212,168,67,0.08) 0%, transparent 70%);
  pointer-events: none;
}

.result-label {
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.25em;
  color: var(--stone);
  text-transform: uppercase;
  margin-bottom: 0.8rem;
}

.result-number {
  font-family: 'Cormorant Garamond', serif;
  font-size: 4.5rem;
  font-weight: 700;
  color: var(--amber);
  line-height: 1;
  letter-spacing: -0.02em;
}

.result-desc {
  font-size: 0.82rem;
  color: var(--stone);
  margin-top: 0.6rem;
  font-weight: 300;
}

.result-badge {
  display: inline-block;
  background: rgba(58,140,58,0.15);
  border: 1px solid rgba(58,140,58,0.3);
  border-radius: 20px;
  padding: 0.3rem 1rem;
  font-size: 0.7rem;
  color: var(--mint);
  letter-spacing: 0.1em;
  margin-top: 1rem;
  font-family: 'DM Mono', monospace;
}

/* ── ATTRACTION INFO CARDS ───────────────────────────────── */
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
}

.info-card {
  background: rgba(26,46,26,0.4);
  border: 1px solid rgba(58,140,58,0.15);
  border-radius: var(--r);
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s, transform 0.3s;
}

.info-card:hover {
  border-color: rgba(58,140,58,0.4);
  transform: translateY(-2px);
}

.info-card-icon { font-size: 1.8rem; margin-bottom: 0.6rem; }
.info-card-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--sand);
  margin-bottom: 0.3rem;
}
.info-card-text {
  font-size: 0.78rem;
  color: var(--text3);
  line-height: 1.5;
  font-weight: 300;
}

/* ── TABS ────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid rgba(58,140,58,0.2) !important;
  gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--stone) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.7rem !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  padding: 0.8rem 1.5rem !important;
  border-bottom: 2px solid transparent !important;
  transition: all 0.2s !important;
}

.stTabs [aria-selected="true"] {
  color: var(--mint) !important;
  border-bottom-color: var(--emerald) !important;
}

/* ── DIVIDER ─────────────────────────────────────────────── */
.fancy-divider {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
}
.fancy-divider span { color: var(--emerald); font-size: 1rem; }
.fancy-divider .line {
  flex: 1; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(58,140,58,0.3), transparent);
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--deep); }
::-webkit-scrollbar-thumb { background: var(--leaf); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ── Load Assets ─────────────────────────────────────────────────────────────
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
if not assets[0]:
    st.stop()
model, encoders = assets
le_country = encoders["le_country"]

MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]
MONTH_MAP = {m: i+1 for i, m in enumerate(MONTHS)}

def predict_arrivals(year, month_num, country_name, dollar, cpi):
    try:
        country_enc = le_country.transform([country_name])[0]
    except ValueError:
        country_enc = le_country.transform(['Other'])[0]
    features = np.array([[year, month_num, country_enc, dollar, cpi]])
    prediction = model.predict(features)[0]
    return max(0, int(prediction))


# ── HERO SECTION ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div style="position:relative;z-index:2;">
    <div class="hero-eyebrow">🌿 Ceylon Intelligence Platform · Sri Lanka Tourism</div>
    <h1 class="hero-title">Predict Visitor<br><strong>Arrivals</strong> to the<br>Pearl of the Orient</h1>
    <p class="hero-sub">AI-powered forecasting for Sri Lanka's tourism landscape —<br>from Sigiriya to Galle, understand tomorrow's footfall today.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── ATTRACTION PHOTO STRIP ───────────────────────────────────────────────────
st.markdown("""
<div class="attraction-strip">
  <div class="attr-card">
    <img src="https://wallpapercave.com/wp/wp6828637.jpg" alt="Sigiriya"/>
    <span class="attr-label">Sigiriya</span>
  </div>
  <div class="attr-card">
    <img src="https://www.ceylonexpeditions.com/medias/destination_places/big/106/temple-of-the-sacred-tooth-relic-kandy.jpg" alt="Kandy"/>
    <span class="attr-label">Kandy</span>
  </div>
  <div class="attr-card">
    <img src="https://cms-artifacts.artlist.io/content/motion-array/1765785/Ancient_Fort_In_Galle_Sri_Lanka_high_resolution_preview_1765785.jpg?Expires=2036334195761&Key-Pair-Id=K2ZDLYDZI2R1DF&Signature=p8YlQkX9~9pxY3lhTYjbXgl6o~Snrn42jBerNLOklfJOEcmpj4ygBoG3jFp6UvLzMa8BsXUWzx6qjfgr6PlOh4COJ-A5wVMBq-kLI-F33E890Ljhaeu-wg3Rs3ri6QWOQVhD43ztCP0Gtp3Lx1o8GufuhcFX801tpaAxjgo-T0XhYy7ACYXaz0DK1N3SHVvGeULe~ZwAKgiiKyyY1Ebzj4NB4r1AWHcdUq7ZL0PBPrsWNYrWaRP7OCvbWPTH~Yx05HALPJfuZK2TIKO7VFxiyN9~IL5qqqI~CHjbaijLTToUTelZUzI3PDsTI~benwwZOCk7vRx5ir93Tz9Il95bxw__"," alt="Galle Fort"/>
    <span class="attr-label">Galle Fort</span>
  </div>
  <div class="attr-card">
    <img src="https://turystycznyninja.pl/wp-content/uploads/2023/01/Mirissa-Beach-Sri-Lanka-shutterstock.com-Creative-Family-1024x663.jpg" alt="Mirissa"/>
    <span class="attr-label">Mirissa Beach</span>
  </div>
  <div class="attr-card">
    <img src="https://wallpaperaccess.com/full/11885925.jpg" alt="Tea Plantations"/>
    <span class="attr-label">Nuwara Eliya</span>
  </div>
  <div class="attr-card">
    <img src="https://s1.it.atcdn.net/wp-content/uploads/2018/12/yala.jpg" alt="Yala"/>
    <span class="attr-label">Yala Safari</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN CONTENT ─────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊  Arrival Forecast", "🗺  Destination Insights"])

# ══════════════════════════════════════════════════════════════
# TAB 1 — FORECAST
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="section-header">
      <div class="dot"></div>
      <h2>Configure Your Forecast</h2>
      <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_result = st.columns([3, 2], gap="large")

    with col_form:
        st.markdown('<div class="forecast-panel">', unsafe_allow_html=True)
        with st.form("forecast_form"):
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                country = st.selectbox("Origin Country", le_country.classes_)
            with r1c2:
                month = st.selectbox("Month of Arrival", MONTHS)
            with r1c3:
                year = st.number_input("Target Year", 2018, 2040, 2026)

            st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

            r2c1, r2c2 = st.columns(2)
            with r2c1:
                dollar = st.slider("LKR / USD Exchange Rate", 150.0, 600.0, 310.0,
                                   help="Current LKR to USD rate impacts travel affordability")
            with r2c2:
                cpi = st.slider("Consumer Price Index", 80.0, 450.0, 210.0,
                                help="Cost of living index affecting tourist spending")

            submitted = st.form_submit_button("🌿  Run Forecast Projection")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        if submitted:
            val = predict_arrivals(year, MONTH_MAP[month], country, dollar, cpi)
            # Trend indicator (mock comparison)
            trend = "▲ Projected Growth" if val > 15000 else "◆ Stable Projection"

            st.markdown(f"""
            <div class="result-card">
              <div class="result-label">Estimated Monthly Arrivals</div>
              <div class="result-number">{val:,}</div>
              <div class="result-desc">
                Visitors from <strong style="color:var(--sand)">{country}</strong><br>
                arriving in <strong style="color:var(--sand)">{month} {year}</strong>
              </div>
              <div class="result-badge">{trend}</div>
              <div style="margin-top:1.5rem; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,0.07);">
                <div style="display:flex;justify-content:space-around;">
                  <div style="text-align:center;">
                    <div style="font-size:0.6rem;letter-spacing:0.15em;color:var(--stone);font-family:'DM Mono',monospace;text-transform:uppercase;">Exchange Rate</div>
                    <div style="font-size:1.1rem;color:var(--ivory);font-family:'Cormorant Garamond',serif;font-weight:600;">₨{dollar:.0f}</div>
                  </div>
                  <div style="width:1px;background:rgba(255,255,255,0.07)"></div>
                  <div style="text-align:center;">
                    <div style="font-size:0.6rem;letter-spacing:0.15em;color:var(--stone);font-family:'DM Mono',monospace;text-transform:uppercase;">CPI Index</div>
                    <div style="font-size:1.1rem;color:var(--ivory);font-family:'Cormorant Garamond',serif;font-weight:600;">{cpi:.0f}</div>
                  </div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-card" style="opacity:0.55;">
              <div style="font-size:2.5rem;margin-bottom:1rem;">🌿</div>
              <div class="result-label">Awaiting Input</div>
              <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:var(--sand);font-weight:300;line-height:1.5;">
                Configure the parameters and run your forecast projection
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Mini info cards ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="fancy-divider">
      <div class="line"></div>
      <span>✦</span>
      <div class="line"></div>
    </div>
    <div class="info-grid">
      <div class="info-card">
        <div class="info-card-icon">📅</div>
        <div class="info-card-title">Peak Season</div>
        <div class="info-card-text">December – March sees the highest tourist arrivals, with dry weather across the west and south coasts ideal for beach tourism.</div>
      </div>
      <div class="info-card">
        <div class="info-card-icon">✈️</div>
        <div class="info-card-title">Top Origin Markets</div>
        <div class="info-card-text">India, UK, Germany, China & Australia consistently lead as the largest inbound tourism source markets for Sri Lanka.</div>
      </div>
      <div class="info-card">
        <div class="info-card-icon">💱</div>
        <div class="info-card-title">Economic Sensitivity</div>
        <div class="info-card-text">Exchange rate volatility significantly impacts affordability perception for international visitors and travel decisions.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 2 — DESTINATION INSIGHTS
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="section-header">
      <div class="dot"></div>
      <h2>Sri Lanka's Iconic Destinations</h2>
      <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    destinations = [
        {
            "name": "Sigiriya Rock Fortress",
            "region": "Central Province",
            "type": "UNESCO Heritage",
            "icon": "🏛",
            "img": "https://wallpapercave.com/wp/wp6828637.jpg",
            "desc": "A 5th-century citadel perched atop a volcanic rock column rising 180m. Adorned with ancient frescoes and surrounded by water gardens, it is Sri Lanka's most visited landmark.",
            "best_time": "Jan – Apr",
            "visitors": "~600K/yr",
            "rating": "★★★★★"
        },
        {
            "name": "Temple of the Tooth",
            "region": "Kandy",
            "type": "Sacred Site",
            "icon": "🏯",
            "img": "https://www.ceylonexpeditions.com/medias/destination_places/big/106/temple-of-the-sacred-tooth-relic-kandy.jpg",
            "desc": "Housing the sacred relic of the Buddha's tooth, this temple in Kandy is the holiest place of worship for Buddhists worldwide. The Esala Perahera festival draws thousands annually.",
            "best_time": "Jan – Mar",
            "visitors": "~1M/yr",
            "rating": "★★★★★"
        },
        {
            "name": "Galle Dutch Fort",
            "region": "Southern Province",
            "type": "Colonial Heritage",
            "icon": "⚓",
            "img": "https://cms-artifacts.artlist.io/content/motion-array/1765785/Ancient_Fort_In_Galle_Sri_Lanka_high_resolution_preview_1765785.jpg?Expires=2036334195761&Key-Pair-Id=K2ZDLYDZI2R1DF&Signature=p8YlQkX9~9pxY3lhTYjbXgl6o~Snrn42jBerNLOklfJOEcmpj4ygBoG3jFp6UvLzMa8BsXUWzx6qjfgr6PlOh4COJ-A5wVMBq-kLI-F33E890Ljhaeu-wg3Rs3ri6QWOQVhD43ztCP0Gtp3Lx1o8GufuhcFX801tpaAxjgo-T0XhYy7ACYXaz0DK1N3SHVvGeULe~ZwAKgiiKyyY1Ebzj4NB4r1AWHcdUq7ZL0PBPrsWNYrWaRP7OCvbWPTH~Yx05HALPJfuZK2TIKO7VFxiyN9~IL5qqqI~CHjbaijLTToUTelZUzI3PDsTI~benwwZOCk7vRx5ir93Tz9Il95bxw__",
            "desc": "A UNESCO World Heritage fort built by the Dutch in 1663. Its cobblestone streets, colonial architecture, boutique hotels and art galleries make it a cultural gem by the Indian Ocean.",
            "best_time": "Nov – Apr",
            "visitors": "~500K/yr",
            "rating": "★★★★☆"
        },
        {
            "name": "Mirissa Beach",
            "region": "Southern Coast",
            "type": "Beach & Whales",
            "icon": "🐋",
            "img": "https://turystycznyninja.pl/wp-content/uploads/2023/01/Mirissa-Beach-Sri-Lanka-shutterstock.com-Creative-Family-1024x663.jpg",
            "desc": "One of Asia's premier whale watching destinations. Blue whales and sperm whales migrate through from November to April. The crescent beach also offers world-class surfing and sunsets.",
            "best_time": "Nov – Apr",
            "visitors": "~350K/yr",
            "rating": "★★★★☆"
        },
        {
            "name": "Nuwara Eliya",
            "region": "Hill Country",
            "type": "Tea & Nature",
            "icon": "🍃",
            "img": "https://wallpaperaccess.com/full/11885925.jpg",
            "desc": "Sri Lanka's 'Little England' set at 1,868m altitude. Endless emerald tea estates, colonial bungalows and cool misty air make this the island's most scenic hill destination.",
            "best_time": "Apr – Sep",
            "visitors": "~400K/yr",
            "rating": "★★★★★"
        },
        {
            "name": "Yala National Park",
            "region": "Uva Province",
            "type": "Wildlife Safari",
            "icon": "🐆",
            "img": "https://s1.it.atcdn.net/wp-content/uploads/2018/12/yala.jpg",
            "desc": "Home to the world's highest density of wild leopards. Also hosts elephants, sloth bears, crocodiles, and over 215 bird species across diverse ecosystems of scrub jungle and lagoons.",
            "best_time": "Feb – Jun",
            "visitors": "~300K/yr",
            "rating": "★★★★★"
        },
    ]

    for i in range(0, len(destinations), 2):
        cols = st.columns(2, gap="large")
        for j, col in enumerate(cols):
            if i + j < len(destinations):
                d = destinations[i + j]
                with col:
                    st.markdown(f"""
                    <div style="
                      background: rgba(26,46,26,0.35);
                      border: 1px solid rgba(58,140,58,0.15);
                      border-radius: var(--r);
                      overflow: hidden;
                      margin-bottom: 1.2rem;
                      transition: border-color 0.3s;
                    ">
                      <div style="position:relative;height:180px;overflow:hidden;">
                        <img src="{d['img']}"
                          style="width:100%;height:100%;object-fit:cover;filter:brightness(0.75) saturate(1.3);"
                          alt="{d['name']}"/>
                        <div style="
                          position:absolute;inset:0;
                          background:linear-gradient(180deg,transparent 40%,rgba(10,18,10,0.85) 100%);
                        "></div>
                        <div style="position:absolute;top:12px;left:12px;">
                          <span style="
                            background:rgba(58,140,58,0.75);
                            border:1px solid rgba(126,200,126,0.4);
                            border-radius:20px;
                            padding:0.2rem 0.7rem;
                            font-family:'DM Mono',monospace;
                            font-size:0.58rem;
                            letter-spacing:0.12em;
                            color:var(--mint);
                          ">{d['type']}</span>
                        </div>
                        <div style="position:absolute;bottom:12px;left:14px;right:14px;">
                          <div style="
                            font-family:'Cormorant Garamond',serif;
                            font-size:1.35rem;
                            font-weight:700;
                            color:var(--ivory);
                            line-height:1.1;
                          ">{d['icon']} {d['name']}</div>
                          <div style="font-size:0.68rem;color:var(--mist);margin-top:2px;font-family:'DM Mono',monospace;">{d['region']}</div>
                        </div>
                      </div>
                      <div style="padding:1.2rem 1.4rem 1.4rem;">
                        <p style="font-size:0.8rem;color:var(--text2);line-height:1.65;font-weight:300;">{d['desc']}</p>
                        <div style="
                          display:flex;justify-content:space-between;
                          margin-top:1rem;padding-top:0.8rem;
                          border-top:1px solid rgba(58,140,58,0.12);
                        ">
                          <div style="text-align:center;">
                            <div style="font-size:0.58rem;letter-spacing:0.12em;color:var(--stone);font-family:'DM Mono',monospace;text-transform:uppercase;">Best Time</div>
                            <div style="font-size:0.82rem;color:var(--sand);margin-top:2px;">{d['best_time']}</div>
                          </div>
                          <div style="text-align:center;">
                            <div style="font-size:0.58rem;letter-spacing:0.12em;color:var(--stone);font-family:'DM Mono',monospace;text-transform:uppercase;">Annual Visitors</div>
                            <div style="font-size:0.82rem;color:var(--sand);margin-top:2px;">{d['visitors']}</div>
                          </div>
                          <div style="text-align:center;">
                            <div style="font-size:0.58rem;letter-spacing:0.12em;color:var(--stone);font-family:'DM Mono',monospace;text-transform:uppercase;">Rating</div>
                            <div style="font-size:0.78rem;color:var(--amber);margin-top:2px;">{d['rating']}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
  border-top: 1px solid rgba(58,140,58,0.15);
  padding: 1.5rem 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
">
  <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:var(--stone);">
    Ceylon <em style="color:var(--mint)">Forecast</em>
  </div>
  <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.15em;color:var(--text3);">
    POWERED BY AI · SRI LANKA TOURISM DATA
  </div>
  <div style="font-size:0.72rem;color:var(--text3);">
    🌿 Pearl of the Indian Ocean
  </div>
</div>
""", unsafe_allow_html=True)