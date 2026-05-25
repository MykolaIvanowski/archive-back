from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app_article.db.database import SessionLocal, get_db
from app_article.services.articles_service import (
    ArticlesService,
    InvalidArticleData,
)
from app_article.repositories.articles_repository import (
    ArticleNotFound,
    VersionConflict,
)
from app_article.schemas.article import (
    ArticleCreate,
    ArticleRead,
    ArticleUpdate,
    ArticlePatch,
)


router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("/", response_model=ArticleRead, status_code=201)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)):
    service = ArticlesService(db=db)

    try:
        return service.create_article(title=payload.title, content=payload.content)
    except InvalidArticleData as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{article_id}", response_model=ArticleRead)
def get_article(article_id: int, db: Session = Depends(get_db)):
    service = ArticlesService(db=db)

    try:
        return service.get_article(article_id)
    except ArticleNotFound as e:
        raise HTTPException(status_code=404, detail="Article not found")


@router.get("/", response_model=List[ArticleRead])
def list_articles(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                  title: Optional[str] = None, version_min: Optional[int] = None, version_max: Optional[int] = None,
                  db: Session = Depends(get_db)):
    service = ArticlesService(db=db)
    return service.list_articles(page=page, page_size=page_size, title=title,
                                 version_min=version_min, version_max=version_max)


@router.put("/{article_id}", response_model=ArticleRead)
def update_article(article_id: int, payload: ArticleUpdate, db: Session = Depends(get_db)):
    service = ArticlesService(db=db)
    try:
        return service.update_article(article_id, title=payload.title, content=payload.content,version=payload.version)
    except ArticleNotFound as e:
        raise HTTPException(status_code=404, detail="Article not found")
    except InvalidArticleData as e:
        raise HTTPException(status_code=400, detail=str(e))
    except VersionConflict as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/{article_id}", response_model=ArticleRead)
def patch_article(article_id: int, payload: ArticleUpdate, db: Session = Depends(get_db)):
    service = ArticlesService(db=db)

    try:
        return service.update_article(article_id=article_id, title=payload.title, content=payload.content,
                                      version=payload.version)
    except ArticleNotFound as e:
        raise HTTPException(status_code=404, detail="Article not found")
    except InvalidArticleData as e:
        raise HTTPException(status_code=400, detail=str(e))
    except VersionConflict as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.delete("/{article_id}", status_code=204)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    service = ArticlesService(db=db)
    try:
        service.delete_article(article_id)
        return
    except ArticleNotFound as e:
        raise HTTPException(status_code=404, detail="Article not found")

