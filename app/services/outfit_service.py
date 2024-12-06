from ..models.outfit_model import OutfitModel
from ..schemas.outfit_schema import OutfitRecommendationRequest, OutfitRecommendationResponse
from ..core.firebase_config import get_db
from google.cloud import firestore
from firebase_admin import firestore
from google.cloud.firestore import Client
from pydantic import UUID4
from fastapi import HTTPException, status

db = get_db

class OutfitService:
    def get_outfit(user_id: UUID4, db: Client):
        doc_ref = db.collection("outfit").document(str(user_id))
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="outfit recommendation not found.")
        
        #data = doc.to_dict()
        return OutfitRecommendationResponse(**doc.to_dict())