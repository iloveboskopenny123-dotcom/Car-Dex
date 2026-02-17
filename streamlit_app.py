import streamlit as st
import pandas as pd
import datetime
import os
from PIL import Image

# 1. --- CONFIG & DIRECTORY SETUP ---
st.set_page_config(page_title="Hyper-Dex Final", page_icon="🏎️")
DB_FILE = "cardex_db.csv"
IMG_DIR = "saved_cars"

# Create folders if they don't exist
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# 2. --- LOAD DATA ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["brand", "name", "rarity", "time", "img_path"])

# 3. --- SCANNER SIDEBAR ---
with st.sidebar:
    st.header("📡 HYPER SCANNER")
    uploaded_file = st.file_uploader("Upload Car Photo", type=["jpg", "png", "jpeg"])
    
    # BRAND LOGIC FIX
    brand_choice = st.selectbox("Brand", ["McLaren", "Ferrari", "Lamborghini", "Porsche", "Other"])
    if brand_choice == "Other":
        brand = st.text_input("Type Brand Name")
    else:
        brand = brand_choice

    model = st.text_input("Model Name")
    rarity = st.selectbox("Rarity", ["Common", "Uncommon", "Rare", "Legendary", "Unicorn"])
    
    if st.button("LOG SIGHTING"):
        if model and uploaded_file and brand:
            # SAVE THE IMAGE FILE
            img_filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            img_path = os.path.join(IMG_DIR, img_filename)
            img = Image.open(uploaded_file)
            img.save(img_path)

            # SAVE TEXT DATA + IMAGE PATH TO CSV
            new_entry = pd.DataFrame([{
                "brand": brand,
                "name": model,
                "rarity": rarity,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "img_path": img_path
            }])
            
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(f"Secured {brand} {model}!")
            st.rerun() # Refresh to show the new car immediately
        else:
            st.error("Missing Info: Need Brand, Model, and Photo!")

# 4. --- MAIN DISPLAY ---
st.title("🏎️ RSF CAR-DEX")

if not df.empty:
    # Use reversed order to show newest first
    for index, row in df.iloc[::-1].iterrows():
        with st.container(border=True):
            # Display the Brand and Model
            st.subheader(f"{row['brand']} {row['name']}")
            st.write(f"**TIER:** {row['rarity']} | **LOGGED:** {row['time']}")
            
            # Display the saved image using the path from the CSV
            if os.path.exists(str(row['img_path'])):
                st.image(row['img_path'], use_container_width=True)
else:
    st.info("No cars logged yet. Get out there and start spotting!")
