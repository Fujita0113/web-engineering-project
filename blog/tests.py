from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Post


class PostCreateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dave", password="a-strong-passw0rd")
        self.url = reverse("blog:post_create")

    def test_anonymous_get_redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_anonymous_post_is_rejected(self):
        response = self.client.post(self.url, {"title": "Hi", "content": "Hello"})
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")
        self.assertEqual(Post.objects.count(), 0)

    def test_authenticated_post_creates_post_with_author(self):
        self.client.login(username="dave", password="a-strong-passw0rd")
        response = self.client.post(self.url, {"title": "Hi", "content": "Hello"})
        self.assertRedirects(response, reverse("blog:post_list"))
        post = Post.objects.get()
        self.assertEqual(post.title, "Hi")
        self.assertEqual(post.author, self.user)

    def test_authenticated_get_shows_form(self):
        self.client.login(username="dave", password="a-strong-passw0rd")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")
