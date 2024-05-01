
####CO2 vs. Temperature Pre-processing Script####

import pandas as pd

def load_data():
    co2_data = pd.read_csv('annual-co2-emissions-per-country.csv')
    temperature_data = pd.read_csv('GLB.Ts+dSST.csv', skiprows=1)
    temperature_annual = temperature_data[['Year', 'J-D']].rename(columns={'J-D': 'Annual Temperature Anomaly'}).dropna()

    global_co2 = co2_data.groupby('Year')['Annual CO₂ emissions'].sum().reset_index()

    merged_data = pd.merge(global_co2, temperature_annual, on='Year')
    
    return merged_data


co2temp = load_data()

co2temp.head()

co2temp.to_csv('co2temp.csv', index=False)
