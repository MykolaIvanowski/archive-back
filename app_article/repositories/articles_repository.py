from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Optional, List

from app_article.models.article import Article, ArticleAuditLogs
from app_article.utils.errors import ArticleNotFound, VersionConflict

def deep_merge(original: dict, patch: dict):
    for key, value in patch.items():
        if key in original and isinstance(original[key], dict) and isinstance(value, dict):
            original[key] = deep_merge(original[key], value)
        else:
            original[key] =  value
    return original

class ArticlesRepository:
    def __init__(self, db: Session):
        self.db = db

    def _log(self, article_id: int, action: str, old_data: dict, new_data: dict )-> Article:
        log = ArticleAuditLogs(article_id=article_id, action=action,
                               old_data=old_data, new_data=new_data)
        self.db.add(log)

    def create_article(self, title: str, content, metadata: dict, settings: dict, tags: list) -> Article:
        article = Article(title=title, content=content, metadata=metadata, settings=settings, tags=tags)

        with self.db.begin() :
            self.db.add(article)
            self.db.flush() # get article id
            self._log(article_id=article.id, action="created", old_data=None, new_data={"title": title, "content": content})
        self.db.refresh(article)
        return article


    def get_article(self, article_id: int) -> Article:
        article = self.db.get(Article, article_id)
        if not article:
            raise ArticleNotFound(f"Article with id {article_id} not found")
        return article


    def list_articles(self, page: int = 1, page_size: int = 20, title: Optional[str] = None,
                      version_min: Optional[int]=None, version_max: Optional[int] = None) -> List[Article]:
        query = select(Article).where(Article.delete_at.is_(None))
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

    def update_article(self, article_id: int, title: str, content: str, expected_version: int,
                       metadata: dict, settings: dict, tags: list) -> Article:
        article = self.get_article(article_id)
        old_data = {"title": article.title, "content": article.content}
        if article.version != expected_version:
            raise VersionConflict(f"Article version not match expected {expected_version} actual {article.version}")
        article.title = title
        article.content = content
        article.version = expected_version
        article.metadata = metadata
        article.settings = settings
        article.tags = tags

        with self.db.begin():
            self.db.add(article)
            self._log(
                article_id=article.id,
                action="updated",
                old_data=old_data,
                new_data={"title": article.title, "content": article.content}
            )
        self.db.refresh(article)
        return article

    def patch_article(self, article_id: int,expected_version: int, title: Optional[str] = None,
                      content: Optional[str] = None, metadata: Optional[dict]= None,
                      settings: Optional[dict] = None, tags: Optional[list] = None) -> Article:
        article = self.get_article(article_id)
        old_data = {"title": article.title, "content": article.content}
        if article.version != expected_version:
            raise VersionConflict(f"Article version not match expected {expected_version} actual {article.version}")

        if title is not None:
            article.title = title

        if content is not None:
            article.content = content

        if metadata is not None:
            article.metadata = deep_merge(article.metadata, metadata)

        if settings is not None:
            article.settings = deep_merge(article.settings, settings)

        if tags is not None:
            article.tags = tags


        article.version = expected_version + 1

        with self.db.begin():
            self.db.add(article)
            self._log(
                article_id=article.id,
                action="updated",
                old_data=old_data,
                new_data={"title": article.title, "content": article.content}
            )
        self.db.refresh(article)
        return article

    def delete_article(self, article_id: int) -> bool:
        article = self.get_article(article_id)

        with self.db.begin():
            self.db.delete(article)
            self._log(
                article_id=article.id,
                action="deleted",
                old_data={"title": article.title, "content": article.content},
                new_data={"deleted_at": article.delete_at.isoformat()}
            )
        return True


    def restore_article(self, article_id: int) -> Article:
        article = self.db.get(Article,article_id)
        if not article:
            raise ArticleNotFound(f"Article with id {article_id} not found")
        if article.deleted_at is None:
            return article
        old_data = {"delete_at": article.delete_at.isoformat()}
        article.delete_at = None
        with self.db.begin():
            self.db.add(article)
            self._log(
                article_id=article.id,
                action="restored",
                old_data=old_data,
                new_data={"delete_at": None}
            )
            self.db.refresh(article)
            return article