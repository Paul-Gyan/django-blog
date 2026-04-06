from rest_framework import serializers
from .models import Category, Like, Post, Comment, UserProfile, Category
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','post', 'author','author_name', 'content', 'date']
        read_only_fields = ['author']

    def get_author(self, obj):
        return obj.author.username 
    
class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = ['id','post', 'user', 'date']
        read_only_fields = ['user']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'bio','avatar', 'location', 'website']

    def get_username(self, obj):
        return obj.user.username

   
class PostSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    author_name = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date', 'tags', 'author_name','author','image', 'total_likes', 'total_comments', 'comments']
        read_only_fields = ['author']

    def get_author_name(self, obj):
        return obj.author.username if obj.author else 'Anonymous'
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_total_likes(self, obj):
        return obj.total_likes()
    
    def get_total_comments(self, obj):
        return obj.total_comments()