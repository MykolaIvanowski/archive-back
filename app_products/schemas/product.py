from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str = Field(..., max_length=1, max_digits=255)
    category: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    in_stock: bool = True


class ProductRead(BaseModel):
    id: int
    name: str
    category: str
    price: float
    in_stock: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    in_stock: bool

class ProductPatch(BaseModel):
    name: Optional[str] = Field(..., min_length=1, max_length=255)
    category: Optional[str] = Field(..., min_length=1, max_length=100)
    price: Optional[float] = Field(..., gt=0)
    in_stock: Optional[bool] = None

