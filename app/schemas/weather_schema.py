from pydantic import BaseModel
from typing import List

class WeatherResponse(BaseModel):
    city: str
    temp: float
    preciptype: List[str]
    resolvedAddress: str

class WeatherRequest(BaseModel):
    city: str
