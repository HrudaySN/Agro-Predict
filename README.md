# 🌾 Agro-Predict: Agricultural Risk & Yield Prediction System

An end-to-end machine learning and production web application designed to predict agricultural risk (Success vs. High Risk) based on multi-decadal historical and simulated data (1998–2026).

---

## 🚀 Project Architecture & Directory Structure
```text
Agro-Predict/
│
├── data/
│   └── AgricultureRainfall_1998-2026.csv   # Cleaned and feature-engineered dataset
│
├── models/
│   └── xgb_model.pkl                       # Serialized production XGBoost classifier
│
├── notebooks/                              # Exploratory data analysis notebooks
│
├── src/
│   ├── data_expansion.py                   # Timeline simulation and data extension
│   ├── feature_engineering.py              # Imputation, label encoding, and ratio creation
│   ├── train_model.py                      # Baseline Random Forest with class weighting
│   ├── compare_model.py                    # XGBoost benchmarking & joblib serialization
│   └── app.py                              # FastAPI backend RESTful web service
│
├── app_ui.py                               # Interactive Streamlit Frontend Dashboard
├── .gitignore                              # Git exclusion rules
└── README.md