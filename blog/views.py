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
    CommentSerializer, LikeSerializer, UserProfileSerializer, StorySerializer,  VideoSerializer, VideoCommentSerializer,
    ReportSerializer, ReportCommentSerializer, AudioCommentSerializer, AudioSerializer
)
from .models import (Post, Category, Comment, Like, UserProfile, Story, StoryView, Video, VideoComment, VideoLike,
    Report, ReportComment, ReportLike, AudioLike, Audio, AudioComment             
)

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

@api_view(['POST'])
def api_register(request):
    username = request.data.get('username')
    password = request.data.get('password1')
    password2 = request.data.get('password2')

    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if password != password2:
        return Response(
            {'error': 'Passwords do not match'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password)
    return Response(
        {'message': 'User created successfully'},
        status=status.HTTP_201_CREATED
    )


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

# --- Video Views ---
@api_view(['GET'])
def api_videos(request):
    search = request.query_params.get('search', '')
    videos = Video.objects.all().order_by('-created_at')
    if search:
        videos = videos.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    serializer = VideoSerializer(video)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_video_create(request):
    video = Video(author=request.user)
    video.title = request.data.get('title', '')
    video.description = request.data.get('description', '')
    video.background_color = request.data.get('background_color', '')

    if 'video_file' in request.FILES:
        video.video_file = request.FILES['video_file']
    if 'thumbnail' in request.FILES:
        video.thumbnail = request.FILES['thumbnail']

    video.save()
    serializer = VideoSerializer(video)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if video.author != request.user:
        return Response(
            {'error': 'Not authorized'},
            status=status.HTTP_403_FORBIDDEN
        )
    video.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_video_like(request, pk):
    video = get_object_or_404(Video, pk=pk)
    like = VideoLike.objects.filter(video=video, user=request.user)
    if like.exists():
        like.delete()
        return Response({'liked': False, 'total_likes': video.total_likes()})
    else:
        VideoLike.objects.create(video=video, user=request.user)
        return Response({'liked': True, 'total_likes': video.total_likes()})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_video_comment(request, pk):
    video = get_object_or_404(Video, pk=pk)
    serializer = VideoCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, video=video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_video_comment_delete(request, pk):
    comment = get_object_or_404(VideoComment, pk=pk)
    if comment.author != request.user:
        return Response(
            {'error': 'Not authorized'},
            status=status.HTTP_403_FORBIDDEN
        )
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# --- Report Views ---
@api_view(['GET'])
def api_reports(request):
    category = request.query_params.get('category', '')
    urgency = request.query_params.get('urgency', '')
    search = request.query_params.get('search', '')

    reports = Report.objects.all().order_by('-created_at')

    if category:
        reports = reports.filter(category=category)
    if urgency:
        reports = reports.filter(urgency=urgency)
    if search:
        reports = reports.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )

    serializer = ReportSerializer(reports, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.views += 1
    report.save()
    serializer = ReportSerializer(report)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_report_create(request):
    report = Report(author=request.user)
    report.title = request.data.get('title', '')
    report.description = request.data.get('description', '')
    report.location = request.data.get('location', '')
    report.category = request.data.get('category', 'other')
    report.urgency = request.data.get('urgency', 'normal')
    report.latitude = request.data.get('latitude') or None
    report.longitude = request.data.get('longitude') or None

    if 'image' in request.FILES:
        report.image = request.FILES['image']
    if 'video' in request.FILES:
        report.video = request.FILES['video']

    report.save()
    serializer = ReportSerializer(report)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_report_delete(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.author != request.user:
        return Response(
            {'error': 'Not authorized'},
            status=status.HTTP_403_FORBIDDEN
        )
    report.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_report_like(request, pk):
    report = get_object_or_404(Report, pk=pk)
    like = ReportLike.objects.filter(report=report, user=request.user)
    if like.exists():
        like.delete()
        return Response({'liked': False, 'total_likes': report.total_likes()})
    else:
        ReportLike.objects.create(report=report, user=request.user)
        return Response({'liked': True, 'total_likes': report.total_likes()})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_report_comment(request, pk):
    report = get_object_or_404(Report, pk=pk)
    serializer = ReportCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, report=report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_report_comment_delete(request, pk):
    comment = get_object_or_404(ReportComment, pk=pk)
    if comment.author != request.user:
        return Response(
            {'error': 'Not authorized'},
            status=status.HTTP_403_FORBIDDEN
        )
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# --- Audio Views ---
@api_view(['GET'])
def api_audios(request):
    search = request.query_params.get('search', '')
    category = request.query_params.get('category', '')

    audios = Audio.objects.all().order_by('-created_at')

    if search:
        audios = audios.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    if category:
        audios = audios.filter(category=category)

    serializer = AudioSerializer(audios, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_audio_detail(request, pk):
    audio = get_object_or_404(Audio, pk=pk)
    serializer = AudioSerializer(audio)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_audio_create(request):
    audio = Audio(author=request.user)
    audio.title = request.data.get('title', '')
    audio.description = request.data.get('description', '')
    audio.category = request.data.get('category', 'music')
    audio.duration = request.data.get('duration', '')

    if 'audio_file' in request.FILES:
        audio.audio_file = request.FILES['audio_file']
    if 'cover_image' in request.FILES:
        audio.cover_image = request.FILES['cover_image']

    audio.save()
    serializer = AudioSerializer(audio)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_audio_delete(request, pk):
    audio = get_object_or_404(Audio, pk=pk)
    if audio.author != request.user:
        return Response(
            {'error': 'Not authorized'},
            status=status.HTTP_403_FORBIDDEN
        )
    audio.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_audio_like(request, pk):
    audio = get_object_or_404(Audio, pk=pk)
    like = AudioLike.objects.filter(audio=audio, user=request.user)
    if like.exists():
        like.delete()
        return Response({'liked': False, 'total_likes': audio.total_likes()})
    else:
        AudioLike.objects.create(audio=audio, user=request.user)
        return Response({'liked': True, 'total_likes': audio.total_likes()})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_audio_comment(request, pk):
    audio = get_object_or_404(Audio, pk=pk)
    serializer = AudioCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, audio=audio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_audio_comment_delete(request, pk):
    comment = get_object_or_404(AudioComment, pk=pk)
    if comment.author != request.user:
        return Response(
            {'error': 'Not authorized'},
            status=status.HTTP_403_FORBIDDEN
        )
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)