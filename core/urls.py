from django.urls import path

from core import views

urlpatterns = [
    path('doctors/', views.DoctorView.as_view(), name='get_all_doctors'),
    path('doctors/get-doctor-patients/', views.GetDoctorsPatients.as_view(), name='get_doctor_patients'),
    path('doctors/<str:doctor_id>/', views.DoctorView.as_view(), name='get_doctor'),
    path('patients/', views.PatientView.as_view(), name='get_all_patients'),
    path('patients/<str:patient_id>/', views.PatientView.as_view(), name='get_patient'),
    path('patients/<str:patient_id>/', views.PatientView.as_view(), name='get_patient'),

    path('billing/', views.PatientBillingView.as_view(), name='PatientBillingView'),
]
