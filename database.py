from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.ddl import CreateTable

from config_server import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class Base(DeclarativeBase):
    pass


# Точка входа SqlAlchemy в наше приложение
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def check_tables_exist():
    """Проверяет какие таблицы есть в БД"""
    async with async_session_maker() as session:
        async with session.begin():
            existing_tables = await session.execute(
                text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")
            )
            existing_table_names = [table[0] for table in existing_tables]
            return existing_table_names


async def create_tables_if_not_exist():
    """Создаёт недостающие таблицы"""
    existing_table_names = await check_tables_exist()
    new_table_names = set(Base.metadata.tables.keys()) - set(existing_table_names)
    if new_table_names:
        async with async_session_maker() as session:
            async with session.begin():
                for table_name in new_table_names:
                    table = Base.metadata.tables[table_name]
                    await session.execute(CreateTable(table))


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение асинхронной сессии"""
    async with async_session_maker() as session:
        yield session
