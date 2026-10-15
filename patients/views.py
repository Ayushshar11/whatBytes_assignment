
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Patient, PatientDoctorMapping
from .serializers import (
    PatientSerializer,
    PatientDoctorMappingSerializer,
)


class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        ).select_related(
            "patient", "doctor"
        ).order_by("-created_at")

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]

        if patient.user_id != self.request.user.id:
            raise PermissionDenied(
                "You can only assign doctors to your own patients."
            )

        serializer.save()


class MappingDetailView(generics.GenericAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        ).select_related("patient", "doctor")

    def get(self, request, patient_id):
        # GET /api/mappings/<patient_id>/
        patient = get_object_or_404(
            Patient.objects.filter(user=request.user),
            pk=patient_id,
        )

        mappings = self.get_queryset().filter(patient=patient)
        serializer = self.get_serializer(mappings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, patient_id):
        # DELETE /api/mappings/<mapping_id>/
        mapping = get_object_or_404(
            self.get_queryset(),
            pk=patient_id,
        )

        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
