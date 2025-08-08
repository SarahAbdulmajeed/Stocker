from django.db import models
from django.contrib.auth.models import User 

class Supplier(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class StockEntry(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    received_date = models.DateField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)