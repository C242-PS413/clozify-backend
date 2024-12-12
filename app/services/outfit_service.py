from fastapi import HTTPException, status
from google.cloud.firestore_v1 import Client as FirestoreClient
import requests
from dotenv import load_dotenv
import os


load_dotenv()


url = os.getenv("ML_OUTFIT_ENDPOINT")


class OutfitService:
    @staticmethod
    async def migrate_mood_data_to_recommendations(user_id: str, db: FirestoreClient) -> dict:
        """
        Take data from moods, transformation in recommendations, and return data to ML.
        """
        #Take data from moods
        doc_ref = db.collection("moods").document(user_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood data not found")

        mood_data = doc.to_dict()

        #Transform weather to season for ML
        transformed_weather = [
            "Rainy" if w == "rain" else
            "Sunny" if w == "summer" else w
            for w in mood_data.get("weather", [])
        ]
        season = transformed_weather[0] if transformed_weather else "Unknown"

        #Data for ML recommendations
        recommendation_data = {
            "gender": "Men" if mood_data["gender"].lower() == "male" else "Women",
            "emotion_category": mood_data["predicted_mood"],
            "season": season,
        }

        #Save data to collection recommendations
        new_doc_ref = db.collection("recommendations").document(user_id)
        new_doc_ref.set(recommendation_data)

        return recommendation_data

    @staticmethod
    def fetch_recommendations(payload: dict) -> dict:
        """
        send payload to endpoint ML for outfit recommendations.
        """
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ML service error: {str(e)}")
