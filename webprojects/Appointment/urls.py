
from django.urls import path
from .views import * 

urlpatterns = [
    path('',index,name='index'),
    path('appointment/',appointment,name='appointment'),
    path('appointment/<str:Doctor_id>/',appointmentdoctorwise,name='appoint'),   
    path('contact/',contract,name='contact'),
]
