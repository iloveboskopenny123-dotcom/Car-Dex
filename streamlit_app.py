import streamlit as st
from PIL import Image
import datetime

# --- POKEDEX STYLING ---
st.set_page_config(page_title="Car-Dex", page_icon="🏎️", layout="centered")

# Custom CSS to make it look like a Pokedex
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff1f1f; color: white; font-weight: bold; }
    .stHeader { color: #ff1f1f; font-family: 'Courier New', Courier, monospace; }
    div[data-testid="stMetricValue"] { color: #ff1f1f; }
    .car-card { border: 2px solid #ff1f1f; border-radius: 15px; padding: 15px; background-color: white; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

if "my_cars" not in st.session_state:
    st.session_state.my_cars = []

st.title("🔴 CAR-DEX v1.0")
st.write("---")

# --- SCANNER SECTION ---
with st.expander("📸 OPEN SCANNER", expanded=True):
    uploaded_file = st.file_uploader("Upload T1i or Ray-Ban Shot", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Identify Car", placeholder="e.g. SF90 XX")
            power = st.number_input("Horsepower", min_value=0, value=0)
        with c2:
            rarity = st.selectbox("Tier", ["Common", "Uncommon", "Rare", "Legendary"])
            location = st.text_input("Location", value="Rancho Santa Fe")

        if st.button("LOG TO CAR-DEX"):
            new_car = {
                "name": name, "rarity": rarity, "image": img, "power": power,
                "loc": location, "time": datetime.datetime.now().strftime("%b %d, %H:%M")
            }
            st.session_state.my_cars.append(new_car)
            st.balloons() # This adds a celebratory "Caught it!" animation

# --- COLLECTION SECTION ---
st.header("📖 YOUR DISCOVERIES")

if not st.session_state.my_cars:
    st.info("No cars in the database yet. Head to Miramar or RSF!")
else:
    # Stats Summary
    total_hp = sum(car['power'] for car in st.session_state.my_cars)
    st.metric("Total Collection Power", f"{total_hp} HP")

    for car in reversed(st.session_state.my_cars):
        # Professional looking card for each car
        with st.container():
            st.markdown(f"""<div class='car-card'>""", unsafe_allow_html=True)
            col_img, col_info = st.columns([1, 1.5])
            with col_img:
                st.image(car["image"], use_container_width=True)
            with col_info:
                st.subheader(car["name"])
                st.write(f"**Rank:** {car['rarity']} | **Power:** {car['power']} HP")
                st.caption(f"📍 {car['loc']} | 📅 {car['time']}")
            st.markdown("</div>", unsafe_allow_html=True)
