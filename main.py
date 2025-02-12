import requests
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
from datetime import datetime
from PIL import Image, ImageTk  # For displaying weather icons
import io

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
        icons = []

        for entry in data['list']:
            date = datetime.fromtimestamp(entry['dt']).strftime('%A %d')  # "Friday 13"
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
            icon = entry['weather'][0]['icon']

            daily_forecast[date].append({
                "temp": temperature,
                "temp_min": min_temperature,
                "temp_max": max_temperature,
                "humidity": humidity,
                "wind_speed": wind,
                "description": description,
                "feels_like": feels_like,
                "pressure": pressure,
                "icon": icon
            })
            icons.append(icon)

        weather_label.config(text=f"Weather forecast for {city}:")

        forecast_text = ""
        for date, forecasts in daily_forecast.items():
            forecast_text += f"\n{date}:\n"
            for entry in forecasts[:1]:
                forecast_text += (
                    f"Temp: {entry['temp']}°C\n"
                    f"Max: {entry['temp_max']}°C, Min: {entry['temp_min']}°C\n"
                    f"Wind: {entry['wind_speed']}m/s, Pressure: {entry['pressure']} hPa\n"
                    f"Humidity: {entry['humidity']}%, Feels Like: {entry['feels_like']}°C\n"
                    f"Description: {entry['description'].capitalize()}\n\n"
                )

        forecast_label.config(text=forecast_text)
        display_icons(icons)

    else:
        messagebox.showerror("Error", "City not found!")


# Function to fetch and display weather icons
def display_icons(icons):
    global icon_images  # Store references to prevent garbage collection
    icon_images = []

    # Clear the previous icons
    for widget in icon_frame.winfo_children():
        widget.destroy()

    # Fetch and display new icons
    for icon_code in icons:
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(icon_url)

        if response.status_code == 200:
            image_data = io.BytesIO(response.content)
            img = Image.open(image_data)
            img = img.resize((50, 50))  # Resize image
            icon_photo = ImageTk.PhotoImage(img)
            icon_images.append(icon_photo)  # Store reference

            icon_label = tk.Label(icon_frame, image=icon_photo)
            icon_label.pack(side=tk.LEFT, padx=5)

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

# Frame to hold weather icons
icon_frame = tk.Frame(root)
icon_frame.pack(pady=10)

root.mainloop()
