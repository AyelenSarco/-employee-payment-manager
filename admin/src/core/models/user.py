from sqlalchemy import Column, String, Integer, Boolean, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from src.core.database import db



class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50),nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(200))
    is_active = Column(Boolean, default=True)
    creation_date = Column(Date, default=date.today)
    sys_admin = Column(Boolean, default=False, nullable=False )
    
    rol_id = Column(Integer, ForeignKey("roles.id"))
    rol = relationship("Rol", back_populates="users")
    

    