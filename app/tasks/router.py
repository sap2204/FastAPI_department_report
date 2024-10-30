from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status

from app.tasks.dao import TasksDAO
from app.tasks.model import Tasks
from app.tasks.schemas import STasks, STasksAllWorkers, SUpdateTask
from app.workers.dependencies import get_admin_worker, get_current_worker
from app.workers.model import Workers
from app.workers.schemas import SWorkers



router = APIRouter(
    prefix="/tasks",
    tags=["Выполненные задачи"]
)


# Эндпоинт добавления задачи
@router.post("/add_task", status_code=201)
async def add_task(task_data: STasks, worker: Workers = Depends(get_admin_worker)):
    if worker.role != "admin": # проверка роли работника
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав на добавление задачи")
    
    new_task = task_data.model_dump() # преобразование входных данных (тип Pedantic) в словарь
    await TasksDAO.add(**new_task) # ** - это распаковка словаря, т.к. функция принимает неопределенное кол-во именованных аргументов
    added_task = await TasksDAO.find_one_or_none(task = task_data.task)
    return {"Добавлена задача ": f"{added_task.task}"}
    
    



# Эндпоинт просмотра задачи по ее id
@router.get("/get_task", status_code=200)
async def get_task_by_id(task_id: int) -> STasks:
    existing_task = await TasksDAO.get_by_id(task_id) # получение задачи из БД
    if not existing_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задачи с таким id нет БД")
    return existing_task
    


# Эндпоинт просмотра всех только своих задач
@router.get("/get_my_tasks")
async def get_my_all_tasks(worker: Workers = Depends(get_current_worker)) -> list[STasks]:
    return await TasksDAO.find_all(worker_id = worker.id)
    


# Эндпоинт просмотра задач всех работников по месяцам
@router.get("/get_all_tasks/{starting_date}/{end_date}")
async def get_tasks_all_workers(starting_date: date,
                                end_date: date,
                                worker: SWorkers = Depends(get_admin_worker)) -> list[STasksAllWorkers]:
    if worker.role != "admin": # Проверка право админа
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="У Вас нет прав админа")
    if end_date < starting_date: # проверка дат
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Дата окончания не может быть больше даты начала")
    tasks_of_all_workers = await TasksDAO.find_tasks_all_workers(starting_date, end_date) # список задач всех работников
    return tasks_of_all_workers


# Эндпоинт обновления задачи
@router.patch("/update_task", status_code = 200)
async def update_task(id_task: int,
                      data_to_update_task: SUpdateTask,
                      worker: SWorkers = Depends(get_admin_worker)):
    if worker.role != "admin": # проверка прав админа
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="У Вас нет прав админа")
    existing_task = await TasksDAO.get_by_id(id_task) # поиск в БД задачи с переданным id
    if not existing_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача с таким id нет в БД")
    update_task = data_to_update_task.model_dump(exclude_unset=True)# привожу переданные данные из пайдентик схемы к словарю с необязательными полями
    await TasksDAO.update(id_task, update_task) # вызывается метод обновления без ** в update_task, т.к. метод update принимает словарь
    return {"Сообщение": f'Задача с id = {existing_task.id} обновлена'}


# Эндпоинт удаления задачи
@router.delete("/delete_task/{id_task}")
async def delete_task_by_id(
                            id_task: int,
                            worker: SWorkers = Depends(get_admin_worker)):
    if worker.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="У Вас нет прав админа")
    existing_task = await TasksDAO.get_by_id(id_task)
    if not existing_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задачи с таким id нет в БД")
    await TasksDAO.delete(id = existing_task.id)
    return {"Сообщение": f"Задача {existing_task.task} удалена"}
    