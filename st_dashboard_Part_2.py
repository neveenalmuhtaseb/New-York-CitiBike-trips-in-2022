import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ####################################################

st.set_page_config(page_title='CitiBikes Strategy Dashboard', layout='wide')
myImage = Image.open(r"/Users/yasersouri/Desktop/data analysis/specialization 2/New-York-CitiBike-trips-in-2022/visualizations/citibikelogo.png") 
st.image(myImage,width=300)
st.title("CitiBikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
    ["Intro page", "Weather component and bike usage",
    "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv(r'/Users/yasersouri/Desktop/newyork_Data/reduced_data_to_plot_7.csv', index_col=0)
top20 = pd.read_csv(r'/Users/yasersouri/Desktop/newyork_Data/top20.csv', index_col=0)

######################################### DEFINE THE PAGES #####################################################################

### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems CitiBikes currently faces.")
    myImage2 = Image.open(r"/Users/yasersouri/Desktop/data analysis/specialization 2/New-York-CitiBike-trips-in-2022/visualizations/bike.png") 
    st.image(myImage2,width=200)
    st.markdown("Analyzing user behavior in 2022 to help the business strategy department assess the current logistics model of bike distribution across the city and identify expansion opportunities. The dashboard is separated into 4 sections:")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Most popular stations")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

### Create the dual axis line chart page ###

elif page == 'Weather component and bike usage':
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
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")

### Most popular stations page

elif page == 'Most popular stations':

    # Create the filter on the side bar

    with st.sidebar:
        season_filter = st.multiselect(
            label='Select the season',
            options=df['season'].unique(),
            default=df['season'].unique()
        )

    df1 = df.query('season == @season_filter')

    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label='Total Bike Rides', value=numerize(total_rides))

    # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index=False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')

    fig = go.Figure(go.Bar(
        x=top20['start_station_name'], 
        y=top20['value'], 
        marker={'color': top20['value'], 'colorscale': 'Blues'}
    ))

    fig.update_layout(
        title='Top 20 most popular bike stations in New York',
        xaxis_title='Start stations',
        yaxis_title='Sum of trips',
        width=900, height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("The data shows that bike usage is highly concentrated around a few key stations. Grove St PATH stands out as the most popular starting point for rides, followed by locations such as South Waterfront Walkway, Hoboken Terminal, and City Hall. These stations are located near major transit hubs and waterfront areas, indicating that both commuter and recreational riders rely heavily on the bike-sharing system in these locations.")

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over Chicago")

    path_to_html = "/Users/yasersouri/Desktop/data analysis/specialization 2/New-York-CitiBike-trips-in-2022/CitiBike Trips Aggregated.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height=450)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("The output from the bike trips map highlights that the most common Citi Bike trips in New York City occur in dense, high-traffic areas like Lower Manhattan and parts of Brooklyn such as Williamsburg. These zones are heavily used due to their proximity to workplaces, transit hubs, and popular attractions. The concentration of short trips in these areas suggests that Citi Bikes are primarily used for quick commutes and last-mile travel. The high volume of activity around specific stations reflects both commuter patterns during rush hours and the popularity of recreational routes along scenic corridors like the Hudson River Greenway. This usage pattern underscores Citi Bike’s role as both a practical transportation solution and a leisure option for residents and visitors alike.")

else:

    st.header("Conclusions and recommendations")
    st.markdown("### Our analysis has shown that CitiBikes should focus on the following objectives moving forward:")
    st.markdown("Increase docking capacity at top stations to avoid congestion and ensure availability.and Implement dynamic bike rebalancing, especially during morning and evening peaks.")
    st.markdown("Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costs")
