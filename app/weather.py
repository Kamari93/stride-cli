from abc import ABC, abstractmethod # used to define a blueprint or a common interface for a group of subclasses. Any subclass that inherits from your abstract class must override and implement all abstract methods.
from app.models import Weather
import requests

'''Any weather provider Stride uses must know how to turn a city into a Weather object.'''

class WeatherProvider(ABC):
    '''Interface for retrieving weather data.'''
    @abstractmethod
    def get_weather(self, city: str) -> Weather:
        '''Return current weather for a city.'''
        raise NotImplementedError


class Weather_Service:
    '''Coordinates weather-related application logic.'''
    def __init__(self, provider: WeatherProvider) -> None:
        self.provider = provider

    def get_weather(self, city: str) -> Weather:
        '''Return current weather for a city.'''
        city = city.strip()

        if not city:
            raise ValueError("City cannot be empty.")

        return self.provider.get_weather(city)
    
class OpenMeteoProvider(WeatherProvider):
    '''Weather Provider using the Open-Meteo API.'''
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search" # convert city names into coordinates | accepts a search term and returns a list of matching locations
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, city: str) -> Weather:
        '''Return current weather for a city.'''
        '''Keep network-specific errors inside OpenMeteoProvider'''
        try:
            coordinates = self._get_coordinates(city)

            response = requests.get(self.WEATHER_URL, params={
                "latitude": coordinates["latitude"],
                "longitude": coordinates["longitude"],
                "current": (
                    "temperature_2m",
                    "apparent_temperature",
                    "weather_code",
                    "wind_speed_10m"

                ),
                "hourly": "precipitation_probability",
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "forecast_days": 1,
            },

            timeout=10,
            )

            response.raise_for_status()

        except requests.RequestException as exc:
            raise ConnectionError(
                "Unable to connect to the weather service."
            ) from exc

        data = response.json()

        try:
            """Ensure malformed API data is handled cleanly"""
            current = data["current"]
            precipitation_probability = data["hourly"]["precipitation_probability"][0]

            return Weather(
                city = coordinates["name"],
                country = coordinates["country"],
                temperature = current["temperature_2m"],
                feels_like = current["apparent_temperature"],
                conditions = self._weather_code_to_description(current["weather_code"]),
                wind_speed = current["wind_speed_10m"],
                precipitation_probability = precipitation_probability,
            )
        except (KeyError, TypeError, IndexError) as exc:
            raise ConnectionError(
                "Invalid weather data received."
            ) from exc

    def _get_coordinates(self, city: str) -> dict:
        '''Return coordinates for a city.'''
        '''Keep network-specific errors inside OpenMeteoProvider'''
        try:
            response = requests.get(self.GEOCODING_URL, params={
                "name": city,
                "count": 1,
                "format": "json",
                "language": "en"
            },
            timeout=10,
            )

            response.raise_for_status()

        except requests.RequestException as exc:
            raise ConnectionError(
                "Unable to connect to the weather service."
            ) from exc
        
        data = response.json()

        if not data.get("results"):
            raise ValueError(f"City not found: {city}")

        # return data["results"][0]
        '''validate geocoding return data'''
        try:
            result =  data["results"][0]

            if not all(key in result for key in ("name", "latitude", "longitude", "country")):
                raise KeyError

            return result
        
        except (KeyError, TypeError, IndexError) as exc:
            raise ConnectionError(
                "Invalid location data received."
                ) from exc


    def _weather_code_to_description(self, code: int) -> str:
        '''Convert an Open-Meteo weather code into a readable description.'''
        descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",

        }

        return descriptions.get(code, "Unknown")