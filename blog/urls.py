from django.urls import path
from . import views

urlpatterns = [
    # Template views
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # API endpoints
    path('api/register/', views.api_register, name='api_register'),
    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/posts/create/', views.api_post_create, name='api_post_create'),
    path('api/posts/<int:pk>/', views.api_post_detail, name='api_post_detail'),
    path('api/posts/<int:pk>/edit/', views.api_post_edit, name='api_post_edit'),
    path('api/posts/<int:pk>/delete/', views.api_post_delete, name='api_post_delete'),
    path('api/posts/<int:pk>/like/', views.api_like_toggle, name='api_like_toggle'),
    path('api/posts/<int:pk>/comment/', views.api_comment_create, name='api_comment_create'),
    path('api/comments/<int:pk>/delete/', views.api_comment_delete, name='api_comment_delete'),
    path('api/categories/', views.api_categories, name='api_categories'),
    path('api/profile/update/', views.api_profile_update, name='api_profile_update'),
    path('api/profile/<str:username>/', views.api_profile, name='api_profile'),
    # Story endpoints
    path('api/stories/', views.api_stories, name='api_stories'),
    path('api/stories/create/', views.api_story_create, name='api_story_create'),
    path('api/stories/<int:pk>/', views.api_story_detail, name='api_story_detail'),
    path('api/stories/<int:pk>/delete/', views.api_story_delete, name='api_story_delete'),
    # Video endpoints
    path('api/videos/', views.api_videos, name='api_videos'),
    path('api/videos/create/', views.api_video_create, name='api_video_create'),
    path('api/videos/<int:pk>/', views.api_video_detail, name='api_video_detail'),
    path('api/videos/<int:pk>/delete/', views.api_video_delete, name='api_video_delete'),
    path('api/videos/<int:pk>/like/', views.api_video_like, name='api_video_like'),
    path('api/videos/<int:pk>/comment/', views.api_video_comment, name='api_video_comment'),
    path('api/videos/comments/<int:pk>/delete/', views.api_video_comment_delete, name='api_video_comment_delete'),
    # Report endpoints
    path('api/reports/', views.api_reports, name='api_reports'),
    path('api/reports/create/', views.api_report_create, name='api_report_create'),
    path('api/reports/<int:pk>/', views.api_report_detail, name='api_report_detail'),
    path('api/reports/<int:pk>/delete/', views.api_report_delete, name='api_report_delete'),
    path('api/reports/<int:pk>/like/', views.api_report_like, name='api_report_like'),
    path('api/reports/<int:pk>/comment/', views.api_report_comment, name='api_report_comment'),
    path('api/reports/comments/<int:pk>/delete/', views.api_report_comment_delete, name='api_report_comment_delete'),
    # Audio endpoints
    path('api/audios/', views.api_audios, name='api_audios'),
    path('api/audios/create/', views.api_audio_create, name='api_audio_create'),
    path('api/audios/<int:pk>/', views.api_audio_detail, name='api_audio_detail'),
    path('api/audios/<int:pk>/delete/', views.api_audio_delete, name='api_audio_delete'),
    path('api/audios/<int:pk>/like/', views.api_audio_like, name='api_audio_like'),
    path('api/audios/<int:pk>/comment/', views.api_audio_comment, name='api_audio_comment'),
    path('api/audios/comments/<int:pk>/delete/', views.api_audio_comment_delete, name='api_audio_comment_delete'),
]   