from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends
from sqlalchemy import select, and_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from database import get_async_session, async_session_maker
from server.models import Message
from server.schemas import MessageOut, MessageIn
from server.utils import count_messages_for_user, count_messages_all, check_messages_number

router = APIRouter(
    prefix='/server',
    tags=['Server'],
)


@router.post("/send_message/", response_model=list[MessageOut])
async def send_message(
        message_in: MessageIn
        ):
    """Обработчик для создания нового сообщения"""

    async with async_session_maker() as session:
        async with session.begin():
            # Проверяем номер последнего сообщения отправителя
            # latest_message = await session.execute(
            #     select(Message.user_message_number)
            #     .where(and_(Message.sender == message_in.sender))
            #     .order_by(Message.created_at.desc())
            #     .limit(1)
            # )
            # latest_message = latest_message.scalar()

            # # Создание SQL-запроса для выборки из последовательности
            # sequence_query = text("SELECT nextval('messages_id_seq')")
            #
            # # Выполнение SQL-запроса
            # result = await session.execute(sequence_query)
            #
            # # Получение значения из результата
            # sequence_value = result.fetchone()[0]
            #
            # # Вывод значения
            # print(f'{sequence_value=}')

            # current = await session.execute(func.currval('messages_id_seq'))
            # current_value = current.scalar()
            await session.execute(text("SELECT nextval('messages_id_seq')"))
            current_value_query = text(
                "SELECT currval('messages_id_seq') FROM messages_id_seq"
            )

            result = await session.execute(current_value_query)
            current_value = result.fetchone()[0]

            print(f'{current_value=}')

            message_count_for_user = await count_messages_for_user(message_in.sender, session)

            # print(f'{message_count_for_user=}')

            message_count = await count_messages_all(session)

            # print(f'{message_count=}')

            if message_count is None:
                # try:
                # message_count += 1
                new_message = Message(
                    sender=message_in.sender,
                    text=message_in.text,
                    user_message_number=current_value,
                    user_message_count=message_count_for_user + 1,
                )
                session.add(new_message)
                await session.commit()
                # except UniqueViolationError:
                #     message_count_for_user = await count_messages_for_user(message_in.sender, session)
                #     message_count = await count_messages_all(session)
                #     new_message = Message(
                #         sender=message_in.sender,
                #         text=message_in.text,
                #         user_message_number=message_count + 1,
                #         user_message_count=message_count_for_user + 1,
                #     )
                #     session.add(new_message)
                #     await session.commit()
            else:
                # try:
                # Создаем новое сообщение
                new_message = Message(
                    sender=message_in.sender,
                    text=message_in.text,
                    user_message_number=current_value + 1,
                    user_message_count=message_count_for_user + 1,
                )
                session.add(new_message)
                await session.commit()
                # except UniqueViolationError:
                #     message_count_for_user = await count_messages_for_user(message_in.sender, session)
                #     message_count = await count_messages_all(session)
                #     new_message = Message(
                #         sender=message_in.sender,
                #         text=message_in.text,
                #         user_message_number=message_count + 1,
                #         user_message_count=message_count_for_user + 1,
                #     )
                #     session.add(new_message)
                #     await session.commit()

        # Получаем последние 10 сообщений
        messages = await session.execute(
            select(Message).where(
                and_(Message.sender == message_in.sender)
            ).order_by(Message.created_at.desc()).limit(10)
        )
        messages = messages.scalars().all()

        # считаем сообщения от пользователя
        # query = select(func.count(Message.id).filter(Message.sender == message_in.sender))
        # query_result = await session.execute(query)
        # user_message_count = query_result.scalar()

        # Собираем исходящий список сообщений
        response_messages = [
            MessageOut(
                sender=message.sender,
                text=message.text,
                created_at=message.created_at,
                message_number=message.user_message_number,
                user_message_count=message.user_message_count,
            )
            for message in reversed(messages)
        ]

    return response_messages
