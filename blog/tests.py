from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User

from .models import Post


def make_post(author, title, when):
    """Create a Post with an explicit created_at. Post.created_at uses
    auto_now_add, which ignores any value passed to create(), so the
    timestamp has to be set with a separate .update() call."""
    post = Post.objects.create(title=title, content="content", author=author)
    Post.objects.filter(pk=post.pk).update(created_at=when)
    post.refresh_from_db()
    return post


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


class PostDetailTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="ivan", password="a-strong-passw0rd")
        self.post = Post.objects.create(title="Full post", content="The full body text.", author=self.author)

    def test_detail_page_shows_full_content(self):
        response = self.client.get(reverse("blog:post_detail", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Full post")
        self.assertContains(response, "The full body text.")

    def test_unknown_post_returns_404(self):
        response = self.client.get(reverse("blog:post_detail", args=[self.post.pk + 999]))
        self.assertEqual(response.status_code, 404)

    def test_post_list_links_to_detail_page(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, reverse("blog:post_detail", args=[self.post.pk]))


class PostListPaginationTests(TestCase):
    """POSTS_PER_PAGE = 5; 12 posts split into pages of 5, 5, 2."""

    def setUp(self):
        author = User.objects.create_user(username="erin", password="a-strong-passw0rd")
        base = timezone.now()
        for i in range(12):
            make_post(author, f"Post {i}", base - timedelta(days=i))

    def test_first_page_has_a_full_page_of_posts(self):
        response = self.client.get(reverse("blog:post_list"))
        page = response.context["posts"]
        self.assertEqual(len(page), 5)
        self.assertFalse(page.has_previous())
        self.assertTrue(page.has_next())

    def test_last_page_has_the_remainder(self):
        response = self.client.get(reverse("blog:post_list"), {"page": 3})
        page = response.context["posts"]
        self.assertEqual(len(page), 2)
        self.assertFalse(page.has_next())

    def test_out_of_range_page_clamps_to_last_page(self):
        response = self.client.get(reverse("blog:post_list"), {"page": 999})
        self.assertEqual(response.context["posts"].number, 3)

    def test_non_numeric_page_falls_back_to_first_page(self):
        response = self.client.get(reverse("blog:post_list"), {"page": "not-a-number"})
        self.assertEqual(response.context["posts"].number, 1)


class PostListDateFilterTests(TestCase):
    def setUp(self):
        author = User.objects.create_user(username="frank", password="a-strong-passw0rd")
        self.on_date = make_post(
            author, "On date", timezone.make_aware(timezone.datetime(2026, 1, 15, 12, 0))
        )
        make_post(author, "Other date", timezone.make_aware(timezone.datetime(2026, 1, 16, 12, 0)))

    def test_date_filter_returns_only_matching_posts(self):
        response = self.client.get(reverse("blog:post_list"), {"date": "2026-01-15"})
        self.assertEqual(list(response.context["posts"]), [self.on_date])

    def test_no_date_filter_returns_all_posts(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(len(response.context["posts"]), 2)


class PostsByAuthorFilterCombinationTests(TestCase):
    """Covers CLAUDE.md's "easy to break": author filter + date filter together."""

    def setUp(self):
        author = User.objects.create_user(username="grace", password="a-strong-passw0rd")
        other_author = User.objects.create_user(username="heidi", password="a-strong-passw0rd")
        self.match = make_post(
            author, "Match", timezone.make_aware(timezone.datetime(2026, 2, 1, 9, 0))
        )
        make_post(author, "Wrong date", timezone.make_aware(timezone.datetime(2026, 2, 2, 9, 0)))
        make_post(
            other_author, "Wrong author", timezone.make_aware(timezone.datetime(2026, 2, 1, 9, 0))
        )

    def test_author_and_date_filters_combine(self):
        response = self.client.get(
            reverse("blog:posts_by_author"), {"author": "grace", "date": "2026-02-01"}
        )
        self.assertEqual(list(response.context["posts"]), [self.match])

    def test_date_without_author_shows_nothing(self):
        response = self.client.get(reverse("blog:posts_by_author"), {"date": "2026-02-01"})
        self.assertEqual(response.context["posts"].count(), 0)
