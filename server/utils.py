from sqlalchemy import select
from sqlalchemy.sql import func

from server.models import Message


async def count_messages_for_user(
        sender,
        session
        ):
    """Считает сколько сообщений есть у пользователя"""
    query = select(func.count(Message.id).filter(Message.sender == sender))
    query_result = await session.execute(query)
    user_message_count = query_result.scalar()
    return user_message_count


async def count_messages_all(
        session
        ):
    """Считает сколько сообщений есть у пользователя"""
    query = select(func.count(Message.id))
    query_result = await session.execute(query)
    message_count = query_result.scalar()
    return message_count


async def check_messages_number(message_count, session):
    query = select(Message).filter(Message.user_message_count == message_count)
    query_result = await session.execute(query)
    message_number = query_result.scalar()
    print(f'{message_number=}')
    return message_number


