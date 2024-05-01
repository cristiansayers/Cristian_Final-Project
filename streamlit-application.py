import streamlit as st

st.set_page_config(layout='wide', page_title='An Exploration of Emission Trends and Climate Trajectories')
st.title('Exploring Emission Trends and Climate Trajectories')
st.markdown('---')
st.write('Currently, there is an urgent need to understand and communicate the effects of greenhouse gas emissions on global climate patterns.')
st.write('It is imperative to elucidate the connections between carbon dioxide emissions and the events we observe in the world around us. This will allow us to gain a better understanding for our world and how we are impacting our envirionment')
st.write('The data and visualizations presented here show key relationships between carbon dioxide emissions, global temperature, detrimental weather events and deforestation, the connection between technological advancements and emissions, and show future projections that speak to the future of our world under different scenarios.')
st.write('***Side Note: For every visualization below, hover your mouse over the data points to get specific values and more details!***')
st.markdown('---')

import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

##DATA-LOADING##

co2_temp_data = pd.read_csv('data/co2temp.csv')
projected_data = pd.read_csv('data/projected_impacts.csv')
gdp_emissions_data = pd.read_csv('data/co2gdp.csv')
renewablesdata = pd.read_csv('data/renewables.csv')
deforestdata = pd.read_csv('data/deforestation-co2-dataset.csv')
weatherdata = pd.read_csv('data/weather-co2.csv')
df = pd.read_csv('data/paris_agreement.csv')
###############################CARBON DIOXIDE-TEMPERATURE##########################################################

st.subheader('**CO2 Emissions and Global Temperature Trends**')

st.write('***Relationship Between Emissions and Temperature for the Previous Century***') 

st.write('***Select Year Range***')
year_range = st.slider('Year Range', int(co2_temp_data['Year'].min()), int(co2_temp_data['Year'].max()), (1970, 2020))

filtered_data = co2_temp_data[(co2_temp_data['Year'] >= year_range[0]) & (co2_temp_data['Year'] <= year_range[1])]

correlation = filtered_data['Annual CO₂ emissions'].corr(filtered_data['Annual Temperature Anomaly'])

fig = px.scatter(filtered_data, x='Annual CO₂ emissions', y='Annual Temperature Anomaly', trendline='ols',
                 labels={'Annual CO₂ emissions': 'Global CO2 Emissions (tonnes)', 'Annual Temperature Anomaly': 'Temperature Anomaly (°C)'},
                 title='Correlation between Global CO2 Emissions and Temperature Anomaly',
                 color_continuous_scale=px.colors.diverging.Tealrose, color='Year')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

st.write('The relationship between global carbon dioxide emissions and yearly temperature anomaly can be shown through the a numerical correlation of the two values over a specified time period. This is the **correlation coefficient** shown below.')
st.write('As the number more closely approaches 1, the relationship becomes more directly proportional between the temperature anomaly and co2 emissions per year.')
st.write(f'**Correlation coefficient: {correlation:.2f}**')

st.plotly_chart(fig, use_container_width=True)

st.write('The plots below show the global carbon dioxide and temperature progressions over time.')

fig_co2 = px.line(filtered_data, x='Year', y='Annual CO₂ emissions', title='Global CO2 Emissions Over Time', line_shape='linear', render_mode='svg')
fig_co2.update_traces(line_color='green')
fig_temp = px.line(filtered_data, x='Year', y='Annual Temperature Anomaly', title='Global Temperature Anomalies Over Time', line_shape='linear', render_mode='svg')
fig_temp.update_traces(line_color='red')
col1, col2 = st.columns(2)
col1.plotly_chart(fig_co2, use_container_width=True)
col2.plotly_chart(fig_temp, use_container_width=True)

##########
st.markdown('---')
st.write('***Climate Change Projections to the Year 2100***')

st.write('Below there are three scenarios which represent different socio-economic standards for the future and the impact of these standards on the carbon dioxide emissions and global temperature.')
st.write('> SSP1-26  > A ***sustainable and equitable*** global future with low greenhouse gas emissions.')
st.write('> SSP2-45  > A ***moderate effort*** at climate mitigation into the future.')
st.write('> SSP5-Baseline  > A future with high greenhouse gas emissions and ***minimal climate restrictions***.')

colors = {
    "SSP1-26": "rgb(44, 160, 44)",  # Green
    "SSP2-45": "rgb(31, 119, 180)",  # Blue
    "SSP5-Baseline": "rgb(255, 127, 200)"  # Orange
}

fig_emissions = go.Figure()
fig_temperature = go.Figure()

for scenario in projected_data['Scenario'].unique():
    scenario_data = projected_data[projected_data['Scenario'] == scenario]
    
    fig_emissions.add_trace(go.Scatter(
        x=scenario_data['Year'], y=scenario_data['CO2 Emissions'],
        mode='lines+markers',
        name=scenario,
        line=dict(color=colors.get(scenario, 'gray'), width=2),  # Use 'gray' as default if not in dictionary
        marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey'))
    ))
    
    fig_temperature.add_trace(go.Scatter(
        x=scenario_data['Year'], y=scenario_data['Temperature Change'],
        mode='lines+markers',
        name=scenario,
        line=dict(color=colors.get(scenario, 'gray'), width=2),  # Use 'gray' as default if not in dictionary
        marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey'))
    ))

common_layout_args = {
    'xaxis': {'title': 'Year'},
    'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40},
    'legend': {'title': 'Scenarios', 'x': 0.02, 'y': 1, 'xanchor': 'left'},
    'hovermode': 'x'
}

fig_emissions.update_layout(
    **common_layout_args,
    yaxis={'title': 'CO2 Emissions (metric tons)'},
    title='CO2 Emissions Over Time for Each Scenario'
)

fig_temperature.update_layout(
    **common_layout_args,
    yaxis={'title': 'Temperature Change (°C)'},
    title='Temperature Change Over Time for Each Scenario'
)

st.plotly_chart(fig_emissions, use_container_width=True)

st.plotly_chart(fig_temperature, use_container_width=True)

selected_scenario = st.selectbox("Select a Scenario for Detailed View", options=projected_data['Scenario'].unique())

filtered_data = projected_data[projected_data['Scenario'] == selected_scenario]
fig_detailed = go.Figure()

fig_detailed.add_trace(go.Scatter(
    x=filtered_data['Year'], y=filtered_data['CO2 Emissions'],
    mode='lines+markers',
    name='CO2 Emissions (metric tons)',
    line=dict(color='RoyalBlue', width=4),
    marker=dict(size=10, symbol='circle')
))

fig_detailed.add_trace(go.Scatter(
    x=filtered_data['Year'], y=filtered_data['Temperature Change'],
    mode='lines+markers',
    name='Temperature Change (°C)',
    line=dict(color='Crimson', width=4, dash='dash'),
    marker=dict(size=10, symbol='x'),
    yaxis='y2'
))

fig_detailed.update_layout(
    title=f'CO2 Emissions vs. Temperature Change for the {selected_scenario} Scenario',
    xaxis_title='Year',
    yaxis=dict(
        title='CO2 Emissions (metric tons)',
        titlefont=dict(color='RoyalBlue'),
        tickfont=dict(color='RoyalBlue'),
        showgrid=True,
        gridcolor='RoyalBlue'
    ),
    yaxis2=dict(
        title='Temperature Change (°C)',
        titlefont=dict(color='Crimson'),
        tickfont=dict(color='Crimson'),
        overlaying='y',
        side='right',
        gridcolor='Crimson'
    ),
    legend_title="Measurements"
)

st.plotly_chart(fig_detailed, use_container_width=True)

###############################ECONOMY##########################################################
st.markdown('---')
st.subheader('**Economic Outlook on Global Emission Trends**')

st.write('***Analyzing the Relationship Between Emissions, GDP, & Population for the Top 10 Emitters***')

def assign_colors(data_frame, column, color_list):
    unique_countries = data_frame[column].unique()
    color_map = {country: color_list[i % len(color_list)] for i, country in enumerate(unique_countries)}
    return color_map

def create_bar_chart(data, x_column, y_column, title, color_map):
    fig = px.bar(data, x=x_column, y=y_column, title=title,
                 color=x_column, color_discrete_map=color_map)
    st.plotly_chart(fig, use_container_width = True)


hex_colors = [
    '#1f77b4',  
    '#ff7f0e',  
    '#2ca02c',  
    '#d62728',  
    '#9467bd',  
    '#8c564b',  
    '#e377c2',  
    '#7f7f7f',  
    '#bcbd22',  
    '#17becf'   
]


st.write('The following visualizations show the relationships between the top 10 countries in carbon dioxide emissions for the year 2022, their GDP, and population size.')
st.write('For exact values, hover over the bars/data points to see more information.')

color_map = assign_colors(gdp_emissions_data, 'Entity', hex_colors)

data_gdp_sorted = gdp_emissions_data.sort_values(by='GDP (current US$)', ascending=False)
data_pop_sorted = gdp_emissions_data.sort_values(by='Population, total', ascending=False)


tab1, tab2, tab3 = st.tabs(["CO2 Emissions", "GDP by Country", "Population by Country"])

with tab1:
    st.write('***Carbon Dioxide Emissions for 2022 of the Top 10 Emitters***')
    create_bar_chart(gdp_emissions_data, 'Entity', 'Annual CO₂ emissions', 'Annual CO₂ emissions by Country for 2022 in Tonnes', color_map)
with tab2:
    st.write('***GDP of the Top 10 Emitters for 2022***')
    create_bar_chart(data_gdp_sorted, 'Entity', 'GDP (current US$)', 'GDP by Country', color_map)

with tab3:
    st.write('***Population of the Top 10 Emitter for 2022***')
    create_bar_chart(data_pop_sorted, 'Entity', 'Population, total', 'Population by Country', color_map)



    

taba, tabb = st.tabs(['CO2 Emissions vs. GDP', 'CO2 Emissions vs. Population'])
with taba:
    st.write('***CO2 Emissions vs GDP Scatter Plot***')
    st.write('***Dot size represents annual carbon dioxide emissions.***')
    fig4 = px.scatter(
        gdp_emissions_data, x='GDP (current US$)', y='Annual CO₂ emissions', text='Entity',
        title='CO2 Emissions vs GDP (Log Scale)', log_x=True, log_y=True,
        labels={'GDP (current US$)': 'GDP (current US$)', 'Annual CO₂ emissions': 'CO2 Emissions'},
        size='Annual CO₂ emissions', size_max=40, color='Entity',  # Adjusted size_max and color
        hover_data=['GDP (current US$)', 'Annual CO₂ emissions'])
    fig4.update_traces(textposition='middle left')
    fig4.update_layout(legend_title_text='Country', yaxis_range=[8.6, 10.4])
    st.plotly_chart(fig4, use_container_width = True)
    st.write(' > Higher emissions come from countries with higher GDP for this subset.')
with tabb:
    st.write('***CO2 Emissions vs Population Scatter Plot***')
    st.write('***Dot size represents annual carbon dioxide emissions.***')
    fig5 = px.scatter(
        gdp_emissions_data, x='Population, total', y='Annual CO₂ emissions', text='Entity',
        title='CO2 Emissions vs Population (Log Scale)', log_x=True, log_y=True,
        labels={'Population, total': 'Population', 'Annual CO₂ emissions': 'CO2 Emissions'},
        size='Annual CO₂ emissions', size_max=30, color='Entity',  # Adjusted size_max and color
        hover_data=['Population, total', 'Annual CO₂ emissions'])
    fig5.update_traces(textposition='middle right')
    fig5.update_layout(legend_title_text='Country', yaxis_range=[8.6, 10.4])
    st.plotly_chart(fig5, use_container_width = True)
    st.write(' > There is a general trend of higher emissions being seen from countries with larger populations for this subset.')



st.markdown('---')
###RENEWABLES###########################

st.write('***In the tree map below, the size of the box represents the magnitude of carbon dioxide emissions.***')
st.write('***Hover over each box to see more information.***')

gdp_reload = pd.read_csv('data/co2gdp.csv')

gdp_reload['Economic Classification'] = pd.cut(
    gdp_reload['GDP (current US$)'] / gdp_reload['Population, total'],
    bins=[0, 1000, 10000, 100000],
    labels=["Low Income", "Middle Income", "High Income"],
    right=False)
filtered_data = gdp_reload[['Entity','Annual CO₂ emissions', 'Economic Classification', 'GDP (current US$)', 'Population, total']]

fig = px.treemap(
    filtered_data,
    path=['Entity', 'Economic Classification'],
    values='Annual CO₂ emissions',
    color='Annual CO₂ emissions',
    hover_data=['GDP (current US$)', 'Population, total', 'Annual CO₂ emissions', 'Economic Classification'],
    color_continuous_scale='reds',
    title="Treemap of the Top 10 Emitters")

fig.update_layout(
    margin=dict(t=50, l=25, r=25, b=25),
    font=dict(size=12, color="RebeccaPurple"))

st.plotly_chart(fig, use_container_width=True)


st.markdown('---')

def plot_dual_axis_trends(data, country=None):
    if country:
        data = data[data['Entity'] == country]
    else:
        data = data.groupby('Year').agg({
            'Share of modern renewables in final energy consumption, World': 'mean',
            'Annual CO₂ emissions': 'sum'
        }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=data['Year'], y=data['Share of modern renewables in final energy consumption, World'],
            name='Renewable Energy Share (%)',
            mode='lines+markers',
            line=dict(color='green', dash='dash'),  
            marker=dict(symbol='circle', size=8)
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=data['Year'], y=data['Annual CO₂ emissions'],
            name='CO₂ Emissions (tons)',
            mode='lines+markers',
            yaxis='y2',
            line=dict(color='magenta', dash='dot'),  
            marker=dict(symbol='square', size=8)
        )
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis=dict(
            title="Global Renewable Energy Share (%)",
            gridcolor='blue',
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        yaxis2=dict(
            title="CO₂ Emissions (tons)",
            overlaying='y',
            side='right',
            gridcolor='red',
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        title="Worldwide Renewable Energy Share vs Country CO₂ Emissions Over Time",
        title_font=dict(size=16, family='Helvetica'),
        legend=dict(x=0.1, y=1.1, orientation='h'),
        hovermode='closest'
    )
    
    return fig


st.write('***Renewable Energy Investement Outlook***')
st.write('> The following visualization allows us to see how carbon dioxide emissions for specific countries and the world, compare against the overall worldwide share of renewable energy.')
country = st.selectbox('Select Global or a Country:', ['Global'] + sorted(renewablesdata['Entity'].unique().tolist()))
trend_fig = plot_dual_axis_trends(renewablesdata, country if country != 'Global' else None)
st.plotly_chart(trend_fig, use_container_width = True)
st.write('> When comparing the global CO2 emissions over time vs. the worldwide renewable energy share, it can be seen that both lines trend parallel to each other for the majority of the plot.')
st.write('> This could imply that we are at a stage in which we are reacting to the energy crisis as we observe the negative effects rather than being proactive to reduce effects ahead of time.')

st.markdown('---')

#############################################################################
st.subheader('Exploring Environmental Consequences from Emissions')
st.write('***Analyzing the Relationship Between Deforestation Rates and Emissions***')
st.write('> The visualizations below show the effects of deforestation on carbon dioxide emissions for critical regions such as the Amazon, Congo Basin, and SouthEast Asia.')
st.write('***Dot size represents tree cover loss***')
selected_region = st.selectbox('Select a Region:', deforestdata['region'].unique())

filtered_data = deforestdata[deforestdata['region'] == selected_region]

scatter_fig = px.scatter(filtered_data, x='tree_cover_loss', y='co2_emissions',
                         size='tree_cover_loss', color='country',
                         hover_data=['year', 'country'], title=f"CO2 Emissions vs. Tree Cover Loss in {selected_region}")
scatter_fig.update_layout(legend_title_text='Country')
scatter_fig.update_xaxes(title_text='Tree Cover Loss (ha)')
scatter_fig.update_yaxes(title_text='CO2 Emissions (tonnes)')

st.plotly_chart(scatter_fig, use_container_width=True)

st.write('> From the scatter plots for each region, there is a consistent trend in which countries within the regions with higher tree cover loss emit greater amounts of carbon dioxide as a result')

annual_data = filtered_data.groupby('year').agg({'tree_cover_loss': 'mean', 'co2_emissions': 'mean'}).reset_index()

line_fig = go.Figure()

line_fig.add_trace(go.Scatter(x=annual_data['year'], y=annual_data['tree_cover_loss'],
                              mode='lines+markers',
                              name='Tree Cover Loss',
                              line=dict(color='blue', width=2),
                              marker=dict(size=10, opacity=0.8)))

line_fig.add_trace(go.Scatter(x=annual_data['year'], y=annual_data['co2_emissions'],
                              mode='lines+markers',
                              name='CO2 Emissions',
                              line=dict(color='red', width=2),
                              marker=dict(size=10, opacity=0.8),
                              yaxis='y2'))

line_fig.update_layout(
    title=f"Progression of Tree Cover Loss and CO2 Emissions Over Time in {selected_region}",
    xaxis_title="Year",
    yaxis=dict(
        title="Tree Cover Loss (ha)",
        type='log',
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgrey'
    ),
    yaxis2=dict(
        title='CO2 Emissions (tonnes)',
        overlaying='y',
        side='right',
        type='log'
    ),
    legend_title="Metric",
    plot_bgcolor='white',
    font=dict(family="Helvetica, Arial, sans-serif", size=14, color="black")
)

st.plotly_chart(line_fig, use_container_width=True)
st.write('> A consistent trend between CO2 emissions and tree cover loss can be seen for the Congo Basin data, but not for the Amazon or SouthEast Asia Regions.')

st.markdown('---')
##############################################################################################
st.write('***Extreme Weather Event Frequency Correlation with Carbon Dioxide Emissions***')

annual_data = weatherdata.groupby('year').agg({
    'co2 emissions': 'sum',
    'natural disaster': 'count'
}).reset_index()

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=annual_data['year'], y=annual_data['co2 emissions'], name='Total CO2 Emissions',
                         line=dict(color='blue', width=2)), secondary_y=False)
fig.add_trace(go.Scatter(x=annual_data['year'], y=annual_data['natural disaster'], name='Total Disaster Frequency',
                         line=dict(color='red', width=2, dash='dash')), secondary_y=True)

fig.update_layout(
    title='Total Disaster Weather Frequency vs CO2 Emissions Over Time',
    xaxis_title='Year',
    yaxis_title='CO2 Emissions',
    yaxis2_title='Disaster Frequency',
    plot_bgcolor='white',
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey'),
    legend=dict(x=0.01, y=0.99, bordercolor='Black', borderwidth=1)
)
fig.update_xaxes(tickangle=-45)
st.plotly_chart(fig, use_container_width = True )
st.write('> There is a very faint generalized trend that can be seen above. The peaks of each dataset seem to be correlating. This will be explored in more depth in the next visualization')

st.write('***Comparing Specific Disaster Weather Types Against Total Carbon Dioxide Emissions***')
disaster_type = st.selectbox('Select Disaster Type:', weatherdata['natural disaster'].unique())

type_data = weatherdata[weatherdata['natural disaster'] == disaster_type]
type_annual_data = type_data.groupby('year').agg({
    'co2 emissions': 'sum',
    'natural disaster': 'count'
}).reset_index()

fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(go.Scatter(x=type_annual_data['year'], y=type_annual_data['co2 emissions'], name='CO2 Emissions',
                          line=dict(color='blue', width=2)), secondary_y=False)
fig2.add_trace(go.Scatter(x=type_annual_data['year'], y=type_annual_data['natural disaster'], name=f'{disaster_type} Frequency',
                          line=dict(color='red', width=2, dash='dash')), secondary_y=True)

fig2.update_layout(
    title=f'Total CO2 Emissions and {disaster_type} Frequency Over Time',
    xaxis_title='Year',
    yaxis_title='CO2 Emissions',
    yaxis2_title='Disaster Frequency',
    plot_bgcolor='white',
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey'),
    legend=dict(x=0.01, y=0.99, bordercolor='Black', borderwidth=1)
)
fig2.update_xaxes(tickangle=-45)
st.plotly_chart(fig2,use_container_width = True )

st.write('> ***For all disaster weather types that are affected by atmospheric variables, there is a clear correlation between peaks in CO2 emissions and event frequency. This gives grounds to believe that weather events that are extreme in nature are somewhat affected by CO2 emissions.***')

st.markdown('---')
###############################################################################
st.subheader('The Paris Agreement')
st.write('> Based on the carbon dioxide emissions over time, it can be assessed as to whether the Paris Agreement has made any significant changes to global carbon dioxide emissions since the enactment of the agreement.')
st.write('> The data will be shown from 2017 onwards as the Paris Agreement was brought into existence in late 2016.')
def create_emission_plot(df, country):
    filtered_df = df[df['Entity'] == country]
    filtered_df['SMA_3'] = filtered_df['Annual CO₂ emissions'].rolling(window=3, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Annual CO₂ emissions'], mode='lines+markers',
                             name='Actual Emissions', line=dict(color='blue', width=3),
                             marker=dict(color='blue', size=7, line=dict(width=3, color='DarkSlateGrey')),
                             text=filtered_df['Annual CO₂ emissions'],
                             hoverinfo='text+x+y'))

    fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['SMA_3'], mode='lines',
                             name='3-Year SMA', line=dict(color='red', dash='dash', width=2.5),
                             hoverinfo='skip'))

    fig.update_layout(title=f'Annual CO₂ Emissions for {country} since enactment of Paris Agreement',
                      xaxis_title='Year',
                      yaxis_title='CO2 Emissions (tonnes)',
                      font=dict(color='white', size=12),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    try:
        emissions_2017 = filtered_df[filtered_df['Year'] == 2017]['Annual CO₂ emissions'].values[0]
        emissions_2022 = filtered_df[filtered_df['Year'] == 2022]['Annual CO₂ emissions'].values[0]
        net_difference = emissions_2022 - emissions_2017
    except IndexError:
        net_difference = "Data not available for full range"

    return fig, net_difference

st.write('> By changing the country in the selection box, the emissions over time and the 3-year rolling average for each country will be visualized.')
    
country = st.selectbox('Select a Country', options=df['Entity'].unique())
plot, net_diff = create_emission_plot(df, country)
    
st.plotly_chart(plot, use_container_width=True)

st.write('***Country Emissions Status Since Enactment of Agreement:***')

if int(net_diff) >= 1:
    st.write(f'> ***Emissions are still trending upwards for {country}.***')
else:
    st.write(f'> ***Emissions are decreasing for {country}.***')

if isinstance(net_diff, str):
    st.write(net_diff)
else:
    st.write(f'> ***Net emissions since agreement: {net_diff:,} tonnes***')

st.markdown('---')

st.subheader('Conclusions')

st.write('Clearly there is a multifaceted impact that carbon dioxide emissions have on the world around us as elucidated by the above data visualizations. The above data highlights room to grow as well as progress that has been made.')
st.write('This dashboard clearly explains the effects of carbon dioxide emissions on the climate. We should all work towards reducing emissions to mitigate this impact.')








