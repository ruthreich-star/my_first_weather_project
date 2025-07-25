import streamlit as st
import pandas as pd
import numpy as np
import requests as rq
from datetime import datetime, timedelta
#df = pd.read_csv(r"C:\Users\reich\OneDrive\מסמכים\GitHub\israel-cities.csv")
#print(df)
#city_names = df["name"].tolist()
#city_names = sorted(df["name"].dropna().unique().tolist())
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
            "timezone_offset_sec" : data["timezone"]
        }
    else:
        return None
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
st.title("My Privet Reich Weather ☀️ or 🌧️ ")
city = st.text_input("Enter city name")
if st.button("Get Weather") and city:
    result = get_weather(city)
    if result:
        st.write(f"### Weather in {result['city']}")
        st.write(f"Temperature: {result['temperature']}°C")
        icon = get_weather_icon(result['weather'])
        st.write(f"Condition: {icon} {result['weather']}")
#        st.write(f"Condition: {result['weather']}")
        st.write(f"Humidity: {result['humidity']}%")
        utc_now = datetime.utcnow()
        local_time = utc_now + timedelta(seconds=result["timezone_offset_sec"])
        formatted_time = local_time.strftime("%A, %B %d, %Y, %I:%M %p")
        st.write(f"Local Time: {formatted_time}")
    else:
        st.error("City not found.")