import requests
import subprocess
from datetime import datetime
from config import API_KEY

def calculate_feels_like(temperature, humidity, wind_speed):
    # Simple formula for demonstration purposes
    feels_like = temperature - ((100 - humidity) / 5) + (wind_speed**0.7)
    return round(feels_like, 2)

def fetch_weather(api_key, locality_id):
    base_url = "https://www.weatherunion.com/gw/weather/external/v0/get_locality_weather_data"
    headers = {
        "content-type": "application/json",
        "x-zomato-api-key": api_key
    }
    params = {"locality_id": locality_id}
    
    response = requests.get(base_url, headers=headers, params=params)
    weather_data = response.json().get('locality_weather_data', {})
    if weather_data:
        weather_data['Feels like'] = calculate_feels_like(
            weather_data.get('temperature', 0),
            weather_data.get('humidity', 0),
            weather_data.get('wind_speed', 0)
        )
    return weather_data

def send_desktop_notification(title, text):
    apple_script = f'display notification "{text}" with title "{title}" sound name "Submarine"'
    subprocess.run(["osascript", "-e", apple_script])

def format_weather_notification(weather_data, request_time):
    title = "Kora weather"
    temperature = weather_data.get('temperature', 0)
    feels_like = weather_data.get('Feels like', 0)
    rain_intensity = weather_data.get('rain_intensity', 0)
    
    body = f"Time: {request_time.strftime('%H:%M')} | Temp: {temperature}°C, Feels like: {feels_like}°C | Rain: {rain_intensity}mm/min"
    return title, body

# Usage
locality_id = "ZWL001156"
weather = fetch_weather(API_KEY, locality_id)
current_time = datetime.now()
title, body = format_weather_notification(weather, current_time)
send_desktop_notification(title, body)