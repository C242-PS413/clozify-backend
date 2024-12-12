
from typing import List, Dict
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form, Depends
from google.cloud.firestore_v1 import Client as FirestoreClient


class OutfitService:
    @staticmethod
    async def migrate_mood_data_to_recommendations(user_id: str, db: FirestoreClient):
        # Fetch data from `moods` collection
        doc_ref = db.collection('moods').document(user_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood data not found")
        
        mood_data = doc.to_dict()

        # Transform weather to season
        transformed_weather = (
            'Rainy' if mood_data["weather"][0] == 'rain' else
            'Sunny' if mood_data["weather"][0] == 'summer' else
            mood_data["weather"][0]
        )

        # Prepare recommendation data
        recommendation_data = {
            "gender": mood_data["gender"],
            "predicted_mood": mood_data["predicted_mood"],
            "season": transformed_weather,
        }

        # Save data in `recommendations`
        new_doc_ref = db.collection('recommendations').document(user_id)
        new_doc_ref.set(recommendation_data)

        return {"message": "Data migrated successfully to recommendations"}

