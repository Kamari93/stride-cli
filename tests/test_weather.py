import pytest
import requests
from unittest.mock import Mock, patch
from app.models import Weather
from app.weather import WeatherProvider, Weather_Service, OpenMeteoProvider

class FakeWeatherProvider(WeatherProvider):
    '''Fake provider used for testing.'''

    def get_weather(self, city: str) -> Weather:
        return Weather (
            city = city,
            country = "United States",
            temperature = 75.0,
            feels_like = 77.0,
            conditions = "Sunny",
            wind_speed = 8.0,
            precipitation_probability = 10.0,
        )

def test_weather_service_returns_weather():
    '''Weather Service should retrieve data from provider given city name'''
    provider = FakeWeatherProvider()
    service = Weather_Service(provider)

    weather = service.get_weather("Austin")

    assert weather.city == "Austin"
    assert weather.country == "United States"
    assert weather.temperature == 75.0
    assert weather.conditions == "Sunny"


def test_weather_service_rejects_empty_city():
    '''Weather Service should reject empty city and raise Value Error'''
    provider = FakeWeatherProvider()
    service = Weather_Service(provider)

    with pytest.raises(ValueError, match="City cannot be empty."):
        service.get_weather(" ")

'''
unittest.mock is Python's built-in library for isolating systems under test by replacing production code components 
with mock objects. It allows you to simulate external dependencies (like APIs, databases, or file systems), 
define specific behavior for them, and assert exactly how your code interacted with them.
'''

'''
The unittest.mock.patch utility in Python is used to temporarily replace parts of your system under test with Mock 
objects. It is primarily used during unit testing to isolate the code being tested from external dependencies 
(such as APIs, databases, or filesystem operations)
'''
@patch("app.weather.requests.get") # my_module.external_api_call
def test_open_meteo_provider_returns_weather(mock_get):
    geocoding_response = Mock()
    # Configure the mock's return value
    geocoding_response.json.return_value = {
        "results": [
            {
                "name": "Austin",
                "country": "United States",
                "latitude": 30.2672,
                "longitude": -97.7431,
            }
        ]
    }

    weather_response = Mock()
    weather_response.json.return_value = {
        "current": {
            "temperature_2m": 75.0,
            "apparent_temperature": 77.0,
            "weather_code": 0,
            "wind_speed_10m": 8.0,
        },
        "hourly": {
            "precipitation_probability": [10]
        },
    }

    mock_get.side_effect = [geocoding_response, weather_response]

    provider = OpenMeteoProvider()

    weather = provider.get_weather("Austin")

    assert isinstance(weather, Weather)
    assert weather.city == "Austin"
    assert weather.country == "United States"
    assert weather.temperature == 75.0
    assert weather.feels_like == 77.0
    assert weather.conditions == "Clear sky"
    assert weather.wind_speed == 8.0
    assert weather.precipitation_probability == 10


@patch("app.weather.requests.get") # my_module.external_api_call
def test_open_meteo_provider_rejects_unknown_city(mock_get):
    response = Mock()
    response.json.return_value = {"results": []}

    mock_get.return_value = response
    provider = OpenMeteoProvider()
    
    with pytest.raises(ValueError, match="City not found"):
        provider.get_weather("Fake City")


@patch("app.weather.requests.get") # my_module.external_api_call
def test_open_meteo_provider_handles_connection_error(mock_get):
    '''Open Meteo provider should properly handle connection failures'''
    mock_get.side_effect = requests.ConnectionError()

    provider = OpenMeteoProvider()

    with pytest.raises(ConnectionError, match="Unable to connect to the weather service."):
        provider.get_weather("Austin")


@patch("app.weather.requests.get") # my_module.external_api_call
def test_open_meteo_provider_handles_http_error(mock_get):
    '''Open Meteo should properly handle HTTP failures'''
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError()

    mock_get.return_value = response
    provider = OpenMeteoProvider()

    with pytest.raises(ConnectionError, match="Unable to connect to the weather service."):
        provider.get_weather("Austin")

@patch("app.weather.requests.get") # my_module.external_api_call
def test_open_meteo_provider_handles_malformed_response(mock_get):
    '''Test malformed API responses; Testing API response that technically succeeds but contains unexpected/missing data'''
    geocoding_response = Mock()
    geocoding_response.json.return_value = {
        "results": [
            {
                "name": "Austin",
                "country": "United States",
                "latitude": 30.2672,
                "longitude": -97.7431,
            }
        ]
    }
    weather_response = Mock()
    weather_response.json.return_value = {
        "current": {},
    }

    mock_get.side_effect = [geocoding_response, weather_response]

    provider = OpenMeteoProvider()

    with pytest.raises(ConnectionError, match="Invalid weather data received."):
        provider.get_weather("Austin")
    

@patch("app.weather.requests.get") # my_module.external_api_call
def test_open_meteo_provider_handles_malformed_geocoding_response(mock_get):
    '''Test malformed API responses for incomplete geocoding response for city look-up'''
    geocoding_reponse = Mock()
    geocoding_reponse.json.return_value = {
        "results": [
            {
                "name": "Austin",
                #Latitude and Longitude missing
            }
        ]
    }

    provider = OpenMeteoProvider()

    with pytest.raises(ConnectionError, match="Invalid location data received."):
        provider.get_weather("Austin")

def test_weather_code_to_description():
    provider = OpenMeteoProvider()

    assert provider._weather_code_to_description(0) == "Clear sky"
    assert provider._weather_code_to_description(3) == "Overcast"
    assert provider._weather_code_to_description(45) == "Fog"
    assert provider._weather_code_to_description(61) == "Slight rain"
    assert provider._weather_code_to_description(85) == "Slight snow showers"
    assert provider._weather_code_to_description(95) == "Thunderstorm"

def test_unknown_weather_code_returns_unkown():
    provider = OpenMeteoProvider()

    assert provider._weather_code_to_description(999) == "Unknown"

if __name__ == "__main__":
    pytest.main([__file__])