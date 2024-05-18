from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group

class CustomUserManager(BaseUserManager):
    def create_user(self, email,  password=None,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        blogger_group, created = Group.objects.get_or_create(name='Blogger')
 
        user.save(using=self._db)
        user.groups.add(blogger_group)  # Kullanıcıyı Blogger grubuna ekle
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=101, unique=True)  # unique=True eklendi
    image = models.ImageField(upload_to="industry_images", null=False, blank=True)
    icon_class = models.CharField(max_length=50, help_text="FontAwesome ikon sınıfı, örn: 'fas fa-industry'")
    content = models.TextField(verbose_name="İçerik")
    subdescription = models.CharField(max_length=255, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    def get_absolute_url(self):
        return reverse('industry', kwargs={'pk': self.pk}) 

    def __str__(self):
        return self.name

    def clean(self):
        if len(self.name) > 100:
            raise ValidationError({'name': 'Ensure this value has at most 100 characters (it has {}).'.format(len(self.name))})
        
        if len(self.icon_class) > 50:
            raise ValidationError({'icon_class': 'Ensure this value has at most 50 characters (it has {}).'.format(len(self.icon_class))})

        if len(self.subdescription) > 255:
            raise ValidationError({'subdescription': 'Ensure this value has at most 255 characters (it has {}).'.format(len(self.subdescription))})

    def save(self, *args, **kwargs):
        self.full_clean()  # Bu satır doğrulamanın çalışmasını sağlar
        super().save(*args, **kwargs)