from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime
    marketing_opt_in: bool


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    marketing_opt_in: bool | None = None