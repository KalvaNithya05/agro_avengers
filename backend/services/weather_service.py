import requests
import os
import random

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_current_weather(self, city="Hyderabad"):
        """
        Fetches current weather for the location.
        Returns dict with temp, humidity, rainfall (estimated).
        """
        if not self.api_key:
            # print("Weather API Key not found. Using Mock.")
            return self._mock_weather()
            
        try:
            params = {
                'q': city, 
                'appid': self.api_key, 
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                # OpenWeatherMap returns rain in 'rain.1h' or 'rain.3h' mm
                rainfall = 0
                if 'rain' in data:
                    rainfall = data['rain'].get('1h', 0)
                
                return {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'rainfall': rainfall * 24 # Crude estimate for daily total if raining
                }
            else:
                return self._mock_weather()
        except Exception as e:
            print(f"Weather API Error: {e}")
            return self._mock_weather()

    def _mock_weather(self):
        """
        Returns random realistic weather data.
        """
        return { 
            'temperature': round(random.uniform(25.0, 35.0), 1),
            'humidity': round(random.uniform(40.0, 80.0), 1),
            'rainfall': round(random.choice([0, 0, 0, 10, 50]), 1) # Mostly dry, sometimes rain
        }
