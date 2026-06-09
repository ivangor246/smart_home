from pydantic import Field

from .base import BaseEvent


class CameraFrame(BaseEvent):
    image: str


class PeopleDetection(BaseEvent):
    people_count: int = Field(ge=0)
