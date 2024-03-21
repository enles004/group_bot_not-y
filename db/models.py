from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    subject = Column(String, unique=False)
    lesson = Column(String, unique=False)
    day = Column(String, unique=False)
    day_int = Column(Integer, unique=False)
    room = Column(String, unique=False)
    created = Column(DateTime(timezone=True), default=func.now())

