import pandas as pd

def preprocess_and_merge_datasets(co2_data_path, deforestation_data_path):

    co2_data = pd.read_csv(co2_data_path)

    deforestation_data = pd.read_excel(deforestation_data_path, sheet_name='Country tree cover loss')

    relevant_countries = congo_basin_countries + amazon_countries + southeast_asia_countries
    co2_data_filtered = co2_data[(co2_data['Year'] >= 2001) & (co2_data['Year'] <= 2023) & co2_data['Entity'].isin(relevant_countries)]

    deforestation_long = deforestation_data.melt(id_vars=['country', 'threshold', 'area_ha', 'extent_2000_ha', 'extent_2010_ha', 'gain_2000-2020_ha'],
                                                  value_vars=[f'tc_loss_ha_{year}' for year in range(2001, 2024)],
                                                  var_name='year', value_name='tree_cover_loss')
    deforestation_long['year'] = deforestation_long['year'].str.extract('(\d+)').astype(int)

    deforestation_agg = deforestation_long.groupby(['country', 'year']).agg({'tree_cover_loss': 'sum'}).reset_index()

    deforestation_agg['region'] = deforestation_agg['country'].map(country_to_region)

    final_dataset = pd.merge(deforestation_agg,
                             co2_data_filtered,
                             left_on=['country', 'year'],
                             right_on=['Entity', 'Year'],
                             how='inner')

    final_dataset = final_dataset[['year', 'country', 'region', 'tree_cover_loss', 'Annual CO₂ emissions']]
    final_dataset.columns = ['year', 'country', 'region', 'tree_cover_loss', 'co2_emissions']

    return final_dataset

congo_basin_countries = ['Cameroon', 'Central African Republic', 'Democratic Republic of the Congo', 'Republic of the Congo', 'Equatorial Guinea', 'Gabon']
amazon_countries = ['Brazil', 'Peru', 'Colombia', 'Venezuela', 'Ecuador', 'Bolivia', 'Guyana', 'Suriname', 'French Guiana']
southeast_asia_countries = ['Indonesia', 'Malaysia', 'Thailand', 'Philippines']

country_to_region = {country: 'Congo Basin' for country in congo_basin_countries}
country_to_region.update({country: 'Amazon' for country in amazon_countries})
country_to_region.update({country: 'Southeast Asia' for country in southeast_asia_countries})

criticalco2 = preprocess_and_merge_datasets('annual-co2-emissions-per-country.csv', 'global.xlsx')

criticalco2.head()

criticalco2.to_csv('deforestation-co2-dataset.csv', index=False)
