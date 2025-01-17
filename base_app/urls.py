from django.urls import path, include
from .views import *
from base_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/', views.customer, name='customer'),
    path('about/', views.about, name='about'),
]
