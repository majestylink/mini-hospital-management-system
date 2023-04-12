from rest_framework import serializers

from core.models import Doctor, Patient, Billing


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ("doctor_id",)

    # def validate_work_our_start(self, value):
    #     """
    #     Check that the work_our_start field is in the correct format.
    #     """
    #     if value.strftime('%Y-%m-%dT%H:%M') != value.replace(tzinfo=None).strftime('%Y-%m-%dT%H:%M'):
    #         raise serializers.ValidationError(
    #             "Please enter the date and time in the following format: YYYY-MM-DDTHH:MM")
    #     return value
    #
    # def validate_work_our_end(self, value):
    #     """
    #     Check that the work_our_end field is in the correct format.
    #     """
    #     if value.strftime('%Y-%m-%dT%H:%M') != value.replace(tzinfo=None).strftime('%Y-%m-%dT%H:%M'):
    #         raise serializers.ValidationError(
    #             "Please enter the date and time in the following format: YYYY-MM-DDTHH:MM")
    #     return value


class PatientSerializer(serializers.ModelSerializer):
    date_of_appointment = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ("patient_id",)
        extra_fields = {"doctor": {"required": True}}


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = "__all__"
        read_only_fields = ("billing_id",)

