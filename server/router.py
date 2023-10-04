from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from config_server import logger
from database import session_maker, get_session
from server.models import Message
from server.schemas import MessageOut, MessageIn


router = APIRouter(
    prefix='/server',
    tags=['Server'],
)


@router.post("/send_message/", response_model=list[MessageOut])
async def send_message(
        message_in: MessageIn,
        session: Session = Depends(get_session)
        ):
    """Обработчик для создания нового сообщения"""
    try:
        new_message = Message(
            sender=message_in.sender,
            text=message_in.text,
        )
        session.add(new_message)
        session.flush()
        session.commit()
    except Exception as e:
        logger.error(f"Во время добавления записи произошла ошибка: {str(e)}")

    try:
        query = select(func.count(Message.id)).where(
            (Message.sender == message_in.sender) & (Message.id <= new_message.id)
        )
        new_message.user_message_count = session.scalar(query)
        session.commit()
    except Exception as e:
        logger.error(f"Во время обновления записи произошла ошибка: {str(e)}")

    # Получаем последние 10 сообщений
    try:
        messages = session.execute(
            select(Message).where(
                (Message.sender == message_in.sender) & (Message.id <= new_message.id)
            ).order_by(Message.created_at.desc()).limit(10)
        )
        return list(messages.scalars().all())
    except Exception as e:
        logger.error(f"Во время получения данных произошла ошибка: {str(e)}")
