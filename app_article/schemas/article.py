from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Optional
from datetime import datetime


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)

    metadata: Dict = Field(default_factory=dict)
    settings: Dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class  ArticleRead(BaseModel):
    id: int
    title: str
    content: str
    update_at: datetime

    metadata: Dict
    settings: Dict
    tags: List[str]

    class Config:
        orm_mode = True


class ArticleUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    version:int = Field(..., ge=1)

    metadata: Dict = Field(default_factory=dict)
    settings: Dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)

class ArticlePatch(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    version:int = Field(..., ge=1)

    metadata: Optional[Dict] = None
    settings: Optional[Dict] = None
    tags: Optional[List[str]] = None

class ArticleAuditLogsReads(BaseModel):
    id: int
    article_id: int
    action: str
    old_data: Optional[dict] = None
    new_data: Optional[dict] = None
    timestamp: datetime

    
    class Config:
        orm_mode = True