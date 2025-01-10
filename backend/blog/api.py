from ninja import Router, Query
from typing import List, Optional
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import Blog, Comment
from .schemas import BlogOut, BlogIn, CommentOut, CommentIn

router = Router()

@router.get("/blogs", response=List[BlogOut])
def list_blogs(
    request,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    author_id: Optional[int] = None,
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    search: Optional[str] = None
):
    blogs = Blog.objects.filter(is_active=True)
    
    if start_date:
        blogs = blogs.filter(created_at__gte=start_date)
    if end_date:
        blogs = blogs.filter(created_at__lte=end_date)
    if author_id:
        blogs = blogs.filter(author_id=author_id)
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    if tag_id:
        blogs = blogs.filter(tags__id=tag_id)
    if search:
        blogs = blogs.filter(title__icontains=search)
    
    return blogs

@router.get("/blogs/{blog_id}", response=BlogOut)
def get_blog(request, blog_id: int):
    return get_object_or_404(Blog, id=blog_id)

@router.post("/blogs", response=BlogOut)
def create_blog(request, blog_in: BlogIn):
    if not request.auth:
        return {"error": "Authentication required"}
    
    blog = Blog.objects.create(
        author_id=request.auth["user_id"],
        **blog_in.dict()
    )
    return blog

@router.get("/blogs/{blog_id}/comments", response=List[CommentOut])
def list_comments(request, blog_id: int):
    return Comment.objects.filter(blog_id=blog_id)

@router.post("/blogs/{blog_id}/comments", response=CommentOut)
def create_comment(request, blog_id: int, comment_in: CommentIn):
    if not request.auth:
        return {"error": "Authentication required"}
    
    comment = Comment.objects.create(
        blog_id=blog_id,
        author_id=request.auth["user_id"],
        **comment_in.dict()
    )
    return comment