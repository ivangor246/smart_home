import asyncio
import base64

import cv2
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.schemas import CameraFrame, DetectionCamera
from app.services import detector
from app.ws.manager import manager

router = APIRouter(tags=['camera'])


def _decode_image(image_base64: str) -> np.ndarray:
    raw = base64.b64decode(image_base64)
    buffer = np.frombuffer(raw, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError('cannot decode image')
    return image


@router.websocket('/camera')
async def ws_camera(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            payload = await ws.receive_json()
            frame = CameraFrame.model_validate(payload)

            image = _decode_image(frame.image)
            count = await asyncio.to_thread(detector.count_people, image)

            event = DetectionCamera(
                event='detection on camera',
                timestamp=frame.timestamp,
                people_count=count,
            )

            await manager.broadcast('bus', event.model_dump(mode='json'))
    except WebSocketDisconnect:
        return
