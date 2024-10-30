from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column



# Класс описывает таблицу работников
class Workers(Base):

    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    surname: Mapped[str] = mapped_column(nullable= False)
    name: Mapped[str] = mapped_column(nullable= False)
    middle_name: Mapped[str] = mapped_column(nullable= False)
    login: Mapped[str] = mapped_column(nullable= False)
    password: Mapped[str] = mapped_column(nullable= False)
    role: Mapped[str] = mapped_column(nullable= False)