from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from .filters import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
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

@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account created for " + user)
                return redirect('login')

        context = {'form' : form}
        return render(request, 'base_app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
                return redirect('login')

        context = {}
        return render(request, 'base_app/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def products(request):
    products = Products.objects.all()
    return render(request,'base_app/products.html', {'products' : products})    

def about(request):
    return render(request,'base_app/about.html')


@login_required(login_url='login')
def customer(request,pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.orders_set.all()

    orders_count = orders.count()

    customer_filter = OrderFilter(request.GET, queryset=orders)
    orders = customer_filter.qs

    context = {
                'customer': customer,
                'orders': orders,
                'orders_count': orders_count,
                'customer_filter': customer_filter,
            }
    return render(request,'base_app/customers.html', context) 


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Orders, fields=('product', 'status'),fk_name='customer_name',extra=7)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Orders.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer_name':customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        
    context = {'formset' : formset}
    return render(request, 'base_app/order_form.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteOrder(request,pk):
    order = Orders.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
        
    context = {'item' : order}
    return render(request, 'base_app/delete.html',context)