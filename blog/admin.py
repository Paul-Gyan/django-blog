from django.contrib import admin
from .models import Post, Category, Comment, Like, UserProfile, Story

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'category', 'total_likes', 'total_comments')
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

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['author', 'created_at', 'expires_at', 'get_time_left']
    list_filter = ['author', 'created_at']

    def get_time_left(self, obj):
        return f'{obj.time_left} hours'
    get_time_left.short_description = 'Time Left'