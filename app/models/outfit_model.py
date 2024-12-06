from pydantic import BaseModel
from pydantic import UUID4


class OutfitModel(BaseModel):
    id: UUID4
    outfit: str
    mood: str
    weather: str
    gender: str

