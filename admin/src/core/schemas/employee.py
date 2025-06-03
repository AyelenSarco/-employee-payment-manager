from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class EmployeeCreate(BaseModel):
    name: str = Field(...,min_length=2, max_length=50)
    email: EmailStr = Field(...)
    is_active: bool = Field(default=True)
    dni: str  

    @field_validator("dni")
    @classmethod
    def validate_dni(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("DNI must contain only digits.")
        
        
        if len(v) < 7 or len(v) > 8:
            raise ValueError("DNI must be between 7 and 8 digits long.")
        
        
        dni_int = int(v)
        if dni_int < 1000000 or dni_int > 99999999:
            raise ValueError("DNI must be between 1,000,000 and 99,999,999.")

        return v
    
class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(min_length=2, max_length=50)
    email: Optional[EmailStr]
    is_active: Optional[bool]