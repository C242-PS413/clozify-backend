from pydantic import BaseModel, Field, UUID4
from datetime import datetime, timezone
from enum import Enum

class MoodEnum(str, Enum):
    JOY = "joy"
    CONTENTMENT = "contentment"
    NEUTRAL = "neutral"
    SADNESS = "sadness"
    ANGER = "anger"


class WeatherEnum(str, Enum):
    SUMMER = "summer"
    RAINY = "rainy"


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class MoodInput(BaseModel):
    user_id: UUID4
    mood: MoodEnum
    weather: WeatherEnum
    gender: GenderEnum

    
class MoodOutput(BaseModel):
    user_id: UUID4
    mood: str
    weather: str
    gender: str
    file_url: str = None
    timestamp: int = Field(default_factory=lambda: int(datetime.now(timezone.utc).timestamp()))
    

class DeleteMoodResponse(BaseModel):
    message: str