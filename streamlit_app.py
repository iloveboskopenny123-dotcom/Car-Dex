import streamlit as st
from PIL import Image
import datetime

# 1. --- CONFIG & STYLE ---
st.set_page_config(page_title="Hyper-Dex Terminal", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); color: white; }
    [data-testid="stSidebar"] { background-color: #111; border-right: 2px solid #444; }
    .car-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px;
        padding: 20px; margin-bottom: 20px;
    }
    h1, h2, h3 { font-family: 'Courier New', monospace; text-transform: uppercase; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. --- DATA SETUP ---
if "my_cars" not in st.session_state:
    st.session_state.my_cars = []

car_data = {
    "Koenigsegg": ["Jesko", "Jesko Absolut", "Gemera", "Regera", "Agera RS", "One:1", "CCX"],
    "Pagani": ["Utopia", "Huayra R", "Huayra BC", "Huayra Roadster", "Zonda Cinque", "Zonda R"],
    "Bugatti": ["Tourbillon", "Chiron Super Sport", "Chiron Pur Sport", "Divo", "Veyron", "Bolide"],
    "Ferrari": ["SF90 XX", "LaFerrari", "Daytona SP3", "Monza SP1/SP2", "Enzo", "F40", "F50", "288 GTO", "812 Comp"],
    "Lamborghini": ["Revuelto", "Countach LPI 800-4", "Sian", "Centenario", "Veneno", "Aventador SVJ", "Huracán STO"],
    "McLaren": ["P1", "Senna", "Senna GTR", "Speedtail", "Elva", "765LT", "Solus GT", "F1"],
    "Porsche": ["918 Spyder", "Carrera GT", "911 GT3 RS (992)", "911 S/T", "959", "Dakar"],
    "Hyper-Luxury": ["Rolls-Royce Spectre", "Rolls-Royce Cullinan", "Bentley Bacalar", "Aston Martin Valkyrie", "Aston Martin Valour"],
    "Aviation (Copters)": ["Eurocopter AS350", "Bell 407", "Robinson R44", "AgustaWestland AW109", "Sikorsky S-76"],
    "JDM Legends": ["Lexus LFA", "Nissan GT-R Nismo", "Honda NSX-R (NA2)", "Toyota 2000GT"],
    "Other": [] 
}

# 3. --- SCANNER SIDEBAR ---
with st.sidebar:
    st.header("📡 HYPER SCANNER")
    uploaded_file = st.file_uploader("Upload Shot", type=["jpg", "png", "jpeg"])
    
    # Brand Selection
    brand = st.selectbox("Select Manufacturer", options=list(car_data.keys()))
    
    # --- DYNAMIC MODEL LOGIC ---
    if brand == "Other":
        model = st.text_input("Enter Manual Brand & Model")
    else:
        # We add "Other / Custom" to the end of every brand's list
        model_options = car_data[brand] + ["Other / Custom"]
        model_choice = st.selectbox("Select Model", options=model_options, key=f"select_{brand}")
        
        # If they pick "Other / Custom", show a text box
        if model_choice == "Other / Custom":
            model = st.text_input(f"Enter custom {brand} model name")
        else:
            model = model_choice
            
    rarity = st.select_slider("Rarity Tier", options=["Common", "Uncommon", "Rare", "Legendary", "Unicorn"])
    
    if st.button("LOG SIGHTING"):
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
            st.error("⚠️ Upload a photo and enter a model name!")

# 4. --- MAIN DISPLAY ---
st.title("🏎️ RSF CAR-DEX")

if not st.session_state.my_cars:
    st.info("System Empty. No targets detected.")
else:
    for car in reversed(st.session_state.my_cars):
        color_map = {
            "Common": "#A9A9A9", "Uncommon": "#32CD32", "Rare": "#9370DB", 
            "Legendary": "#FFD700", "Unicorn": "#00FFFF"
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
