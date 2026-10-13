import requests
import streamlit as st

st.set_page_config(
    page_title="Agro-Predict - Agricultural Risk Dashboard", page_icon="🌾"
)

st.title("🌾 Agro-Predict: Agricultural Risk Dashboard")
st.write(
    "Select your farm region, crop type, and current weather metrics below to"
    " assess agricultural success or risk."
)

# Mappings (keep your full state and crop mappings here)
STATE_MAPPING = {
    "punjab": 24,
    "rajasthan": 25,
    "tamil nadu": 27,
    "maharashtra": 17,
    "andhra pradesh": 1,
    "andaman and nicobar islands": 0,
}  # (Include your full dictionary)
CROP_MAPPING = {
    "Wheat": 50,
    "Rice": 37,
    "Bajra": 2,
    "Sugarcane": 43,
    "Maize": 23,
}  # (Include your full dictionary)

st.header("📍 Farm & Crop Selection")
selected_state = st.selectbox("Select State", list(STATE_MAPPING.keys()))
selected_crop = st.selectbox("Select Crop", list(CROP_MAPPING.keys()))

st.header("🌦️ Environmental & Weather Metrics")
col1, col2 = st.columns(2)

with col1:
  area = st.number_input(
      "Farmland Area (Hectares)", min_value=1.0, value=1200.0, step=10.0
  )
  annual_rainfall = st.number_input(
      "Annual Rainfall (mm)", min_value=0.0, value=850.0, step=10.0
  )

with col2:
  monsoon_rainfall = st.number_input(
      "Monsoon Rainfall (mm)", min_value=0.0, value=500.0, step=10.0
  )
  prev_year_yield = st.number_input(
      "Previous Year Yield", min_value=0.0, value=45.0, step=0.5
  )

# Auto-calculated physics indicators
monsoon_ratio = (
    monsoon_rainfall / annual_rainfall if annual_rainfall > 0 else 0.0
)
rain_per_area = annual_rainfall / area if area > 0 else 0.0

st.info(
    f"💡 **Calculated Indicators:** Monsoon Ratio = **{monsoon_ratio:.3f}** |"
    f" Rain Per Area = **{rain_per_area:.3f}**"
)

if st.button("🚀 Predict Agricultural Risk", type="primary"):
  payload = {
      "Crop": int(CROP_MAPPING[selected_crop]),
      "State": int(STATE_MAPPING[selected_state]),
      "Area": float(area),
      "Annual": float(annual_rainfall),
      "Monsoon": float(monsoon_rainfall),
      "PrevYearYield": float(prev_year_yield),
      "Monsoon_ratio": float(monsoon_ratio),
      "Rainperarea": float(rain_per_area),
  }

  try:
    response = requests.post("https://agro-predict-backend.onrender.com/predict", json=payload)
    if response.status_code == 200:
      result = response.json()
      status = result.get("risk_status")
      probs = result.get("probabilities", [])

      st.markdown("---")
      st.subheader("📊 Assessment Results")
      if status == "High":
        st.error(
            "⚠️ **Assessment: HIGH RISK**\n\nConditions indicate water stress or"
            f" unfavorable rainfall distribution (Confidence: {probs[0]*100:.1f}%)"
        )
      else:
        st.success(
            "✅ **Assessment: LOW RISK / SUCCESS**\n\nEnvironmental metrics look"
            f" favorable for successful yield (Confidence: {probs[1]*100:.1f}%)"
        )
    else:
      st.error(f"Error: {response.text}")
  except requests.exceptions.ConnectionError:
    st.error("Could not connect to the backend server.")