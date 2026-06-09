from pathlib import Path

import numpy as np
from ultralytics import YOLO

from app.core import config

PERSON_CLASS_ID: int = 0


class Detector:
    def __init__(
        self,
        model: YOLO = YOLO(config.DETECTOR_MODEL),
        confidence: float = config.DETECTOR_CONFIDENCE,
    ):
        self.model = model
        self.confidence = confidence

    def count_people(self, image: str | Path | np.ndarray) -> int:
        results = self.model.predict(
            image,
            classes=[PERSON_CLASS_ID],
            conf=self.confidence,
            verbose=False,
        )
        return len(results[0].boxes)


detector = Detector()
