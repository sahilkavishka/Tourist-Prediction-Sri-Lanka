import streamlit as st
import pickle
import numpy as np
import pandas as pd
import time
import plotly.express as px
from datetime import datetime

# --- 1. LOAD THE SAVED FILES ---
@st.cache_resource
def load_data():
    """Load model and encoders with error handling"""
    try:
        with open('tourist_model.pickle', 'rb') as file:
            model = pickle.load(file)
    except FileNotFoundError:
        st.error("❌ Model file 'tourist_model.pickle' not found.")
        return None, None

    try:
        with open('encoders.pickle', 'rb') as file:
            encoders = pickle.load(file)
    except FileNotFoundError:
        st.error("❌ Encoders file 'encoders.pickle' not found.")
        return None, None

    return model, encoders

model, encoders = load_data()

if model and encoders:
    # Extract encoders from the dictionary saved in your training step
    le_country = encoders["le_country"]

    # --- 2. PAGE CONFIGURATION & STYLING ---
    st.set_page_config(
        page_title="Sri Lanka Tourist Predictor 2026",
        page_icon="🌴",
        layout="wide"
    )

    st.markdown("""
        <style>
        .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        .stButton > button {
            background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
            color: white; font-size: 18px; font-weight: 600;
            border-radius: 12px; padding: 12px 28px; width: 100%;
            border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .metric-card {
            background: white; padding: 25px; border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
        }
        h1 { background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             text-align: center; font-size: 42px; font-weight: 700; }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    st.sidebar.image("https://flagcdn.com/w320/lk.png", width=100)
    st.sidebar.title("⚙️ Market Settings")
    st.sidebar.info("Predicting tourist arrivals based on economic indicators.")

    # --- MAIN PAGE ---
    st.markdown("<h1> 🌴 Sri Lanka Tourist Predictor</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔮 Prediction", "📈 Analysis", "ℹ️ Guide"])

    with tab1:
        with st.form("tourist_form"):
            st.markdown("### 📋 Journey Details")
            col1, col2 = st.columns(2)
            
            with col1:
                # Use encoders.classes_ to populate the dropdown
                country = st.selectbox("📍 Origin Country", le_country.classes_)
                month = st.selectbox("📅 Month", 
                    ['January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December'])
                year = st.number_input("📅 Target Year", value=2026, min_value=2018)

            with col2:
                dollar_rate = st.number_input("💱 Dollar Rate (LKR)", value=300.0, step=1.0)
                cpi = st.number_input("📉 Consumer Price Index", value=200.0, step=0.1)

            submitted = st.form_submit_button("🚀 Calculate Forecast")

        if submitted:
            with st.spinner("🔍 Simulating Arrivals..."):
                time.sleep(0.5)
                
                # Preprocessing
                month_map = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,
                             'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
                
                # Prepare Inputs (Ensure this matches the order in your X_train)
                # Features used: ['year', 'month_num', 'country_encoded', 'dollarRate', 'consumerPriceIndex']
                month_num = month_map[month]
                country_enc = le_country.transform([country])[0]
                
                features = np.array([[year, month_num, country_enc, dollar_rate, cpi]])
                prediction = model.predict(features)[0]

                # --- DISPLAY RESULTS ---
                st.markdown("### 📊 Predicted Monthly Arrivals")
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4 style="color: #666;">Estimated Arrivals</h4>
                        <h1 style="color: #00b09b; font-size: 50px;">{int(prediction):,}</h1>
                        <p>Expected visitors from {country}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col_res2:
                    st.info("💡 Tip: Use these predictions to plan hotel capacity and service availability.")

    with tab2:
        st.markdown("### 📈 Market Trends")
        st.write("This section can display historical trends from your `touristData.csv`.")

    with tab3:
        st.markdown("### ℹ️ How to Use")
        st.write("1. Select the origin country. Note: Countries with very few historical records are grouped as **'Other'**.")
        st.write("2. Input the expected dollar exchange rate and CPI.")
        st.write("3. View the AI-generated prediction.")

else:
    st.error("⚠️ Ensure 'tourist_model.pickle' and 'encoders.pickle' are in the same folder as app.py.")