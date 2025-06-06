from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date
from enum import Enum

class PaymentType(str, Enum):
    salary = "Salary"
    bonus = "Bonus"
    expense = "Expense"

class PaymentCreate(BaseModel):
    amount: float = Field(...)
    date: date 
    payment_type: PaymentType = Field(..., max_length=200)
    description: str 
    employee_id: Optional[int]


    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
    
        if v < date.today():
            raise ValueError("The date must be today or later.")
        return v