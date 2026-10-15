
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class AuthenticationAPITests(APITestCase):
    def setUp(self):
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.email = 'testuser@example.com'
        self.password = 'StrongPass123!'

    def test_user_registration(self):
        response = self.client.post(
            self.register_url,
            {
                'first_name': 'Test',
                'last_name': 'User',
                'email': self.email,
                'password': self.password,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(email=self.email).exists()
        )

    def test_duplicate_email_registration(self):
        User.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password,
        )

        response = self.client.post(
            self.register_url,
            {
                'first_name': 'Another',
                'last_name': 'User',
                'email': self.email,
                'password': self.password,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_login(self):
        User.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password,
        )

        response = self.client.post(
            self.login_url,
            {
                'email': self.email,
                'password': self.password,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
