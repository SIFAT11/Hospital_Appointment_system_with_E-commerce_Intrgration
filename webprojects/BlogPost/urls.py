from django.urls import path
from .views import * 

urlpatterns = [
    path('bg/',blog,name='blog'),
    path('de/<int:blog_id>/',blogIDdetail,name='blogIDdetail'),
]
