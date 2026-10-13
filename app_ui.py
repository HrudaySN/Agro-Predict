import requests
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgroPredict - Agricultural Risk Dashboard",
    page_icon="🌾",
    layout="centered",
)

st.title("🌾 AgroPredict: Agricultural Risk Dashboard")
st.write(
    "Welcome! Select your farm region, crop type, and weather parameters below"
    " to predict agricultural success or risk."
)

# --- DATASET-EXACT MAPPINGS FOR DROPDOWNS ---
STATE_MAPPING = {
    "andaman and nicobar islands": 0,
    "andhra pradesh": 1,
    "arunachal pradesh": 2,
    "assam": 3,
    "bihar": 4,
    "chandigarh": 5,
    "chhattisgarh": 6,
    "delhi": 7,
    "goa": 8,
    "gujarat": 9,
    "haryana": 10,
    "himachal pradesh": 11,
    "jammu and kashmir": 12,
    "jharkhand": 13,
    "karnataka": 14,
    "kerala": 15,
    "madhya pradesh": 16,
    "maharashtra": 17,
    "manipur": 18,
    "meghalaya": 19,
    "mizoram": 20,
    "nagaland": 21,
    "odisha": 22,
    "puducherry": 23,
    "punjab": 24,
    "rajasthan": 25,
    "sikkim": 26,
    "tamil nadu": 27,
    "telangana": 28,
    "tripura": 29,
    "uttar pradesh": 30,
    "uttarakhand": 31,
    "west bengal": 32,
}

CROP_MAPPING = {
    "Arecanut": 0,
    "Arhar/Tur": 1,
    "Bajra": 2,
    "Banana": 3,
    "Barley": 4,
    "Black pepper": 5,
    "Cardamom": 6,
    "Cashewnut": 7,
    "Castor seed": 8,
    "Coriander": 9,
    "Cotton(lint)": 10,
    "Cowpea(Lobia)": 11,
    "Dry chillies": 12,
    "Garlic": 13,
    "Ginger": 14,
    "Gram": 15,
    "Groundnut": 16,
    "Guar seed": 17,
    "Horse-gram": 18,
    "Jowar": 19,
    "Jute": 20,
    "Khesari": 21,
    "Linseed": 22,
    "Maize": 23,
    "Masoor": 24,
    "Mesta": 25,
    "Moong(Green Gram)": 26,
    "Moth": 27,
    "Niger seed": 28,
    "Onion": 29,
    "Other Cereals & Millets": 30,
    "Other Kharif pulses": 31,
    "Other Rabi pulses": 32,
    "Peas & beans (Pulses)": 33,
    "Potato": 34,
    "Ragi": 35,
    "Rapeseed &Mustard": 36,
    "Rice": 37,
    "Safflower": 38,
    "Sannhamp": 39,
    "Sesamum": 40,
    "Small millets": 41,
    "Soyabean": 42,
    "Sugarcane": 43,
    "Sunflower": 44,
    "Sweet potato": 45,
    "Tapioca": 46,
    "Tobacco": 47,
    "Turmeric": 48,
    "Urad": 49,
    "Wheat": 50,
}

# --- UI INPUT FORM ---
st.header("📍 Farm & Crop Selection")
selected_state = st.selectbox("Select State", list(STATE_MAPPING.keys()))
selected_crop = st.selectbox("Select Crop", list(CROP_MAPPING.keys()))

st.header("🌦️ Environmental & Agricultural Parameters")
col1, col2 = st.columns(2)

with col1:
  year = st.number_input("Year", min_value=1998, max_value=2030, value=2026)
  area = st.number_input(
      "Farmland Area (Hectares)", min_value=1.0, value=1500.0, step=10.0
  )
  annual_rainfall = st.number_input(
      "Annual Rainfall (mm)", min_value=0.0, value=950.0, step=10.0
  )

with col2:
  monsoon_rainfall = st.number_input(
      "Monsoon Rainfall (mm)", min_value=0.0, value=550.0, step=10.0
  )
  prev_year_yield = st.number_input(
      "Previous Year Yield", min_value=0.0, value=52.4, step=0.1
  )

# --- AUTOMATIC PHYSICS-INFORMED FEATURE CALCULATION ---
monsoon_ratio = (
    monsoon_rainfall / annual_rainfall if annual_rainfall > 0 else 0.0
)
rain_per_area = annual_rainfall / area if area > 0 else 0.0

st.info(
    "💡 **Auto-calculated Engineering Features:** `Monsoon Ratio` ="
    f" **{monsoon_ratio:.3f}** | `Rain Per Area` = **{rain_per_area:.3f}**"
)

# --- PREDICTION ACTION ---
if st.button("🚀 Predict Agricultural Risk", type="primary"):
  # Map selected names to dataset-exact integer codes
  state_code = STATE_MAPPING[selected_state]
  crop_code = CROP_MAPPING[selected_crop]

  # Construct JSON payload matching FastAPI Pydantic schema
  payload = {
      "Year": int(year),
      "Crop": int(crop_code),
      "State": int(state_code),
      "Area": float(area),
      "Annual": float(annual_rainfall),
      "Monsoon": float(monsoon_rainfall),
      "PrevYearYield": float(prev_year_yield),
      "Monsoon_ratio": float(monsoon_ratio),
      "Rainperarea": float(rain_per_area),
  }

  try:
    # Send POST request to FastAPI backend
   
# To your live Render backend URL:
    response = requests.post(
    "https://agro-predict-backend.onrender.com/predict", json=payload
    )

    if response.status_code == 200:
      result = response.json()
      status = result.get("risk_status")
      code = result.get("prediction")

      st.markdown("---")
      st.subheader("📊 Prediction Results")

      if status == "High":
        st.error(
            "⚠️ **Assessment: HIGH RISK** (Model Code: "
            f"{code})\n\nConditions indicate potential drought or crop stress"
            " factors."
        )
      else:
        st.success(
            "✅ **Assessment: LOW RISK / SUCCESS** (Model Code: "
            f"{code})\n\nConditions look favorable for successful yield."
        )
    else:
      st.error(f"Backend Error: {response.text}")

  except requests.exceptions.ConnectionError:
    st.error(
        "❌ **Connection Failed:** Could not reach the FastAPI backend."
        " Make sure your Uvicorn server is running in your terminal (`uvicorn"
        " src.app:app --reload`)."
    )