
from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patients'
    )
    name = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    medical_history = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
