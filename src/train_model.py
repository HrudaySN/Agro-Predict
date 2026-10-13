import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,accuracy_score


df=pd.read_csv("data/AgricultureRainfall_1998-2026.csv")


Y=df['Target']
X=df.drop('Target',axis=1)
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=42)


model=RandomForestClassifier(n_estimators=100,max_depth=10,max_features='sqrt',class_weight='balanced',random_state=42)
model.fit(x_train,y_train)
importances=model.feature_importances_
importance_df=pd.DataFrame({'Feature':X.columns,'Importance':importances})
importance_df=importance_df.sort_values(by='Importance',ascending=False)
print("Feature Importances:\n",importance_df)
y_pred=model.predict(x_test)

print("Classification Report:\n",classification_report(y_test,y_pred))
print("Accuracy Score:",accuracy_score(y_test,y_pred))