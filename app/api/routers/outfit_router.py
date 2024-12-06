from fastapi import APIRouter, Depends, HTTPException
from ...services.outfit_service import OutfitService, OutfitModel
from ...schemas.outfit_schema import OutfitRecommendationResponse
from google.cloud.firestore import Client
from ...core.firebase_config import get_db

router = APIRouter(
    prefix="/outfit",
    tags=["outfit"]
)

@router.get("/recommendations", response_model=OutfitRecommendationResponse)
async def get_outfit_recommendation(user_id: str, db: Client = Depends(get_db)):
    try:
        return OutfitService.get_outfit(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")




