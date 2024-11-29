from fastapi import FastAPI
from .api.routers import mood_router

app = FastAPI()


app.include_router(mood_router.router)

@app.get("/")
def root():
    return{"messages": "Hello World"}