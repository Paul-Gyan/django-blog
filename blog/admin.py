from django.contrib import admin
from .models import Post, Category, Comment, Like, UserProfile

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'category','date', 'total_likes', 'total_comments')
    search_fields = ('title', 'content')
    list_filter = ('date', 'category')
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'date')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website')
    
