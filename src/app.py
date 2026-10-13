from fastapi import FastAPI
import joblib as jb
from pydantic import BaseModel
import pandas as pd

app=FastAPI(title='AgroPredict')

model_path="models/xgb_model.pkl"
model=jb.load(model_path)

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


@app.get('/')
def home():
    return {'message':'Welcome to AgroPredict API'}

@app.post('/predict')
def predict(data:FarmData):
    input_df=pd.DataFrame([data.dict()])
    prediction=model.predict(input_df)
    result='High' if prediction==1 else 'Low'
    return {'prediction':int(prediction),'risk_status':result}
