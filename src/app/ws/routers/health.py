from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.ws.manager import manager

router = APIRouter(tags=['health'])


@router.websocket('/health')
async def ws_health(ws: WebSocket):
    await manager.connect(ws)

    try:
        await manager.broadcast({'status': 'ok'})

        while True:
            data = await ws.receive_json()
            await manager.broadcast({'echo': data})

    except WebSocketDisconnect:
        await manager.disconnect(ws)
