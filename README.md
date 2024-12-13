### Installation

1. Clone the repository:
   ```
   git clone https://github.com/C242-PS413/clozify-backend.git
   ```
2. Navigate to the project directory:
   ```
   cd clozify-backend
   ```
3. Install dependencies:
   ```
   python -m venv venv
   ./venv/Scripts/activate
   pip install -r /path/to/requirements.txt
   uvicorn app.main:app --reload
   ```

### Configuration

1. Create a **.env** file in the project root `.env`.
2. Add the following configurations to the .env file, modifying them according to your environment:

   ```bash
	GOOGLE_APPLICATION_CREDENTIALS_FIRESTORE=
	DATABASE_PROJECTID=
	DATABASE_INSTANCE=
	API_KEY =
	BASE_URL =
	BUCKET_NAME=
	GOOGLE_APPLICATION_CREDENTIALS=
	ML_MOOD_ENDPOINT =
	ML_OUTFIT_ENDPOINT =
   ```

### Usage

- Run project

```
  uvicorn app.main:app --reload
```
