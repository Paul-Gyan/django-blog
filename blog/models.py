from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from datetime import timedelta
from django.utils import timezone
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
    
def story_expiry():
    return timezone.now() + timedelta(hours=48)

class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='stories/', null=True, blank=True)
    video = models.FileField(upload_to='stories/videos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=story_expiry)
    background_color = models.CharField(max_length=20, default='#1d4ed8')

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'

    def __str__(self):
        return f'{self.author.username} story at {self.created_at}'

    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def time_left(self):
        remaining = self.expires_at - timezone.now()
        hours = int(remaining.total_seconds() // 3600)
        return max(0, hours)
        
class StoryView(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'viewer')

    def __str__(self):
        return f'{self.viewer.username} viewed {self.story}'


class Video(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.video_likes.count()

    def total_comments(self):
        return self.video_comments.count()


class VideoLike(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')

    def __str__(self):
        return f'{self.user.username} likes {self.video.title}'


class VideoComment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.video.title}'
    
class Report(models.Model):
    URGENCY_CHOICES = [
        ('breaking', '🔴 Breaking'),
        ('normal', '🟡 Normal'),
        ('update', '🔵 Update'),
    ]

    CATEGORY_CHOICES = [
        ('crime', '🚨 Crime'),
        ('weather', '⛈️ Weather'),
        ('traffic', '🚗 Traffic'),
        ('community', '👥 Community'),
        ('fire', '🔥 Fire'),
        ('medical', '🏥 Medical'),
        ('politics', '🏛️ Politics'),
        ('other', '📌 Other'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='reports/images/', null=True, blank=True)
    video = models.FileField(upload_to='reports/videos/', null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.urgency} - {self.title}'

    def total_likes(self):
        return self.report_likes.count()

    def total_comments(self):
        return self.report_comments.count()


class ReportLike(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='report_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('report', 'user')

    def __str__(self):
        return f'{self.user.username} likes {self.report.title}'


class ReportComment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='report_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.report.title}'
    
class Audio(models.Model):
    CATEGORY_CHOICES = [
        ('music', '🎵 Music'),
        ('podcast', '🎙️ Podcast'),
        ('voice', '🎤 Voice Note'),
        ('sermon', '⛪ Sermon'),
        ('audiobook', '📚 Audiobook'),
        ('other', '📌 Other'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='audio/')
    cover_image = models.ImageField(upload_to='audio/covers/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='music')
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.audio_likes.count()

    def total_comments(self):
        return self.audio_comments.count()


class AudioLike(models.Model):
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='audio_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('audio', 'user')

    def __str__(self):
        return f'{self.user.username} likes {self.audio.title}'


class AudioComment(models.Model):
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='audio_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.audio.title}'
    
