from database.db import Base
from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Mensagem(Base):
    __tablename__ = 'mensagem'

    id : Mapped[int] = mapped_column(primary_key=True)
    tel_n : Mapped[str] = mapped_column(String(11), nullable=False)
    question : Mapped[str] = mapped_column(String(1000), nullable=False)
    answer : Mapped[str] = mapped_column(String(1000), nullable=False)
    date : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now())

