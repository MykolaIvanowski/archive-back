from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class  ArticleRead(BaseModel):
    id: int
    title: str
    content: str
    update_at: datetime

    class Config:
        orm_mode = True


class ArticleUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    version:int = Field(..., ge=1)


class ArticlePatch(BaseModel):
    title: Optional[str] = Field(..., min_length=1, max_length=255)
    content: Optional[str] = Field(..., min_length=1)
    version:int = Field(..., ge=1)


class ArticleAuditLogsReads(BaseModel):
    id: int
    article_id: int
    action: str
    old_data: Optional[dict] = None
    new_data: Optional[dict] = None
    timestamp: datetime

    class Config:
        orm_mode = True