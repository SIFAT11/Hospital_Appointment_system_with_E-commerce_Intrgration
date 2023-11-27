from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.
def blog(request):
    blogposts = Blogpost.objects.all()
    return render(request,'blog.html',locals())

def blogIDdetail(request,blog_id):
    blogpost = get_object_or_404(Blogpost, post_id=blog_id)
    return render(request,'blogIDdetail.html',locals())