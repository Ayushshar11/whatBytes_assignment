
from rest_framework import generics

from .models import Doctor
from .serializers import DoctorSerializer
from .permissions import IsAdminOrReadOnly


class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all().order_by('-created_at')
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminOrReadOnly]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminOrReadOnly]
