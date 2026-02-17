import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# 1. --- CONFIG & STYLE ---
st.set_page_config(page_title="Hyper-Dex Lite", page_icon="🏎️")

st.markdown("""
    <style>
    .stApp { background: #0f0c29; color: white; }
    .car-card { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #FFD700; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. --- CONNECT TO SHEET ---
# This uses the public link you put in your Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. --- SCANNER SIDEBAR ---
with st.sidebar:
    st.header("📡 HYPER SCANNER")
    brand = st.selectbox("Brand", ["Ferrari", "Lamborghini", "Porsche", "McLaren", "Other"])
    model = st.text_input("Model Name")
    rarity = st.selectbox("Rarity", ["Common", "Uncommon", "Rare", "Legendary", "Unicorn"])
    
    if st.button("LOG SIGHTING"):
        if model:
            # Create a new row of data
            new_data = pd.DataFrame([{
                "brand": brand,
                "name": model,
                "rarity": rarity,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            
            # Get existing data and add the new row
            existing_data = conn.read()
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            
            # Save back to Google Sheets
            conn.update(data=updated_df)
            st.success("Target Saved!")
        else:
            st.error("Please enter a model name")

# 4. --- DISPLAY ---
st.title("🏎️ RSF CAR-DEX (LIVE)")

try:
    df = conn.read()
    if not df.empty:
        for index, row in df.iloc[::-1].iterrows():
            st.markdown(f"""
                <div class="car-card">
                    <h4>{row['brand']} {row['name']}</h4>
                    <p>TIER: {row['rarity']} | LOGGED: {row['time']}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No cars logged yet!")
except Exception as e:
    st.warning("Database connecting... make sure your Sheet link is in Secrets!")
