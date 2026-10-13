import joblib as jb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel

app = FastAPI(title="Agro-Predict API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = jb.load("models/xgb_model.pkl")


# NO 'Year' FIELD HERE ANYMORE
class FarmData(BaseModel):
  Crop: int
  State: int
  Area: float
  Annual: float
  Monsoon: float
  PrevYearYield: float
  Monsoon_ratio: float
  Rainperarea: float


@app.post("/predict")
def predict(data: FarmData):
  try:
    input_df = pd.DataFrame([{
        "State": int(data.State),
        "Crop": int(data.Crop),
        "Area": float(data.Area),
        "Annual": float(data.Annual),
        "Monsoon": float(data.Monsoon),
        "PrevYearYield": float(data.PrevYearYield),
        "Monsoon_ratio": float(data.Monsoon_ratio),
        "Rainperarea": float(data.Rainperarea),
    }])

    prediction = int(model.predict(input_df)[0])
    probabilities = model.predict_proba(input_df)[0].tolist()
    risk_status = "High" if prediction == 0 else "Low"

    return {
        "prediction": prediction,
        "risk_status": risk_status,
        "probabilities": probabilities,
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))