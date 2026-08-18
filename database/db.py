from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

class Base(DeclarativeBase):
    pass


dsn = os.getenv('DATABASE_URL')
engine = create_engine(dsn)

Session = sessionmaker(bind=engine)