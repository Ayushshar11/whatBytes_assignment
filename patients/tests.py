from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from doctors.models import Doctor
from .models import Patient, PatientDoctorMapping


class PatientAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="patient-owner@example.com",
            email="patient-owner@example.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="other-owner@example.com",
            email="other-owner@example.com",
            password="StrongPass123!",
        )
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("patient-list-create")

    def patient_data(self, **overrides):
        data = {
            "name": "Jordan Smith",
            "age": 35,
            "gender": "Other",
            "address": "12 Sample Street",
            "phone": "+911234567890",
            "medical_history": "No known allergies",
        }
        data.update(overrides)
        return data

    def test_authenticated_user_can_create_list_retrieve_update_and_delete(self):
        created = self.client.post(
            self.list_url,
            self.patient_data(user=self.other_user.id),
            format="json",
        )
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        patient = Patient.objects.get(pk=created.data["id"])
        self.assertEqual(patient.user_id, self.user.id)
        self.assertNotIn("user", created.data)
        detail_url = reverse("patient-detail", args=[patient.id])

        listed = self.client.get(self.list_url)
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in listed.data], [patient.id])

        retrieved = self.client.get(detail_url)
        self.assertEqual(retrieved.status_code, status.HTTP_200_OK)

        updated = self.client.put(
            detail_url,
            self.patient_data(age=36),
            format="json",
        )
        self.assertEqual(updated.status_code, status.HTTP_200_OK)
        self.assertEqual(updated.data["age"], 36)

        deleted = self.client.delete(detail_url)
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(pk=patient.id).exists())

    def test_unauthenticated_user_cannot_access_patients(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_access_is_isolated_by_owner(self):
        patient = Patient.objects.create(
            user=self.other_user,
            **self.patient_data(),
        )
        detail_url = reverse("patient-detail", args=[patient.id])

        self.assertEqual(
            self.client.get(detail_url).status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(
            self.client.put(
                detail_url,
                self.patient_data(age=40),
                format="json",
            ).status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(
            self.client.delete(detail_url).status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_invalid_patient_data_is_rejected(self):
        response = self.client.post(
            self.list_url,
            self.patient_data(age=121),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexistent_patient_returns_not_found(self):
        response = self.client.get(reverse("patient-detail", args=[99999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PatientDoctorMappingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="mapping-owner@example.com",
            email="mapping-owner@example.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="mapping-other@example.com",
            email="mapping-other@example.com",
            password="StrongPass123!",
        )
        self.patient = Patient.objects.create(
            user=self.user,
            name="Jordan Smith",
            age=35,
            gender="Other",
            address="12 Sample Street",
            phone="+911234567890",
        )
        self.other_patient = Patient.objects.create(
            user=self.other_user,
            name="Taylor Jones",
            age=40,
            gender="Female",
            address="14 Sample Street",
            phone="+911234567891",
        )
        self.doctor = Doctor.objects.create(
            name="Dr. Asha Rao",
            specialization="Cardiology",
            email="asha.rao@example.com",
            phone="+911234567892",
            qualification="MBBS, MD",
            experience_years=12,
        )
        self.other_doctor = Doctor.objects.create(
            name="Dr. Ravi Shah",
            specialization="Neurology",
            email="ravi.shah@example.com",
            phone="+911234567893",
            qualification="MBBS, DM",
            experience_years=10,
        )
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("mapping-list-create")

    def mapping_data(self, **overrides):
        data = {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
        }
        data.update(overrides)
        return data

    def test_create_and_list_only_owned_patient_mappings(self):
        own_mapping = PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor,
        )
        PatientDoctorMapping.objects.create(
            patient=self.other_patient,
            doctor=self.other_doctor,
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [own_mapping.id])

        created = self.client.post(
            self.list_url,
            self.mapping_data(doctor=self.other_doctor.id),
            format="json",
        )
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created.data["patient"], self.patient.id)

    def test_duplicate_mapping_is_rejected(self):
        PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor,
        )

        response = self.client.post(
            self.list_url,
            self.mapping_data(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_mapping_for_another_users_patient(self):
        response = self.client.post(
            self.list_url,
            self.mapping_data(patient=self.other_patient.id),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            PatientDoctorMapping.objects.filter(
                patient=self.other_patient,
                doctor=self.doctor,
            ).exists()
        )

    def test_nonexistent_patient_or_doctor_is_rejected(self):
        for data in (
            self.mapping_data(patient=99999),
            self.mapping_data(doctor=99999),
        ):
            with self.subTest(data=data):
                response = self.client.post(
                    self.list_url,
                    data,
                    format="json",
                )
                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

    def test_patient_mapping_detail_and_delete(self):
        PatientDoctorMapping.objects.create(
            patient=self.other_patient,
            doctor=self.other_doctor,
        )
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor,
        )

        patient_mappings = self.client.get(
            reverse("mapping-patient-detail", args=[self.patient.id])
        )
        self.assertEqual(
            patient_mappings.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(patient_mappings.data), 1)

        deleted = self.client.delete(
            reverse("mapping-patient-detail", args=[mapping.id])
        )
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            PatientDoctorMapping.objects.filter(pk=mapping.id).exists()
        )

    def test_other_users_patient_mappings_are_not_visible_or_deletable(self):
        mapping = PatientDoctorMapping.objects.create(
            patient=self.other_patient,
            doctor=self.other_doctor,
        )

        patient_response = self.client.get(
            reverse("mapping-patient-detail", args=[self.other_patient.id])
        )
        delete_response = self.client.delete(
            reverse("mapping-patient-detail", args=[mapping.id])
        )

        self.assertEqual(
            patient_response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(
            delete_response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertTrue(
            PatientDoctorMapping.objects.filter(pk=mapping.id).exists()
        )

    def test_mapping_endpoints_require_authentication(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
