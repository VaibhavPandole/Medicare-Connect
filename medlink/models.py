from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    """
    Custom model to store role of user.
    """

    ROLE_CHOICES = [
        ("doctor", "Doctor"),
        ("patient", "Patient"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="role")
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default="patient")


class Patient(models.Model):
    """
    Model to store the patient information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medical_history = models.TextField(null=True)


class Prescription(models.Model):
    """
    Model to store prescription assigned by doctor to patient.
    """

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    instructions = models.TextField()
    date_prescribed = models.DateTimeField(auto_now_add=True)
