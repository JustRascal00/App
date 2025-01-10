from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
class Category(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']
    def __str__(self):
        return self.title
class Tag(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title
class Blog(models.Model):
    title = models.CharField(max_length=200)
    main_image = models.ImageField(upload_to='blog_images/')
    description = HTMLField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.title
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'
class Menu(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    url = models.URLField(null=True, blank=True)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title