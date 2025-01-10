from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from django.contrib.auth import get_user_model
from typing import List
from datetime import datetime
from blog.models import Blog, Category, Tag, Comment, Menu
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        # JWT validation logic here
        return token
api = NinjaAPI(auth=AuthBearer())
# Schemas
class UserSchema(Schema):
    username: str
    email: str
    profile_image: str = None
class BlogSchema(Schema):
    id: int
    title: str
    main_image: str
    description: str
    author: UserSchema
    created_at: datetime
    is_active: bool
class CategorySchema(Schema):
    id: int
    title: str
    parent_id: int = None
class TagSchema(Schema):
    id: int
    title: str
class CommentSchema(Schema):
    id: int
    content: str
    author: UserSchema
    created_at: datetime
    likes: int
    dislikes: int
# Endpoints
@api.get("/blogs", response=List[BlogSchema])
def list_blogs(request):
    return Blog.objects.filter(is_active=True)
@api.get("/categories", response=List[CategorySchema])
def list_categories(request):
    return Category.objects.all()
@api.get("/tags", response=List[TagSchema])
def list_tags(request):
    return Tag.objects.all()
@api.get("/blog/{blog_id}/comments", response=List[CommentSchema])
def list_blog_comments(request, blog_id: int):
    return Comment.objects.filter(blog_id=blog_id)