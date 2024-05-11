from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        blogger_group, created = Group.objects.get_or_create(name='Blogger')
 
        if role:
            user.role = role
        user.save(using=self._db)
        user.groups.add(blogger_group)  # Kullanıcıyı Blogger grubuna ekle
        return user

    def create_superuser(self, email, password=None, role=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if role:
            raise ValueError('Superuser cannot have a role.')

        return self.create_user(email, password, role, **extra_fields)

class CustomUser(AbstractUser):
    is_blogger = models.BooleanField(default=False)
    objects = CustomUserManager()



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
    cover_image = models.ImageField(upload_to='blog_covers/', null=False, blank=True)  # Kapak fotoğrafı
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk}) 
    

class Comment(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog_post.title}'





class Industry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="industries", verbose_name="Kullanıcı")
    name = models.CharField(max_length=100, verbose_name="Endüstri Adı")
    image = models.ImageField(upload_to="industry_images", null=False, blank=True, verbose_name="Endüstri Resmi")
    icon_class = models.CharField(max_length=50, verbose_name="Endüstri İkon Sınıfı", help_text="FontAwesome ikon sınıfı, örn: 'fas fa-industry'")
    content = models.TextField(verbose_name="İçerik")
    subdescription = models.CharField(max_length=255, verbose_name="Alt Açıklama", blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Endüstri"
        verbose_name_plural = "Endüstriler"

    def get_absolute_url(self):
        return reverse('industry', kwargs={'pk': self.pk}) 
    def __str__(self):
        return self.name