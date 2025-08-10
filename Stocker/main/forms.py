from django import forms
from .models import Category, Supplier, Product, StockEntry

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = "__all__"