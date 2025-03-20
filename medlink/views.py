from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import IntegrityError

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient, Prescription, Role
from .serializers import (
    CreatePatientRequestSerializer,
    PatientListResponseSerializer,
    PrescriptionInfoSerializer,
    PrescriptionListRequestSerializer,
    PrescriptionRequestSerializer,
    PrescriptionSerializer,
    UserRegistrationSerializer,
)


class RegisterUserView(APIView):
    """
    This class is created for user registration.
    """

    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            username = serializer.data["email"]
            email = serializer.data["email"]
            password = serializer.data["password"]
            role_name = serializer.data["role"]
            # Create user
            user = get_user_model().objects.create_user(
                username=username, email=email, password=password
            )

            # Assign role
            role, created = Role.objects.get_or_create(user=user)
            role.role = role_name
            role.save()

            return Response(
                {"message": "User created successfully", "role": role_name},
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response(
                {
                    "message": f"User already exist with email {serializer.data['email']}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"message": "Something Went Wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CreatePatientView(APIView):
    """
    This class contains business logic to register the patients by doctors only.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if self.request.user.role.role != "doctor":
                return Response(
                    {"error": "Only doctors can create patients"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Retrieve the user with role patient
            try:
                serial_data = CreatePatientRequestSerializer(data=request.data)
                if not serial_data.is_valid():
                    return Response(
                        serial_data.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                user = User.objects.get(username=serial_data.data.get("patient"))
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Register patient
            patient = Patient.objects.create(
                user=user, medical_history=serial_data.data.get("medical_history")
            )
            return Response(
                {"message": "Patient created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response(
                {
                    "message": f"Patient already exist with email {serial_data.data.get('patient')}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"message": "Something Went Wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListPatientsView(APIView):
    """
    This class contains business logic to fetch the list of patients.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user

        # Check if the user is a doctor
        if user.role.role != "doctor":
            return Response(
                {"error": "Only doctors can see patients"},
                status=status.HTTP_403_FORBIDDEN,
            )

        patients = Patient.objects.all().select_related("user")
        serializer = PatientListResponseSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePrescriptionView(APIView):
    """
    This class contains business logic to create prescription by the doctors.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if request.user.role.role != "doctor":
                return Response(
                    {"error": "Only doctors can prescribe medications"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer = PrescriptionRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                patient = Patient.objects.get(
                    user__username=serializer.data.get("patient_username")
                )
            except Patient.DoesNotExist:
                return Response(
                    {
                        "error": f"Patient does not exist with username {serializer.data.get('patient_username')}"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            prescription = Prescription.objects.create(
                patient=patient,
                doctor=request.user,
                medication=serializer.data.get("medication"),
                dosage=serializer.data.get("dosage"),
                instructions=serializer.data.get("instruction"),
            )

            return Response(
                {"message": "Prescription created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception:
            return Response(
                {"message": "Something Went Wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListPrescriptionsView(APIView):
    """
    This class contains business logic to fetch the list od prescription for individual patient.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            username = request.GET.get("patient_username")

            # Check if the user is a patient, he can see own prescription only.
            if request.user.role.role == "patient":
                username = request.user.username
            serializer = PrescriptionListRequestSerializer(
                data={"patient_username": username}
            )
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            patient = Patient.objects.get(user__username=username)
            prescriptions = Prescription.objects.filter(patient=patient)
            serializer = PrescriptionSerializer(prescriptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response(
                {"error": f"Patient does not exist with username {username}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                {"message": "Something Went Wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PrescriptionsDetailView(APIView):
    """
    This class contains business login to fetch detailed information of description.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, prescription_id):
        try:
            prescriptions = Prescription.objects.get(id=prescription_id)
            serializer = PrescriptionInfoSerializer(prescriptions)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Prescription.DoesNotExist:
            return Response(
                {"error": f"Prescription does not exist with id {prescription_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                {"message": "Something Went Wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
