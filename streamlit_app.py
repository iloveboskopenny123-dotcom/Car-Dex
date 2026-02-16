import streamlit as st
from PIL import Image
import datetime

# --- CUSTOM CSS: THE DESIGN LAYER ---
st.set_page_config(page_title="Car-Dex Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
        color: #ffffff;
    }
    
    /* Custom Card Styling */
    .car-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #ff1f1f; /* Red Racing Stripe */
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .car-card:hover {
        transform: scale(1.02);
        border-color: #ff1f1f;
    }
    
    /* Metric & Header Styling */
    h1, h2, h3 {
        font-family: 'Share Tech Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #ff1f1f;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
if "my_cars" not in st.session_state:
    st.session_state.my_cars = []

st.title("🏎️ CAR-DEX // TERMINAL")
st.write(f"Logged in as: **SuperNURD_01** | {datetime.datetime.now().strftime('%Y-%m-%d')}")

# Scanner Section
with st.sidebar:
    st.header("📡 TARGET SCANNER")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])
    if uploaded_file:
        name = st.text_input("Model ID")
        rarity = st.select_slider("Class", options=["Common", "Rare", "Legendary"])
        if st.button("SYNC TO DATABASE"):
            img = Image.open(uploaded_file)
            st.session_state.my_cars.append({"name": name, "rarity": rarity, "img": img})
            st.toast("Data Encrypted and Saved!")

# Display Collection
st.subheader("📋 RECENT CATCHES")
if not st.session_state.my_cars:
    st.info("No active targets detected. Scanning required.")
else:
    for car in reversed(st.session_state.my_cars):
        st.markdown(f"""
            <div class="car-card">
                <div style="display: flex; gap: 20px; align-items: center;">
                    <div style="flex: 1;">
                        <h3 style="margin:0;">{car['name']}</h3>
                        <p style="color: #888;">CLASS: {car['rarity'].upper()}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # We place the actual image below the HTML card since Streamlit can't easily put st.image inside raw HTML
        st.image(car["img"], width=300)
import streamlit as st
from PIL import Image
import datetime

# 1. --- PRO DESIGN LAYER (The Chassis) ---
st.set_page_config(page_title="Car-Dex Terminal", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%); color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111; border-right: 2px solid #ff1f1f; }
    .car-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-left: 5px solid #ff1f1f;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #ff1f1f; font-family: 'Courier New', monospace; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 2. --- DATA INITIALIZATION ---
if "my_cars" not in st.session_state:
    st.session_state.my_cars = []

# Our Brand/Model Dictionary
car_data = {
    "Ferrari": ["SF90 XX Stradale", "SF90 Stradale", "296 GTB", "458 Italia", "F40"],
    "Lamborghini": ["Revuelto", "Huracán STO", "Aventador SVJ", "Urus"],
    "Porsche": ["911 GT3 RS", "718 Cayman GT4 RS", "918 Spyder"],
    "Other": []
}

# 3. --- THE SCANNER SIDEBAR (The Intake) ---
with st.sidebar:
    st.header("📡 SCANNER")
    uploaded_file = st.file_uploader("Upload Shot", type=["jpg", "png"])
    
    # --- DEPENDENT DROPDOWNS START HERE ---
    brand = st.selectbox("Select Brand", options=list(car_data.keys()))
    
    # Check if 'Other' is picked for manual entry
    if brand == "Other":
        model = st.text_input("Enter Model Name")
    else:
        model = st.selectbox("Select Model", options=car_data[brand])
    
    rarity = st.select_slider("Tier", options=["Common", "Rare", "Legendary"])
    
    if st.button("SYNC TO DEX"):
        if uploaded_file and model:
            img = Image.open(uploaded_file)
            new_entry = {
                "name": f"{brand} {model}" if brand != "Other" else model,
                "rarity": rarity,
                "img": img,
                "time": datetime.datetime.now().strftime("%H:%M")
            }
            st.session_state.my_cars.append(new_entry)
            st.toast("Target Locked!")
        else:
            st.error("Upload a photo first!")

# 4. --- THE MAIN DISPLAY (The Gallery) ---
st.title("🏎️ CAR-DEX // DATABASE")

if not st.session_state.my_cars:
    st.info("No active targets in range. Open the scanner to log a spot.")
else:
    for car in reversed(st.session_state.my_cars):
        st.markdown(f"""
            <div class="car-card">
                <h3>{car['name']}</h3>
                <p>CLASS: {car['rarity'].upper()} | LOG TIME: {car['time']}</p>
            </div>
        """, unsafe_allow_html=True)
        st.image(car["img"], width=400)
