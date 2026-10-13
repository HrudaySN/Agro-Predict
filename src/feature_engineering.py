import pandas as pd

df=pd.read_csv("data/AgricultureRainfall_1998-2026.csv")
# print(df.shape)
# print(df.head())
# print(df.info())
# print(df.describe())

df['Monsoon_ratio']=df['Monsoon']/(df['Annual']+1e-5)
df['Rainperarea']=df['Annual']/(df['Area']+1e-5)

output=df['Target']
df=df.drop('Target',axis=1)
df['Target']=output

df.to_csv("data/AgricultureRainfall_1998-2026.csv", index=False)