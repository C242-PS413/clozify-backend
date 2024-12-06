import os 
import httpx
from dotenv import load_dotenv
from ..core.firebase_config import get_db
from google.cloud.firestore import Client
from fastapi import Depends
from ..models.weather_model import Weather
from ..schemas.weather_schema import WeatherResponse


load_dotenv()

async def get_weather_from_api(city: str) -> dict:
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")

    if not api_key or not base_url:
        raise EnvironmentError("API_KEY or BASE_URL not found")
    
    url = f"{base_url}/{city}?unitGroup=us&key={api_key}&contentType=json"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to get weather data: {response.status_code}")
    
    data = response.json()
    
    if "days" in data and len(data["days"]) > 0:
        day_data = data["days"][0]

        # API using Celsius convert to Celcius
        temp_fahrenheit = day_data.get("temp", 0)
        temp_celsius = (temp_fahrenheit - 32) * 5 / 9

        # Create WeatherResponse object
        return WeatherResponse(
            city=data.get("resolvedAddress", "Unknown"),
            temp=round(temp_celsius, 2),
            preciptype=day_data.get("preciptype", []),
            resolvedAddress=data.get("resolvedAddress", "Unknown"),
        )
    else:
        raise Exception("No weather data found for the city.")

def save_weather_to_firestore(weather: dict, db: Client = Depends(get_db)):
    weather_ref = db.collection("weather").document(weather["city"])
    weather_ref.set(weather)


def get_weather_from_firestore(city: str, db: Client):
    """Retrieve weather data from Firestore."""
    weather_ref = db.collection("weather").document(city)
    snapshot = weather_ref.get()
    if snapshot.exists:
        return Weather.from_dict(snapshot.to_dict())
    return None