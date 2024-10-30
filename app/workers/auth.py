from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from app.config import settings
from app.workers.dao import WorkersDAO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

# Функция хеширования пароля
def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


# Функция верификации пароля
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



# Создание jwt-токена
def create_access_token(data: dict) -> str:
    to_encode = data.copy() # принимаю словарь {"sub": id работника} и копирую его, т.к. словарь изменяемая структура данных
    expire = datetime.now(timezone.utc) + timedelta(minutes=60) # установка времени жизни токена
    to_encode.update({"exp": expire}) # обновление словаря данными о жизни токена
    jwt_token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORIHM) # создание токена из обновленного словаря с помощью секретного ключа и алгоритма
    return jwt_token


# Фунция аутентификации работника
async def authenticate_worker(login: str, password: str):
    existing_worker = await WorkersDAO.find_one_or_none(login = login) # поиск работника с переданным логином
    if not existing_worker or not verify_password(password, existing_worker.password): # если в БД нет работника с таким логином или не 
                                                                                       # совпадает переданный пароль с паролем в БД
        return None
    return existing_worker
    