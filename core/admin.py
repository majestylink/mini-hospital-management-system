from django.contrib import admin

from core.models import Doctor, Patient, Billing

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Billing)
