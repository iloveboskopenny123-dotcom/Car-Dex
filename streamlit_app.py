import streamlit as st
from PIL import Image
import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Car-Dex", page_icon="🏎️")

# --- DATA STORAGE (Simulated) ---
if "my_cars" not in st.session_state:
    st.session_state.my_cars = []

st.title("🏎️ Car-Dex: Kanto Edition")
st.write("Upload a spot from your T1i or Phone to log it!")

# --- THE SCANNER ---
# This widget automatically opens the camera on mobile or the gallery on desktop
uploaded_file = st.file_uploader("Scan a Car", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the photo you just uploaded
    img = Image.open(uploaded_file)
    st.image(img, caption="New Discovery!", use_container_width=True)
    
    # Input fields for your "Catch"
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Car Name", placeholder="e.g. Ferrari SF90 XX")
    with col2:
        rarity = st.selectbox("Rarity", ["Common", "Rare", "Epic", "Legendary"])
    
    if st.button("Add to Car-Dex"):
        new_car = {
            "name": name,
            "rarity": rarity,
            "image": img,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.my_cars.append(new_car)
        st.success(f"{name} was added to your collection!")

# --- THE COLLECTION (THE POKEDEX) ---
st.divider()
st.header("📖 Your Collection")

if not st.session_state.my_cars:
    st.info("Your Dex is empty. Go hit up RSF Cars & Coffee!")
else:
    for car in reversed(st.session_state.my_cars):
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(car["image"], use_container_width=True)
            with c2:
                st.subheader(car["name"])
                st.caption(f"Rank: {car['rarity']} | Spotted: {car['time']}")
