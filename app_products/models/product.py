from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, true
from sqlalchemy.sql import func
from app_products.db.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True),
    price = Column(Numeric(10,2), nullable=False)
    in_stock = Column(Boolean, nullable=False, default=True)
    created_at =  Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    