from sqlalchemy import Column, String, Integer, Boolean, Date, Enum
from datetime import date
from src.core.database import db

Rol = Enum (
    'Administrator',
    'Viewer',
    name = "user_rol_enum"
)


class User(db.Model):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50),nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    rol = Column(Rol, nullable=False)
    hashed_password = Column(String(10))
    is_active = Column(Boolean, default=True)
    creation_date = Column(Date, default=date.today)
    

    