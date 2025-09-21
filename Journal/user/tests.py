from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class SignupFlowTests(TestCase):
    def test_user_can_signup(self):
        response = self.client.post(
            reverse("user:signup"),
            {
                "username": "newuser",
                "password1": "complex-pass-123",
                "password2": "complex-pass-123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(username="newuser").exists(),
            "Signup should create the new user",
        )
        self.assertEqual(response.url, reverse("entries:home"))


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.password = "complex-pass-123"
        self.user = get_user_model().objects.create_user(
            username="authuser", email="auth@example.com", password=self.password
        )

    def test_login_view_logs_user_in(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "username": self.user.username,
                "password": self.password,
                "next": reverse("entries:home"),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("entries:home"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_view_logs_user_out(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("user:logout"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user:login"))
        self.assertNotIn("_auth_user_id", self.client.session)
