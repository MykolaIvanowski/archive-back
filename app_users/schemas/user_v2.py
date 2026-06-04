from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreateV2(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., min_length=1, max_length=70)

class  UserReadV2(BaseModel):
    id: int
    email: EmailStr
    last_name: str
    first_name: str
    age: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdateV2(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., min_length=1, max_length=70)


class UserPatchV2(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, min_length=1, max_length=70)