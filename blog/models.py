from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from django.contrib.auth import get_user_model

    
class CustomUser(AbstractUser):
    is_blogger = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

User = get_user_model()

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='blog_covers/', null=True, blank=True)  # Kapak fotoğrafı
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog_post.title}'