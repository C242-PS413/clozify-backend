from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Any
from typing import Self
from datetime import datetime, timezone
from uuid import UUID


class MoodInput(BaseModel):
    user_id: UUID
    mood: int

    @model_validator(mode='before')
    @classmethod
    def validate_user_id(cls, data: Any) -> Any:
        if "user_id" in data:
            try:
                UUID(data["user_id"])
            except ValueError:
                raise ValueError("Invalid UUID format for user_id.")
        else:
            raise ValueError("user_id is required.")
        return data

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if not self.user_id:
            raise ValueError("user_id must not be empty.")
        if not (1 <= self.mood < 6):
            raise ValueError("Mood must be between 1 and 6.")
        return self


class MoodOutput(BaseModel):
    user_id: str
    mood: int
    timestamp: int = Field(default_factory=lambda: int(datetime.now(timezone.utc).timestamp()))