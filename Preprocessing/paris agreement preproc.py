import pandas as pd

def preprocess_paris_agreement_data(data_path):
  df = pd.read_csv(data_path)

  df_filtered = df[df['Year'] >= 2017]

    
  if df_filtered['Annual CO₂ emissions'].isnull().any():
     raise ValueError("Missing values found in Annual CO₂ emissions data.")

    
  non_country_entities = ['World', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania',
        'European Union (27)', 'European Union (28)', 'High-income countries', 'Low-income countries',
        'Lower-middle-income countries', 'Upper-middle-income countries', 'International aviation', 'International shipping',
        'Asia (GCP)', 'Europe (GCP)', 'North America (GCP)', 'South America (GCP)', 'Oceania (GCP)', 'Middle East (GCP)',
        'Central America (GCP)', 'Non-OECD (GCP)', 'OECD (GCP)', 'Africa (GCP)', 'Asia (excl. China and India)',
        'Europe (excl. EU-27)', 'Europe (excl. EU-28)', 'North America (excl. USA)']

  df_filtered = df_filtered[~df_filtered['Entity'].isin(non_country_entities)]

  annual_co2_summary = df_filtered.groupby(['Entity', 'Year'])['Annual CO₂ emissions'].sum().reset_index()

  return annual_co2_summary


paris_agreement = preprocess_paris_agreement_data('annual-co2-emissions-per-country.csv')

paris_agreement.head()

paris_agreement.to_csv('paris_agreement.csv', index=False)
