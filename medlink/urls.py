from django.urls import path

from medlink.views import (
    CreatePatientView,
    CreatePrescriptionView,
    ListPatientsView,
    ListPrescriptionsView,
    PrescriptionsDetailView,
    RegisterUserView,
)

urlpatterns = [
    path("user-registration/", RegisterUserView.as_view(), name="register_user"),
    path("patients/create/", CreatePatientView.as_view(), name="create_patient"),
    path("patients/list/", ListPatientsView.as_view(), name="list_patients"),
    path(
        "patient/prescriptions/create/",
        CreatePrescriptionView.as_view(),
        name="create_prescription",
    ),
    path(
        "patient/prescriptions/list/",
        ListPrescriptionsView.as_view(),
        name="list_prescriptions",
    ),
    path(
        "patient/prescriptions/<int:prescription_id>/",
        PrescriptionsDetailView.as_view(),
        name="prescription_detail",
    ),
]
