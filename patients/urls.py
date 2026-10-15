
from django.urls import path
from .views import (
    PatientListCreateView,
    PatientDetailView,
    PatientDoctorMappingListCreateView,
    PatientDoctorMappingDetailView,
)

urlpatterns = [
    path('', PatientListCreateView.as_view(), name='patient-list-create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),

    path(
        'mappings/',
        PatientDoctorMappingListCreateView.as_view(),
        name='mapping-list-create'
    ),
    path(
        'mappings/<int:pk>/',
        PatientDoctorMappingDetailView.as_view(),
        name='mapping-delete'
    ),
]
