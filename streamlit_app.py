import streamlit as st
from PIL import Image
import datetime

# 1. --- CONFIG & STYLE (Must be at the top) ---
st.set_page_config(page_title="Car-Dex Terminal", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    [data-testid="stSidebar"] {
        background-color: #111;
        border-right: 2px solid #444;
    }
    .car-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. --- DATA SETUP ---
if "my_cars" not in st.session_state:
    st.session_state.my_cars = []

# The Database
car_data = {
    "Ferrari": ["SF90 XX Stradale", "SF90 Stradale", "296 GTB", "812 Competizione", "458 Italia", "LaFerrari", "F40", "Enzo"],
    "Lamborghini": ["Revuelto", "Temerario", "Huracán STO", "Aventador SVJ", "Urus", "Murciélago", "Gallardo"],
    "Porsche": ["911 GT3 RS", "911 Turbo S", "718 Cayman GT4 RS", "Taycan", "918 Spyder", "Carrera GT", "Macan"],
    "McLaren": ["750S", "720S", "P1", "Senna", "Artura", "570S", "600LT"],
    "BMW": ["M3 Competition", "M4 CSL", "M5 CS", "i8", "Z4", "X5 M"],
    "Mercedes-Benz": ["AMG GT Black Series", "G-Wagon", "SLS AMG", "C63 AMG"],
    "Audi": ["R8 V10", "RS6 Avant", "RS7", "e-tron GT"],
    "Tesla": ["Model S Plaid", "Cybertruck", "Model 3", "Roadster"],
    "Toyota": ["Supra MK5", "GR Corolla", "Camry", "Tacoma", "86"],
    "Ford": ["GT", "Mustang Shelby GT500", "F-150 Raptor", "Focus RS"],
    "Chevrolet": ["Corvette Z06", "Corvette E-Ray", "Camaro ZL1"],
    "Nissan": ["GT-R R35", "Z (RZ34)", "Skyline GT-R"],
    "Aviation": ["F-22 Raptor", "F-35 Lightning II", "Blue Angel #1", "C-130 Fat Albert"],
    "Other": [] 
}

# 3. --- SCANNER SIDEBAR ---
with st.sidebar:
    st.header("📡 TARGET SCANNER")
    uploaded_file = st.file_uploader("Upload Shot", type=["jpg", "png", "jpeg"])
    
    # THE FIX: We add a 'key' to the selectbox so it resets when brand changes
    brand = st.selectbox("Select Brand", options=list(car_data.keys()))
    
    # Logic for Model Selection
    if brand == "Other":
        model = st.text_input("Enter Manual Model Name")
    elif not car_data[brand]:
        # Fallback if a brand has an empty list in the code
        model = st.text_input("Enter Model Name", key=f"input_{brand}")
    else:
        # THE FIX: key=f"select_{brand}" forces a fresh dropdown for every brand
        model = st.selectbox("Select Model", options=car_data[brand], key=f"select_{brand}")
            
    rarity = st.select_slider("Class Tier", options=["Common", "Uncommon", "Rare", "Legendary"])
    
    if st.button("LOG TARGET TO DEX"):
        if uploaded_file and model:
            img = Image.open(uploaded_file)
            new_entry = {
                "name": f"{brand} {model}" if brand != "Other" else model,
                "rarity": rarity,
                "img": img,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.my_cars.append(new_entry)
            st.toast("Target Logged!", icon="✅")
        else:
            st.error("⚠️ Upload a photo and pick a model!")

# 4. --- MAIN DISPLAY ---
st.title("🏎️ CAR-DEX // DATABASE")

if not st.session_state.my_cars:
    st.info("System Empty. No targets detected.")
else:
    for car in reversed(st.session_state.my_cars):
        
        # Color Logic
        color_map = {
            "Common": "#A9A9A9",    # Grey
            "Uncommon": "#32CD32",  # Green
            "Rare": "#9370DB",      # Purple
            "Legendary": "#FFD700"  # Gold
        }
        this_color = color_map.get(car['rarity'], "white")
        
        st.markdown(f"""
            <div class="car-card" style="border-left: 5px solid {this_color};">
                <h3 style="margin-bottom: 5px; color: white;">{car['name']}</h3>
                <p style="font-family: monospace; font-size: 14px; margin: 0; color: #ccc;">
                    TIER: <span style="color: {this_color}; font-weight: bold; font-size: 16px;">{car['rarity'].upper()}</span> 
                    | LOG: {car['time']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.image(car["img"], use_container_width=True)
