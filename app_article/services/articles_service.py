from sqlalchemy.orm import Session
from typing import Optional, List

from app_article.repositories.articles_repository import (
    ArticlesRepository,
    ArticleNotFound,
    VersionConflict,
)
from app_article.models.article import Article
from app_article.utils.errors import InvalidArticleData


class ArticlesService:
    def __init__(self, db: Session):
        self.db = db
        self.articles_repository = ArticlesRepository(db)


    def create_article(self, title: str, content: str) -> Article:

        if not title:
            raise InvalidArticleData("Title cannot be empty")
        if not content:
            raise InvalidArticleData("Content cannot be empty")
        return self.articles_repository.create_article(title, content)

    def get_article(self, article_id: int) -> Article:
        return self.articles_repository.get_article(article_id)


    def list_articles(self, page: int=1, page_size: int=20, title: Optional[str] = None,
                      version_min: Optional[int] = None, version_max: Optional[int] = None) -> List[Article]:

        return self.articles_repository.list_articles(
            page=page, page_size=page_size, title=title, version_min=version_min, version_max=version_max)


    def update_article(self, article_id: int, title: str, content: str, version: int) -> Article:
        if not title.strip():
            raise InvalidArticleData("Title cannot be empty")
        if not content.strip():
            raise InvalidArticleData("Content cannot be empty")

        try:
            self.articles_repository.update_article(
                article_id=article_id, title=title, content=content, expected_version=version)
        except VersionConflict as e :
            raise VersionConflict(str(e))
        except ArticleNotFound as e:
            raise ArticleNotFound(f"Article with id {article_id} not found")


    def patch_article(self, article_id: int, version: int, title: Optional[str]= None,
                    content: Optional[str] = None) -> Article:
        if title is not None and not title.strip():
            raise InvalidArticleData("Title cannot be empty")

        if content is not None and not title.strip():
            raise InvalidArticleData("Content cannot be empty")

        try:
            self.articles_repository.patch_article(
                article_id=article_id, title=title, content=content, expected_version=version
            )
        except VersionConflict as e:
            raise VersionConflict(str(e))
        except ArticleNotFound as e:
            raise ArticleNotFound( f"Article with id {article_id} not found")

    def delete_article(self, article_id: int) -> bool:
        return self.articles_repository.delete_article(article_id)


    def restore_article(self, article_id: int) -> Article:
        try:
            self.articles_repository.restore_article(article_id)
        except ArticleNotFound as e:
            raise ArticleNotFound(f"Article with id {article_id} not found")
