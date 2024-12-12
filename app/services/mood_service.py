from typing import Optional
from google.cloud.firestore import Client
from google.cloud import firestore
from fastapi import HTTPException, status
from ..schemas.mood_schema import MoodOutput
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import UUID4
from ..core.cloud_storage import StorageClient
from google.cloud.storage import Client as StorageClient
from datetime import datetime
from urllib.parse import urlparse
import httpx
import os
import httpx
import requests
from dotenv import load_dotenv


load_dotenv()


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


    async def upload_mood_photo(self, user_id: str, gender: str, file, city: str) -> str:
        try:
            #Check existing mood data
            mood_exists = self.check_existing_mood(user_id, self.db)
            if mood_exists:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood data already exists for this user.")

            #take weather from Firestore
            weather_ref = self.db.collection("weather").document(city)
            weather_doc = weather_ref.get()
            
            if not weather_doc.exists:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Weather data not found for the city.")
            
            weather_data = weather_doc.to_dict()
            weather_type = weather_data.get("preciptype", "Unknown")

            #upload and save
            file_name = f"{user_id}/{UUID4}/{file.filename}"
            bucket = self.storage_client.bucket(os.getenv("BUCKET_NAME"))
            blob = bucket.blob(file_name)
            blob.upload_from_file(file.file, content_type=file.content_type)

            #Generate public URL
            file_url = blob.public_url

            #Save metadata to Firestore
            mood_data = {
                "file_url": file_url,
                "user_id": user_id,
                "gender": gender,
                "weather": weather_type,
                "city": city,
                "timestamp": firestore.SERVER_TIMESTAMP
            }

            #Insert the document into Firestore with user_id as document ID
            self.db.collection("moods").document(user_id).set(mood_data)

            return file_url
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload file: {str(e)}")

    #Check existing mood data
    def check_existing_mood(self, user_id: str, db: firestore.Client) -> bool:
        doc_ref = db.collection("moods").document(user_id)
        doc = doc_ref.get()
        return doc.exists
    


    @staticmethod
    def get_mood(user_id: UUID4, db: firestore.Client) -> Optional[MoodOutput]:
        """Retrieve mood data for a given user_id."""
        doc_ref = db.collection("moods").document(str(user_id))
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood data not found.")
        
        data = doc.to_dict()

        #`timestamp` convert to datetime
        if isinstance(data.get("timestamp"), datetime):
            data["timestamp"] = data["timestamp"].strftime("%B %d, %Y at %I:%M:%S.%f %p UTC+8")

        #take predict mood
        predicted_mood = data.get("predicted_mood", "Unknown")
        data["predicted_mood"] = predicted_mood

        return MoodOutput(**data)



    async def update_mood(self, user_id: UUID4, gender: str, file) -> MoodOutput:
        try:
            # Convert UUID to string before using it in Firestore queries
            user_id_str = str(user_id)

            #Check existing mood data
            mood_exists = self.check_existing_mood(user_id_str, self.db)  # Ensure passing string to this function
            if not mood_exists:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood data not found.")

            #Upload new photo
            file_name = f"{user_id_str}/{file.filename}"  # Ensure using string for file path
            bucket = self.storage_client.bucket(os.getenv("BUCKET_NAME"))
            blob = bucket.blob(file_name)
            blob.upload_from_file(file.file, content_type=file.content_type)
            file_url = blob.public_url

            #Take data weather and city from Firestore
            doc_ref = self.db.collection("moods").document(user_id_str)  # Ensure using string for Firestore document reference
            mood_doc = doc_ref.get()
            if not mood_doc.exists:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood document not found in Firestore.")

            mood_data = mood_doc.to_dict()
            city = mood_data.get("city", "Unknown")
            weather = mood_data.get("weather", "Unknown")

            #save metadata
            updated_mood_data = {
                "file_url": file_url,
                "user_id": user_id_str,  # Ensure saving as string in Firestore
                "gender": gender,
                "timestamp": firestore.SERVER_TIMESTAMP
            }

            #update firestore
            doc_ref.set(updated_mood_data, merge=True)

            #Analyze mood with ML after updating the document
            predicted_mood = await self.analyze_mood_with_ml(user_id_str, file_url, self.db)  # Pass string to ML model

            #Convert timestamp to string for MoodOutput
            timestamp_str = str(int(datetime.now().timestamp()))

            return MoodOutput(
                user_id=user_id_str,
                gender=gender,
                file_url=file_url,
                timestamp=timestamp_str,
                weather=weather,
                city=city,
                predicted_mood=predicted_mood
            )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error updating mood: {str(e)}")



    async def delete_mood_photo(self, user_id: UUID4, file_name: str) -> dict:
        try:
            #Extract the path from the full URL
            parsed_url = urlparse(file_name)
            
            #Correctly extract the relative file path from the URL
            file_path = parsed_url.path.lstrip("/")

            # Debugging: Print the extracted file path
            print(f"Attempting to delete file: {file_path}")

            #Delete file from Cloud Storage
            bucket = self.storage_client.bucket(os.getenv("BUCKET_NAME"))
            blob = bucket.blob(file_path)

            if blob.exists():
                blob.delete()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found in Cloud Storage")

            # Remove file metadata from Firestore
            doc_ref = self.db.collection("moods").document(str(user_id))
            doc = doc_ref.get()
            
            if doc.exists:
                # Delete the entire document, not just the file_url
                doc_ref.delete()
                print(f"Deleted document for user: {user_id}")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User mood data not found in Firestore")

            return {"message": "File and metadata deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete file: {str(e)}")



    async def analyze_mood_with_ml(self, user_id: str, file_url: str, db: firestore.Client) -> str:

        ml_endpoint = os.getenv("ML_MOOD_ENDPOINT")  # Endpoint ML

        try:
            #download file URl
            response = requests.get(file_url)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to download file from URL: {file_url}"
                )
            
            #save in memory
            file_content = response.content
            file_name = file_url.split("/")[-1]  #take file name from URL

            #send to ML
            files = {"file": (file_name, file_content)}
            async with httpx.AsyncClient(follow_redirects=True) as client:
                ml_response = await client.post(ml_endpoint, files=files)

                if ml_response.status_code == 200:
                    try:
                        #Parsing JSON respons
                        result = ml_response.json()
                        predicted_mood = result.get("predicted_mood")
                        
                        if not predicted_mood:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST, detail="ML model did not return a prediction."
                            )

                        #save to firestore
                        doc_ref = db.collection("moods").document(user_id)
                        doc_ref.update({
                            "predicted_mood": predicted_mood,
                            "timestamp": firestore.SERVER_TIMESTAMP
                        })

                        return predicted_mood
                    except ValueError as e:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid JSON from ML model: {str(e)}"
                        )
                else:
                    raise HTTPException(
                        status_code=ml_response.status_code,
                        detail=f"Failed to get prediction from ML model. {ml_response.text}",
                    )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error analyzing mood with ML: {str(e)}"
            )