from google.cloud import firestore
from dotenv import load_dotenv
import os
from firebase_admin import firestore


load_dotenv()

def get_db():
    google_creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_FIRESTORE')
    if not google_creds_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_FIRESTORE environment variable is not set!")
    
    db = firestore.Client.from_service_account_json(google_creds_path, project=os.getenv('DATABASE_PROJECTID'), database=os.getenv("DATABASE_INSTANCE"))
    try:
        yield db
    finally:
        pass        