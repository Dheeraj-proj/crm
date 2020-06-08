from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    logo_pic = models.ImageField(default="DELO.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    CATEGORY = (
        ('POD', 'POD'),
        ('MANUF', 'MANUF'),
        ('BULK', 'BULK'),

    )



    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_manufactured = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('OUT FOR DELIVERY', 'OUT FOR DELIVERY'),
        ('DELIVERED', 'DELIVERED'),
        )



    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status =  models.CharField(max_length=100, null=True, choices=STATUS)
    note =  models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.product.name
        return self.customer.name



