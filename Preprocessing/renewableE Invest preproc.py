import pandas as pd

def load_data():
    global_renewables = pd.read_csv('Global renewables energy share.csv')
    global_renewables['Year'] = global_renewables['Year'].astype(int)
    emissions = pd.read_csv('annual-co2-emissions-per-country.csv')
    emissions['Year'] = emissions['Year'].astype(int)
    non_countries = [
        'World', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania',
        'European Union (27)', 'European Union (28)', 'High-income countries', 'Low-income countries',
        'Lower-middle-income countries', 'Upper-middle-income countries', 'International aviation', 'International shipping',
        'Asia (GCP)', 'Europe (GCP)', 'North America (GCP)', 'South America (GCP)', 'Oceania (GCP)', 'Middle East (GCP)',
        'Central America (GCP)', 'Non-OECD (GCP)', 'OECD (GCP)', 'Africa (GCP)', 'Asia (excl. China and India)',
        'Europe (excl. EU-27)', 'Europe (excl. EU-28)', 'North America (excl. USA)'
    ]
    emissions = emissions[~emissions['Entity'].isin(non_countries)]
    merged_data = pd.merge(global_renewables, emissions, on='Year', how='inner')
    return merged_data

renewables = load_data()

renewables.head()

renewables.to_csv('renewables.csv', index=False)
