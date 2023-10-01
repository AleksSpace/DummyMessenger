from datetime import datetime

from pydantic import BaseModel


class MessageIn(BaseModel):
    """Схема для входящего JSON-сообщения"""
    sender: str
    text: str


class MessageOut(BaseModel):
    """Схема для исходящего JSON-сообщения"""
    id: int
    sender: str
    text: str
    created_at: datetime
    user_message_count: int

    class Config:
        from_attributes = True
