
from rest_framework import serializers
from .models import Patient


from doctors.serializers import DoctorSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'age',
            'gender',
            'address',
            'phone',
            'medical_history',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_age(self, value):
        if value < 0 or value > 120:
            raise serializers.ValidationError(
                'Age must be between 0 and 120.'
            )
        return value

from doctors.models import Doctor

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(
        source='doctor',
        read_only=True
    )

    class Meta:
        from .models import PatientDoctorMapping

        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'doctor_details', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        patient = attrs['patient']
        doctor = attrs['doctor']
        request = self.context['request']

        if patient.user_id != request.user.id:
            raise serializers.ValidationError(
                'You can only assign doctors to your own patients.'
            )

        from .models import PatientDoctorMapping

        if PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor
        ).exists():
            raise serializers.ValidationError(
                'This doctor is already assigned to this patient.'
            )

        return attrs
