from django.urls import path
from .views import * 

urlpatterns = [
    
    
    path('admin_pannel/admin_login/',admin_login, name='admin_login'),
    path('admin_logout/', admin_logout, name='admin_logout'),
    
    path('AdminPannel/',adminDashboard,name='adminDashboard'),
    path('adminDoctor/',adminDoctor,name='adminDoctor'),
    path('sAppointment/',sAppointment,name='sAppointment'),
    
    
    
    path('edit-doctor/<str:doctor_id>/',update_doctor, name='edit_doctor'),
    path('delete-doctor/<str:doctor_id>/',delete_doctor, name='delete_doctor'),

    path('AdminPannel/add-doctor/',add_doctor, name='add_doctor'),
   
    path('add-medicine/',add_medicine, name='add_medicine'),
   
    path('remove_appointment/<str:appointment_id>/',remove_appointment, name='remove_appointment'),
    
    
    path('totalsell/',totalorder,name='totalorder'),
    path('update_payment_status/',update_payment_status, name='update_payment_status'),
    path('vieworder/<int:order_id>/',view_order, name='view_order'),
    
    
    path('blogadmin/',blogadmin, name='blogadmin'),
    path('add_blog/',add_blog, name='addBlog'), 
]



