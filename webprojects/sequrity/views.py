from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Profile
from django.contrib import auth
from django.contrib.auth import login as auth_login,logout
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

def register(request):
    if request.method == 'POST':
        # Get user registration data from the form
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST.get('email')
        age = request.POST['age']
        phone = request.POST['phone']
        gender = request.POST['gender']
        password = request.POST['password']
        repassword = request.POST['repassword']
        
        # Check if passwords match and meet length requirements
        if password != repassword:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        elif len(password) < 8 or len(password) > 10:
            messages.error(request, 'Password must be between 8 and 10 characters.')
            return redirect('register')

        # Check if the email already exists
        if Profile.objects.filter(email=email).exists():
            messages.error(request, 'This email address is already registered. Please use a different email.')
            return redirect('register')

        try:
            # Create a new user and profile
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = Profile(
                user=user,
                email=email,
                full_name=full_name,
                age=age,
                phone=phone,
                gender=gender
            )
            profile.save()

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('register')
    else:
        # Render the registration form template for GET requests
        return render(request, 'register.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use the renamed auth_login function
            return redirect('index') 
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')



def log_out(request):
    logout(request)
    messages.error(request, 'logout success.')
    return redirect('login')


def reset(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        new_pass = request.POST['new_pass']

        try:
            user = User.objects.get(username=username)
            if user.email == email:
                user.set_password(new_pass)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Reset password is successful')
                return redirect('login')
            else:
                messages.error(request, 'Email does not match.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'reset.html')
