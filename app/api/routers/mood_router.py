from fastapi import APIRouter, Depends, HTTPException
from ...core.database import get_db
from ...schemas.mood_schema import MoodInput, MoodOutput
from google.cloud.firestore import Client, SERVER_TIMESTAMP

db = get_db

router = APIRouter(
    prefix="/mood",
    tags=["Mood"]
)

"""
MOOD_MAPPING = {
    1: "Joy",
    2: "Contentment",
    3: "Neutral",
    4: "Fear",
    5: "Sadness",
    6: "Anger"
}
"""

@router.post("/", response_model=MoodOutput)
async def create_mood(mood_input: MoodInput, db: Client = Depends(get_db)):
    if mood_input.mood not in range(1, 7):
        raise HTTPException(status_code=400, detail="Invalid mood value. Must be between 1 and 6.")
    
    # Create Firestore document
    mood_data = MoodOutput(
        user_id=str(mood_input.user_id),
        mood=mood_input.mood
    )

    # Save data to firestore
    try:
        doc_ref = db.collection("moods").document(mood_data.user_id)
        doc_ref.set(mood_data.model_dump())
        return mood_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save mood data: {str(e)}")