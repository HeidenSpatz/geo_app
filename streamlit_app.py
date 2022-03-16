from matplotlib.pyplot import get
import streamlit as st
import pandas as pd
import numpy as np
import geemap.foliumap as geemap


#OpenStreetMap API for geocoding
from geopy.geocoders import Nominatim 
#To avoid time out in API
from geopy.extra.rate_limiter import RateLimiter



#------------------
# config
st.set_page_config(page_title='Geo App Demo',
                page_icon=":shark:",
                layout='wide')


@ st.cache
def get_csv(url):
    df = pd.read_csv(url, encoding='utf-8')
    return df

url = "https://raw.githubusercontent.com/HeidenSpatz/geo_app/master/lat_lon.csv"
df = get_csv(url)


# sidebar
#------------------
app_type = st.sidebar.selectbox(
    "This can be used to structure the app.",
    ("Find Location", "ImmoScout Offers", "Basic Stats"), 
    index=0
)


if app_type == "Find Location":
    st.header("please enter address and parameters")
    # street, housenumber, city, zip code
    col1, col2, col3, col4 = st.columns([4, 1, 3, 2])

    with col1:
        street = col1.text_input('Street')

    with col2:
        housenr = col2.text_input('Nr.')

    with col3:
        zip = st.text_input('Zip Code')
        
    with col4:
        city = st.text_input('City')

    st.write('address: ', street, " ", housenr, ", ", zip, " ", city)


    geolocator = Nominatim(user_agent="my_user_agent")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

    address = street + " " + housenr + ", " + city + " " + zip


    if len(address) > 5:
        
        location = geolocator.geocode(address)

        lat = location.latitude
        lon = location.longitude

        st.write(location.address)
        st.write(lat, lon)
        popup = f"lat, lon: {lat}, {lon}"

        m = geemap.Map(center=[lat, lon], zoom=15)
        m.add_basemap("ROADMAP")
        m.add_marker(location=(lat, lon), popup=popup)    
        m.to_streamlit(height=600)
    else:
        m = geemap.Map(center=[50.12978175, 8.693144895303579], zoom=15)
        m.to_streamlit(height=600)




if app_type == "ImmoScout Offers":
    st.title("ImmoScout Offers")    

    #districts_single = st.selectbox("Select One District", df['regio3'].unique())
    districts_selected = st.multiselect("Select Districts", df['regio3'].unique(), 'Bornheim')
    

    districts_data = df[df.regio3.isin(districts_selected)]

    m = geemap.Map(locate_control=True, plugin_LatLngPopup=False)
    m = geemap.Map(center=[50.12978175, 8.693144895303579], zoom=5)
    m.add_points_from_xy(districts_data, "lon", "lat")

    m.to_streamlit()


if app_type == "Basic Stats":

    st.header("Basic Stats")

    with st.expander("Click to see basic stats!"):
        st.write("df.columns", list(df.columns))
        st.write("df.head()", df.head())
        st.write("df.astype(str)", df.astype(str).head())
        st.write("df.describe()", df.describe())
        st.write("df.info()", df.info())





