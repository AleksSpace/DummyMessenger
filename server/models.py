from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    text = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    user_message_number = Column(Integer, default=0)
    user_message_count = Column(Integer, default=0)
