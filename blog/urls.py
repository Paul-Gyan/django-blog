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
]