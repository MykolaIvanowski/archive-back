from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app_users.db.database import Base

class User(Base):
    __tablename__ = "user"

    id  = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    