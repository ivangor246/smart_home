from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, topic: str, ws: WebSocket):
        await ws.accept()
        self.active[topic].add(ws)

    def disconnect(self, topic: str, ws: WebSocket):
        self.active[topic].discard(ws)

    async def broadcast(self, topic: str, data: dict):
        for ws in set(self.active[topic]):
            try:
                await ws.send_json(data)
            except Exception:
                self.active[topic].discard(ws)


manager = ConnectionManager()
