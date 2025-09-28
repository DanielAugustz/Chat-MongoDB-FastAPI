# app/database.py
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime, timezone
from bson import ObjectId
from .config import MONGO_URL, MONGO_DB

_client: Optional[AsyncIOMotorClient] = None

def get_db():
    '''
    Retorna a instancia do banco de dados (AsyncIOMotorDatabase), criando o cliente quando necessario
    Dispara um RuntimeError caso a variavel MONGO_URL não esteja configurada
    '''
    global _client
    if _client is None:
        if not MONGO_URL:
            raise RuntimeError("Defina MONGO_URL no .env .")
        _client = AsyncIOMotorClient(MONGO_URL)
    return _client[MONGO_DB]

def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()

def serialize(doc: dict) -> dict:
    '''
    Converte um documento do Mongo em JSON-serializável:
    - ObjectId -> str
    - datetime -> ISO string
    '''
    d = dict(doc)
    if "_id" in d:
        d["_id"] = str(d["_id"])
    if "created_at" in d and isinstance(d["created_at"], datetime):
        d["created_at"] = _iso(d["created_at"])
    return d

