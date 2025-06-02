from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50,
                      description="Should have at least 2 characters")
    email: EmailStr = Field(...)
    hashed_password: str = Field(..., min_length=4, max_length=128)
    rol_id: int = Field(...,ge=1, le=2)
    is_active: bool = Field(default=True)
    sys_admin: bool = Field(default=False)
    creation_date: date

    @field_validator("creation_date")
    @classmethod
    def validate_creation_date(cls, v):
    
        if v < date.today():
            raise ValueError("The date must be today or later.")
        return v
    
class UserUpdate(BaseModel):
    name: Optional[str] = Field(min_length=2,max_length=128)
    rol_id: Optional[int] = Field(ge=1,le=2)
    is_active: Optional[bool] 
    sys_admin: Optional[bool] 