# app/routes/messages.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..database import get_db, serialize, ObjectId
from ..models import MessageIn, MessageOut, MessagesPage
from datetime import datetime, timezone

router = APIRouter(prefix="/rooms", tags=["messages"])

@router.get("/{room}/messages", response_model=MessagesPage)
async def get_messages(    
    room: str, limit: int = Query(20, ge=1, le=100),
    before_id: str = Query(None),
):
    ''''
    retorna o historico de mensagens da sala, se before_id for invalido retorna 'before_id inválido'
    '''
    query = {"room": room}
    if before_id:
        try:
            query["_id"] = {"$lt": ObjectId(before_id)}
        except ValueError:
            raise HTTPException(detail="before_id inválido")

    cursor = get_db()["messages"].find(query).sort("_id", -1).limit(limit)
    docs = [serialize(d) async for d in cursor]
    docs.reverse()
    next_cursor = docs[0]["_id"] if docs else None
    return {"items": docs, "next_cursor": next_cursor}

@router.post("/{room}/messages", response_model=MessageOut)
async def post_message(
    room: str,
    payload: MessageIn,
):
    '''
    insere uma nova mensagem no banco a validacao e feita pelo pydantic MessageIn mensagens sem conteudo ou com username invalido serao bloqueadas pelo pydantic
    '''
    doc = {
        "room": room,
        "username": payload.username[:50],
        "content": payload.content[:1000],
        "created_at": datetime.now(timezone.utc),
    }
    res = await get_db()["messages"].insert_one(doc)
    doc["_id"] = res.inserted_id
    return serialize(doc)
