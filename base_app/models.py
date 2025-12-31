from django.db import models


class TimeStamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(TimeStamps):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=13, null=True)

    def __str__(self):
        return self.name


class Products(TimeStamps):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=100, null=True)
    supplier = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Orders(TimeStamps):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )

    customer_name = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS_CHOICES)
    note = models.CharField(max_length=255, null=True)  

    def __str__(self):
        return self.product.name