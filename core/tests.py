from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Like, Subscription


class HomePageTests(TestCase):
    """Tests for the home page."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_home_page_opens_for_anonymous(self):
        """Anonymous user can open the home page (status 200)."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_opens_for_logged_in_user(self):
        """Logged-in user can open the home page."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class PostTests(TestCase):
    """Tests for creating posts."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_anonymous_cannot_create_post(self):
        """Anonymous user is redirected to login when creating a post."""
        response = self.client.post(reverse('create-post'), {'text': 'Hello'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

    def test_logged_in_user_can_create_post(self):
        """Logged-in user can create a post via the form."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('create-post'),
            {'text': 'My first post'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.text, 'My first post')
        self.assertEqual(post.author, self.user)


class LikeTests(TestCase):
    """Tests for the like functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(author=self.user, text='Test post')
        self.client.login(username='testuser', password='testpass123')

    def test_like_creates_record(self):
        """Liking a post creates a Like record."""
        self.client.post(reverse('like-post', args=[self.post.id]))
        self.assertEqual(Like.objects.count(), 1)
        self.assertTrue(
            Like.objects.filter(post=self.post, user=self.user).exists()
        )

    def test_second_like_removes_it(self):
        """Liking the same post twice removes the like (toggle)."""
        self.client.post(reverse('like-post', args=[self.post.id]))
        self.client.post(reverse('like-post', args=[self.post.id]))
        self.assertEqual(Like.objects.count(), 0)


class SubscriptionTests(TestCase):
    """Tests for the subscription functionality."""

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        self.client.login(username='user1', password='testpass123')

    def test_user_can_subscribe_to_another(self):
        """User can subscribe to another user."""
        self.client.post(reverse('subscribe', args=[self.user2.id]))
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertTrue(
            Subscription.objects.filter(
                subscriber=self.user1, target=self.user2
            ).exists()
        )

    def test_user_cannot_subscribe_to_self(self):
        """User cannot subscribe to themselves."""
        self.client.post(reverse('subscribe', args=[self.user1.id]))
        self.assertEqual(Subscription.objects.count(), 0)