from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.workers.dao import WorkersDAO
from app.workers.dependencies import get_admin_worker
from app.workers.schemas import SAuthWorkers, SUpdateWorkers, SWorkers
from app.workers.auth import authenticate_worker, create_access_token, get_hashed_password



router = APIRouter(
    prefix="/workers",
    tags=["Работники"]
    )


# Эндпоинт добавления нового работника
@router.post("/register", status_code=201)
async def add_worker(new_worker: SWorkers):
    worker = await WorkersDAO.find_one_or_none(login = new_worker.login) # поиск в БД работника с логином, переданным с фронта
    if worker: # если работник с таким логином существует в БД, то выдается ошибка
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Работник с таким логином уже существует")
    
    hashed_password = get_hashed_password(new_worker.password) # хеширование переданного пароля
    new_data_worker = new_worker.model_dump() # преобразовние переданных данных, которые являются схемой Pydantic в словарь
    new_data_worker["password"] = hashed_password # изменение значения колонки password на захешированный пароль
    
    await WorkersDAO.add(**new_data_worker) # применяется метод добавления записи в БД, ** распаковка словаря, т.к. метод принимает именнованные аргументы
    return {"Сообщение" : f'Добавлен работник {new_worker.name} {new_worker.surname} с логином: {new_worker.login}'}





# Эндпоинт залогинивания работника
@router.post("login", status_code=200)
async def login_worker(response: Response, worker: SAuthWorkers): # т.к. при ответе в куки будет устанавливаться токен, то в ф-ции надо указать response типа Response 
    existing_worker = await authenticate_worker(worker.login, worker.password) # аутентификация работника по логину и паролю
    if not existing_worker: # проверка наличия в БД работника с введенными логином и паролем
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
    
    access_token = create_access_token({"sub": str(existing_worker.id)}) # создание токена, передаю в ф-цию создания токена словарь объект (sub) - id работника из БД
    response.set_cookie("depart_report", access_token, httponly=True) # установка в куки jwt-токена
    


# Эндпоинт выхода из учетной записи
@router.post("/logout", status_code=201)
async def logout_worker(response: Response):
    response.delete_cookie("depart_report") # удаление jwt-токена из кук
    


# Эндпоинт обновления работника
@router.patch("/update", status_code=201)
async def update_worker(worker_id: int, data_worker: SUpdateWorkers, current_worker = Depends(get_admin_worker)):
    if current_worker.role != "admin": # проверка, что залогиненный работник имеет права админа
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не имеете прав админа")
    existing_worker = await WorkersDAO.get_by_id(worker_id) # поиск в БД работника по id
    if not existing_worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работника с таким id нет в БД")
    update_worker = data_worker.model_dump(exclude_unset=True) # привожу переданные данные в пайдениковской схеме к словарю
    await WorkersDAO.update(worker_id, update_worker) # вызывается метод обновления без ** в update_worker, т.к. метод update принимает словарь
    return "Работник обновлен"





# Эндпоинт удаления работника ТОЛЬКО АДМИНОМ
@router.delete("/delete")
async def delete_worker(worker_id: int, current_worker: SWorkers = Depends(get_admin_worker)): 
    if current_worker.role != "admin": # если у текущего работника роль не АДМИНА
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="У Вас не прав админа для удаления работника")
    worker_to_delete = await WorkersDAO.get_by_id(worker_id) # поиск в БД работника с переданным id работника
    if not worker_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работника с таким id нет в БД")
    await WorkersDAO.delete(id = worker_id)
    return {"Сообщение": f"Работник {worker_to_delete.surname} {worker_to_delete.name} удален "}

