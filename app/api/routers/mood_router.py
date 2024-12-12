from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends, status
from ...core.firebase_config import get_db
from ...schemas.mood_schema import MoodOutput
from ...services.mood_service import MoodService
from google.cloud.firestore import Client as StorageClient
from pydantic import UUID4

db = get_db

router = APIRouter(
    prefix="/mood",
    tags=["Mood"]
)



@router.post("/upload", response_model=dict)
async def upload_photo(
    user_id: str = Form(...),
    gender: str = Form(...),
    city: str = Form(...),
    file: UploadFile = File(...),
    db: StorageClient = Depends(get_db)
):
    if gender not in ["Men", "Women"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid gender value.")
    
    try:
        mood_service = MoodService(db=db)
        
        #Uploadphoto and get the file URL
        file_url = await mood_service.upload_mood_photo(user_id=user_id, gender=gender, file=file, city=city)

        #Call ML analysis and get the predicted mood
        predicted_mood = await mood_service.analyze_mood_with_ml(user_id=user_id, file_url=file_url, db=db)

        #Return the result to Firestore
        return {"message": "File uploaded and mood analyzed successfully", "file_url": file_url, "predicted_mood": predicted_mood}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {str(e)}")
    


@router.get("/{user_id}", response_model=MoodOutput)
async def get_mood(user_id: str, db: StorageClient = Depends(get_db)):
    return MoodService.get_mood(user_id, db)



@router.put("/upload/{user_id}")
async def update_mood(
    user_id: UUID4,
    gender: str = Form(...),
    file: UploadFile = File(...),
    db: StorageClient = Depends(get_db) 
):
    
    if gender not in ["Men", "Women"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid gender value.")
    
    try:
        mood_service = MoodService(db=db)
        updated_mood = await mood_service.update_mood(user_id, gender, file)

        return updated_mood

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")

    

@router.delete("/upload/{user_id}", response_model=dict)
async def delete_photo(
    user_id: UUID4,
    file_name: str,
    db: StorageClient = Depends(get_db)
):
    try:
        mood_service = MoodService(db=db)
        response = await mood_service.delete_mood_photo(user_id=user_id, file_name=file_name)
        return response
    except HTTPException as e:
        raise e





