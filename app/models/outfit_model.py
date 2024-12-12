from typing import List
from dataclasses import dataclass

@dataclass
class MoodData:
    user_id: str
    predicted_mood: str
    gender: str
    weather: List[str]
    file_url: str

    def transform_weather(self) -> List[str]:
        return [
            'Rainy' if w == 'rain' else 
            'Sunny' if w == 'summer' else 
            w 
            for w in self.weather
        ]

from google.cloud import firestore

class OutfitModel:
    def __init__(self):
        self.db = firestore.Client()
        self.collection_name = "outfit"

    def save_recommendations(self, user_id: str, recommendations: dict):
        document_ref = self.db.collection(self.collection_name).document(user_id)
        document_ref.set(recommendations)
