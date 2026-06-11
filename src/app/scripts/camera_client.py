"""Testing the camera's detection features"""

import asyncio
import base64
import json
from datetime import datetime, timezone

import cv2
import websockets

CAMERA_URL = 'ws://127.0.0.1:8000/ws/camera'
BUS_URL = 'ws://127.0.0.1:8000/ws/bus'
CAMERA_INDEX = 0
FPS = 2
INTERVAL = 1 / FPS
JPEG_QUALITY = 80


def encode_frame(frame) -> str:
    ok, buffer = cv2.imencode(
        '.jpg',
        frame,
        [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY],
    )
    if not ok:
        raise RuntimeError('failed to encode frame')
    return base64.b64encode(buffer).decode('ascii')


async def drain_replies(ws) -> None:
    try:
        while True:
            reply = await asyncio.wait_for(ws.recv(), timeout=0.001)
            print('server:', reply)
    except (asyncio.TimeoutError, websockets.ConnectionClosed):
        return


async def send_frames(cap) -> None:
    async with websockets.connect(CAMERA_URL) as ws:
        print(f'sending {FPS} fps to {CAMERA_URL}')
        while True:
            tick = asyncio.get_event_loop().time()

            ok, frame = await asyncio.to_thread(cap.read)
            if not ok:
                print('frame grab failed, retry...')
                await asyncio.sleep(INTERVAL)
                continue

            payload = {
                'event': 'detection on camera',
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'image': encode_frame(frame),
            }
            await ws.send(json.dumps(payload))
            await drain_replies(ws)

            elapsed = asyncio.get_event_loop().time() - tick
            await asyncio.sleep(max(0.0, INTERVAL - elapsed))


async def listen_bus() -> None:
    async with websockets.connect(BUS_URL) as ws:
        print(f'subscribed to bus {BUS_URL}')
        async for message in ws:
            print('bus:', message)


async def main() -> None:
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        raise RuntimeError(f'cannot open camera #{CAMERA_INDEX}')

    print(f'camera #{CAMERA_INDEX} opened')
    try:
        await asyncio.gather(send_frames(cap), listen_bus())
    finally:
        cap.release()
        print('camera released')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nstopped')
