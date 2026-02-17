import streamlit as st
import pandas as pd
import datetime
import os

# 1. --- CONFIG & STYLE ---
st.set_page_config(page_title="Hyper-Dex Local", page_icon="🏎️")

# 2. --- LOCAL STORAGE SETUP ---
DB_FILE = "cardex_db.csv"

# Load data from the CSV file if it exists
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["brand", "name", "rarity", "time"])

# 3. --- SCANNER SIDEBAR ---
with st.sidebar:
    st.header("📡 HYPER SCANNER")
    uploaded_file = st.file_uploader("Upload Car Photo", type=["jpg", "png", "jpeg"])
    
    brand = st.selectbox("Brand", ["McLaren", "Ferrari", "Lamborghini", "Porsche", "Other"])
    model = st.text_input("Model Name")
    rarity = st.selectbox("Rarity", ["Common", "Uncommon", "Rare", "Legendary", "Unicorn"])
    
    if st.button("LOG SIGHTING"):
        if model:
            # Create new entry
            new_entry = pd.DataFrame([{
                "brand": brand,
                "name": model,
                "rarity": rarity,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            
            # Combine and save to the CSV file
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(f"Logged {brand} {model}!")
            st.balloons()
        else:
            st.error("Enter a model name!")

# 4. --- MAIN DISPLAY ---
st.title("🏎️ RSF CAR-DEX")

if not df.empty:
    for index, row in df.iloc[::-1].iterrows():
        with st.container(border=True):
            st.subheader(f"{row['brand']} {row['name']}")
            st.write(f"TIER: {row['rarity']} | LOGGED: {row['time']}")
else:
    st.info("No cars logged yet.")
