import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            # self.role = self.base_role
            return super().save(*args, **kwargs)


class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PATIENT)


class Patient(User):
    base_role = User.Role.PATIENT

    Patient = PatientManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Patients"


class PatientProfile(models.Model):
    user = models.OneToOneField(Patient, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    # patient_id = models.IntegerField(null=True, blank=True)
    # image = models.ImageField(null=True, blank=True)
    # phone_number = models.CharField(max_length=20, null=True, blank=True)
    # GENDER_CHOICES = (
    #     ("M", "Male"),
    #     ("F", "Female"),
    # )
    # gender = models.CharField(
    #     max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    # )
    # CITY_CHOICES = (
    #     ("City1", "City1"),
    #     ("City2", "City2"),
    #     ("City3", "City3"),
    #     # Add more city choices as needed
    # )
    # city = models.CharField(max_length=100, choices=CITY_CHOICES, null=True, blank=True)
    # GOVERNMENT_CHOICES = (
    #     ("Gov1", "Government1"),
    #     ("Gov2", "Government2"),
    #     ("Gov3", "Government3"),
    #     # Add more government choices as needed
    # )
    # government = models.CharField(
    #     max_length=100, choices=GOVERNMENT_CHOICES, null=True, blank=True
    # )

    def __str__(self):
        return f"Profile for {self.username}"


class DoctorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.DOCTOR)


class Doctor(User):
    base_role = User.Role.DOCTOR

    doctor = DoctorManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for doctors"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # doctor_id = models.IntegerField(null=True, blank=True)
    # bio = models.TextField(null=True, blank=True)
    # image = models.ImageField(null=True, blank=True)
    # verified = models.BooleanField(default=False)
    # rating = models.IntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(5)]
    # )

    def __str__(self):
        return f"Profile for Doctor {self.username}"
