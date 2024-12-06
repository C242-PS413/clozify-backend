from typing import Optional
from google.cloud.firestore import Client
from google.cloud import firestore
from fastapi import HTTPException, status
from ..schemas.mood_schema import MoodOutput
from ..models.mood_model import MoodInput
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import UUID4
from ..core.cloud_storage import StorageClient
from google.cloud.storage import Client as StorageClient


from dotenv import load_dotenv
load_dotenv()
import os

class MoodService:
    @staticmethod
    def check_existing_mood(user_id: UUID4, db: Client) -> bool:
        #Check if a mood for user_id already exists
        query = db.collection("moods").where(filter=FieldFilter("user_id", op_string="==", value=str(user_id)))
        docs = query.stream()

        return any(docs)

    def __init__(self, db: Client):
        self.storage_client = StorageClient()
        self.db = db

    async def upload_mood_photo(self, user_id: str, file) -> str:
        try:
            # Generate file name and upload to Cloud Storage
            file_name = f"{user_id}/{file.filename}"
            bucket = self.storage_client.bucket(os.getenv("BUCKET_NAME"))
            blob = bucket.blob(file_name)
            blob.upload_from_file(file.file, content_type=file.content_type)

            # Generate public URL
            file_url = blob.public_url

            # Save metadata to Firestore
            self.db.collection("moods").document(user_id).set({
                "file_url": file_url,
                "user_id": user_id,
                "timestamp": firestore.SERVER_TIMESTAMP,
            })

            return file_url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    async def delete_mood_photo(self, user_id: UUID4, file_name: str) -> dict:
        try:
            # Delete file from Cloud Storage
            blob_name = f"{user_id}/{file_name}"
            bucket = self.storage_client.bucket(os.getenv("BUCKET_NAME"))
            blob = bucket.blob(blob_name)
            if blob.exists():
                blob.delete()
            else:
                raise HTTPException(status_code=404, detail="File not found")

            # Remove entry from Firestore
            doc_ref = self.db.collection("moods").document(str(user_id))
            doc_ref.update({"file_url": firestore.DELETE_FIELD})

            return {"message": "File deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
    

    @staticmethod
    def create_mood(mood_input: MoodInput, db: Client) -> MoodOutput:
        # Check for existing mood data
        if MoodService.check_existing_mood(mood_input.user_id, db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mood data already exists for this user.")
        
        # Create Mood object
        mood_data = MoodInput(
            user_id=str(mood_input.user_id),
            mood=mood_input.mood,
            weather=mood_input.weather,
            gender=mood_input.gender,
        )
        
        # Prepare data for Firestore
        mood_data_dict = mood_data.model_dump()
        mood_data_dict['user_id'] = str(mood_data_dict['user_id'])
        
        try:
            # Save data to Firestore
            db.collection("moods").document(mood_data_dict['user_id']).set(mood_data_dict, merge=False)
            return MoodOutput(**mood_data_dict)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to save mood data: {str(e)}")


    @staticmethod
    def get_mood(user_id: UUID4, db: Client) -> Optional[MoodOutput]:
        """Retrieve mood data for a given user_id."""
        doc_ref = db.collection("moods").document(str(user_id))
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood data not found.")
        return MoodOutput(**doc.to_dict())
    

    @staticmethod
    def update_mood(user_id: UUID4, mood_data: MoodInput, db: Client) -> MoodOutput:
        user_id_str = str(user_id)

        query = db.collection("moods").where(filter=FieldFilter("user_id", "==", user_id_str)).stream()
        docs = list(query)

        if not docs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood data not found.")

        doc_ref = docs[0].reference
        doc_data = docs[0].to_dict()

        # validation
        if all(doc_data.get(key) == value for key, value in mood_data.model_dump().items()):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Data is already up-to-date.")

        # update doc
        updated_data = mood_data.model_dump()
        doc_ref.set(updated_data, merge=True)

        return MoodOutput(**updated_data)

        

    @staticmethod
    def delete_mood(user_id: UUID4, db: Client) -> str:
        user_id_str = str(user_id)
        query = db.collection("moods").where(filter=FieldFilter("user_id", "==", user_id_str)).stream()

        deleted_count = 0
        for doc in query:
            doc.reference.delete()
            deleted_count += 1

        if deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood data not found.")

        return f"{deleted_count} mood data(s) successfully deleted."

