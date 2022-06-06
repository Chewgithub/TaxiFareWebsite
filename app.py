import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np
'''
# New York City Taxi Fare Prediction
'''

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

'''
### Pickup
'''
col1, col2= st.columns(2)

with col1:
#asking pickup longtitude
    pickup_longtitude = st.number_input('What is your pickup longtitude')
    st.write('The pickup_longtitude is ', pickup_longtitude)

#asking pickup latitude
with col2:
    pickup_latitude = st.number_input('What is your pickup latitude')
    st.write('The pickup_latitude is ', pickup_latitude)

'''
### Dropoff
'''
col1, col2= st.columns(2)
with col1:
#asking dropoff longtitude
    dropoff_longtitude = st.number_input('What is your dropoff longtitude')
    st.write('The dropoff_longtitude is ', dropoff_longtitude)
with col2:
#asking dropoff latitude
    dropoff_latitude = st.number_input('What is your dropoff latitude')
    st.write('The dropoff_latitude is ', dropoff_latitude)


option = st.slider('How many passenger(s) do you have?', 1, 10, 3)
st.write('The passenger count is ', option)



url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')



#build a dictionary containing the parameters for our API...
combined = str(d)+' '+str(t)

params=dict(
  pickup_datetime=combined,
  pickup_longitude=pickup_longtitude,
  pickup_latitude=pickup_latitude,
  dropoff_longitude=dropoff_longtitude,
  dropoff_latitude=dropoff_latitude,
  passenger_count=option
)
df = pd.DataFrame(
     [[pickup_latitude,pickup_longtitude],[dropoff_latitude,dropoff_longtitude]],
     columns=['lat', 'lon'])

st.map(df)


a=st.button('pred')
if a==False:
    st.stop()
#call our API using the `requests` package...
res=requests.get(url, params=params)
data=res.json()

#retrieve the prediction from the **JSON** returned by the API...
pred=data['fare']


#Finally, we can display the prediction to the user
st.write(f'The fare is {round(pred,2)}USD')
