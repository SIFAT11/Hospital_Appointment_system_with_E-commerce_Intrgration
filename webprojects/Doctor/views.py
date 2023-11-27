from django.shortcuts import get_object_or_404, render
from .admin import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def doctor(request):
    doctors=Doctor.objects.all()
    appointmentTime=AppointmentTime.objects.all()
    return render(request,'Doctors.html',locals())


@login_required(login_url='login')
def doctorlist(request,Doctor_id):
    doctors=Doctor.objects.all()
    appointmentTime=AppointmentTime.objects.all()
    doctorDetails=DoctorDetails.objects.get(Doctor_id=Doctor_id)
    return render(request,'Doctors.html',locals())


def doctor_details(request, doctor_id):
    doctor = get_object_or_404(Doctor, Doctor_id=doctor_id)
    doctor_details = DoctorDetails.objects.filter(doctor=doctor).first()  # Assuming one-to-one relationship

    context = {
        'doctor': doctor,
        'doctor_details': doctor_details
    }
    return render(request, 'doctordetails.html', context)