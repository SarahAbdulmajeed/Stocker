from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse 
from django.contrib import messages
from django.contrib.auth.decorators	import login_required
from .models import Category, Supplier, Product
from .forms import CategoryForm, SupplierForm, ProductForm
from django.core.paginator import Paginator 



def home_view(request: HttpRequest):
	return render(request, "main/index.html")

def dashboard_view(request: HttpRequest):
	return render(request, "main/dashboard.html")

#===========[Category]===========
def categories_view(request: HttpRequest):
	categories = Category.objects.all()
	total_categories = categories.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(categories,7)
	categories_page = paginator.get_page(page_number)
	return render(request, "main/category/all.html", {'categories':categories_page, 'total_categories':total_categories})

def add_category(request: HttpRequest):
	if request.method == "POST":
		category_form = CategoryForm(request.POST)
		if category_form.is_valid():
			category_form.save()
			messages.success(request, "Created Category Successfully!")
			return redirect('main:categories_view')
		else:
			print(category_form.errors)
	return render(request, "main/category/add.html")

def edit_category(request: HttpRequest, category_id):
	category = Category.objects.get(pk=category_id)
	if request.method == "POST":
		category_form = CategoryForm(request.POST, instance=category)
		if category_form.is_valid():
			category_form.save()
			messages.success(request, "Edit Category Successfully!")
			return redirect("main:categories_view")
		else:
			print(category_form.errors)
	return render(request, "main/category/edit.html",{"category":category})

def delete_category(request: HttpRequest, category_id):
	category = Category.objects.get(pk=category_id)
	if request.method == "POST":
		category.delete()
		messages.success(request, "Category Deleted Successfully!")
		return redirect("main:categories_view")
	return render(request, "main/category/delete.html",{"category":category})

#===========[Supplier]===========
def suppliers_view(request: HttpRequest):
	suppliers = Supplier.objects.all()
	total_suppliers = suppliers.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(suppliers,7)
	suppliers_page = paginator.get_page(page_number)
	return render(request, "main/supplier/all.html", {'suppliers':suppliers_page, 'total_suppliers':total_suppliers})

def add_supplier(request: HttpRequest):
	if request.method == "POST":
		supplier_form = SupplierForm(request.POST)
		if supplier_form.is_valid():
			supplier_form.save()
			messages.success(request, "Created Supplier Successfully!")
			return redirect('main:suppliers_view')
		else:
			print(supplier_form.errors)
	return render(request, "main/supplier/add.html")

def edit_supplier(request: HttpRequest, supplier_id):
	supplier = Supplier.objects.get(pk=supplier_id)
	if request.method == "POST":
		supplier_form = SupplierForm(request.POST, instance=supplier)
		if supplier_form.is_valid():
			supplier_form.save()
			messages.success(request, "Edit Supplier Successfully!")
			return redirect("main:suppliers_view")
		else:
			print(supplier_form.errors)
	return render(request, "main/supplier/edit.html",{"supplier":supplier})

def delete_supplier(request: HttpRequest, supplier_id):
	supplier = Supplier.objects.get(pk=supplier_id)
	if request.method == "POST":
		supplier.delete()
		messages.success(request, "Supplier Deleted Successfully!")
		return redirect("main:suppliers_view")
	return render(request, "main/supplier/delete.html",{"supplier":supplier})

#===========[Product]===========
def products_view(request: HttpRequest):
	products = Product.objects.all()
	total_products = products.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(products,7)
	products_page = paginator.get_page(page_number)
	return render(request, "main/product/all.html", {'products':products_page, 'total_products':total_products})

def add_product(request: HttpRequest):
	categories = Category.objects.all()
	if request.method == "POST":
		product_form = ProductForm(request.POST)
		if product_form.is_valid():
			product_form.save()
			messages.success(request, "Created Product Successfully!")
			return redirect('main:products_view')
		else:
			messages.error(request, "Please fix the errors below.")
			print(product_form.errors)
	return render(request, "main/product/add.html", {'categories':categories})

def edit_product(request: HttpRequest, product_id):
	categories = Category.objects.all()
	product = Product.objects.get(pk=product_id)
	if request.method == "POST":
		product_form = ProductForm(request.POST, instance=product)
		if product_form.is_valid():
			product_form.save()
			messages.success(request, "Edit Product Successfully!")
			return redirect("main:products_view")
		else:
			print(product_form.errors)
	return render(request, "main/product/edit.html",{"product":product, 'categories':categories})

def delete_product(request: HttpRequest, product_id):
	categories = Category.objects.all()
	product = Product.objects.get(pk=product_id)
	if request.method == "POST":
		product.delete()
		messages.success(request, "Product Deleted Successfully!")
		return redirect("main:products_view")
	return render(request, "main/product/delete.html",{"product":product, 'categories':categories})
