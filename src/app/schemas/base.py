from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class BaseSchema(BaseModel): ...


class BaseEvent(BaseSchema):
    event: str = Field(min_length=1)
    timestamp: datetime
    comment: str | None = Field(default=None, exclude=True)

    @field_validator('timestamp')
    @classmethod
    def timestamp_to_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError('timestamp must include timezone info')
        return value.astimezone(timezone.utc)
