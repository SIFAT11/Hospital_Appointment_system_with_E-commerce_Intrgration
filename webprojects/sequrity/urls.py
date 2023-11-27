from django.urls import path
from .views import * 

urlpatterns = [
    path('login/',login,name='login'), 
    path('log_out/', log_out, name='logout'),
    path('reset/', reset, name='reset'),
    path('register/',register,name='register'), 
]

