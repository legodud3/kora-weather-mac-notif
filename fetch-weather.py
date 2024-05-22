import requests
import subprocess
from datetime import datetime
import google.generativeai as genai
from config import weatherunion_api_key
from config import GOOGLE_API_KEY


def calculate_feels_like(temperature, humidity, wind_speed):
    if temperature is None or humidity is None or wind_speed is None:
        return None

    feels_like = temperature - ((100 - humidity) / 5) + (wind_speed**0.7)
    return round(feels_like, 1)


def fetch_weather(api_key, locality_id):
    base_url = "https://www.weatherunion.com/gw/weather/external/v0/get_locality_weather_data"
    headers = {
        "content-type": "application/json",
        "x-zomato-api-key": api_key,
    }
    params = {"locality_id": locality_id}

    response = requests.get(base_url, headers=headers, params=params)
    weather_data = response.json().get("locality_weather_data", {})
    if weather_data:
        weather_data["Feels like"] = calculate_feels_like(
            weather_data.get("temperature", 0),
            weather_data.get("humidity", 0),
            weather_data.get("wind_speed", 0),
        )
    return weather_data


def send_desktop_notification(title, text):
    apple_script = f'display notification "{text}" with title "{title}" sound name "Submarine"'
    subprocess.run(["osascript", "-e", apple_script])


def format_weather_notification(weather_data, request_time):
    if weather_data is None:
        return "Weather data is unavailable", ""

    else:
        temperature = weather_data.get("temperature", 0)
        summary = weather_data.get("summary", "")
        rain = weather_data.get("rain", 0)

        notification_message = f"Temp: {round(temperature,0)}°C. Rain: {round(rain,0)}. Summary: {summary}"  # Corrected
        title = "Weather Update"

        prompt = f"{weather}\n{weather_data}"
        response = chat_session.send_message(prompt)
        message = response.text

    return title, f"{notification_message}\n\n{message}" if message else notification_message


genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name = "gemini-1.5-flash-latest",
  generation_config = generation_config,
  safety_settings = None,
  system_instruction = "Become one of the following star wars characters: Darth Vader, Count Dooku, Emperor Palpatine, Darth Maul, General Grievous. I will give you the weather data as a json. Respond with your opinion on it in 15 words or less.",
)

chat_session = model.start_chat(history=[])


#usage
locality_id = "ZWL001156"
weather = fetch_weather(weatherunion_api_key, locality_id)
current_time = datetime.now()
title, message = format_weather_notification(weather, current_time)
send_desktop_notification(title, message)