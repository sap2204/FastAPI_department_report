from pydantic import BaseModel


# Схема для валидации переданных данных о работнике
class SWorkers(BaseModel):
    
    surname: str
    name: str
    middle_name: str
    login: str
    password: str
    role: str


# Схема для залогинивания (аутентификации и авторизации)
class SAuthWorkers(BaseModel):
    
    login: str
    password: str


# Схема для обновления работника (т.к. в этой схеме указываем, что все данные не обязательны)
class SUpdateWorkers(BaseModel):
    
    surname: str | None = None
    name: str | None = None
    middle_name: str | None = None
    login: str | None = None
    password: str | None = None
    role: str | None = None