from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "success",
        "message": "Healthcare Backend API is running"
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response({
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "name": user.get_full_name() or user.first_name,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    })