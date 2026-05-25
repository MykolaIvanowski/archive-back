from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app_article.db.database import Base


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    update_at = Column(DateTime, default=func.now())
