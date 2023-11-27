from django.db import models
from Doctor.models import Doctor
import uuid

class Spasalist(models.Model):
    name =models.CharField(max_length=100)
    description =models.TextField()
    image = models.ImageField(upload_to='images/', default='images.png')
   
    def __str__ (self):
        return self.name

import random
import string
from django.db import models

def generate_short_uuid():
    # Generate a random 6-character string using uppercase letters and digits
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Appointment(models.Model):
    Appointment_id = models.CharField(primary_key=True, max_length=6, unique=True, default=generate_short_uuid, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('other', 'Other'), ('male', 'Male'), ('female', 'Female')])
    reservation_date = models.DateField()
    reservation_time = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return f"Appointment for {self.doctor.Doctor_name} on {self.reservation_date}"
