from ninja import Schema
from datetime import datetime
from typing import Optional, List

class TagSchema(Schema):
    id: int
    title: str

class CategorySchema(Schema):
    id: int
    title: str

class BlogIn(Schema):
    title: str
    description: str
    category_id: Optional[int]
    tag_ids: List[int]

class BlogOut(Schema):
    id: int
    title: str
    description: str
    main_image: Optional[str]
    author_id: int
    category: Optional[CategorySchema]
    tags: List[TagSchema]
    created_at: datetime
    is_active: bool

class CommentIn(Schema):
    content: str
    parent_id: Optional[int]

class CommentOut(Schema):
    id: int
    content: str
    author_id: int
    parent_id: Optional[int]
    likes: int
    dislikes: int
    created_at: datetime