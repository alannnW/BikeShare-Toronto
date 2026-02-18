from helpers import *
import streamlit as st
import folium # for map visualization
from streamlit_folium import folium_static # to display folium maps in streamlit + package

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
col1, col2, col3 = st.columns(3) # Create three columns for metrics
with col1:
    st.metric(label = 'Bikes Available Now', value = sum(data['num_bikes_available'])) # total number of bikes available across all stations
    st.metric(label = 'E-Bikes Available Now', value = sum(data['ebike'])) # total number of e-bikes available across all stations
with col2:
    st.metric(label = 'Stations w Available Bikes', value = len(data[data['num_bikes_available'] > 0])) # number of stations with at least 1 bike available
    st.metric(label = 'Stations w Available E-Bikes', value = len(data[data['ebike'] > 0])) # number of stations with at least 1 e-bike available
with col3:
    st.metric(label = 'Stations w Empty Docks', value = len(data[data['num_docks_available'] > 0])) # number of stations with no docks available

with st.sidebar:
    bike_method = st.selectbox(
        'Are you looking to rent or return a bike?',
        ('Rent', 'Return')
    )
    if bike_method == 'Rent':
        st.multiselect(
            'What kind of bikes are you looking to rent?',
            ['E-bike', 'Mechanical']
        )
        st.header('Where are you located?')
        input_street = st.text_input('Street', "")
        input_city = st.text_input('City', 'Toronto')
        input_country = st.text_input('Country', 'Canada')
        drive = st.checkbox("I'm driving there.") #gives true or false button
        findmeabike = st.button('Find me a bike!', type = 'primary') #gives a button to click
        # go time!
        if findmeabike:
            if input_street != "":
                iamhere = geocode(input_street+ " " + input_city + " " + input_country) #geocode the address
                if iamhere == '':
                    st.subheader(':red[Input address not valid!]')
            else:
                st.subheader(':red[Input address not valid!]')
    elif bike_method == 'Return':
        st.subheader('Where are you located?')
        input_street = st.text_input('Street', "")
        input_city = st.text_input('City', 'Toronto')
        input_country = st.text_input('Country', 'Canada')
        findmeabike = st.button('Find me a dock!', type = 'primary') #gives a button to click
        if findmeabike:
            if input_street != "":
                iamhere_return = geocode(input_street+ " " + input_city + " " + input_country) #geocode the address
                if iamhere_return == '':
                    st.subheader(':red[Input address not valid!]')
            else:
                st.subheader(':red[Input address not valid!]')

# initial map visualization
# Create a folium map centered around Toronto
center = [43.651070, -79.347015] # Toronto's latitude and longitude
m = folium.Map(location=center, zoom_start=13, tiles='cartodbpositron') # Create a map with a grey background

# Add circle markers to the map for each station
for _, row in data.iterrows():
    marker_color = get_marker_color(row['num_bikes_available'])
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=2,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7,
        popup=folium.Popup(f"Station ID: {row['station_id']}<br>"
                           f"Total Bikes Available: {row['num_bikes_available']}<br>"
                           f"Mechanical Bike Available: {row['mechanical']}<br>"
                           f"E-Bikes Available: {row['ebike']}", max_width=300)
    ).add_to(m)


# Display the map in Streamlit
folium_static(m)

if findmeabike:
    



if findmeadock:
