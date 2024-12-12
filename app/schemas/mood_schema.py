from pydantic import BaseModel, UUID4
from enum import Enum
from typing import List

class ImageMoodEnum(str, Enum):
    IMAGE = "image"

class WeatherEnum(str, Enum):
    SUMMER = "Sunny"
    RAINY = "Rainy"


class GenderEnum(str, Enum):
    MALE = "Men"
    FEMALE = "Women"


class MoodInput(BaseModel):
    user_id: UUID4
    picture_mood: ImageMoodEnum
    gender: GenderEnum

    
class MoodOutput(BaseModel):
    user_id: UUID4
    gender: str
    weather: List[str]
    file_url: str
    city: str
    predicted_mood: str
    timestamp: str
