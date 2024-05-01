from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from django.contrib.auth import get_user_model

    
class CustomUser(AbstractUser):
    is_blogger = models.BooleanField(default=False)


User = get_user_model()

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='blog_covers/', null=True, blank=True)  # Kapak fotoğrafı
    def __str__(self):
        return self.title