from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content'
        )

    def test_post_created_successfully(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Test Content')

    def test_post_str_returns_title(self):
        self.assertEqual(str(self.post), 'Test Post')


class PostAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content'
        )

    def test_get_all_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_post(self):
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Post',
            'content': 'New Content'
        }
        response = self.client.post('/api/posts/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_unauthenticated(self):
        data = {
            'title': 'New Post',
            'content': 'New Content'
        }
        response = self.client.post('/api/posts/create/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_nonexistent_post(self):
        response = self.client.get('/api/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserAuthTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_get_token(self):
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_credentials(self):
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)