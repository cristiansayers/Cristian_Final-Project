
######CO2 vs GDP/Pop Pre-processing Script######

import pandas as pd

def load_and_preprocess_data():
    
    co2_data = pd.read_csv('annual-co2-emissions-per-country.csv')
    indicators_data = pd.read_csv('Popular Indicators Data.csv')

    indicators_data['Country Name'].replace({
        'Iran, Islamic Rep.': 'Iran',
        'Russian Federation': 'Russia',
        'Korea, Rep.': 'South Korea'
    }, inplace=True)

    
    indicators_2022 = indicators_data[['Country Name', 'Series Name', '2022 [YR2022]']]
    gdp_population_filter = indicators_2022['Series Name'].str.contains('GDP|Population, total', na=False)
    gdp_population_2022 = indicators_2022[gdp_population_filter]
    gdp_population_2022['2022 [YR2022]'] = pd.to_numeric(gdp_population_2022['2022 [YR2022]'].replace('..', pd.NA), errors='coerce')
    pivot_data_2022 = gdp_population_2022.pivot(index='Country Name', columns='Series Name', values='2022 [YR2022]')

    
    latest_year = co2_data['Year'].max()
    country_co2_data = co2_data[(co2_data['Code'].notna()) & (co2_data['Entity'] != 'World')]
    top_emitters = country_co2_data[country_co2_data['Year'] == latest_year].nlargest(10, 'Annual CO₂ emissions')

    
    final_data = top_emitters.merge(pivot_data_2022, left_on='Entity', right_index=True, how='left')
    return final_data


co2gdp = load_and_preprocess_data()

co2gdp.head()

co2gdp.to_csv('co2gdp.csv', index=False)
