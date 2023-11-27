from django.db import models
import random
import string

class Department(models.Model):
    Department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.Department_name
    

class Doctor(models.Model):
    Doctor_id = models.CharField(primary_key=True, max_length=10, unique=True, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    Doctor_name = models.CharField(max_length=100)
    Doctor_email = models.EmailField(max_length=100)
    Doctor_education_shortlist = models.CharField(max_length=100)
    Doctor_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.Doctor_name

    def save(self, *args, **kwargs):
        if not self.Doctor_id:
            # Generate a random 5-character ID using uppercase letters and digits
            random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            self.Doctor_id = random_id
        super().save(*args, **kwargs)



class AppointmentTime(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

class DoctorDetails(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Added department field
    Alevel = models.CharField(max_length=100)
    higher_educations = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=100)
    appointment = models.CharField(max_length=100)
    appointment_times = models.ManyToManyField(AppointmentTime)
    description = models.TextField()

    def add_appointment_time(self, start_time, end_time):
        appointment_time = AppointmentTime(doctor=self.doctor, start_time=start_time, end_time=end_time)
        appointment_time.save()
