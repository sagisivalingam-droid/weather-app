import urllib.request
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

API_KEY = "c5757b4baa0cf9425b2d90009f16c9f3"

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "City name type pannu da!")
        return

    # Current weather URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    # 5-day forecast URL
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        # 1. Current Weather
        with urllib.request.urlopen(url) as res:
            data = json.loads(res.read().decode())
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        result_label.config(text=f"{city.title()} - Ippo:\n{temp}°C, {desc}\nHumidity: {humidity}%")

        # 2. 5-Day Forecast
        with urllib.request.urlopen(forecast_url) as res:
            f_data = json.loads(res.read().decode())

        # Forecast list ah clear pannidu
        forecast_list.delete(0, tk.END)

        seen_days = []
        for item in f_data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime("%a, %d %b")
            if date not in seen_days:
                seen_days.append(date)
                f_temp = item['main']['temp']
                f_desc = item['weather'][0]['description']
                forecast_list.insert(tk.END, f"{date} : {f_temp}°C, {f_desc}")
                if len(seen_days) == 5:
                    break

        if len(seen_days) == 0:
            forecast_list.insert(tk.END, "Forecast data not found")

    except Exception as e:
        messagebox.showerror("Error", "Wrong city name! Check and try again")
        print(e)

window = tk.Tk()
window.title("Weather App v2 - Sagirtha")
window.geometry("380x480")

tk.Label(window, text="City Name:", font=("Arial", 12, "bold")).pack(pady=10)
city_entry = tk.Entry(window, font=("Arial", 12), justify="center")
city_entry.pack(pady=5)

tk.Button(window, text="Get Weather + 5-Day Forecast", command=get_weather, font=("Arial", 11, "bold"), bg="#38bdf8").pack(pady=10)

result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack(pady=10)

tk.Label(window, text="📅 Next 5 Days Forecast:", font=("Arial", 11, "bold")).pack(pady=5)

forecast_list = tk.Listbox(window, font=("Arial", 11), width=45, height=8)
forecast_list.pack(pady=5)

window.mainloop()