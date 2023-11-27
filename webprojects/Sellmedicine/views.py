from audioop import reverse
from decimal import Decimal
from gettext import translation
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.test import TransactionTestCase
from .models import Product
from .models import *
from django.db.models import Count, Sum
from django.contrib import messages
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from sslcommerz_lib import SSLCOMMERZ
import os


def medicine(request):
    query = request.GET.get('q')
    medicines = Product.objects.all()
    if query:  # Check if a query is provided
        medicines = medicines.filter(Q(name__icontains=query)) 
    return render(request, 'medicine.html', {'medicines': medicines})

def add_to_cart(request, id):
    user = request.user
    if user.is_authenticated:
        try:
           prod = Product.objects.get(id=id)
        except Product.DoesNotExist:
           return HttpResponseBadRequest('Invalid product ID')

        try:
           cart = Cart.objects.get(Q(user=user, product=prod))
           cart.quantity += 1
           cart.save()
        except Cart.DoesNotExist:
           Cart.objects.create(user=user, product=prod)
        return redirect('medicine')
    else:
        return redirect('login')


def view_cart_items(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = cart_items.aggregate(total=Sum('subtotal'))['total'] or 0
    shipping_cost = 100
    total_amount = cart_total + shipping_cost
    return render(request, 'cart.html',locals())


def remove_from_cart(request,id):
    remove_product =Cart.objects.get(id =id)
    remove_product.delete()
    return redirect('view_cart_items') 


def update_cart_item(request,item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            product = cart_item.product
            if quantity <= product.quantity:
                product.quantity -= (quantity - cart_item.quantity)
                product.save()
                cart_item.quantity = quantity
                cart_item.save()
            else:
                messages.error(request, 'Requested quantity exceeds available quantity.')
        elif quantity == 0:
            cart_item.delete()
        else:
            messages.error(request, 'Invalid quantity.')
    return redirect('view_cart_items')




@login_required
def creatOrder(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_price = Decimal('0.00')
    subtotalall = Decimal('0.00')  # Initialize the cumulative subtotal
    delivery_fee = 100
    
    for item in cart_items:
        subtotal = item.product.price * item.quantity
        subtotalall += subtotal
        total_price += subtotal
        item.subtotal = subtotal
    
    # Add a fixed delivery fee of 100 taka
    total_price += delivery_fee
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email_address = request.POST.get('email_address')
        payment = 'pending'
        
        if all([first_name, last_name, address, phone_number, email_address]):
            order = Order.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone_number=phone_number,
                email_address=email_address,
                total_price=total_price,
                payment=payment
            )
            return redirect('medicine')  # Replace 'shop' with the appropriate URL name for your shop page
    
    return render(request, 'checkout.html', locals())


@login_required
def cheak_out(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)
    total_price = Decimal('0.00')
    subtotalall = Decimal('0.00')  # Initialize the cumulative subtotal
    delivery_fee = 100  # Define your delivery fee

    for item in cart_items:
        subtotal = item.product.price * item.quantity
        subtotalall += subtotal
        total_price += subtotal
        item.subtotal = subtotal

    if subtotalall == 0:
        messages.warning(request, 'Your cart is empty. Add products to proceed to checkout.')
        return redirect('medicine')

    if request.method == 'POST':
        payment_option = request.POST.get('payment_option')

        if payment_option == 'sslcommerz_payment':
            cart_products = Cart.objects.filter(user=request.user)
            
            if cart_products:
                total_amount = Decimal('0.00')
                for cart_product in cart_products:
                    total_amount += cart_product.quantity * cart_product.product.price
                total_with_shipping = total_amount + delivery_fee

                sslcz = SSLCOMMERZ({
                    'store_id': 'niyam6412dc52e1e89',
                    'store_pass': 'niyam6412dc52e1e89@ssl',
                    'issandbox': True
                })

                data = {
                    'total_amount': str(total_with_shipping),
                    'currency': 'BDT',
                    'tran_id': 'tran_12345',
                    'success_url': 'http://127.0.0.1:8000/payment/success/',
                    'fail_url': 'http://127.0.0.1:8000/payment/fail/',
                    'cancel_url': 'http://127.0.0.1:8000/payment/cancel/',
                    'emi_option': '0',
                    'cus_name': 'test',
                    'cus_email': 'test@test.com',
                    'cus_phone': '01700000000',
                    'cus_add1': 'customer address',
                    'cus_city': 'Dhaka',
                    'cus_country': 'Bangladesh',
                    'shipping_method': 'NO',
                    'multi_card_name': '',
                    'num_of_item': 1,
                    'product_name': 'Test',
                    'product_category': 'Test Category',
                    'product_profile': 'general',
                }

                response = sslcz.createSession(data)
                return HttpResponseRedirect(response['GatewayPageURL'])

        elif payment_option == 'cash_on_delivery':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            email_address = request.POST.get('email_address')

            if all([first_name, last_name, address, phone_number, email_address]):
                order = Order.objects.create(
                    user=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    phone_number=phone_number,
                    email_address=email_address,
                    total_price=total_price + delivery_fee,
                    payment='pending'
                )
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        subtotal_amount=item.subtotal
                    )
                    # Decrease product quantity
                    item.product.quantity -= item.quantity
                    item.product.save()
                cart_items.delete()

                messages.success(request, 'Cash on Delivery selected. Your order has been placed.')
                return redirect('medicine')
            else:
                messages.error(request, 'Please fill out all the required fields.')
                return redirect('cheak_out')

    pending_order = Order.objects.filter(user=request.user, payment='pending').first()
    return render(request, 'shop_checkout.html', locals())
