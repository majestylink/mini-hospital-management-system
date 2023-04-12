from random import randint

from django.db import models
from django.utils.translation import gettext_lazy as _

from constants import USER_INSURANCE_CHOICES


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Doctor(BaseModel):
    doctor_id = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    email = models.EmailField(_("email address"), unique=True)
    work_our_start = models.CharField(max_length=50)
    work_our_end = models.CharField(max_length=50)

    @staticmethod
    def doctor_id_exist(doctor_id):
        doctors = Doctor.objects.filter(doctor_id=doctor_id)
        if doctors.exists():
            return True
        return False

    @staticmethod
    def generate_doctor_id():
        doctor_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        while Doctor.doctor_id_exist(doctor_id):
            doctor_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        return doctor_id


class Patient(BaseModel):
    patient_id = models.CharField(max_length=200)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients')
    company_name = models.CharField(max_length=200)
    company_designation = models.CharField(max_length=200)
    date_of_appointment = models.DateTimeField(default=None)
    insurance = models.CharField(max_length=50, default="no insurance", choices=USER_INSURANCE_CHOICES)
    work_our_start = models.CharField(max_length=50)
    work_our_end = models.CharField(max_length=50)
    confirmed = models.BooleanField(default=False)

    @staticmethod
    def patient_id_exist(patient_id):
        patients = Patient.objects.filter(patient_id=patient_id)
        if patients.exists():
            return True
        return False

    @staticmethod
    def generate_patient_id():
        patient_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        while Patient.patient_id_exist(patient_id):
            patient_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        return patient_id


class Billing(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="billing")
    billing_id = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, db_index=True)
    deduction_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=0, db_index=True)

    @staticmethod
    def billing_id_exist(billing_id):
        billings = Billing.objects.filter(billing_id=billing_id)
        if billings.exists():
            return True
        return False

    @staticmethod
    def generate_billing_id():
        billing_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        while Billing.billing_id_exist(billing_id):
            billing_id = "".join(["{}".format(randint(1, 9)) for num in range(0, 7)])
        return billing_id
