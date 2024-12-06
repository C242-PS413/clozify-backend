from fastapi import FastAPI
from .api.routers import mood_router
from .api.routers import outfit_router
from .api.routers import weather_router

app = FastAPI()


app.include_router(mood_router.router)
app.include_router(outfit_router.router)
app.include_router(weather_router.router)

@app.get("/")
def root():
    return{"messages": "Hello World"}