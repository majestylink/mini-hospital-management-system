from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from core.models import Doctor, Patient, Billing
from core.serializers import DoctorSerializer, PatientSerializer, BillingSerializer
from utilities.response import ApiResponse


class DoctorView(APIView):
    serializer_class = DoctorSerializer

    def get(self, request, doctor_id=None):
        if doctor_id:
            try:
                doctor = Doctor.objects.get(doctor_id=doctor_id)
                data = self.serializer_class(doctor).data
                return ApiResponse(200, data=data, message="success").response()
            except:
                return ApiResponse(400, message="Doctor with doctor_id does not exist").response()
        doctors = Doctor.objects.all()
        data = self.serializer_class(doctors, many=True).data
        return ApiResponse(200, data=data, message="success").response()

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            data = ser.save()
            data.doctor_id = Doctor.generate_doctor_id()
            data.save()
            return ApiResponse(200, data=ser.data, message="success").response()
        else:
            return ApiResponse(400, data=ser.errors, message="Validation error").response()


class PatientView(APIView):
    serializer_class = PatientSerializer

    def get(self, request, patient_id=None):
        if patient_id:
            try:
                patient = Patient.objects.get(patient_id=patient_id)
                data = self.serializer_class(patient).data
                return ApiResponse(200, data=data, message="success").response()
            except:
                return ApiResponse(400, message="Patient with patient_id does not exist").response()
        patients = Patient.objects.all()
        data = self.serializer_class(patients, many=True).data
        return ApiResponse(200, data=data, message="success").response()

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
            instance = ser.save()  # Save the validated data to the database
            instance.patient_id = Patient.generate_patient_id()
            instance.save()
            return ApiResponse(200, data=ser.data, message="success").response()
        else:
            return ApiResponse(400, data=ser.errors, message="Validation error").response()

    def put(self, request, patient_id=None):
        if patient_id:
            try:
                patient = Patient.objects.get(patient_id=patient_id)
                patient.confirmed = True
                patient.save()
                data = self.serializer_class(patient).data
                return ApiResponse(200, data=data, message="success").response()
            except:
                return ApiResponse(400, message="Patient with patient_id does not exist").response()
        else:
            return ApiResponse(400, message="Please provide patient id").response()


class GetDoctorsPatients(APIView):
    def get(self, request):
        doctor_id = request.data.get("doctor_id", None)
        if doctor_id:
            try:
                doctor = Doctor.objects.get(doctor_id=doctor_id)
                patients = doctor.patients.all()
                data = PatientSerializer(patients, many=True)
                return ApiResponse(200, data={"patients": data.data}, message="success").response()
            except:
                return ApiResponse(400, message=f"Doctor with ID {doctor_id} does not exist").response()
        else:
            return ApiResponse(400, message="Please provide doctor id").response()


class PatientBillingView(APIView):
    def post(self, request):
        try:
            patient = Patient.objects.get(patient_id=request.data['patient_id'])
            total = request.data['total']
            if patient.insurance == "no insurance":
                deduction_percentage = 0
            elif patient.insurance == "semi comprehensive":
                deduction_percentage = 20
            elif patient.insurance == "comprehensive":
                deduction_percentage = 100
            else:
                deduction_percentage = None
            bill = Billing.objects.create(
                patient=patient,
                billing_id=Billing.generate_billing_id(),
                total=total,
                deduction_percentage=deduction_percentage
            )
            data = BillingSerializer(bill).data
            return ApiResponse(200, data=data, message="success").response()
        except:
            return ApiResponse(400, message=f"Make sure you include a valid patient_id").response()
