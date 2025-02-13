import requests
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
from datetime import datetime

# API Key
API_KEY = "f8b58435a5d7caa37f0ab596ce623b13"

# Function to fetch and display weather
def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        daily_forecast = defaultdict(list)

        for entry in data['list']:
            date = datetime.fromtimestamp(entry['dt']).strftime('%A %d')
            suffix = "th" if 11 <= int(date[-2:]) <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(int(date[-1]), "th")
            date += suffix  # Append correct suffix

            temperature = entry['main']['temp']
            max_temperature = entry['main']['temp_max']
            min_temperature = entry['main']['temp_min']
            wind = entry['wind']['speed']
            description = entry['weather'][0]['description']
            feels_like = entry['main']['feels_like']
            pressure = entry['main']['pressure']
            humidity = entry['main']['humidity']
            weather_id = entry['weather'][0]['id']

            daily_forecast[date].append({
                "temp": temperature,
                "id": weather_id,
                "temp_min": min_temperature,
                "temp_max": max_temperature,
                "humidity": humidity,
                "wind_speed": wind,
                "description": description,
                "feels_like": feels_like,
                "pressure": pressure,
            })

        def get_weather_emoji(weather_id):
            if 200 <= weather_id <= 232:
                return "⛈"
            elif 300 <= weather_id <= 321:
                return "🌦"
            elif 500 <= weather_id <= 531:
                return "🌧"
            elif 600 <= weather_id <= 622:
                return "❄"
            elif 701 <= weather_id <= 741:
                return "🌫"
            elif weather_id == 762:
                return "🌋"
            elif weather_id == 771:
                return "💨"
            elif weather_id == 781:
                return "🌪"
            elif weather_id == 800:
                return "☀"
            elif 801 <= weather_id <= 804:
                return "☁"
            else:
                return "❓"

        weather_label.config(text=f"Weather forecast for {city}:")

        forecast_text = ""
        for date, forecasts in daily_forecast.items():
            forecast_text += f"\n{date}:\n"
            for entry in forecasts[:1]:
                emoji = get_weather_emoji(entry['id'])
                forecast_text += (
                    f"Temp:{entry['temp']}°C {emoji} \n"
                    f"Max: {entry['temp_max']}°C, Min: {entry['temp_min']}°C\n"
                    f"Wind: {entry['wind_speed']}m/s, Pressure: {entry['pressure']} hPa\n"
                    f"Humidity: {entry['humidity']}%, Feels Like: {entry['feels_like']}°C\n"
                    f"Description: {entry['description'].capitalize()}\n\n"
                )

        forecast_label.config(text=forecast_text)

    else:
        messagebox.showerror("Error", "City not found!")

# GUI Setup
root = tk.Tk()
root.title("Weather Search")

tk.Label(root, text="Enter City:").pack(pady=5)
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=get_weather)
search_button.pack(pady=5)

weather_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
weather_label.pack(pady=10)

forecast_label = tk.Label(root, text="", justify="left", font=("Arial", 10))
forecast_label.pack(pady=10)

root.mainloop()
