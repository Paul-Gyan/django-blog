from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    PostSerializer, CategorySerializer,
    CommentSerializer, LikeSerializer, UserProfileSerializer, StorySerializer
)
from .models import Post, Category, Comment, Like, UserProfile, Story, StoryView
from .forms import PostForm
from django.utils import timezone


# --- Template Views ---
def home(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'blog/home.html', {'posts': posts})

def about(request):
    return render(request, 'blog/about.html')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/post_delete.html', {'post': post})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


# --- API Views ---
@api_view(['GET'])
def api_posts(request):
    search = request.query_params.get('search', '')
    category = request.query_params.get('category', '')
    tag = request.query_params.get('tag', '')
    page = int(request.query_params.get('page', 1))

    posts = Post.objects.all().order_by('-date')

    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(author__username__icontains=search) |
            Q(category__name__icontains=search)
        ).distinct()
        
    if category:
        posts = posts.filter(category__slug=category)
    if tag:
        posts = posts.filter(tags__name__in=[tag])

    page_size = 5
    start = (page - 1) * page_size
    end = start + page_size
    total = posts.count()

    serializer = PostSerializer(posts[start:end], many=True)
    return Response({
        'posts': serializer.data,
        'total': total,
        'pages': (total + page_size - 1) // page_size,
        'current_page': page
    })


@api_view(['GET'])
def api_post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(post=post, user=request.user)
    if like.exists():
        like.delete()
        return Response({'liked': False, 'total_likes': post.total_likes()})
    else:
        Like.objects.create(post=post, user=request.user)
        return Response({'liked': True, 'total_likes': post.total_likes()})


@api_view(['GET'])
def api_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['GET', 'PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def api_profile_update(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_stories(request):
    # Only return active non-expired stories
    stories = Story.objects.filter(
        expires_at__gt=timezone.now()
    ).order_by('-created_at')
    serializer = StorySerializer(stories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_story_create(request):
    story = Story(author=request.user)
    story.text = request.data.get('text', '')
    story.background_color = request.data.get('background_color', '#1d4ed8')

    if 'image' in request.FILES:
        story.image = request.FILES['image']
    if 'video' in request.FILES:
        story.video = request.FILES['video']

    story.save()
    serializer = StorySerializer(story)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def api_story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.is_expired():
        return Response(
            {'error': 'Story has expired'},
            status=status.HTTP_404_NOT_FOUND
        )
    # Track view if user is authenticated
    if request.user.is_authenticated:
        StoryView.objects.get_or_create(
            story=story,
            viewer=request.user
        )
    serializer = StorySerializer(story)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_story_delete(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.author != request.user:
        return Response(
            {'error': 'Not authorized'},
            status=status.HTTP_403_FORBIDDEN
        )
    story.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)