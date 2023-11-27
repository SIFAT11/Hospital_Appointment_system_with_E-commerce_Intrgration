from django.shortcuts import render,redirect
from .admin import *
from django.contrib import messages
# Create your views here.
def index(request):
    sp =Spasalist.objects.all()
    return render(request,'index.html',locals())

from django.shortcuts import get_object_or_404

def appointment(request):
    doctors_name = Doctor.objects.all()
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_name')  # Assuming you capture the doctor's ID in the form
        patient_name = request.POST.get('patient_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            messages.error(request, 'Invalid doctor selection')
            return redirect('appointment')
        
        appointment = Appointment(
            doctor=doctor,  # Use the doctor field, which is a ForeignKey
            patient_name=patient_name,
            age=age,
            gender=gender,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            email=email,
            phone=phone,
            message=message
        )
        appointment.save()
        
        messages.success(request, 'Appointment created successfully!')
        return redirect('doctor')
    else:
        return render(request, 'appointment.html', {'doctors_name': doctors_name})


def appointmentdoctorwise(request,Doctor_id):
    doctors_name = Doctor.objects.all()
    Doctor_id=Doctor.objects.get(Doctor_id=Doctor_id)
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_name')  # Assuming you capture the doctor's ID in the form
        patient_name = request.POST.get('patient_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            messages.error(request, 'Invalid doctor selection')
            return redirect('appointment')
        
        appointment = Appointment(
            doctor=doctor,  # Use the doctor field, which is a ForeignKey
            patient_name=patient_name,
            age=age,
            gender=gender,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            email=email,
            phone=phone,
            message=message
        )
        appointment.save()
        messages.success(request, 'Appointment created successfully!')
        return redirect('doctor')
        
        
    return render(request,'appointmentdoctorwise.html',locals())


def contract(request):
    return render(request,'contact.html')
    
