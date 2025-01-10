from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    class Meta:
        permissions = [
            ("view_api_docs", "Can view API documentation"),
        ]
    def __str__(self):
        return self.username