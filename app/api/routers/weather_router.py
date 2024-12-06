from fastapi import HTTPException, status, APIRouter, Depends
from ...core.firebase_config import get_db
from ...utils.cache import RedisCache
from ...services.weather_service import get_weather_from_api, save_weather_to_firestore, get_weather_from_firestore
from ...schemas.weather_schema import WeatherResponse
from google.cloud.firestore import Client

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)

redis_cache = RedisCache()

@router.get("/", response_model=WeatherResponse, status_code=status.HTTP_200_OK)
async def get_weather(city: str, db: Client = Depends(get_db)):
    cached_data = redis_cache.get(city)
    if cached_data:
        return {"city": city, "data": cached_data, "cached": True}

    # check firestore
    firestore_data = get_weather_from_firestore(city, db)
    if firestore_data:
        # save back to redis
        redis_cache.set(city, firestore_data.to_dict(), ttl=600)
        return {"city": city, **firestore_data.to_dict(), "cached": False}
    
    try:
        # get weather from API
        weather_data = await get_weather_from_api(city)
        weather_dict = weather_data.dict()

        # save data to cache and Firestore
        redis_cache.set(city, weather_dict, ttl=600)  # TTL 10 minutes
        save_weather_to_firestore(weather_dict, db)

        return {"city": city, **weather_dict, "cached": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    