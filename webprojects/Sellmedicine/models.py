from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import admin
from django.utils import timezone
from django.db import models

User = get_user_model()

# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='prof_pic/', null=True, blank=True)
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE)  # Corrected field name
    details = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        self.total_amount = self.subtotal + 100  # Add the shipping cost
        super().save(*args, **kwargs)
from django.db import models
from django.contrib.auth.models import User
from random import randint
from decimal import Decimal
from django.utils import timezone

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )
    
    first_name = models.CharField(max_length=50, default='', blank=True)
    last_name = models.CharField(max_length=50, default='', blank=True)
    phone_number = models.CharField(max_length=20, default='', blank=True)
    order_id = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=50)
    payment = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    order_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - Order ID: {self.order_id}"

    def generate_order_id(self):
        while True:
            order_id = randint(100000, 999999)
            if not Order.objects.filter(order_id=order_id).exists():
                return order_id

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()

        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=False)
    subtotal_amount = models.DecimalField(max_digits=9, decimal_places=2)  # Change field name to avoid conflict

    def calculate_subtotal(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        self.subtotal_amount = self.calculate_subtotal()
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.id} - {self.product.name} ({self.quantity})"
