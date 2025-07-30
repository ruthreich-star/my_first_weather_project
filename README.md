# my_first_weather_project
Weatherly ☔️

Weatherly is a sleek, interactive weather app built with Python and Streamlit. It provides real-time weather updates, interactive maps, historical temperature graphs, and a user-friendly interface enhanced by custom styling.

🚀 Features

🔍 Search for any city to get live weather data

🗺️ View interactive map of the selected location

📊 See average monthly temperatures over the past 5 years

🕒 View local time for both user and selected city

🌡️ Emoji-based visual weather icons

🎨 Beautiful custom CSS styling

📆 Libraries Used

Library           Purpose
streamlit         Web app UI and interactivity
pandas, numpy     Data processing 
requests          API requests (OpenWeatherMap & Open-Meteo)
datetime, pytz    Date and time operations including timezones
folium, streamlit_folium  Interactive maps
matplotlib, Temperature trend plots
 seaborn  io.BytesIO        Rendering graphs as image in app



🧠 App Logic Overview

get_weather(city)

Fetches current weather data for a given city from the OpenWeatherMap API.

get_weather_icon(condition)

Returns an emoji representing the weather condition.

get_monthly_avg_temps(lat, lon, month)

Fetches and averages daily high temperatures for the selected month across the past 5 years from the Open-Meteo historical archive.

plot_temp_history(data)

Displays a line plot of monthly average temperatures using seaborn and matplotlib.

📚 How to Use

Enter a city name in the input box.

Click the "Get Weather" button.

The app will display:

Real-time weather data

An interactive map of the location

Time at the location and for the user

A trend graph of historical temperatures

⚙️ API Key Setup

You need an API key from OpenWeatherMap.

Replace the API key in the script:

API_KEY = "0a867690493989d87c77fa39ebf46377"

with your actual API key.

📺 User Interface Design

The app includes a logo (weatherly_logo.png) at the top.

Custom CSS styles the input box and button.

The layout is clean and responsive, with subtle animations and shadow effects.
