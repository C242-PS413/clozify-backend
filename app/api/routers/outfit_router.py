from fastapi import APIRouter, Depends, HTTPException, status
from google.cloud.firestore_v1 import Client as FirestoreClient
from ...core.firebase_config import get_db
from ...services.outfit_service import OutfitService

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)

@router.post("/process/{user_id}")
async def process_mood_to_result_outfit(user_id: str, db: FirestoreClient = Depends(get_db)):
    """
    take data from moods, and migrate to recommendations, for call ML and save result in result_outfit.
    """
    try:
        #Migrate data from moods to recommendations
        recommendation_data = await OutfitService.migrate_mood_data_to_recommendations(user_id, db)

        #Call ML for recommendations outfit
        result_outfit = OutfitService.fetch_recommendations(recommendation_data)

        #Save result fetch_recommendations in firestore collection result_outfit
        result_doc_ref = db.collection("result_outfit").document(user_id)
        result_doc_ref.set(result_outfit)

        return {"message": "Process completed successfully", "result": result_outfit}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
