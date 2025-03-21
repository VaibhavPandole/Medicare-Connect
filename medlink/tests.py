from unittest.mock import patch

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from .models import Patient, Prescription, Role


class RegisterUserViewTest(APITestCase):
    def test_register_user_success(self):
        data = {
            "email": "testuser@example.com",
            "password": "password123",
            "role": "doctor",
        }
        response = self.client.post("/medlink/user-registration/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User created successfully")
        self.assertEqual(response.data["role"], "doctor")

    def test_register_user_already_exists(self):
        User = get_user_model()
        User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password123",
        )
        data = {
            "email": "testuser@example.com",
            "password": "password123",
            "role": "doctor",
        }
        response = self.client.post("/medlink/user-registration/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User already exist", response.data["message"])

    def test_register_user_invalid_data(self):
        data = {"email": "invalidemail", "password": "123", "role": "doctor"}
        response = self.client.post("/medlink/user-registration/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


class CreatePatientViewTest(APITestCase):
    @patch("medlink.views.get_user_model")
    def test_create_patient_success(self, mock_user_model):
        # Mock doctor user
        doctor_user = get_user_model().objects.create_user(
            username="doctor1", email="doctor1@example.com", password="password123"
        )
        doctor_role = Role.objects.create(user=doctor_user, role="doctor")
        self.client.force_authenticate(user=doctor_user)

        # Mock patient user
        patient_user = get_user_model().objects.create_user(
            username="patient1@example.com",
            email="patient1@example.com",
            password="password123",
        )

        data = {
            "patient": "patient1@example.com",
            "medical_history": "No significant history",
        }
        response = self.client.post("/medlink/patients/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Patient created successfully")

    def test_create_patient_not_doctor(self):
        patient_user = get_user_model().objects.create_user(
            username="user1", email="user1@example.com", password="password123"
        )
        patient_role = Role.objects.create(user=patient_user, role="patient")
        self.client.force_authenticate(user=patient_user)
        data = {
            "patient": "patient1@example.com",
            "medical_history": "No significant history",
        }
        response = self.client.post("/medlink/patients/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"], "Only doctors can create patients")

    def test_create_patient_user_not_found(self):
        doctor_user = get_user_model().objects.create_user(
            username="doctor1", email="doctor1@example.com", password="password123"
        )
        doctor_role = Role.objects.create(user=doctor_user, role="doctor")
        self.client.force_authenticate(user=doctor_user)

        data = {
            "patient": "nonexistent_user@example.com",
            "medical_history": "No significant history",
        }
        response = self.client.post("/medlink/patients/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "User not found")

    def test_create_patient_invalid_data(self):
        doctor_user = get_user_model().objects.create_user(
            username="doctor1", email="doctor1@example.com", password="password123"
        )
        doctor_role = Role.objects.create(user=doctor_user, role="doctor")
        self.client.force_authenticate(user=doctor_user)
        data = {"patient": "", "medical_history": ""}
        response = self.client.post("/medlink/patients/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListPatientsViewTest(APITestCase):
    def test_list_patients_success(self):
        doctor_user = get_user_model().objects.create_user(
            username="doctor1@example.com",
            email="doctor1@example.com",
            password="password123",
        )
        doctor_role = Role.objects.create(user=doctor_user, role="doctor")
        self.client.force_authenticate(user=doctor_user)

        patient_user = get_user_model().objects.create_user(
            username="patient1@example.com",
            email="patient1@example.com",
            password="password123",
        )
        Patient.objects.create(
            user=patient_user, medical_history="No significant history"
        )

        response = self.client.get("/medlink/patients/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_patients_not_doctor(self):
        patient_user = get_user_model().objects.create_user(
            username="user1@example.com",
            email="user1@example.com",
            password="password123",
        )
        patient_role = Role.objects.create(user=patient_user, role="patient")
        self.client.force_authenticate(user=patient_user)
        response = self.client.get("/medlink/patients/list/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"], "Only doctors can see patients")


class CreatePrescriptionViewTest(APITestCase):
    def test_create_prescription_success(self):
        doctor_user = get_user_model().objects.create_user(
            username="doctor1@example.com",
            email="doctor1@example.com",
            password="password123",
        )
        doctor_role = Role.objects.create(user=doctor_user, role="doctor")
        self.client.force_authenticate(user=doctor_user)

        patient_user = get_user_model().objects.create_user(
            username="patient1@example.com",
            email="patient1@example.com",
            password="password123",
        )
        patient = Patient.objects.create(
            user=patient_user, medical_history="No significant history"
        )

        data = {
            "patient_username": "patient1@example.com",
            "medication": "Paracetamol",
            "dosage": "500mg",
            "instruction": "Take twice a day",
        }
        response = self.client.post(
            "/medlink/patient/prescriptions/create/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Prescription created successfully")

    def test_create_prescription_not_doctor(self):
        patient_user = get_user_model().objects.create_user(
            username="user1@example.com",
            email="user1@example.com",
            password="password123",
        )
        patient_role = Role.objects.create(user=patient_user, role="patient")
        self.client.force_authenticate(user=patient_user)

        data = {
            "patient_username": "patient1@example.com",
            "medication": "Paracetamol",
            "dosage": "500mg",
            "instruction": "Take twice a day",
        }
        response = self.client.post(
            "/medlink/patient/prescriptions/create/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["error"], "Only doctors can prescribe medications"
        )

    def test_create_prescription_patient_not_found(self):
        doctor_user = get_user_model().objects.create_user(
            username="doctor1@example.com",
            email="doctor1@example.com",
            password="password123",
        )
        doctor_role = Role.objects.create(user=doctor_user, role="doctor")
        self.client.force_authenticate(user=doctor_user)

        data = {
            "patient_username": "nonexistent_patient@example.com",
            "medication": "Paracetamol",
            "dosage": "500mg",
            "instruction": "Take twice a day",
        }
        response = self.client.post(
            "/medlink/patient/prescriptions/create/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["error"],
            "Patient does not exist with username nonexistent_patient@example.com",
        )


class ListPrescriptionsViewTest(APITestCase):
    def test_list_prescriptions_success(self):
        doctor_user = get_user_model().objects.create_user(
            username="doctor1@example.com",
            email="doctor1@example.com",
            password="password123",
        )
        doctor_role = Role.objects.create(user=doctor_user, role="doctor")
        self.client.force_authenticate(user=doctor_user)

        patient_user = get_user_model().objects.create_user(
            username="patient1@example.com",
            email="patient1@example.com",
            password="password123",
        )
        patient = Patient.objects.create(
            user=patient_user, medical_history="No significant history"
        )

        prescription = Prescription.objects.create(
            patient=patient,
            doctor=doctor_user,
            medication="Paracetamol",
            dosage="500mg",
            instructions="Take twice a day",
        )
        response = self.client.get(
            "/medlink/patient/prescriptions/list/?patient_username=patient1@example.com"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_prescriptions_patient_not_found(self):
        doctor_user = get_user_model().objects.create_user(
            username="doctor1@example.com",
            email="doctor1@example.com",
            password="password123",
        )
        doctor_role = Role.objects.create(user=doctor_user, role="doctor")
        self.client.force_authenticate(user=doctor_user)

        response = self.client.get(
            "/medlink/patient/prescriptions/list/?patient_username=nonexistent_patient@example.com"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["error"],
            "Patient does not exist with username nonexistent_patient@example.com",
        )


class PrescriptionsDetailViewTest(APITestCase):
    def test_prescription_detail_success(self):
        doctor_user = get_user_model().objects.create_user(
            username="doctor1@example.com",
            email="doctor1@example.com",
            password="password123",
        )
        doctor_role = Role.objects.create(user=doctor_user, role="doctor")
        self.client.force_authenticate(user=doctor_user)

        patient_user = get_user_model().objects.create_user(
            username="patient1@example.com",
            email="patient1@example.com",
            password="password123",
        )
        patient = Patient.objects.create(
            user=patient_user, medical_history="No significant history"
        )

        prescription = Prescription.objects.create(
            patient=patient,
            doctor=doctor_user,
            medication="Paracetamol",
            dosage="500mg",
            instructions="Take twice a day",
        )

        response = self.client.get(f"/medlink/patient/prescriptions/{prescription.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["medication"], "Paracetamol")

    @patch("medlink.views.PrescriptionsDetailView.permission_classes")
    def test_prescription_detail_not_found(self, mock_permission):
        # Mock the permission class to bypass authentication
        mock_permission.return_value = [IsAuthenticated]
        response = self.client.get("/medlink/patient/prescriptions/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["error"], "Prescription does not exist with id 9999"
        )
