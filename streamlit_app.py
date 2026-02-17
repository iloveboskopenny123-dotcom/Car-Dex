import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# 1. --- CONFIG & STYLE ---
st.set_page_config(page_title="Hyper-Dex Lite", page_icon="🏎️")

# 2. --- SESSION STATE (Memory) ---
# This prevents the "disappearing photo" glitch
if "last_uploaded_image" not in st.session_state:
    st.session_state.last_uploaded_image = None

# 3. --- CONNECT TO SHEET ---
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. --- SCANNER SIDEBAR ---
with st.sidebar:
    st.header("📡 HYPER SCANNER")
    
    # The Photo Uploader
    uploaded_file = st.file_uploader("Upload Car Photo", type=["jpg", "png", "jpeg"])
    
    # If a file is uploaded, show a tiny preview in the sidebar so you know it's there
    if uploaded_file:
        st.session_state.last_uploaded_image = uploaded_file
        st.image(uploaded_file, caption="Photo Loaded ✅", width=150)

    brand = st.selectbox("Brand", ["Ferrari", "Lamborghini", "Porsche", "McLaren", "Koenigsegg", "Pagani", "Bugatti", "Other"])
    model = st.text_input("Model Name")
    rarity = st.select_slider("Rarity", options=["Common", "Uncommon", "Rare", "Legendary", "Unicorn"])
    
    if st.button("LOG SIGHTING"):
        if model and uploaded_file:
            # Create a new row (Note: Since this is Lite, we log the text to the sheet)
            new_data = pd.DataFrame([{
                "brand": brand,
                "name": model,
                "rarity": rarity,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            
            # Save to Google Sheets
            try:
                existing_data = conn.read()
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"Logged {model} to your Google Sheet!")
                st.balloons()
            except:
                st.error("Connection Error. Check your Sheet link in Secrets!")
        else:
            st.warning("⚠️ Please upload a photo and enter the model name first!")

# 5. --- MAIN DISPLAY ---
st.title("🏎️ RSF CAR-DEX")

try:
    df = conn.read()
    if not df.empty:
        # Show the list of cars caught
        for index, row in df.iloc[::-1].iterrows():
            with st.container(border=True):
                st.subheader(f"{row['brand']} {row['name']}")
                st.write(f"**TIER:** {row['rarity']} | **LOGGED:** {row['time']}")
    else:
        st.info("The streets are quiet... No cars logged yet.")
except:
    st.info("Connect your Google Sheet link in the Streamlit Settings to see the database.")
