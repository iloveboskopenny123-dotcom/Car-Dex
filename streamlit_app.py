import streamlit as st
from PIL import Image
import datetime

# 1. --- PRO DESIGN LAYER (The "Skin") ---
st.set_page_config(page_title="Car-Dex Terminal", page_icon="🏎️", layout="wide")

# This CSS makes the app look like a high-tech scanner
st.markdown("""
    <style>
    /* Dark Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111;
        border-right: 2px solid #ff1f1f;
    }
    /* Card Styling */
    .car-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #ff1f1f;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    /* Text Styling */
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        color: #ff1f1f;
        text-shadow: 0 0 10px rgba(255, 31, 31, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. --- DATA STORAGE & LISTS ---
if "my_cars" not in st.session_state:
    st.session_state.my_cars = []

# The "Mega-Dex" Database
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
    "Other": [] # Select this to type in a custom name
}

# 3. --- THE SCANNER SIDEBAR (The Inputs) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=50)
    st.header("📡 TARGET SCANNER")
    st.write("---")
    
    # Image Upload
    uploaded_file = st.file_uploader("Upload Shot", type=["jpg", "png", "jpeg"])
    
    # --- DEPENDENT DROPDOWNS LOGIC ---
    # Step A: Choose Brand
    brand = st.selectbox("Select Brand", options=list(car_data.keys()))
    
    # Step B: Choose Model (Updates based on Step A)
    if brand == "Other":
        model = st.text_input("Enter Manual Model Name")
    else:
        # If the brand has models, show them. Otherwise, let user type.
        if car_data[brand]:
            model = st.selectbox("Select Model", options=car_data[brand])
        else:
            model = st.text_input("Enter Model Name")
            
    # Step C: Rarity & Location
    rarity = st.select_slider("Class Tier", options=["Common", "Rare", "Epic", "Legendary"])
    
    # Submit Button
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

# 4. --- THE MAIN DISPLAY (The Gallery) ---
st.title("🏎️ CAR-DEX // DATABASE")
st.write(f"**STATUS:** SYSTEM ONLINE | **USER:** SUPERNURD_01")

if not st.session_state.my_cars:
    st.info("System Empty. No targets detected. Use the sidebar to scan.")
else:
    # Calculate Total Catches
    total = len(st.session_state.my_cars)
    st.markdown(f"### TOTAL DISCOVERIES: {total}")
    
    # Loop through cars (Newest first)
    for car in reversed(st.session_state.my_cars):
        # Color coding the rarity text
        color_map = {"Common": "#aaa", "Rare": "#4facfe", "Epic": "#d4fc79", "Legendary": "#ff1f1f"}
        rarity_color = color_map.get(car['rarity'], "white")
        
        # HTML Card Design
        st.markdown(f"""
            <div class="car-card">
                <h3 style="margin-bottom: 5px;">{car['name']}</h3>
                <p style="font-family: monospace; font-size: 14px; margin: 0;">
                    CLASS: <span style="color: {rarity_color}; font-weight: bold;">{car['rarity'].upper()}</span> 
                    | LOG: {car['time']}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display Image
        st.image(car["img"], use_container_width=True)
