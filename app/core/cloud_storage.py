import os
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

class StorageClient:
    def __init__(self):
        self.client = storage.Client.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS_CLOUDSTORAGE")
        )
        self.bucket_name = os.getenv("BUCKET_NAME")

    def upload_file(self, file_obj, file_name: str) -> str:
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(file_name)
            blob.upload_from_file(file_obj)
            return blob.public_url
        except Exception as e:
            raise RuntimeError(f"Error uploading file: {str(e)}")
