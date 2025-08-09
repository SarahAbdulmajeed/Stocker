from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse 
from django.contrib import messages
from django.contrib.auth.decorators	import login_required
from .models import Category, Supplier
from .forms import CategoryForm
from django.core.paginator import Paginator 



def home_view(request: HttpRequest):
	return render(request, "main/index.html")

def dashboard_view(request: HttpRequest):
	return render(request, "main/dashboard.html")

#===========[Category]===========
def categories_view(request: HttpRequest):
	categories = Category.objects.all()
	page_number = request.GET.get("page",1)
	paginator = Paginator(categories,7)
	categories_page = paginator.get_page(page_number)
	return render(request, "main/category/all.html", {'categories':categories_page})

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
def Suppliers_view(request: HttpRequest):
	suppliers = Supplier.objects.all()
	page_number = request.GET.get("page",1)
	paginator = Paginator(suppliers,7)
	suppliers_page = paginator.get_page(page_number)
	return render(request, "main/category/all.html", {'suppliers':suppliers_page})

def add_supplier(request: HttpRequest):
	if request.method == "POST":
		category_form = CategoryForm(request.POST)
		if category_form.is_valid():
			category_form.save()
			messages.success(request, "Created Category Successfully!")
			return redirect('main:categories_view')
		else:
			print(category_form.errors)
	return render(request, "main/category/add.html")

def edit_supplier(request: HttpRequest, category_id):
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

def delete_supplier(request: HttpRequest, category_id):
	category = Category.objects.get(pk=category_id)
	if request.method == "POST":
		category.delete()
		messages.success(request, "Category Deleted Successfully!")
		return redirect("main:categories_view")
	return render(request, "main/category/delete.html",{"category":category})

#===========[Product]===========
def all_products_view(request: HttpRequest):
	return render(request, "main/products.html")