from rest_framework import serializers
from .models import Category, Like, Post, Comment, UserProfile, Story, Video, VideoComment, ReportComment, Report, ReportLike, Audio, AudioComment, AudioLike
from taggit.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'content', 'date']
        read_only_fields = ['author', 'post', 'author_name']

    def get_author_name(self, obj):
        return obj.author.username


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'date']
        read_only_fields = ['user']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'bio', 'avatar', 'location', 'website']
        extra_kwargs = {
            'bio': {'required': False},
            'avatar': {'required': False},
            'location': {'required': False},
            'website': {'required': False}
        }

    def get_username(self, obj):
        return obj.user.username


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'date',
            'author', 'author_name', 'category', 'category_name',
            'tags', 'image', 'total_likes', 'total_comments', 'comments'
        ]
        read_only_fields = ['author']

    def get_author_name(self, obj):
        return obj.author.username if obj.author else 'Anonymous'

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_total_comments(self, obj):
        return obj.total_comments()


class StorySerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    time_left = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = [
            'id', 'author', 'author_name', 'author_avatar',
            'text', 'image', 'video', 'background_color',
            'created_at', 'expires_at',
            'total_views', 'is_expired', 'time_left'
        ]
        read_only_fields = ['author']
        extra_kwargs = {
            'text': {'required': False},
            'image': {'required': False},
            'video': {'required': False},
            'background_color': {'required': False},
        }

    def get_author_name(self, obj):
        return obj.author.username

    def get_author_avatar(self, obj):
        try:
            profile = obj.author.profile
            if profile.avatar:
                return profile.avatar.url
        except:
            pass
        return None

    def get_total_views(self, obj):
        return obj.views.count()

    def get_is_expired(self, obj):
        return obj.is_expired()

    def get_time_left(self, obj):
        return obj.time_left
    
class VideoCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = VideoComment
        fields = ['id', 'video', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['author', 'video']
        extra_kwargs = {
            'content': {'required': True}
        }

    def get_author_name(self, obj):
        return obj.author.username


class VideoSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    video_comments = VideoCommentSerializer(many=True, read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'video_file',
            'thumbnail', 'created_at', 'author', 'author_name',
            'category', 'category_name', 'tags',
            'total_likes', 'total_comments', 'video_comments'
        ]
        read_only_fields = ['author']
        extra_kwargs = {
            'description': {'required': False},
            'thumbnail': {'required': False},
            'category': {'required': False},
            'tags': {'required': False},
        }

    def get_author_name(self, obj):
        return obj.author.username

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_total_comments(self, obj):
        return obj.total_comments()
    
class ReportCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = ReportComment
        fields = ['id', 'report', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['author', 'report']

    def get_author_name(self, obj):
        return obj.author.username


class ReportSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    report_comments = ReportCommentSerializer(many=True, read_only=True)
    urgency_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'description', 'image', 'video',
            'location', 'latitude', 'longitude',
            'category', 'category_display',
            'urgency', 'urgency_display',
            'created_at', 'is_verified', 'views',
            'author', 'author_name',
            'total_likes', 'total_comments', 'report_comments'
        ]
        read_only_fields = ['author', 'is_verified', 'views']
        extra_kwargs = {
            'image': {'required': False},
            'video': {'required': False},
            'location': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
        }

    def get_author_name(self, obj):
        return obj.author.username

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_total_comments(self, obj):
        return obj.total_comments()

    def get_urgency_display(self, obj):
        return dict(Report.URGENCY_CHOICES).get(obj.urgency, obj.urgency)

    def get_category_display(self, obj):
        return dict(Report.CATEGORY_CHOICES).get(obj.category, obj.category)
    
class AudioCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = AudioComment
        fields = ['id', 'audio', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['author', 'audio']

    def get_author_name(self, obj):
        return obj.author.username


class AudioSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    audio_comments = AudioCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Audio
        fields = [
            'id', 'title', 'description', 'audio_file',
            'cover_image', 'category', 'category_display',
            'created_at', 'duration',
            'author', 'author_name',
            'total_likes', 'total_comments', 'audio_comments'
        ]
        read_only_fields = ['author']
        extra_kwargs = {
            'description': {'required': False},
            'cover_image': {'required': False},
            'duration': {'required': False},
        }

    def get_author_name(self, obj):
        return obj.author.username

    def get_category_display(self, obj):
        return obj.get_category_display()

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_total_comments(self, obj):
        return obj.total_comments()