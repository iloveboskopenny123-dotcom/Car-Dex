    # Cimport streamlit as st
from PIL import Image
import datetime

# 1. --- PRO DESIGN LAYER ---
st.set_page_config(page_title="Car-Dex Terminal", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* Dark Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #111;
        border-right: 2px solid #444;
    }
    /* Base Card Styling */
    .car-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    .car-card:hover {
        transform: scale(1.02);
    }
    /* Text Styling */
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. --- DATA STORAGE & LISTS ---
if "my_cars" not in st.session_state:
    st.session_state.my_cars = []

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

# 3. --- THE SCANNER SIDEBAR ---
with st.sidebar:
    st.header("📡 TARGET SCANNER")
    uploaded_file = st.file_uploader("Upload Shot", type=["jpg", "png", "jpeg"])
    
    brand = st.selectbox("Select Brand", options=list(car_data.keys()))
    
    if brand == "Other":
        model = st.text_input("Enter Manual Model Name")
    else:
        model = st.selectbox("Select Model", options=car_data[brand])
            
    # UPDATED: The new color tier list
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
            st.toast("Target Successfully Logged!", icon="✅")
        else:
            st.error("⚠️ Error: Upload a photo first!")

# 4. --- THE MAIN DISPLAY ---
st.title("🏎️ CAR-DEX // DATABASE")

if not st.session_state.my_cars:
    st.info("System Empty. No targets detected.")
else:
    for car in reversed(st.session_state.my_cars):
        
        # --- COLOR LOGIC ---
        # This dictionary maps your Rarity text to actual Hex Colors
        color_map = {
            "Common": "#A9A9A9",    # Grey
            "Uncommon": "#32CD32",  # Green
            "Rare": "#9370DB",      # Purple
            "Legendary": "#FFD700"  # Gold
        }
        
        # Get the color for this specific car
        this_color = color_map.get(car['rarity'], "white")
        
        # We inject the color into the border-left and the text span
        st.markdown(f"""
            <div class="car-card" style="border-left: 5px solid {this_color};">
                <h3 style="margin-bottom: 5px;">{car['name']}</h3>
                <p style="font-family: monospace; font-size: 14px; margin: 0;">
                    TIER: <span style="color: {this_color}; font-weight: bold; font-size: 16px;">{car['rarity'].upper()}</span> 
                    | LOG: {car['time']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.image(car["img"], use_container_width=True)

