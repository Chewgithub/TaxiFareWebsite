import config
import streamlit as st
import datetime
import requests
import pandas as pd


'''
# New York City Taxi Fare Prediction
'''
import gmaps
from ipywidgets import embed
import streamlit.components.v1 as components
import googlemaps

# if you wish to run locally on your machine, please replace api_key to your personal api key

gmaps.configure(config.api_key)
maps_api = googlemaps.Client(config.api_key)


st.markdown('''
We help you to predict taxi fare in New York City!
''')
'''
### Datetime
'''
col1, col2= st.columns(2)

with col1:
#Asking date
    d = st.date_input(
        "Date of Travel",
        datetime.datetime(2022, 6, 6))

    st.write('Date of Travel is:', d)

with col2:
    # Asking time
    t = st.time_input('Time for travel', datetime.time(8, 45))
    st.write('Time for travel', t)


########################################################################################################################

col1, col2= st.columns(2)
with col1:
    '''
    ### Pickup
    '''
    pickup_location=st.text_input(label='Please enter Pickup location', placeholder='Empire State Building')

    try:
        geocode_result = maps_api.geocode(pickup_location)

        pickup_latitude=geocode_result[0]['geometry']['location']['lat']
        pickup_longitude=geocode_result[0]['geometry']['location']['lng']
        pickup_1=geocode_result[0]['address_components'][1]['short_name']
        pickup_2=geocode_result[0]['address_components'][2]['short_name']
        pickup_3=geocode_result[0]['address_components'][3]['short_name']
        st.write(f'Pickup Address: {pickup_1}, {pickup_2}, {pickup_3}')

        st.write('Pickup latitude: ', pickup_latitude)
        st.write('Pickup longitude: ', pickup_longitude)
    except:
        pass

with col2:
    '''
    ### Drop-off
    '''
    dropoff_location=st.text_input(label='Please enter Dropoff location', placeholder='New York Botanical Garden')

    try:
        geocode_result_drop = maps_api.geocode(dropoff_location)

        dropoff_latitude=geocode_result_drop[0]['geometry']['location']['lat']
        dropoff_longitude=geocode_result_drop[0]['geometry']['location']['lng']
        dropoff_1=geocode_result_drop[0]['address_components'][1]['short_name']
        dropoff_2=geocode_result_drop[0]['address_components'][2]['short_name']
        dropoff_3=geocode_result_drop[0]['address_components'][3]['short_name']
        st.write(f'Pickup Address: {dropoff_1}, {dropoff_2}, {dropoff_3}')

        st.write('Dropoff latitude: ', dropoff_latitude)
        st.write('Dropoff longitude: ', dropoff_longitude)
    except:
        pass
########################################################################################################################


option = st.slider('How many passenger(s) do you have?', 1, 10, 3)
st.write('The passenger count is ', option)
#Labelling coordinates on google map
try:
    c=((pickup_latitude+dropoff_latitude)/2, (pickup_longitude+dropoff_longitude)/2)

    fig = gmaps.figure(center=c,zoom_level=10)


    #locations for both pick-up and drop-off
    locations = [
            (pickup_latitude, pickup_longitude),]
    locations2=[(dropoff_latitude, dropoff_longitude)]


    #labelling for both pick-up and drop-off on map
    pickup_label = ['Pickup here!']
    symbols = gmaps.symbol_layer(
            locations, fill_color='red', stroke_color='red',info_box_content=pickup_label)
    fig.add_layer(symbols)


    dropoff_label = ['Dropoff here!']
    symbols2 = gmaps.symbol_layer(
            locations2, fill_color='blue', stroke_color='blue',info_box_content=dropoff_label)
    fig.add_layer(symbols2)


    #snippet for streamlit frontend
    snippet = embed.embed_snippet(views=fig)
    html = embed.html_template.format(title="googlemap", snippet=snippet)
    components.html(html, height=400,width=700)
    n=1
except:
    n=0

if n==0:
    try:
        maps_df = pd.DataFrame(
        [[pickup_latitude,pickup_longitude],[dropoff_latitude,dropoff_longitude]],
        columns=['lat', 'lon'])
        st.map(maps_df)
    except:
        pass

url = 'https://taxifare.lewagon.ai/predict'




try:
#build a dictionary containing the parameters for our API...
    combined = str(d)+' '+str(t)

    params=dict(
    pickup_datetime=combined,
    pickup_longitude=pickup_longitude,
    pickup_latitude=pickup_latitude,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude=dropoff_latitude,
    passenger_count=option
    )
    df = pd.DataFrame(
     [[pickup_latitude,pickup_longitude],[dropoff_latitude,dropoff_longitude]],
     columns=['lat', 'lon'])


    #prediction button
    col1, col2, col3 = st.columns(3)
    with col2:
        a=st.button('Make Prediction Now')
        if a==False:
            st.stop()

    #call our API using the `requests` package...
    st.balloons()
    res=requests.get(url, params=params)
    data=res.json()

    #retrieve the prediction from the **JSON** returned by the API...
    pred=data['fare']

    st.write(f'The fare is {round(pred,2)}USD')

except:
    pass
