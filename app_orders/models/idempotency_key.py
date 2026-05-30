from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app_orders.db.database import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_key"

    id = Column(Integer, primary_key=True)

    key = Column(String(255), unique=True, nullable=False, index=True)

    status = Column(String(50), nullable=False, default="processing")
    response = Column(JSON, nullable=True)

    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())