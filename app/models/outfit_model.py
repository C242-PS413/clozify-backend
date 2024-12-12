from typing import List, Optional
from dataclasses import dataclass

@dataclass
class MoodData:
    user_id: str
    predicted_mood: str
    gender: str
    weather: List[str]
    file_url: str

    def transform_weather(self) -> List[str]:
        return [
            'Rainy' if w == 'rain' else 
            'Sunny' if w == 'summer' else 
            w 
            for w in self.weather
        ]