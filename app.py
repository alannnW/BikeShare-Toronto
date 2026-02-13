from helpers import *
import streamlit as st

# Example URL to fetch bike share data (replace with the actual URL from resource_urls list)
station_url = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json'  # Replace with the actual URL from resource_urls
latlon_url = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"

st.title('Toronto Bike Share Station Status')
st.markdown('This dashboard tracks bike availability at each Bike Share Station in Toronto.')

# Fetch data for intial visulization
data_df = query_station_status(station_url) # Gets station status
latlon_df = get_station_latlon(latlon_url)
data = join_latlon(data_df, latlon_df) # Joins station status with lat/lon data
# st.dataframe(data) # Uncomment to see the data in the web app

