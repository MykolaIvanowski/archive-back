from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app_article.db.database import Base


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    version = Column(Integer, nullable=False, default=1)

    delete_at = Column(DateTime(timezone=True), nullable=True,)
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    metadata = Column(JSON, nullable=False, default=dict)
    settings = Column(JSON, nullable=False, default=dict)
    tags = Column(JSON, nullable=False, default=list)

class ArticleAuditLogs(Base):
    __tablename__ = 'article_audit_logs'
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)

    action = Column(String(255), nullable=False) # register - create update delete restored
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


