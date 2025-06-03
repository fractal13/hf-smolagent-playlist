#!/usr/bin/env python3
"""Weather related tools accessing openweathermap.

- GeocodeTool: translates city,state,country into a latitude,longitude
- WeatherInfoTool: translates latitude,longitude into current weather
"""

from smolagents import Tool
import random

# https://openweathermap.org/api/geocoding-api
class GeocodeTool(Tool):
    name = "geocode"
    description = "Given a string describing a location, return the latitude and longitude, as comma separated values."
    inputs = {
        "location": {
            "type": "string",
            "description": "The location to get weather information for. City, State, Country"
        }
    }
    output_type = "string"

    def forward(self, location: str):
        import dotenv
        import os
        dotenv.load_dotenv()

        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        import requests
        limit = 1
        api_url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit={limit}&appid={api_key}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return f"{data[0].get("lat")},{data[0].get("lon")}"
        else:
            return f"Error: Unable to fetch geocode data. {response} API key: {api_key} url: {api_url}"



# https://openweathermap.org/current#one
class WeatherInfoTool(Tool):
    name = "weather_info"
    description = "Fetches dummy weather information for a given location."
    inputs = {
        "location": {
            "type": "string",
            "description": "The latitude and longitude of the location, as a comma separated string."
        }
    }
    output_type = "string"

    def forward(self, location: str):
        import dotenv
        import os
        dotenv.load_dotenv()

        lat, lon = location.split(",")

        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        import requests
        #api_url = f"https://api.weather.com/v1/location/{location}?apiKey={api_key}"
        api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return [ data.get("weather")[0], data.get("main") ]
        else:
            return f"Error: Unable to fetch weather data. {response} API key: {api_key} url: {api_url}"

    def fake_forward(self, location: str):
        # Dummy weather data
        weather_conditions = [
            {"condition": "Rainy", "temp_c": 15},
            {"condition": "Clear", "temp_c": 25},
            {"condition": "Windy", "temp_c": 20}
        ]
        # Randomly select a weather condition
        data = random.choice(weather_conditions)
        return f"Weather in {location}: {data['condition']}, {data['temp_c']}°C"

if __name__ == "__main__":
    # Initialize the tool
    geocode_tool = GeocodeTool()
    weather_info_tool = WeatherInfoTool()
    print(weather_info_tool(geocode_tool("St. George, Utah, US")))
