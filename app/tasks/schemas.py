from pydantic import BaseModel
from datetime import date


# Схема задач
class STasks(BaseModel):

    
    worker_id: int
    task: str
    date: date
    days_per_task: int



# Схема для обновления задачи
class SUpdateTask(BaseModel):

    worker_id: int | None = None
    task: str | None = None
    date_task: date | None = None
    days_per_task: int | None = None


# Схема для возврата всех задач всех работников (после join таблиц workers и tasks)
class STasksAllWorkers(BaseModel):

    surname: str
    name: str
    middle_name: str
    task: str
    days_per_task: int
