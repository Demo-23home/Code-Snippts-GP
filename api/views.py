from django.shortcuts import get_object_or_404
from .models import User, Doctor, Patient, DoctorProfile
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterDoctorSerializer,
    RegisterPatientSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterPatientView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterPatientSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.PATIENT)


class RegisterDoctorView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterDoctorSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.DOCTOR)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def dahsBoard(request):
    if request.method == "GET":
        context = f"hey {request.user} you're seeing a GET response"
        return Response({"response": context}, status=status.HTTP_200_OK)

    elif request.method == "POST":
        text = request.POST.get("text")
        response = f"hey {request.user} this is an POST response , your text is {text}"
        return Response({" ": response}, status=status.HTTP_200_OK)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def patient_info(request):
    serializer = PatientProfileSerializer(request.user, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def get_crrunt_host(request):
    protocol = request.is_secure() and "http" or "https"
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


@api_view(["POST"])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(Patient, email=data["email"])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    reset_password_token = user.patientprofile.reset_password_token = token
    reset_password_expire = user.patientprofile.reset_password_expire = expire_date


@api_view(["GET"])
def get_doctor_profile(request, pk):
    doctor_profile = get_object_or_404(DoctorProfile, doctor_id=pk)
    serializer = DoctorProfileSerializer(doctor_profile)
    return Response(serializer.data)
