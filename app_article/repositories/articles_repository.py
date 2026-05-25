from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Optional, List

from app_article.models.article import Article
from app_article.utils.errors import ArticleNotFound, VersionConflict


class ArticlesRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_article(self, title: str, content) -> Article:
        article = Article(title=title, content=content)

        with self.db.begin() :
            self.db.add(article)

        self.db.refresh(article)
        return article


    def get_article(self, article_id: int) -> Article:
        article = self.db.get(Article, article_id)
        if not article:
            raise ArticleNotFound(f"Article with id {article_id} not found")
        return article


    def list_articles(self, page: int = 1, page_size: int = 20, title: Optional[str] = None,
                      version_min: Optional[int]=None, version_max: Optional[int] = None) -> List[Article]:
        query = select(Article)
        conditions= []
        if title:
            conditions.append(Article.title.ilike(f"%{title}%"))

        if version_min is not None:
            conditions.append(Article.version >= version_min)

        if version_max is not None:
            conditions.append(Article.version <= version_max)
        if conditions:
            query = query.filter(and_(*conditions))

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        return self.db.execute(query).scalars().all()

    def update_article(self, article_id: int, title: str, content: str, expected_version: int) -> Article:
        article = self.get_article(article_id)

        if article.version != expected_version:
            raise VersionConflict(f"Article version not match expected {expected_version} actual {article.version}")
        article.title = title
        article.content = content
        article.version = expected_version

        with self.db.begin():
            self.db.add(article)
        self.db.refresh(article)
        return article

    def patch_article(self, article_id: int,expected_version: int, title: Optional[str] = None,
                      content: Optional[str] = None) -> Article:
        article = self.get_article(article_id)

        if article.version != expected_version:
            raise VersionConflict(f"Article version not match expected {expected_version} actual {article.version}")

        if title is not None:
            article.title = title

        if content is not None:
            article.content = content

        article.version = expected_version + 1

        with self.db.begin():
            self.db.add(article)
        self.db.refresh(article)
        return article

    def delete_article(self, article_id: int) -> bool:
        article = self.get_article(article_id)

        with self.db.begin():
            self.db.delete(article)

        return True
