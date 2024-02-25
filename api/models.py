from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"

    base_role = Role.PATIENT

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
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


@receiver(post_save, sender=Patient)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "PATIENT":
        PatientProfile.objects.create(user=instance)


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Patient_id = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


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
    doctor_id = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    verified = models.BooleanField(default=False)


@receiver(post_save, sender=Doctor)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "DOCTOR":
        DoctorProfile.objects.create(user=instance)
