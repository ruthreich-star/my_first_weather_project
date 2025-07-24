import streamlit as st
import pandas as pd
import numpy as np
import requests as rq

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
            "humidity": data["main"]["humidity"]
        }
    else:
        return None

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
        st.write(f"Condition: {result['weather']}")
        st.write(f"Humidity: {result['humidity']}%")
    else:
        st.error("City not found.")