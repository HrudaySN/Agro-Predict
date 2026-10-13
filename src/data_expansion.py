import pandas as pd
import numpy as np


df=pd.read_csv("data/AgricultureRainfall_1998-2017.csv")

df['PrevYearYield']=df['PrevYearYield'].fillna(df.groupby(['State', 'Crop'])['PrevYearYield'].transform('mean'))
df['PrevYearYield']=df['PrevYearYield'].fillna(df['PrevYearYield'].median())

simulated_rows=[]

for year in range(2018,2027):
    for state in df['State'].unique():
        for crop in df['Crop'].unique():
            subset=df[(df['State']==state)&(df['Crop']==crop)]

            if len(subset)>0:
                mean_area=subset['Area'].mean()
                std_area=subset['Area'].std()
                
                mean_annual=subset['Annual'].mean()
                std_annual=subset['Annual'].std()
                
                mean_monsoon=subset['Monsoon'].mean()
                std_monsoon=subset['Monsoon'].std()
                
                mean_prev=subset['PrevYearYield'].mean()
                std_prev=subset['PrevYearYield'].std()
                
                            
                
                # Inside your loops, right after getting your means and stds:
                sim_area = max(100, np.random.normal(mean_area,std_area * 0.1))
                sim_annual = max(50, np.random.normal(mean_annual, std_annual * 0.15))
                sim_monsoon = max(20, np.random.normal(mean_monsoon, std_monsoon * 0.15))
                sim_yield = max(0, np.random.normal(mean_prev, std_prev * 0.1))
                sim_target=1 if (sim_monsoon/(sim_annual+1e-5))>0.4 else 0
                
                simulated_rows.append({
                                'Year': year,
                                'State': state,
                                'Crop': crop,
                                'Area': sim_area,
                                'Annual': sim_annual,
                                'Monsoon': sim_monsoon,
                                'PrevYearYield': sim_yield,
                                'Target': sim_target    
                            })
extended_df=pd.DataFrame(simulated_rows)
df=pd.concat([df, extended_df], ignore_index=True)
df.to_csv("data/AgricultureRainfall_1998-2026.csv", index=False)
print(df.shape)