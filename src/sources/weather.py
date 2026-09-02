import requests as req
from src.config import load_config
from datetime import datetime, timedelta
from src.storage.postgres import WeatherTable
import os
from dotenv import load_dotenv
load_dotenv()
class Weather_info:
    def __init__(self):
        self.API_Key = os.getenv('OPENWEATHER_API_KEY')
    def get_info(self, latitude, longitude):
        weather_response = req.get(f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={self.API_Key}")
        weather_json = weather_response.json()
        return self.extract_params(weather_json, latitude, longitude)
    def extract_params(self, dict, latitude, longitude):
        return{
            'time': datetime.fromtimestamp(dict['dt']).isoformat(),
            'longitude': longitude ,
            'latitude': latitude,
            'temperature': dict['main']['temp'],
            'wind_speed': dict['wind']['speed'],
        }
