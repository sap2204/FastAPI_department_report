from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date, ForeignKey
from datetime import date



# Класс описывает таблицу задач
class Tasks(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"), nullable=False)
    task: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    days_per_task: Mapped[int] = mapped_column(nullable=False)