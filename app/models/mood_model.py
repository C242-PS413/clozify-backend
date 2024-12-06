from pydantic import BaseModel, model_validator, UUID4
from ..schemas.mood_schema import MoodEnum, WeatherEnum, GenderEnum
from typing import Any

# Model MoodInput
class MoodInput(BaseModel):
    user_id: UUID4
    mood: MoodEnum
    weather: WeatherEnum
    gender: GenderEnum

    @model_validator(mode='before')
    @classmethod
    def validate_user_id(cls, data: Any) -> Any:
        if not all(key in data for key in ["user_id", "gender", "weather"]):
            raise ValueError("user_id, weather, and gender are required.")

        try:
            UUID4(str(data["user_id"]))
        except ValueError:
            raise ValueError("Invalid UUID format for user_id.")
        
        if data["gender"] not in ["male", "female"]:
            raise ValueError("Invalid gender. Must be 'male', 'female'.")
        
        return data

    @model_validator(mode='after')
    def check_validate_match(self) -> "MoodInput":
        if not self.user_id and not self.gender:
            raise ValueError("user_id must not be empty.")
        if self.mood not in ["joy", "contentment", "neutral", "fear", "sadness", "anger"]:
            raise ValueError("Mood must joy, contentment, neutral, fear, sadness, anger")
        
        return self