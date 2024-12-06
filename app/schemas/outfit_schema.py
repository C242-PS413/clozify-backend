from pydantic import BaseModel
from typing import Any

class OutfitRecommendationRequest(BaseModel):
    id: str
    outfit: str
    mood: str
    weather: str
    gender: str

class OutfitRecommendationResponse(BaseModel):
    id: str
    outfit: str
    mood: str
    weather: str
    gender: str
