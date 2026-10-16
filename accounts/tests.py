from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.email = "testuser@example.com"
        self.password = "StrongPass123!"

    def register_data(self, **overrides):
        data = {
            "name": "Test User",
            "email": self.email,
            "password": self.password,
        }
        data.update(overrides)
        return data

    def test_user_registration_hashes_password_and_omits_it_from_response(self):
        response = self.client.post(
            self.register_url,
            self.register_data(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.email)
        self.assertEqual(user.first_name, "Test User")
        self.assertNotEqual(user.password, self.password)
        self.assertNotIn("password", response.data["user"])
        self.assertEqual(response.data["user"]["name"], "Test User")

    def test_duplicate_email_registration_is_rejected_case_insensitively(self):
        User.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password,
        )

        response = self.client.post(
            self.register_url,
            self.register_data(email=self.email.upper()),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_registration_data_is_rejected(self):
        response = self.client.post(
            self.register_url,
            {"email": "not-an-email", "password": "short"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_requires_a_name(self):
        response = self.client.post(
            self.register_url,
            {
                "email": self.email,
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_legacy_first_and_last_name_registration_remains_supported(self):
        response = self.client.post(
            self.register_url,
            {
                "first_name": "Test",
                "last_name": "User",
                "email": self.email,
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["name"], "Test User")

    def test_jwt_login_returns_access_and_refresh_tokens(self):
        User.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password,
        )

        response = self.client.post(
            self.login_url,
            {"email": self.email.upper(), "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login_credentials_are_rejected(self):
        User.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password,
        )

        response = self.client.post(
            self.login_url,
            {"email": self.email, "password": "WrongPassword123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_current_user_requires_and_accepts_a_valid_jwt(self):
        user = User.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password,
        )
        current_user_url = reverse("current-user")

        unauthorized = self.client.get(current_user_url)
        self.assertEqual(
            unauthorized.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.client.force_authenticate(user=user)
        authenticated = self.client.get(current_user_url)
        self.assertEqual(authenticated.status_code, status.HTTP_200_OK)
        self.assertEqual(authenticated.data["email"], self.email)

        self.client.force_authenticate(user=None)
        login = self.client.post(
            self.login_url,
            {"email": self.email, "password": self.password},
            format="json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login.data['access']}"
        )
        jwt_response = self.client.get(current_user_url)
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        self.assertEqual(jwt_response.data["id"], user.id)
