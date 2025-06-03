################################################ DIVVY BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'CitiBikes Strategy Dashboard', layout='wide')
st.title("New York CitiBikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems CitiBikes currently faces")
st.markdown("analyzing user behavior in 2022 to help the business strategy department assess the current logistics model of bike distribution across the city and identify expansion opportunities.")

########################## Import data ###########################################################################################

df = pd.read_csv(r'/Users/yasersouri/Desktop/newyork_Data/NewYork_CitiBike_data2.csv', index_col = 0)
top20 = pd.read_csv(r'/Users/yasersouri/Desktop/newyork_Data/top20.csv', index_col = 0)

# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 600, height = 400
)
st.plotly_chart(fig, use_container_width=True)


## Line chart 

# Drop missing values
df = df.dropna(subset=['date', 'bike_rides_daily', 'avgTemp'])

# Sort by date
df = df.sort_values('date')

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(
    go.Scatter(x=df['date'], y=df['bike_rides_daily'], mode='lines', name='Daily bike rides', line=dict(color='blue')),
    secondary_y=False
)

fig2.add_trace(
    go.Scatter(x=df['date'], y=df['avgTemp'], mode='lines', name='Daily temperature', line=dict(color='red')),
    secondary_y=True
)

fig2.update_layout(
    title='Daily Bike Rides and Temperature in 2022',
    xaxis_title='Date',
    yaxis_title='Daily Bike Rides',
    legend=dict(x=0.01, y=0.99)
)

fig2.update_yaxes(title_text="Daily bike rides", secondary_y=False)
fig2.update_yaxes(title_text="Temperature (°C)", secondary_y=True)

st.plotly_chart(fig2, use_container_width=True)
st.markdown("From May to October, city bikes saw higher usage, likely due to the warmer weather.")


### Add the map ###

path_to_html = "/Users/yasersouri/Desktop/data analysis/specialization 2/New-York-CitiBike-trips-in-2022/CitiBike Trips Aggregated.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=450)
st.markdown("The output from the bike trips map highlights that the most common Citi Bike trips in New York City occur in dense, high-traffic areas like Lower Manhattan and parts of Brooklyn such as Williamsburg. These zones are heavily used due to their proximity to workplaces, transit hubs, and popular attractions. The concentration of short trips in these areas suggests that Citi Bikes are primarily used for quick commutes and last-mile travel. The high volume of activity around specific stations reflects both commuter patterns during rush hours and the popularity of recreational routes along scenic corridors like the Hudson River Greenway. This usage pattern underscores Citi Bike’s role as both a practical transportation solution and a leisure option for residents and visitors alike.")