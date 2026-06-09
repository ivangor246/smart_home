from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core import config
from app.ws.manager import manager

router = APIRouter(tags=['bus'])


@router.websocket('/bus')
async def ws_bus(ws: WebSocket):
    await manager.connect(config.T_BUS, ws)

    try:
        while True:
            await ws.receive_text()

    except WebSocketDisconnect:
        ...
    finally:
        manager.disconnect(config.T_BUS, ws)
