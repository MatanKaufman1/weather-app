"""These modules are for calculate weather forecast using OpenMeteo API.
geopy : used in  WeatherUtility class
openmeteo_request : This ia an API client to get weather data from the Open-Meteo Weather API.
 used in class WeatherUtility
requests_cache : requests-cache is a persistent HTTP cache. used in class WeatherUtility:
pandas : use for 'def process_weather_data'
retry_requests : used in  WeatherUtility class
"""
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from exceptions import NoLocation, NoApiResponse, ErrorCalculate, ErrorProcessingData

class Forecast:
    """This class initiates parameters for daily forecast"""
    def __init__(self, date, day_temperature, night_temperature, humidity):
        self.date = date
        self.day_temperature = int(day_temperature)
        self.night_temperature = int(night_temperature)
        self.humidity = int(humidity)

    def to_dict(self):
        return {
            'date': self.date,
            'day_temperature': self.day_temperature,
            'night_temperature': self.night_temperature,
            'humidity': self.humidity
        }


class WeatherUtility:
    """Utility Class for handle location, weather data,
    process the weather data and calculate daily weather data """
    def __init__(self):
        self.geolocator = Nominatim(user_agent="app.py")
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo_req = openmeteo_requests.Client(session=self.retry_session)



    def get_location(self, city):
        """Expect city name enter by user, return its location using geolocator"""
        try:
            location = self.geolocator.geocode(city, language="en")
            return location
        except NoLocation as no_location:
            print(no_location)
            return None

    def get_weather_data(self, location):
        """Expect location, return api_responses filled with data by the chosen parameters"""
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "hourly": ["temperature_2m", "relative_humidity_2m", "is_day"],
            "timezone": "GMT"
        }
        try:
            responses = self.openmeteo_req.weather_api(url, params=params)
            if responses is None or responses[0] is None:
                return None
            api_response = responses[0]
            return api_response
        except NoApiResponse as no_api_respond:
            print(no_api_respond)
            return None

    def process_weather_data(self, api_response):
        """Expect api_response, return hourly_data"""
        try:
            hourly = api_response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
            hourly_is_day = hourly.Variables(2).ValuesAsNumpy()
            hourly_data = {"date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
                "temperature_2m": hourly_temperature_2m,
                "relative_humidity_2m": hourly_relative_humidity_2m,
                "is_day": hourly_is_day
            }

            return hourly_data

        except ErrorProcessingData as err_processing_data:
            print(err_processing_data)
            return None

    def calculate_weather(self, hourly_data):
        """Expect hourly_data, return list of weather calculated for a week"""
        weather_days = []
        try:
            for day in range(7):
                day_temp = 0
                night_temp = 0
                is_day_index = 0
                is_night_index = 0
                for hour in range(24):
                    idx = (day * 24) + hour
                    if hourly_data["is_day"][hour] == 1:
                        is_day_index += 1
                        day_temp += hourly_data["temperature_2m"][idx]
                    else:
                        night_temp += hourly_data["temperature_2m"][idx]
                        is_night_index += 1
                if is_night_index == 0:
                    avg_temp_nighttime = 0
                else:
                    avg_temp_nighttime = night_temp / is_night_index
                if is_day_index == 0:
                    avg_temp_daytime = 0
                else:
                    avg_temp_daytime = day_temp / is_day_index

                humidity = hourly_data["relative_humidity_2m"][day * 24]
                date = (datetime.today().date() + timedelta(days=day)).strftime("%Y-%m-%d")

                # Create a Forecast object and convert it to a dictionary
                forecast = Forecast(date, avg_temp_daytime, avg_temp_nighttime, humidity)
                weather_days.append(forecast.to_dict())

            return weather_days
        except ErrorCalculate as err_calculate:
            print(err_calculate)
            return None

