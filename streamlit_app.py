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

car_data = {
    "Ferrari": ["SF90 XX Stradale", "SF90 Stradale", "296 GTB", "812 Competizione", "458 Italia", "LaFerrari", "F40", "Enzo"],
    "Lamborghini": ["Revuelto", "Temerario", "Huracán STO", "Aventador SVJ", "Urus", "Murciélago", "Gallardo"],
    "Porsche": ["911 GT3 RS", "911 Turbo S", "718 Cayman GT4 RS", "Taycan", "918 Spyder", "Carrera GT", "Macan"],
    "McLaren": ["750S", "720S", "P1", "Senna", "Artura", "570S", "600LT"],
    "BMW": ["M3 Competition", "M4 CSL", "M5 CS", "i8", "Z4", "X5 M", "8 Series"],
    "Mercedes-Benz": ["AMG GT Black Series", "G-Wagon", "SLS AMG", "C63 AMG", "S-Class"],
    "Audi": ["R8 V10", "RS6 Avant", "RS7", "e-tron GT", "TT RS"],
    "Tesla": ["Model S Plaid", "Model X", "Model 3", "Model Y", "Cybertruck", "Roadster"],
    "Toyota": ["Supra MK5", "GR Corolla", "Camry", "RAV4", "Tacoma", "86"],
    "Nissan": ["GT-R R35", "Z (RZ34)", "370Z", "Altima", "Skyline GT-R"],
    "Ford": ["GT", "Mustang Shelby GT500", "F-150 Raptor", "Focus RS"],
    "Chevrolet": ["Corvette Z06", "Corvette E-Ray", "Camaro ZL1", "Silverado"],
    "Aviation": ["F-22 Raptor", "F-35 Lightning II", "Blue Angel #1", "C-130 Fat Albert"],
    "Other": []
}
