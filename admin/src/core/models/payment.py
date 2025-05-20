from sqlalchemy import Column, Float, Date, Enum, String, Integer, ForeignKey
from datetime import date
from sqlalchemy.orm import relationship
from src.core.database import db

Payment_type = Enum (
    'Salary', #for employees
    'Bonus', #for employees
    'Expense', #for clients/suppliers
    name = "payment_type_enum",
)

class Payment(db.Model):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float,nullable=False)
    date = Column(Date, default=date.today)
    payment_type = Column(Payment_type, nullable=False)
    description = Column(String(200), nullable=True)

    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    employee = relationship('Employee', back_populates="payments")