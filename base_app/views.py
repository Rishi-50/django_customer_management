from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *


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

def customer(request,pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.orders_set.all()

    orders_count = orders.count()

    context = {
                'customer': customer,
                'orders': orders,
                'orders_count': orders_count
            }
    return render(request,'base_app/customers.html', context) 


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {'form' : form}
    return render(request, 'base_app/order_form.html', context)


def updateOrder(request,pk):
    order = Orders.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form' : form}
    return render(request, 'base_app/order_form.html', context)


def deleteOrder(request,pk):
    order = Orders.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
        
    context = {'item' : order}
    return render(request, 'base_app/delete.html',context)