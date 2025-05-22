from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from src.core.database import db

class Employee(db.Model):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(8), nullable = False, unique=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

    payments = relationship("Payment", back_populates="employee")

