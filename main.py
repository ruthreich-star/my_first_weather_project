import streamlit as st
import pandas as pd
import numpy as np
import requests as rq
from datetime import datetime, timedelta
import pytz
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
st.image("weatherly_logo.png", width=250)
# padding: 10px 0 20px 0;">
#🌦️ Weatherly
#        <h3 style="color: #444;">Smart Weather. Live Maps. Simple Vibe.</h3>
current_month = datetime.now().month
month_name = datetime.now().strftime("%B")
def get_monthly_avg_temps(lat, lon, month=current_month):
    current_year = datetime.now().year
    years = [current_year - i for i in range(1, 6)]
    avg_temps = []

    for year in years:
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max",
            "timezone": "auto"
        }
        response = rq.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            temps = data.get("daily", {}).get("temperature_2m_max", [])
            if temps:
                avg = sum(temps) / len(temps)
                avg_temps.append((year, round(avg, 1)))
            else:
                avg_temps.append((year, None))
        else:
            avg_temps.append((year, None))
    return avg_temps

def plot_temp_history(data):
    df = pd.DataFrame(data, columns=["Year", "Avg Temperature"])
    fig, ax = plt.subplots(figsize=(4, 2))
    sns.barplot(x="Year", y="Avg Temperature", data=df, palette="coolwarm", ax=ax,width=0.4)
    ax.set_title(f"{month_name} Avg Temps - Past 5 Years",fontsize=5, fontweight='bold', color="#00aaff")
    ax.set_xlabel("YEAR", color="#00aaff", fontsize=5)
    ax.set_ylabel("°C" , color="#00aaff", fontsize=5)
    ax.set_ylim(20, 36)
    ax.tick_params(axis='both', labelsize=4)
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.image(buf, caption=f"Historical {month_name} Temperatures", use_container_width=True)


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

        history = get_monthly_avg_temps(result["latitude"], result["longitude"])
        plot_temp_history(history)
         #   folium.Marker([lat, lon], tooltip=result["city"]).add_to(m)
         #   folium_static(m, width=350, height=300)
    else:
        st.error("City not found.")
