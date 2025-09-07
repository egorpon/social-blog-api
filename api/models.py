from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# Create your models here.

class User(AbstractUser):
    pass

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        

class Post(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank= True, null=True)

    def __str__(self):
        return f'{self.title} by {self.user.username}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='DELETED USER')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.text} by {self.user.username}'
    