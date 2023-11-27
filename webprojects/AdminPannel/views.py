from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from Appointment.admin import AppointmentAdmin
from Appointment.models import Appointment
from BlogPost.models import Blogpost
from Doctor.models import Department, Doctor, DoctorDetails
from Sellmedicine.models import Catagory, Order, OrderItem, Product
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='/admin_login/')
def adminDashboard(request):
    superuser_name = request.user.username
    Doctors =Doctor.objects.all()
    appointments = Appointment.objects.all()
    OrderItems=OrderItem.objects.all()
    total_doctors = Doctor.objects.all().count()
    total_appointments = Appointment.objects.all().count()
    total_order_items = OrderItem.objects.all().count()
    total_sales_amount = Order.objects.filter(payment='paid').aggregate(total_amount=Sum('total_price'))['total_amount'] or 0
    return render(request,'admin/adminDashboard.html',locals())


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('adminDashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
    
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('adminDashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'admin/loginAdmin.html')

@login_required(login_url='/admin_login/')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='/admin_login/')
def adminDoctor(request):
    Doctors=Doctor.objects.all()
    return render(request,'admin/adminDoctor.html',locals())

@login_required(login_url='/admin_login/')
def update_doctor(request,Doctor_id):
    doctor = get_object_or_404(Doctor, Doctor_id=Doctor_id)
    return render(request, 'admin/updateDoctor.html',locals())

@login_required(login_url='/admin_login/')
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, Doctor_id=doctor_id)
    if request.method == 'POST':
        doctor.delete()
        # Redirect to the list of doctors after successful deletion
        return redirect('adminDoctor')  # Make sure to update the URL name

    # Pass the doctor object to the template
    return render(request, 'admin/adminDoctor.html', {'doctor': doctor})


@login_required(login_url='/admin_login/')
def update_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, Doctor_id=doctor_id)

    if request.method == 'POST':
        data = request.POST
        doctor.Doctor_name = data['full_name']
        doctor.Doctor_education_shortlist = data['education_shortlist']
        doctor.Doctor_email = data['email']
        doctor.Doctor_education_shortlist=data['education_shortlist']
        if 'doctor_image' in request.FILES:
            doctor.Doctor_image = request.FILES['doctor_image']

        doctor.save()
        return redirect('adminDoctor')

    return render(request, 'admin/updateDoctor.html', {'doctor': doctor})

@login_required(login_url='/admin_login/')
def sAppointment(request):
    Appointments=Appointment.objects.all()
    return render(request,'admin/sAppointment.html',locals())



def remove_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(Appointment_id=appointment_id)
        appointment.delete()
    except Appointment.DoesNotExist:
        # Handle the case when the appointment does not exist
        pass
    return redirect('sAppointment')


@login_required(login_url='/admin_login/')
def add_doctor(request):
    departments=Department.objects.all()
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        department_name = request.POST.get('department')
        doctor_name = request.POST.get('doctor_name')
        doctor_email = request.POST.get('doctor_email')
        education_shortlist = request.POST.get('education_shortlist', '')  # Set a default value
        # Get the uploaded image file
        doctor_image = request.FILES.get('doctor_image')

        # Check if the Department with the provided name exists
        try:
            department = Department.objects.get(Department_name=department_name)
        except Department.DoesNotExist:
            # Handle the situation where the Department does not exist
            # You might want to create the Department here or handle the error in some other way
            # For now, let's just create a new Department with the given name
            department = Department.objects.create(Department_name=department_name)

        # Create a new Doctor instance and save it
        new_doctor = Doctor(
            Doctor_id=doctor_id,
            department=department,
            Doctor_name=doctor_name,
            Doctor_email=doctor_email,
            Doctor_education_shortlist=education_shortlist,
            Doctor_image=doctor_image
        )
        new_doctor.save()

        return redirect('adminDoctor')  # Adjust the URL name as needed

    return render(request, 'admin/addoctor.html',locals())


@login_required(login_url='/admin_login/')
def add_medicine(request):
    if request.method == 'POST':
        medicine_name = request.POST.get('product_name')
        price = request.POST.get('price')
        medicine_description = request.POST.get('product_description')  # Use 'product_description' instead of 'medicine_description'
        medicine_image = request.FILES.get('product_image')
        category_id = request.POST.get('category_id')
        quantity = request.POST.get('quantity')  # Retrieve the value of 'quantity' from the form

        try:
            category = Catagory.objects.get(pk=category_id)
        except Catagory.DoesNotExist:
            return HttpResponse("Category does not exist")

        new_medicine = Product(
            name=medicine_name,
            price=price,
            category=category,
            details=medicine_description,
            picture=medicine_image,
            quantity=quantity  # Include the 'quantity' in the creation of the Product instance
        )
        new_medicine.save()

        return redirect('adminDashboard')  # Adjust the URL name as needed

    categories = Catagory.objects.all()
    return render(request, 'admin/MedicineAdmin.html', {'categories': categories})



def totalorder(request):
    unique_order_ids = Order.objects.values_list('order_id', flat=True).distinct()
    orders = []
    for order_id in unique_order_ids:
        order_item = OrderItem.objects.filter(order__order_id=order_id).first()
        orders.append(order_item)
    context = {
        'order': orders
    }
    return render(request, 'admin/totalorder.html', context)



def update_payment_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_status = request.POST.get('payment_status')
        try:
            order = Order.objects.get(order_id=order_id)
            order.payment = payment_status
            order.save()
        except Order.DoesNotExist:
            pass
    return redirect('totalorder')


def view_order(request, order_id):
    order_items = OrderItem.objects.filter(order__order_id=order_id)
    order = order_items.first().order
    context = {
        'order_items': order_items,
        'order_id': order.order_id,
        'payment_status': order.payment,
        'order_date': order.order_time,
        'total_amount': order.total_price
    }
    return render(request, 'admin/view_order.html', context)


from datetime import date

def blogadmin(request):
    return render(request, 'admin/BlogAdmin.html')

def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        head0 = request.POST.get('head0')
        chead0 = request.POST.get('chead0')
        head1 = request.POST.get('head1')
        chead1 = request.POST.get('chead1')
        head2 = request.POST.get('head2')
        chead2 = request.POST.get('chead2')
        thumbnail = request.FILES.get('thumbnail')

        # Assign the current date automatically
        pub_date = date.today()

        new_blogpost = Blogpost(
            title=title,
            head0=head0,
            chead0=chead0,
            head1=head1,
            chead1=chead1,
            head2=head2,
            chead2=chead2,
            pub_date=pub_date,
            thumbnail=thumbnail
        )
        new_blogpost.save()

        return redirect('adminDashboard')  # Replace 'adminDashboard' with the appropriate URL name

    return render(request, 'admin/BlogAdmin.html')
