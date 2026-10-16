
from rest_framework import serializers

from .models import Patient, PatientDoctorMapping
from doctors.serializers import DoctorSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "address",
            "phone",
            "medical_history",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Patient name cannot be empty."
            )
        return value

    def validate_age(self, value):
        if value > 120:
            raise serializers.ValidationError(
                "Age cannot exceed 120."
            )
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Phone number cannot be empty."
            )
        return value

    def validate_address(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Address cannot be empty."
            )
        return value


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(
        source="doctor",
        read_only=True,
    )

    class Meta:
        model = PatientDoctorMapping
        fields = [
            "id",
            "patient",
            "doctor",
            "doctor_details",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        patient = attrs.get(
            "patient",
            getattr(self.instance, "patient", None),
        )
        doctor = attrs.get(
            "doctor",
            getattr(self.instance, "doctor", None),
        )

        if request and patient and patient.user_id != request.user.id:
            raise serializers.ValidationError({
                "patient": "You can only assign doctors to your own patients."
            })

        if patient and doctor:
            existing = PatientDoctorMapping.objects.filter(
                patient=patient,
                doctor=doctor,
            )

            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise serializers.ValidationError({
                    "doctor": "This doctor is already assigned to this patient."
                })

        return attrs
