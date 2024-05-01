import pandas as pd

def load_and_process_data(natural_disasters_path, co2_emissions_path):
  natural_disasters_data = pd.read_excel(natural_disasters_path)
  co2_emissions_data = pd.read_csv(co2_emissions_path)

    
  natural_disasters_filtered = natural_disasters_data[natural_disasters_data['Disaster Subgroup'] != 'Biological']
  natural_disasters_filtered = natural_disasters_filtered[natural_disasters_filtered['Disaster Type'] != 'Glacial lake outburst flood']
  natural_disasters_filtered = natural_disasters_filtered[natural_disasters_filtered['Disaster Type'] != 'Impact']

    
  natural_disasters_filtered = natural_disasters_filtered[natural_disasters_filtered['Start Year'].between(2000, 2023)]
  co2_emissions_filtered = co2_emissions_data[co2_emissions_data['Year'].between(2000, 2023)]

    
  common_codes = set(natural_disasters_filtered['Code']).intersection(set(co2_emissions_filtered['Code']))
  natural_disasters_final = natural_disasters_filtered[natural_disasters_filtered['Code'].isin(common_codes)]
  co2_emissions_final = co2_emissions_filtered[co2_emissions_filtered['Code'].isin(common_codes)]

    
  merged_data = pd.merge(natural_disasters_final, co2_emissions_final, left_on=['Code', 'Start Year'], right_on=['Code', 'Year'])

    
  final_df = merged_data[['Start Year', 'Entity', 'Disaster Type', 'Annual CO₂ emissions']]
  final_df.columns = ['year', 'country', 'natural disaster', 'co2 emissions']

  return final_df


weatherco2 = load_and_process_data('Natural Disasters 2000 - 2023.xlsx', 'annual-co2-emissions-per-country.csv')

weatherco2.head()

weatherco2.to_csv('weatherco2.csv', index=False)
