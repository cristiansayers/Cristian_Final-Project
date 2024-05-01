
#####Projected FUTURE CO2 vs. Temp Preproc.#######

import pandas as pd

def preprocess_and_sort_data(co2_path, temp_path):

  co2_df = pd.read_excel(co2_path)
  temp_df = pd.read_excel(temp_path)
  co2_long = co2_df.melt(id_vars=['Scenario'], value_vars=co2_df.columns[4:],
                           var_name='Year', value_name='CO2 Emissions')

    
  temp_long = temp_df.melt(id_vars=['Scenario'], value_vars=temp_df.columns[4:],
                             var_name='Year', value_name='Temperature Change')

    
  combined_df = pd.merge(co2_long, temp_long, on=['Scenario', 'Year'])

    
  combined_df['Year'] = combined_df['Year'].astype(int)

    
  sorted_df = combined_df.sort_values(by=['Scenario', 'Year'])

  return sorted_df

projected_impacts = preprocess_and_sort_data('world co2 projections.xlsx', 'world temp projection.xlsx')

projected_impacts.head()

projected_impacts.to_csv('projected_impacts.csv', index=False)
