from google.cloud import firestore
from dotenv import load_dotenv
import os
from firebase_admin import firestore


load_dotenv()

def get_db():
    google_creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not google_creds_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set!")
    
    # Menginisialisasi klien Firestore menggunakan kredensial dari file JSON
    db = firestore.Client.from_service_account_json(google_creds_path, project="bangkitinc", database="clozify-firestore")
    

    try:
        yield db
    finally:
        pass