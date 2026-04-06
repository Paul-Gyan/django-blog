from rest_framework import serializers
from .models import Category, Like, Post, Comment, UserProfile, Story
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