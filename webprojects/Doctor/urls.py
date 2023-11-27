from django.urls import path
from .views import * 

urlpatterns = [
    path('',doctor,name='doctor'),   
    path('doctor/<str:Doctor_id>/',doctorlist,name='doctors'), 
    path('doctors/<str:doctor_id>/',doctor_details, name='doctor_details'),
]

