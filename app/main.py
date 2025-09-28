# app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .routes.messages import router as messages_router
from .ws_manager import WSManager
from .database import get_db, serialize
from datetime import datetime, timezone

app = FastAPI(title="Chat MongoDB + FastAPI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(messages_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", include_in_schema=False)
async def index():
    return FileResponse("app/static/index.html")

manager = WSManager()

@app.websocket("/ws/{room}")
async def ws_room(ws: WebSocket, room: str):

    '''
    Endpoint WebSocket que
      - conecta o cliente
      - envia histórico (últimas 20 mensagens)
      - recebe mensagens e as salva no banco + broadcast
    Mensagens vazias não são salvas nem enviadas
    '''

    await manager.connect(room, ws)
    try:
          # histórico inicial
        cursor = get_db()["messages"].find({"room": room}).sort("_id", -1).limit(20)
        items = [serialize(d) async for d in cursor]
        items.reverse()
        await ws.send_json({"type": "history", "items": items})

        while True:
            payload = await ws.receive_json()
            username = str(payload.get("username", "anon"))[:50]
            content = str(payload.get("content", "")).strip()
            if not content:
                continue
            doc = {
                "room": room,
                "username": username,
                "content": content,
                "created_at": datetime.now(timezone.utc),
            }
            res = await get_db()["messages"].insert_one(doc)
            doc["_id"] = res.inserted_id
            await manager.broadcast(room, {"type": "message", "item": serialize(doc)})
    except WebSocketDisconnect:
        manager.disconnect(room, ws)
