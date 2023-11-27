from django.contrib import admin
from .models import *

admin.site.register(Department)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('Doctor_id', 'Doctor_name', 'Doctor_email', 'Doctor_education_shortlist')   
admin.site.register(Doctor, DoctorAdmin)


admin.site.register(AppointmentTime)
admin.site.register(DoctorDetails)