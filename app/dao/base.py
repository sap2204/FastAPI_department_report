from sqlalchemy import delete, insert, select, update
from app.database import async_session_maker




# Базовый класс для работы с БД (CRUD)
class BaseDAO:

    model = None

    # Метод для поиска по id
    @classmethod
    async def get_by_id(cls, model_id):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id = model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        


    # Метод поиска один или ничего
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        
    


    # Метод поиска всех строк по фильтру
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        
        
        


    # Метод добавления чего-то в БД
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()
            
        


    # Метод обновления чего-то
    @classmethod
    async def update(cls, model_id: int, data: dict):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == model_id).values(**data)
            await session.execute(stmt)
            await session.commit()
        


    # Метод удаления из БД
    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
        