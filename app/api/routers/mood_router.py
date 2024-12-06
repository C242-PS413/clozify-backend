from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form, Depends
from ...core.firebase_config import get_db
from ...models.mood_model import MoodInput
from ...schemas.mood_schema import MoodOutput, DeleteMoodResponse
from ...services.mood_service import MoodService
from google.cloud.firestore import Client
from pydantic import UUID4

db = get_db

router = APIRouter(
    prefix="/mood",
    tags=["Mood"]
)


@router.post("/upload", response_model=dict)
async def upload_photo(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    db: Client = Depends(get_db)
):
    try:
        mood_service = MoodService(db=db)
        file_url = await mood_service.upload_mood_photo(user_id=user_id, file=file)
        return {"message": "File uploaded successfully", "file_url": file_url}
    except HTTPException as e:
        raise e


@router.delete("/upload", response_model=dict)
async def delete_photo(
    user_id: UUID4,
    file_name: str,
    db: Client = Depends(get_db)
):
    try:
        mood_service = MoodService(db=db)
        response = await mood_service.delete_mood_photo(user_id=user_id, file_name=file_name)
        return response
    except HTTPException as e:
        raise e


@router.post("/", response_model=MoodOutput)
async def create_mood(mood_input: MoodInput, db: Client = Depends(get_db)):
    return MoodService.create_mood(mood_input, db)


@router.get("/{user_id}", response_model=MoodOutput)
async def get_mood(user_id: str, db: Client = Depends(get_db)):
    return MoodService.get_mood(user_id, db)


@router.put("/{user_id}", response_model=MoodOutput)
async def update_mood(
    user_id: UUID4,
    mood_data: MoodInput,
    db: Client = Depends(get_db),
):
    try:
        updated_mood = MoodService.update_mood(user_id, mood_data, db)
        return updated_mood
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )


@router.delete("/{user_id}", response_model=DeleteMoodResponse)
async def delete_user_mood(user_id: UUID4, db: Client = Depends(get_db)):
    try:
        message = MoodService.delete_mood(user_id, db)
        return DeleteMoodResponse(message=message)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )
