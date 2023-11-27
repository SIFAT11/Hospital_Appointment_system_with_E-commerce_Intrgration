from django.contrib import admin
from .models import *

admin.site.register(Spasalist)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('Appointment_id', 'doctor', 'patient_name', 'age', 'gender', 'reservation_date', 'reservation_time', 'email', 'phone', 'message')
    
admin.site.register(Appointment, AppointmentAdmin)