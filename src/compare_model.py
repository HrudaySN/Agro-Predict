import joblib
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/AgricultureRainfall_1998-2026.csv")

# Drop Year entirely so it never biases predictions
if "Year" in df.columns:
  df = df.drop("Year", axis=1)

Y = df["Target"]
X = df.drop("Target", axis=1)

x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, stratify=Y, random_state=42
)

model = xgb.XGBClassifier(
    n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42
)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Accuracy Score:", accuracy_score(y_test, y_pred))

# Save the updated model
joblib.dump(model, "models/xgb_model.pkl")