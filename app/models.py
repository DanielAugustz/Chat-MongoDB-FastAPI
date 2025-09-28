# app/models.py
from pydantic import BaseModel, Field, constr
from datetime import datetime

UsernameType = constr(strip_whitespace=True, min_length=1, max_length=50)
ContentType = constr(strip_whitespace=True, min_length=1, max_length=1000)

class MessageIn(BaseModel):

    '''
    Payload de entrada para criar uma mensagem WS
    '''
    username: UsernameType
    content: ContentType

class MessageOut(BaseModel):
    '''
    como a mensagem retornada pela api o _id e uma string do objectid e created_at e uma string de data no formato iso
    '''
    
    _id: str
    room: str
    username: str
    content: str
    created_at: str

class MessagesPage(BaseModel):
    items: list[MessageOut]
    next_cursor: str = None
