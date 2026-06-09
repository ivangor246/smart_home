from pydantic import Field

from .base import BaseEvent


class CameraFrame(BaseEvent):
    image: str


class DetectionCamera(BaseEvent):
    people_count: int = Field(ge=0)
