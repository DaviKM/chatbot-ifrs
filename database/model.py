from database.db import Base
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Mensagem(Base):
    __tablename__ = 'mensagem'

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tel_n : Mapped[str] = mapped_column(String(11))
    content : Mapped[str] = mapped_column(String(1000))
    isfromuser : Mapped[bool] = mapped_column(Boolean)
