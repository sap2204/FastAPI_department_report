from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings


# Создание асинхронного движка, который как менеджер управляет подключениями к БД
engine = create_async_engine(settings.get_db_url)


# Создание фабрики сессий
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Класс будет хранить всю информацию о таблицах для БД на бэкенде
class Base(DeclarativeBase):
    pass

