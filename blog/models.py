from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
# 
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager(blank=True)  
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
    def total_comments(self):
        return self.comments.count()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'Like by {self.user.username} likes {self.post.title}'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'
