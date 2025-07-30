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
#ICON for application
st.image("weatherly_logo.png", width=250)
#changing default settings of UI in streamlit
st.markdown("""
<style>
/* מזיז את כל התוכן מעלה ע"י הקטנת ה-padding העליון של הקונטיינר */
.block-container {
    padding-top: 0rem !important;
    margin-top: -30px;
    padding-bottom: 0rem !important;
}

/* מזיז את טופס החיפוש למעלה */
form {
    margin-top: -20px;
    margin-bottom: 0px;
}
/* תיבת קלט */
input[type="text"] {
    padding: 6px 10px;
    border-radius: 10px;
    border: 1px solid #00aaff;
    background-color: #f9fbfd;
    font-size: 16px;
    color: #333;
    width: 100%;
    box-shadow: 2px 2px 4px rgba(0,0,0,0.05);
}
input[type="text"]:focus {
    border: 2px solid #00aaff !important;
    outline: none !important;
    box-shadow: 0 0 4px #00aaff !important;
}

/* כפתור Submit של הטופס */
div.stButton > button {
    background-color: #00aaff;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 15px;
    font-weight: bold;
    transition: all 0.3s ease;
    margin-top: 10px;
}
div.stButton > button:hover {
    color: #00aaff !important;
    background-color: #e6f7ff !important;
    border: 1px solid #00aaff !important;
}
</style>
""", unsafe_allow_html=True)

#כותרת מגניבה

st.markdown("""
    <div style="text-align: center; margin-top: -130px;">  
        <h1 style="font-size: 30px; color: #00aaff; font-family: 'Segoe UI', sans-serif;">
            Smart Weather. Live Maps. Simple Vibe.           
        </h1>
    </div>
""", unsafe_allow_html=True)
#save current month for displaying name and number
current_month = datetime.now().month
month_name = datetime.now().strftime("%B")
#calculate avg temp for the same month in the last 5 years ,
# by having coordinates from the entered user city data and current month
#output : list of (year,avg_temp)
def get_monthly_avg_temps(lat, lon, month=current_month):
    current_year = datetime.now().year
    years = [current_year - i for i in range(1, 6)]
    avg_temps = []

    for year in years:
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
        # create API
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
            #result into json
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
#line plot of avg temp for last 5 years
def plot_temp_history(data):
    df = pd.DataFrame(data, columns=["Year", "Avg Temperature"])
    #fix x size
    fig, ax = plt.subplots(figsize=(4, 2))
    sns.lineplot(x="Year", y="Avg Temperature", data=df, marker="o", color="#007acc", ax=ax)
    years = df["Year"].tolist()  # [2020, 2021, 2022, 2023, 2024]
    ax.set_xticks(years)
    #graph title +x desc and y desc
    ax.set_title(f"{month_name} Avg Temps - Past 5 Years",fontsize=6, fontweight='bold', color="#00aaff")
    ax.set_xlabel("YEAR", color="#00aaff", fontsize=6)
    ax.set_ylabel("°C" , color="#00aaff", fontsize=6)
#y values depent on avg values + padding
    y_min = df["Avg Temperature"].min()
    y_max = df["Avg Temperature"].max()
    # נוסיף מרווח קטן כדי שהגרף לא יהיה צמוד לקצוות
    padding = 2

    ax.set_ylim(y_min - padding, y_max + padding)
    ax.tick_params(axis='both', labelsize=6)
    #arrange for streamlit
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    #finaly the graph is like picture with title
    st.image(buf, caption=f"Historical {month_name} Temperatures", use_container_width=True)


API_KEY = "0a867690493989d87c77fa39ebf46377"
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = rq.get(url)
    if response.status_code == 200:
        data = response.json()
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
#local city for local timezone
local_city = "Jerusalem"
url = f"http://api.openweathermap.org/data/2.5/weather?q={local_city}&appid={API_KEY}&units=metric"
response1 = rq.get(url)
data1 = response1.json()
local_zone = data1["timezone"]
#Create interactive form in streamlit
with st.form(key="weather_form"):
    city = st.text_input(label="Enter city name", key="city_input", label_visibility="collapsed") #התיבה מוצגת, אבל בלי כיתוב מעליה.
    submitted = st.form_submit_button("Get Weather")
    # if city entered in  textbox  and user push button
if submitted and city:
    result = get_weather(city)
    if result:
        #חלוקת המסך לתצוגה יפה של התוצאות
        left_col, right_col = st.columns([2, 1])
        #in the left print weathe data
        with left_col:
            # local time print only if different from requested city timezone
            if local_zone != result["timezone_offset_sec"]:
               user_timezone = pytz.timezone("Asia/Jerusalem")
               user_time = datetime.now(user_timezone)
               formatted_user_time = user_time.strftime("%A, %B %d, %Y, %I:%M %p")
               st.write(f"🕒User Time: {formatted_user_time}")
            st.write(f"### Weather in {result['city']}")
            st.write(f"Temperature: {int(result['temperature'])}°C")
            icon = get_weather_icon(result['weather'])
            st.write(f"Condition: {icon} {result['weather']}")
            st.write(f"Humidity: {int(result['humidity'])}%")
            utc_now = datetime.utcnow()
            local_time = utc_now + timedelta(seconds=result["timezone_offset_sec"])
            formatted_time = local_time.strftime("%A, %B %d, %Y, %I:%M %p")
            st.write(f"🌍 weather Location Time: {formatted_time}")
        #print map in the right
        with right_col:
            lat = result["latitude"]
            lon = result["longitude"]
            st.write("🗺️ Map of Location:")
            m = folium.Map(location=[lat, lon], zoom_start=8)
            folium.Marker([lat, lon], tooltip=result['city']).add_to(m)
            #folium_static(m)
            folium_static(m, width=200, height=200)
# history avg data to graph
        history = get_monthly_avg_temps(result["latitude"], result["longitude"])
        plot_temp_history(history)
    else:
        st.error("City not found.")
