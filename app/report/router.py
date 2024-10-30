#from docx import Document
#from collections import defaultdict
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from app.tasks.router import get_tasks_all_workers
from app.tasks.schemas import STasksAllWorkers
from app.workers.dependencies import get_admin_worker
from app.workers.model import Workers
from app.report.dependencies import create_report



router = APIRouter(
    prefix="/report",
    tags=["Отчет отдела"]
)


# Эндпоинт создания отчета по работам всех сотрудников
@router.get("/genetate_report/{starting_date}/{end_date}")
async def generate_report(starting_date: date, 
                          end_date: date,
                          worker: Workers = Depends(get_admin_worker),
                          data_for_report: STasksAllWorkers = Depends(get_tasks_all_workers)
                          ):
    if end_date < starting_date: # проверка дат
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Дата окончания не может быть больше даты начала")
    if worker.role != "admin": # Проверка прав админа
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="У Вас нет прав админа")
    create_report(starting_date, end_date, data_for_report)
    return {"Собщение": "Отчет успешно сформирован"}







