import joblib as jb
from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel

app = FastAPI(title="AgroPredict")

# Load model
try:
  model = jb.load("models/xgb_model.pkl")
  print("Model loaded successfully!")
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
  return {"message": "AgroPredict API is live"}


@app.post("/predict")
def predict(data: FarmData):
  try:
    # Print incoming payload to your terminal for debugging
    print("Incoming Data:", data.dict())

    # Build DataFrame matching exact training feature order
    input_df = pd.DataFrame([{
        "State": data.State,
        "Crop": data.Crop,
        "Year": data.Year,
        "Area": data.Area,
        "Annual": data.Annual,
        "Monsoon": data.Monsoon,
        "PrevYearYield": data.PrevYearYield,
        "Monsoon_ratio": data.Monsoon_ratio,
        "Rainperarea": data.Rainperarea,
    }])

    print("DataFrame sent to model:\n", input_df)

    # Get prediction and probabilities
    prediction = int(model.predict(input_df)[0])

    # If the model supports predict_proba, print confidence
    if hasattr(model, "predict_proba"):
      proba = model.predict_proba(input_df)[0].tolist()
      print(f"Prediction: {prediction}, Probabilities: {proba}")
    else:
      proba = []

    result_status = "High" if prediction == 1 else "Low"

    return {
        "prediction": prediction,
        "risk_status": result_status,
        "probabilities": proba,
    }

  except Exception as e:
    print(f"Prediction Error: {e}")
    raise HTTPException(status_code=500, detail=str(e))