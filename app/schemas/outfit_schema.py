from pydantic import BaseModel
from typing import List

class RecommendationItem(BaseModel):
    image: str
    name: str

class CategoryRecommendation(BaseModel):
    recommendations_item: RecommendationItem
    more_recommended_items: List[RecommendationItem]

class CategorySection(BaseModel):
    recommendations: List[CategoryRecommendation]

class OutfitRecommendationInput(BaseModel):
    gender: str
    season: str
    emotion_category: str

class OutfitRecommendationResponse(BaseModel):
    TopWear: CategorySection
    Bottomwear: CategorySection
    Footwear: CategorySection

class MoodDataInput(BaseModel):
    user_id: str
    predicted_mood: str
    gender: str
    weather: List[str]
    file_url: str

class RecommendationItem(BaseModel):
    image: str
    name: str

class Recommendation(BaseModel):
    recommendations_item: RecommendationItem
    more_recommended_items: List[RecommendationItem]

class OutfitCategory(BaseModel):
    recommendations: List[Recommendation]

class OutfitRecommendation(BaseModel):
    TopWear: OutfitCategory
    Bottomwear: OutfitCategory
    Footwear: OutfitCategory