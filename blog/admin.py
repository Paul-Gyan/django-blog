from django.contrib import admin
from .models import Post, Category, Comment, Like, UserProfile, Story, Video, VideoLike, VideoComment,Report,ReportLike, ReportComment, Audio, AudioComment, AudioLike

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

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'total_likes', 'total_comments']
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'category']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'urgency', 'created_at', 'is_verified']
    list_filter = ['category', 'urgency', 'is_verified']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_verified']

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'total_likes']
    list_filter = ['category', 'created_at']
    search_fields = ['title','description']