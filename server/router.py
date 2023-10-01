from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.sql import func

from database import session_maker
from server.models import Message
from server.schemas import MessageOut, MessageIn

router = APIRouter(
    prefix='/server',
    tags=['Server'],
)


@router.post("/send_message/", response_model=list[MessageOut])
async def send_message(
        message_in: MessageIn
        ):
    """Обработчик для создания нового сообщения"""
    with session_maker() as session:
        new_message = Message(
            sender=message_in.sender,
            text=message_in.text,
        )
        session.add(new_message)
        session.flush()
        session.commit()

        query = select(func.count(Message.id)).where(
            (Message.sender == message_in.sender) & (Message.id <= new_message.id)
        )
        new_message.user_message_count = session.scalar(query)

        session.commit()

        # Получаем последние 10 сообщений
        messages = session.execute(
            select(Message).where(
                (Message.sender == message_in.sender) & (Message.id <= new_message.id)
            ).order_by(Message.created_at.desc()).limit(10)
        )

        return list(messages.scalars().all())
