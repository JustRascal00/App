from django.contrib import admin
from .models import Blog, Category, Tag, Comment, Menu
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'is_active')
    list_filter = ('is_active', 'category', 'tags')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    search_fields = ('title',)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog', 'created_at', 'likes', 'dislikes')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'blog__title')
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'category', 'url')
    list_editable = ('order',)
    ordering = ('order',)