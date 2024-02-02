from pydantic import *
from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import date
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(45), nullable=False)
    email = Column(String(45), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    date_of_birth: date
