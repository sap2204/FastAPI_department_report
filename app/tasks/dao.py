from datetime import date
from app.dao.base import BaseDAO
from app.tasks.model import Tasks
from app.database import async_session_maker
from sqlalchemy import and_, select

from app.workers.model import Workers


# Класс для работы с таблицей Tasks в БД
class TasksDAO(BaseDAO):

    model = Tasks


    # Метод получения задач всех работников на указанные даты
    @classmethod
    async def find_tasks_all_workers(cls, starting_date: date, end_date: date):
        async with async_session_maker() as session:
            """
            SELECT surname, name, middle_name, task, days_per_task FROM workers
            LEFT JOIN tasks
            ON workers.id = tasks.worker_id
            WHERE tasks.date >= '2024-10-01' AND tasks.date <= '2024-10-31'
            """
            query = select(Workers.surname, Workers.name, 
                           Workers.middle_name, 
                           cls.model.task, 
                           cls.model.days_per_task
                           ).select_from(Workers).outerjoin(
                           cls.model, Workers.id == cls.model.worker_id
                           ).where(
                and_(
                    cls.model.date >= starting_date,
                    cls.model.date <= end_date
                )
            )
            result = await session.execute(query)
            return result.mappings().all()
            
            
        