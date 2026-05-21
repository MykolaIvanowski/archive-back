from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app_orders.models.order import OrderStatus


class Order(BaseModel):
    user_id: int
    total_amount: float = Field(..., gt=0)


class OrderRead(BaseModel):
    id = int
    user_id: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderCreated(BaseModel):
    status: OrderStatus


class OrderAmountUpdate(BaseModel):
    total_amount: float = Field(..., gt=0)