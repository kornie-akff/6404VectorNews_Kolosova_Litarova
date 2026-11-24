from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from schemas.tag import TagOut

class ArticleBase(BaseModel):
    article_title: str = Field(..., max_length=255)
    content: str

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    article_title: str | None = None
    content: str | None = None

class ArticleOut(ArticleBase):
    article_id: int
    author_id: int
    created_time: datetime
    class Config:
        from_attributes = True

class ArticleDetailOut(ArticleOut):
    tags: List[TagOut] = Field(default_factory=list)
    class Config:
        from_attributes = True

class SimilarArticleOut(BaseModel):
    article_id: int
    article_title: str
    author_id: int
    common_likers: int

class ArticleDetailWithRecommendationsOut(ArticleDetailOut):
    similar_articles: List[SimilarArticleOut] = Field(default_factory=list)