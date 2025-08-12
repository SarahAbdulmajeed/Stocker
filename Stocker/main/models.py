from django.db import models
from django.contrib.auth.models import User 
from django.db.models import F

class Supplier(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    mobile = models.CharField(max_length=20, blank=True) 
    email = models.EmailField(max_length=254, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=1024, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    reorder_level = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="images/products/", default="images/products/default.png")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    low_stock_notified = models.BooleanField(default=False)

class StockEntry(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier,on_delete=models.PROTECT)
    initial_quantity = models.PositiveIntegerField(editable=False, default=0)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField(blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_notified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.initial_quantity = self.quantity
        super().save(*args, **kwargs)

class StockWithdrawal(models.Model):
    REASON_CHOICES = [
        ("SALE", "Sale"),
        ("DAMAGE", "Damage"),
        ("RETURN", "Return to supplier"),
        ("ADJUST", "Inventory adjust"),
        ("OTHER", "Other"),
    ]

    stock_entry = models.ForeignKey(StockEntry,on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, editable=False)
    quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=12, choices=REASON_CHOICES, default="SALE")
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
