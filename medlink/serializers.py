# healthcare/serializers.py

from rest_framework import serializers

from .models import Patient, Prescription


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.CharField()

    def validate(self, data):
        role_name = data.get("role")
        if role_name not in ["doctor", "patient"]:
            raise serializers.ValidationError({"error": "Invalid role"})
        return data


class CreatePatientRequestSerializer(serializers.Serializer):
    patient = serializers.EmailField()
    medical_history = serializers.CharField(allow_null=True, required=False)


class PatientListResponseSerializer(serializers.ModelSerializer):
    patient_email = serializers.SerializerMethodField()

    def get_patient_email(self, obj):
        return obj.user.email

    class Meta:
        model = Patient
        fields = ["id", "patient_email"]


class PrescriptionRequestSerializer(serializers.Serializer):
    patient_username = serializers.EmailField()
    medication = serializers.CharField()
    dosage = serializers.CharField()
    instruction = serializers.CharField()


class PrescriptionSerializer(serializers.ModelSerializer):
    patient_username = serializers.SerializerMethodField(
        method_name="get_patient_email"
    )
    doctor_username = serializers.SerializerMethodField(method_name="get_doctor_email")
    date_prescribed = serializers.DateTimeField(format="%d-%m-%Y")

    def get_patient_email(self, obj):
        return obj.patient.user.username

    def get_doctor_email(self, obj):
        return obj.doctor.username

    class Meta:
        model = Prescription
        fields = [
            "id",
            "patient_username",
            "doctor_username",
            "date_prescribed",
        ]


class PrescriptionListRequestSerializer(serializers.Serializer):
    patient_username = serializers.EmailField()


class PrescriptionInfoSerializer(serializers.ModelSerializer):
    patient_username = serializers.SerializerMethodField(
        method_name="get_patient_email"
    )
    doctor_username = serializers.SerializerMethodField(method_name="get_doctor_email")
    date_prescribed = serializers.DateTimeField(format="%d-%m-%Y")

    def get_patient_email(self, obj):
        return obj.patient.user.username

    def get_doctor_email(self, obj):
        return obj.doctor.username

    class Meta:
        model = Prescription
        fields = [
            "id",
            "patient_username",
            "doctor_username",
            "medication",
            "dosage",
            "instructions",
            "date_prescribed",
        ]
