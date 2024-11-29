from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime, timezone
from uuid import UUID, uuid4

class Mood(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    mood: int # 1-6
    timestamp: int = Field(default_factory=lambda: int(datetime.now(timezone.utc).timestamp()))

    @model_validator
    @classmethod
    def validate_mood(cls, values):
        mood = values.get("mood")
        if not 1 <= mood <= 6:
            raise ValueError("Mood must be between 1 and 6.")
        return values