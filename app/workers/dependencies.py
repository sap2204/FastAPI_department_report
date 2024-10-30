from datetime import datetime, timezone
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from app.config import settings
from app.workers.dao import WorkersDAO
from app.workers.model import Workers


# Получение токена из запроса
def get_token(request: Request):
    token = request.cookies.get("depart_report") # поиск в запросе токена с названием "depart_report"
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="В запросе нет нужного токена")
    return token


# Получение текущего работника из токена
async def get_current_worker(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORIHM) # декодирование токена
                    # payload - это 2-я часть токена с данными id работника и временем жизни токена
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен из запроса не является jwt-токеном")
    expire: str = payload.get("exp") # из данных токена беру время жизни токена по ключу "exp"
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()): # если в полученном токене нет ключа exp или время токена истекло
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен или время жизни токена истекло")
    worker_id: str = payload.get("sub") # поиск в токене id по ключю "sub"
    if not worker_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="В токене нет id работника")
    worker = await WorkersDAO.get_by_id(int(worker_id)) # поиск в базе Workers по id, взятому из токена
    if not worker:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Работника с таким id нет в БД")
    return worker # возвращается модель



# Получение из таблицы работников АДМИНА
async def get_admin_worker(admin_worker: Workers = Depends(get_current_worker)): # получение текущего работника
    if admin_worker.role != "admin": # проверка роли текущего работника
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="У вас нет прав админа")
    return admin_worker


    