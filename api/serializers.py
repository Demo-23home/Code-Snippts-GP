from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, DoctorProfile, PatientProfile, Doctor


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email

        return token


class RegisterPatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    role = serializers.CharField(read_only=True, default=User.Role.PATIENT)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password", "role"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        validated_data.pop("password")
        validated_data.pop("role")
        PatientProfile.objects.create(user=user, **validated_data)
        return user


class RegisterDoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    role = serializers.CharField(read_only=True, default=User.Role.DOCTOR)

    class Meta:
        model = Doctor
        fields = ["username", "email", "password", "confirm_password", "role"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        validated_data.pop("password")
        validated_data.pop("role")
        DoctorProfile.objects.create(user=user, **validated_data)
        return user


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = "__all__"


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = "__all__"
