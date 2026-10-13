import joblib as jb
from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel

app = FastAPI(title="AgroPredict")

# Load model
model_path = "models/xgb_model.pkl"
try:
  model = jb.load(model_path)
except Exception as e:
  print(f"Error loading model: {e}")


class FarmData(BaseModel):
  Year: int
  Crop: int
  State: int
  Area: float
  Annual: float
  Monsoon: float
  PrevYearYield: float
  Monsoon_ratio: float
  Rainperarea: float


@app.get("/")
def home():
  return {"message": "Welcome to AgroPredict API"}


@app.post("/predict")
def predict(data: FarmData):
  try:
    # 1. Convert incoming Pydantic data into a dictionary
    input_data = data.dict()

    # 2. Create DataFrame with explicit column order matching training features
    feature_order = [
        "State",
        "Crop",
        "Year",
        "Area",
        "Annual",
        "Monsoon",
        "PrevYearYield",
        "Monsoon_ratio",
        "Rainperarea",
    ]
    input_df = pd.DataFrame([input_data])[feature_order]

    # 3. Run prediction
    prediction = model.predict(input_df)[0]

    # 4. Format result
    result = "High" if int(prediction) == 1 else "Low"

    return {"prediction": int(prediction), "risk_status": result}

  except Exception as e:
    # This will catch the exact error and display it clearly instead of a blank 500
    raise HTTPException(status_code=500, detail=str(e))