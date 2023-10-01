from sqlalchemy import text, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.sql.ddl import CreateTable

from config_server import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class Base(DeclarativeBase):
    pass


engin_sync = create_engine(DATABASE_URL)
session_maker = sessionmaker(engin_sync, expire_on_commit=False)


def check_tables_exist():
    """Проверяет какие таблицы есть в БД"""
    with session_maker() as session:
        existing_tables = session.execute(
            text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")
        )
        existing_table_names = [table[0] for table in existing_tables]
        return existing_table_names


def create_tables_if_not_exist():
    """Создаёт недостающие таблицы"""
    existing_table_names = check_tables_exist()
    new_table_names = set(Base.metadata.tables.keys()) - set(existing_table_names)
    if new_table_names:
        with session_maker() as session:
            with session.begin():
                for table_name in new_table_names:
                    table = Base.metadata.tables[table_name]
                    session.execute(CreateTable(table))
