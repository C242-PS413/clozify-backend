from fastapi import APIRouter, Depends, HTTPException
from google.cloud.firestore_v1 import Client as FirestoreClient
from typing import List
from pydantic import BaseModel
from ...core.firebase_config import get_db
from ...services.outfit_service import OutfitService

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)

@router.post("/migrate/{user_id}")
async def migrate_mood_data_to_recommendations(
    user_id: str,
    db: FirestoreClient = Depends(get_db)
):
    return await OutfitService.migrate_mood_data_to_recommendations(user_id, db)
