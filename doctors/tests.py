from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Doctor


class DoctorAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="doctor-manager@example.com",
            email="doctor-manager@example.com",
            password="StrongPass123!",
        )
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("doctor-list-create")

    def doctor_data(self, **overrides):
        data = {
            "name": "Dr. Asha Rao",
            "specialization": "Cardiology",
            "email": "asha.rao@example.com",
            "phone": "+911234567890",
            "qualification": "MBBS, MD",
            "experience_years": 12,
        }
        data.update(overrides)
        return data

    def test_authenticated_user_can_create_list_retrieve_update_and_delete(self):
        created = self.client.post(
            self.list_url,
            self.doctor_data(),
            format="json",
        )
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        doctor_id = created.data["id"]
        detail_url = reverse("doctor-detail", args=[doctor_id])

        listed = self.client.get(self.list_url)
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listed.data), 1)

        retrieved = self.client.get(detail_url)
        self.assertEqual(retrieved.status_code, status.HTTP_200_OK)

        updated = self.client.put(
            detail_url,
            self.doctor_data(
                name="Dr. Asha Rao",
                specialization="Neurology",
            ),
            format="json",
        )
        self.assertEqual(updated.status_code, status.HTTP_200_OK)
        self.assertEqual(updated.data["specialization"], "Neurology")

        deleted = self.client.delete(detail_url)
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(pk=doctor_id).exists())

    def test_unauthenticated_user_cannot_access_doctors(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_doctor_data_is_rejected(self):
        response = self.client.post(
            self.list_url,
            self.doctor_data(experience_years=81),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_doctor_email_is_rejected(self):
        Doctor.objects.create(**self.doctor_data())

        response = self.client.post(
            self.list_url,
            self.doctor_data(name="Dr. Other"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexistent_doctor_returns_not_found(self):
        response = self.client.get(reverse("doctor-detail", args=[99999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
