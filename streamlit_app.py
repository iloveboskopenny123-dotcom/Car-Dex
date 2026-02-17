import streamlit as st
import pandas as pd
import datetime
import os
from PIL import Image

# 1. --- CONFIG & DIRECTORY SETUP ---
st.set_page_config(page_title="Hyper-Dex Admin", page_icon="🏎️")
DB_FILE = "cardex_db.csv"
IMG_DIR = "saved_cars"

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
    
    brand_choice = st.selectbox("Brand", ["McLaren", "Ferrari", "Lamborghini", "Porsche", "Koenigsegg", "Pagani", "Bugatti", "Other"])
    brand = st.text_input("Type Brand Name") if brand_choice == "Other" else brand_choice

    model = st.text_input("Model Name")
    rarity = st.selectbox("Rarity", ["Common", "Uncommon", "Rare", "Legendary", "Unicorn"])
    
    if st.button("LOG SIGHTING"):
        if model and uploaded_file and brand:
            img_filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            img_path = os.path.join(IMG_DIR, img_filename)
            Image.open(uploaded_file).save(img_path)

            new_entry = pd.DataFrame([{
                "brand": brand, "name": model, "rarity": rarity,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "img_path": img_path
            }])
            
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(f"Secured {brand} {model}!")
            st.rerun()
        else:
            st.error("Missing Info!")

# 4. --- MAIN DISPLAY & DELETE LOGIC ---
st.title("🏎️ RSF CAR-DEX")

if not df.empty:
    # reversed loop so newest is on top
    for index, row in df.iloc[::-1].iterrows():
        with st.container(border=True):
            st.subheader(f"{row['brand']} {row['name']}")
            st.write(f"**TIER:** {row['rarity']} | **LOGGED:** {row['time']}")
            
            if os.path.exists(str(row['img_path'])):
                st.image(row['img_path'], use_container_width=True)
            
            # --- THE DELETE BUTTON ---
            # We give each button a unique 'key' based on its index
            if st.button(f"🗑️ DELETE {row['name']}", key=f"delete_{index}"):
                # 1. Delete the actual image file from the folder
                if os.path.exists(str(row['img_path'])):
                    os.remove(row['img_path'])
                
                # 2. Remove the row from the CSV
                df = df.drop(index)
                df.to_csv(DB_FILE, index=False)
                
                # 3. Refresh the app
                st.toast(f"Entry {row['name']} removed from database.")
                st.rerun()
else:
    st.info("No cars logged yet.")
