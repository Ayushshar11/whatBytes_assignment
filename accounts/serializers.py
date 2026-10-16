
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=150,
        write_only=True,
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return value

    def validate(self, attrs):
        name = attrs.get("name", "").strip()
        if name:
            attrs["first_name"] = name
            attrs["last_name"] = ""
        elif not (
            attrs.get("first_name", "").strip()
            or attrs.get("last_name", "").strip()
        ):
            raise serializers.ValidationError({
                "name": "A name is required."
            })

        user = User(
            username=attrs["email"],
            email=attrs["email"],
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
        )
        try:
            validate_password(attrs["password"], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({
                "password": exc.messages
            }) from exc

        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        validated_data.pop("name", None)
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        return user




from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

    def validate(self, attrs):
        attrs[self.username_field] = attrs.get('email', '').strip().lower()
        return super().validate(attrs)

