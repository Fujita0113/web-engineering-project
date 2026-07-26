from django.test import TestCase
from django.urls import reverse

from .models import User


class RegisterTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "alice",
                "password1": "a-strong-passw0rd",
                "password2": "a-strong-passw0rd",
            },
        )
        self.assertRedirects(response, reverse("blog:post_list"))
        self.assertTrue(User.objects.filter(username="alice").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "bob",
                "password1": "a-strong-passw0rd",
                "password2": "does-not-match",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="bob").exists())


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="carol", password="a-strong-passw0rd")

    def test_login_with_correct_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "carol", "password": "a-strong-passw0rd"},
        )
        self.assertRedirects(response, reverse("blog:post_list"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "carol", "password": "wrong-password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout(self):
        self.client.login(username="carol", password="a-strong-passw0rd")
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("blog:post_list"))
        self.assertNotIn("_auth_user_id", self.client.session)
