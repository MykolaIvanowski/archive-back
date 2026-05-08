from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=1, le=120)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    age: Optional[int]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=1, le=120)


class UserPatch(BaseModel):
    email: EmailStr
    first_name: str =  Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=1, le=120)
    

class UserLogin(BaseModel):
    pass