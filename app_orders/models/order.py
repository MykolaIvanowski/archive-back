from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app_orders.db.database import Base


class OrderStatus(str, enum.Enum):
    pending = 'pending'
    paid = 'paid'
    canceled = 'canceled'


class Order(Base):
    __tablename__ = "orders"

    id  = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    user = relationship("User")
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.pending)
    total_amount = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())