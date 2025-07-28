import streamlit as st
import pandas as pd
import numpy as np
import requests as rq
from datetime import datetime, timedelta
import pytz
import folium
from streamlit_folium import folium_static
st.image("weatherly_logo.png", width=250)
# padding: 10px 0 20px 0;">
#🌦️ Weatherly
#        <h3 style="color: #444;">Smart Weather. Live Maps. Simple Vibe.</h3>
st.markdown("""
    <div style="text-align: center; margin-top: -130px;">  
        <h1 style="font-size: 30px; color: #00aaff; font-family: 'Segoe UI', sans-serif;">
            Smart Weather. Live Maps. Simple Vibe.           
        </h1>
    </div>
""", unsafe_allow_html=True)

#selected_city = st.selectbox("בחר עיר", city_names)
API_KEY = "0a867690493989d87c77fa39ebf46377"
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = rq.get(url)
    if response.status_code == 200:
        data = response.json()
#       temp = data['main']['temp']
#       weather = data['weather'][0]['description']
#       humidity = data['main']['humidity']
#       print(f"City: {city}")
#       print(f"Temperature: {temp}°C")
#       print(f"Weather: {weather}")
#       print(f"Humidity: {humidity}%")
#   else:
#       print("City not found.")
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "timezone_offset_sec" : data["timezone"],
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"]
        }
    else:
        return None
        # החזרת תשובה של השגיאה במקום כלום
        #return response.raise_for_status()
def get_weather_icon(condition):
    condition = condition.lower()
    if "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "snow" in condition:
        return "❄️"
    elif "storm" in condition or "thunder" in condition:
        return "⛈️"
    elif "mist" in condition or "fog" in condition:
        return "🌫️"
    else:
        return "🌡️"
# Ask user for input
#city = input("Enter city name: ")
#get_weather(city)
#st.title("My Private Reich Weather ☀️ or 🌧️ ")
local_city = "Jerusalem"
url = f"http://api.openweathermap.org/data/2.5/weather?q={local_city}&appid={API_KEY}&units=metric"
response1 = rq.get(url)
data1 = response1.json()
local_zone = data1["timezone"]
#city = st.text_input("Enter city name")
#if st.button("Get Weather") and city:
#cities_list = ["Tel Aviv", "Jerusalem", "Haifa", "Eilat"]
with st.form(key="weather_form"):
    city = st.text_input("Enter city name")
    submitted = st.form_submit_button("Get Weather")
st.markdown("</div>", unsafe_allow_html=True)
#  if st.form_submit_button("") and city:
if submitted and city:

    result = get_weather(city)
    if result:
        left_col, right_col = st.columns([2, 1])
        with left_col:
            if local_zone != result["timezone_offset_sec"]:
               user_timezone = pytz.timezone("Asia/Jerusalem")
               user_time = datetime.now(user_timezone)
               formatted_user_time = user_time.strftime("%A, %B %d, %Y, %I:%M %p")
               st.write(f"🕒User Time: {formatted_user_time}")
            st.write(f"### Weather in {result['city']}")
            st.write(f"Temperature: {int(result['temperature'])}°C")
            icon = get_weather_icon(result['weather'])
            st.write(f"Condition: {icon} {result['weather']}")
#        st.write(f"Condition: {result['weather']}")
            st.write(f"Humidity: {int(result['humidity'])}%")
            utc_now = datetime.utcnow()
            local_time = utc_now + timedelta(seconds=result["timezone_offset_sec"])
            formatted_time = local_time.strftime("%A, %B %d, %Y, %I:%M %p")
            st.write(f"🌍 weather Location Time: {formatted_time}")
        with right_col:
            lat = result["latitude"]
            lon = result["longitude"]
            st.write("🗺️ Map of Location:")
            m = folium.Map(location=[lat, lon], zoom_start=13)
            folium.Marker([lat, lon], tooltip=result['city']).add_to(m)
            #folium_static(m)
            folium_static(m, width=200, height=200)


         #   folium.Marker([lat, lon], tooltip=result["city"]).add_to(m)
         #   folium_static(m, width=350, height=300)
    else:
        st.error("City not found.")
