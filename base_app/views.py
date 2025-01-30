from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.

def home(request):
    orders = Orders.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    context = {
                'orders' : orders, 
                'customers' : customers,
                'total_orders' : total_orders,                                        
                'delivered' : delivered,
                'pending' : pending,
            }
    
    return render(request,'base_app/dashboard.html', context)

def products(request):
    products = Products.objects.all()
    return render(request,'base_app/products.html', {'products' : products})

def about(request):
    return render(request,'base_app/about.html')

def customer(request):
    return render(request,'base_app/customers.html')