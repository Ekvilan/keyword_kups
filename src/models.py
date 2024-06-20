from sqlalchemy import String, text, MetaData, create_engine
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional, Annotated
from database import Base, str_12
from datetime import datetime
from config import settings
# Предполагается, что объект метаданных был создан ранее в коде
from sqlalchemy.ext.declarative import declarative_base



# Определение объекта метаданных
metadata_obj = MetaData()

create_add = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"))]

class WorkersOrm(Base):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(primary_key=True)
    cups: Mapped[str_12] = mapped_column(String(12))
    value: Mapped[str] = mapped_column(String)
    create_add: Mapped[create_add]
    
engine = create_engine(settings.DATABASE_URL_psycopg)  # Используйте DATABASE_URL_psycopg из src/config.py
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=metadata_obj)