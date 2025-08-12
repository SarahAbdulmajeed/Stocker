from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Category, Supplier, Product, StockEntry, StockWithdrawal
from .forms import CategoryForm, SupplierForm, ProductForm, StockEntryForm, StockWithdrawalForm
from django.core.paginator import Paginator
from django.db.models import Sum, Q, F

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date, timedelta

def home_view(request: HttpRequest):
	return render(request, "main/index.html")

@login_required
def dashboard_view(request: HttpRequest):
	total_products = Product.objects.count()
	total_categories = Category.objects.count()
	total_suppliers = Supplier.objects.count()
	total_stock_qty = StockEntry.objects.aggregate(total=Sum('quantity'))['total'] or 0
	low_stock_count = Product.objects.annotate(qty=Sum('stockentry__quantity', default=0)).filter(qty__lt=F('reorder_level')).count() if hasattr(Product, 'reorder_level') else 0
	recent_entries = StockEntry.objects.select_related('product','supplier').order_by('-created_at')[:5]
	recent_withdrawals = StockWithdrawal.objects.select_related('product','stock_entry__supplier').order_by('-created_at')[:5]
	top_categories = Category.objects.annotate(qty=Sum('product__stockentry__quantity', default=0)).order_by('-qty')[:5]
	top_suppliers = Supplier.objects.annotate(qty=Sum('stockentry__quantity', default=0)).order_by('-qty')[:5]
	return render(request, "main/dashboard.html", {
		'total_products': total_products,
		'total_categories': total_categories,
		'total_suppliers': total_suppliers,
		'total_stock_qty': total_stock_qty,
		'low_stock_count': low_stock_count,
		'recent_entries': recent_entries,
		'recent_withdrawals': recent_withdrawals,
		'top_categories': top_categories,
		'top_suppliers': top_suppliers,
	})

#===========[Category]===========
@login_required
def categories_view(request: HttpRequest):
	categories = Category.objects.all()
	if 'search' in request.GET:
		categories = categories.filter(Q(name__icontains=request.GET['search']))
	total_categories = categories.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(categories,7)
	categories_page = paginator.get_page(page_number)
	return render(request, "main/category/all.html", {'categories':categories_page, 'total_categories':total_categories})

@login_required
@permission_required('main.add_category', raise_exception=True)
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

@login_required
@permission_required('main.change_category', raise_exception=True)
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

@login_required
@permission_required('main.delete_category', raise_exception=True)
def delete_category(request: HttpRequest, category_id):
	category = Category.objects.get(pk=category_id)
	if request.method == "POST":
		category.delete()
		messages.success(request, "Category Deleted Successfully!")
		return redirect("main:categories_view")
	return render(request, "main/category/delete.html",{"category":category})

#===========[Supplier]===========
@login_required
def suppliers_view(request: HttpRequest):
	suppliers = Supplier.objects.all()
	if 'search' in request.GET:
		suppliers = suppliers.filter(Q(name__icontains=request.GET['search']))
	total_suppliers = suppliers.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(suppliers,7)
	suppliers_page = paginator.get_page(page_number)
	return render(request, "main/supplier/all.html", {'suppliers':suppliers_page, 'total_suppliers':total_suppliers})

@login_required
@permission_required('main.add_supplier', raise_exception=True)
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

@login_required
@permission_required('main.change_supplier', raise_exception=True)
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

@login_required
@permission_required('main.delete_supplier', raise_exception=True)
def delete_supplier(request: HttpRequest, supplier_id):
	supplier = Supplier.objects.get(pk=supplier_id)
	if request.method == "POST":
		supplier.delete()
		messages.success(request, "Supplier Deleted Successfully!")
		return redirect("main:suppliers_view")
	return render(request, "main/supplier/delete.html",{"supplier":supplier})

@login_required
def supplier_detail(request: HttpRequest, supplier_id: int):
	supplier = Supplier.objects.get(pk=supplier_id)
	products = Product.objects.filter(stockentry__supplier=supplier).annotate(supplier_qty=Sum('stockentry__quantity', filter=Q(stockentry__supplier=supplier), default=0)).order_by('name')
	total_products = products.count()
	stock_entries = StockEntry.objects.filter(supplier=supplier).select_related('product').order_by('-created_at')
	total_entries = stock_entries.count()
	total_qty = stock_entries.aggregate(total=Sum('quantity'))['total'] or 0
	page_number = request.GET.get("page", 1)
	paginator = Paginator(stock_entries, 7)
	entries_page = paginator.get_page(page_number)
	return render(request, "main/supplier/details.html", {'supplier': supplier,'products': products,'total_products': total_products,'total_entries': total_entries,'total_qty': total_qty,'stock_entries': entries_page,})

#===========[Product]===========
@login_required
def products_view(request: HttpRequest):
	products = Product.objects.annotate(total_qty=Sum('stockentry__quantity', default=0))
	if 'search' in request.GET:
		search = request.GET['search']
		products = products.filter(Q(name__icontains=search) | Q(sku__icontains=search))
		if "order_by" in request.GET and request.GET["order_by"] == "category":
			products = products.order_by("-category__name")
		elif "order_by" in request.GET and request.GET["order_by"] == "created_at":
			products = products.order_by("-created_at")
	total_products = products.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(products,7)
	products_page = paginator.get_page(page_number)
	return render(request, "main/product/all.html", {'products':products_page, 'total_products':total_products})

@login_required
def product_detail(request: HttpRequest, product_id):
	product = Product.objects.get(pk=product_id)
	stock_entries = StockEntry.objects.filter(product=product).select_related('supplier').order_by('-created_at')
	total_qty = stock_entries.aggregate(total_qty=Sum('quantity'))['total_qty'] or 0
	stock_status = "LOW" if hasattr(product, 'reorder_level') and total_qty < (product.reorder_level or 0) else "OK"
	return render(request, "main/product/details.html", {'product': product,'stock_entries': stock_entries,'total_qty': total_qty,'stock_status': stock_status,})

@login_required
@permission_required('main.add_product', raise_exception=True)
def add_product(request: HttpRequest):
	categories = Category.objects.all()
	if request.method == "POST":
		product_form = ProductForm(request.POST, request.FILES)
		if product_form.is_valid():
			product_form.save()
			messages.success(request, "Created Product Successfully!")
			return redirect('main:products_view')
		else:
			messages.error(request, "Please fix the errors below.")
			print(product_form.errors)
	return render(request, "main/product/add.html", {'categories':categories})

@login_required
@permission_required('main.change_product', raise_exception=True)
def edit_product(request: HttpRequest, product_id):
	categories = Category.objects.all()
	product = Product.objects.get(pk=product_id)
	if request.method == "POST":
		product_form = ProductForm(request.POST,request.FILES ,instance=product)
		if product_form.is_valid():
			product_form.save()
			messages.success(request, "Edit Product Successfully!")
			return redirect("main:products_view")
		else:
			print(product_form.errors)
	return render(request, "main/product/edit.html",{"product":product, 'categories':categories})

@login_required
@permission_required('main.delete_product', raise_exception=True)
def delete_product(request: HttpRequest, product_id):
	categories = Category.objects.all()
	product = Product.objects.get(pk=product_id)
	if request.method == "POST":
		product.delete()
		messages.success(request, "Product Deleted Successfully!")
		return redirect("main:products_view")
	return render(request, "main/product/delete.html",{"product":product, 'categories':categories})

#===========[Stock Entry]===========
@login_required
def stock_entries_view(request: HttpRequest):
	stock_entries = StockEntry.objects.all()
	if 'search' in request.GET:
		search = request.GET['search']
		stock_entries = stock_entries.filter(product__name__icontains=search)
		if "order_by" in request.GET and request.GET["order_by"] == "category":
			stock_entries = stock_entries.order_by("-product__category__name")
		elif "order_by" in request.GET and request.GET["order_by"] == "supplier":
			stock_entries = stock_entries.order_by("-supplier__name")
	total_stock_entries = stock_entries.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(stock_entries,7)
	products_page = paginator.get_page(page_number)
	return render(request, "main/stock_entry/all.html", {'stock_entries':products_page, 'total_stock_entries':total_stock_entries})

@login_required
@permission_required('main.add_stockentry', raise_exception=True)
def add_stock_entry(request: HttpRequest):
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    if request.method == "POST":
        stock_entry_form = StockEntryForm(request.POST)
        if stock_entry_form.is_valid():
            entry = stock_entry_form.save()
            _maybe_low_stock(entry.product)
            days = int(getattr(settings, "EXPIRY_ALERT_DAYS", 7))
            if entry.quantity and entry.expiry_date:
                if entry.expiry_date <= date.today() + timedelta(days=days) and not getattr(entry, "expiry_notified", False):
                    _send_expiry_email(entry)
                    if hasattr(entry, "expiry_notified"):
                        entry.expiry_notified = True
                        entry.save(update_fields=["expiry_notified"])
            messages.success(request, "Created Stock Entry Successfully!")
            return redirect('main:stock_entries_view')
        else:
            messages.error(request, "Please fix the errors below.")
            print(stock_entry_form.errors)
    return render(request, "main/stock_entry/add.html", {'products':products, 'suppliers':suppliers})

@login_required
@permission_required('main.change_stockentry', raise_exception=True)
def edit_stock_entry(request: HttpRequest, stock_entry_id):
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    stock_entry = StockEntry.objects.get(pk=stock_entry_id)
    if request.method == "POST":
        stock_entry_form = StockEntryForm(request.POST, instance=stock_entry)
        if stock_entry_form.is_valid():
            entry = stock_entry_form.save()
            _maybe_low_stock(entry.product)
            days = int(getattr(settings, "EXPIRY_ALERT_DAYS", 7))
            if entry.quantity and entry.expiry_date:
                if entry.expiry_date <= date.today() + timedelta(days=days) and not getattr(entry, "expiry_notified", False):
                    _send_expiry_email(entry)
                    if hasattr(entry, "expiry_notified"):
                        entry.expiry_notified = True
                        entry.save(update_fields=["expiry_notified"])
            messages.success(request, "Edit Stock Entry Successfully!")
            return redirect("main:stock_entries_view")
        else:
            print(stock_entry_form.errors)
    return render(request, "main/stock_entry/edit.html",{"stock_entry":stock_entry, 'products':products, 'suppliers':suppliers})

@login_required
@permission_required('main.add_stockwithdrawal', raise_exception=True)
@permission_required('main.change_stockentry', raise_exception=True)
def withdraw_stock_entry(request: HttpRequest, stock_entry_id):
	stock_entry = StockEntry.objects.get(pk=stock_entry_id)
	if request.method == "POST":
		withdraw_stock_form = StockWithdrawalForm(request.POST)
		if withdraw_stock_form.is_valid():
			withdrawal = withdraw_stock_form.save(commit=False)
			withdrawal.stock_entry = stock_entry
			withdrawal.product = stock_entry.product
			qty = withdrawal.quantity or 0
			if qty <= 0:
				messages.error(request, "Quantity must be greater than 0.")
			elif stock_entry.quantity < qty:
				messages.error(request, "Not enough quantity in this entry.")
			else:
				stock_entry.quantity = stock_entry.quantity - qty
				stock_entry.save()
				withdrawal.save()
				_maybe_low_stock(stock_entry.product)
				messages.success(request, "Withdrawal recorded and stock updated!")
				return redirect("main:stock_entries_view")
		else:
			print(withdraw_stock_form.errors)
	else:
		withdraw_stock_form = StockWithdrawalForm()
	return render(request, "main/stock_entry/withdraw.html", {'stock_entry': stock_entry})

@login_required
@permission_required('main.delete_stockentry', raise_exception=True)
def delete_stock_entry(request: HttpRequest, stock_entry_id):
	products = Product.objects.all()
	suppliers = Supplier.objects.all()
	stock_entry = StockEntry.objects.get(pk=stock_entry_id)
	if request.method == "POST":
		stock_entry.delete()
		messages.success(request, "Stock Entry Deleted Successfully!")
		return redirect("main:stock_entries_view")
	return render(request, "main/stock_entry/delete.html",{"stock_entry":stock_entry, 'products':products, 'suppliers':suppliers})

@login_required
def withdrawals_view(request: HttpRequest):
	withdrawals = StockWithdrawal.objects.all()
	if 'search' in request.GET:
		search = request.GET['search']
		withdrawals = withdrawals.filter(Q(product__name__icontains=search) | Q(product__sku__icontains=search))
		if "order_by" in request.GET and request.GET["order_by"] == "date":
			withdrawals = withdrawals.order_by("-created_at")
		elif "order_by" in request.GET and request.GET["order_by"] == "product":
			withdrawals = withdrawals.order_by("product__name")
		elif "order_by" in request.GET and request.GET["order_by"] == "supplier":
			withdrawals = withdrawals.order_by("stock_entry__supplier__name")
		elif "order_by" in request.GET and request.GET["order_by"] == "reason":
			withdrawals = withdrawals.order_by("reason")
	total_withdrawals = withdrawals.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(withdrawals,7)
	withdrawals_page = paginator.get_page(page_number)
	return render(request, "main/stock_withdraw/all.html", {'withdrawals': withdrawals_page,'total_withdrawals': total_withdrawals})

#===========[Reports]===========
@login_required
def inventory_report_view(request: HttpRequest):
	products = Product.objects.all()
	if 'search' in request.GET:
		search = request.GET['search']
		products = products.filter(Q(name__icontains=search) | Q(sku__icontains=search))
	start = request.GET.get('start')
	end = request.GET.get('end')
	products = products.annotate(current_stock=Sum('stockentry__quantity', default=0))
	if start and end:
		products = products.annotate(in_qty=Sum('stockentry__initial_quantity', filter=Q(stockentry__created_at__date__range=[start, end]), default=0),out_qty=Sum('stockwithdrawal__quantity', filter=Q(stockwithdrawal__created_at__date__range=[start, end]), default=0),)
	else:
		products = products.annotate(in_qty=Sum('stockentry__initial_quantity', default=0),out_qty=Sum('stockwithdrawal__quantity', default=0),)
	products = products.annotate(net_movement=F('in_qty') - F('out_qty'))
	if 'order_by' in request.GET:
		ob = request.GET['order_by']
		if ob == "current": products = products.order_by("-current_stock")
		elif ob == "in": products = products.order_by("-in_qty")
		elif ob == "out": products = products.order_by("-out_qty")
		elif ob == "net": products = products.order_by("-net_movement")
		else: products = products.order_by("name")
	else:
		products = products.order_by("name")
	total_products = products.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(products, 10)
	products_page = paginator.get_page(page_number)
	return render(request, "main/reports/inventory.html", {'products': products_page,'total_products': total_products,})

@login_required
def supplier_report_view(request: HttpRequest):
	suppliers = Supplier.objects.all()
	if 'search' in request.GET:
		search = request.GET['search']
		suppliers = suppliers.filter(Q(name__icontains=search))
	start = request.GET.get('start')
	end = request.GET.get('end')
	if start and end:
		suppliers = suppliers.annotate(in_qty=Sum('stockentry__initial_quantity', filter=Q(stockentry__created_at__date__range=[start, end]), default=0),out_qty=Sum('stockentry__stockwithdrawal__quantity', filter=Q(stockentry__stockwithdrawal__created_at__date__range=[start, end]), default=0),current_stock=Sum('stockentry__quantity', default=0),)
	else:
		suppliers = suppliers.annotate(in_qty=Sum('stockentry__initial_quantity', default=0),out_qty=Sum('stockentry__stockwithdrawal__quantity', default=0),current_stock=Sum('stockentry__quantity', default=0),)
	if 'order_by' in request.GET:
		ob = request.GET['order_by']
		if ob == "current": suppliers = suppliers.order_by("-current_stock")
		else: suppliers = suppliers.order_by("name")
	else:
		suppliers = suppliers.order_by("name")
	total_suppliers = suppliers.count()
	page_number = request.GET.get("page",1)
	paginator = Paginator(suppliers, 10)
	suppliers_page = paginator.get_page(page_number)
	return render(request, "main/reports/suppliers.html", {'suppliers': suppliers_page,'total_suppliers': total_suppliers,})


# mail 

def _manager_to_list():
	to = []
	if getattr(settings, "MANAGER_EMAIL", None):
		to.append(settings.MANAGER_EMAIL)
	return to

def _product_total_qty(product_id: int):
	return Product.objects.filter(pk=product_id).aggregate(total=Sum('stockentry__quantity'))['total'] or 0

def _send_low_stock_email(product, total_qty):
	to = _manager_to_list()
	if not to:
		return
	subject = f"[Stocker] Low stock: {product.name} ({product.sku})"
	html = render_to_string("emails/low_stock.html", {"product": product, "total_qty": total_qty})
	EmailMessage(subject, html, settings.DEFAULT_FROM_EMAIL, to).send(fail_silently=True)

def _send_expiry_email(entry):
	to = _manager_to_list()
	if not to:
		return
	subject = f"[Stocker] Expiry approaching: {entry.product.name}"
	html = render_to_string("emails/expiry_alert.html", {"entry": entry})
	EmailMessage(subject, html, settings.DEFAULT_FROM_EMAIL, to).send(fail_silently=True)

def _maybe_low_stock(product):
	total_qty = _product_total_qty(product.id)
	reorder = getattr(product, "reorder_level", 0) or 0
	low = total_qty < reorder
	notified = getattr(product, "low_stock_notified", False)
	if low and not notified:
		_send_low_stock_email(product, total_qty)
		if hasattr(product, "low_stock_notified"):
			product.low_stock_notified = True
			product.save(update_fields=["low_stock_notified"])
	elif not low and notified:
		if hasattr(product, "low_stock_notified"):
			product.low_stock_notified = False
			product.save(update_fields=["low_stock_notified"])
