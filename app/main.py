from fastapi import FastAPI
from app.workers.router import router as workers_router
from app.tasks.router import router as tasks_router
from app.report.router import router as report_router


app = FastAPI()

app.include_router(workers_router)
app.include_router(tasks_router)
app.include_router(report_router)