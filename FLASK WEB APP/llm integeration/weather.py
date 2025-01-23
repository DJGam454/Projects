import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("weather_api_key")

def get_weather_data(city, state):
    """Fetch the current temperature and humidity for a city and state."""
    try:
        query = f"{city},{state}"
        url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={query}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        temp_c = data.get('current', {}).get('temp_c', 'N/A')
        humidity = data.get('current', {}).get('humidity', 'N/A')

        return {
            "temp": temp_c,
            "humidity": humidity
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
