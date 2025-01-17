from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request,'base_app/dashboard.html')

def products(request):
    return render(request,'base_app/products.html')

def about(request):
    return render(request,'base_app/about.html')

def customer(request):
    return render(request,'base_app/customers.html')