from app.dao.base import BaseDAO
from app.workers.model import Workers


# Класс для работы с таблицей Workers в БД
class WorkersDAO(BaseDAO):
    
    model = Workers