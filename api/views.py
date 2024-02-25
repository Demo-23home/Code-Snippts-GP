from .models import User, Doctor, Patient
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterPatientView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.PATIENT)


class RegisterDoctorView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

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
