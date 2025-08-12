from django.urls import path 
from . import views  

app_name = "main"

urlpatterns = [ 
    path('', views.home_view, name='home_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    # Product
    path('products/', views.products_view, name='products_view'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/details/<product_id>', views.product_detail, name='product_detail'),
    path('products/edit/<product_id>', views.edit_product, name='edit_product'),
    path('products/delete/<product_id>', views.delete_product, name='delete_product'),
    # Category
    path('categories/', views.categories_view, name='categories_view'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<category_id>', views.edit_category, name='edit_category'),
    path('categories/delete/<category_id>', views.delete_category, name='delete_category'),
    # Supplier
    path('suppliers/', views.suppliers_view, name='suppliers_view'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/view/<supplier_id>', views.supplier_detail, name='supplier_detail'),
    path('suppliers/edit/<supplier_id>', views.edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<supplier_id>', views.delete_supplier, name='delete_supplier'),
   # Stock Entry 
    path('stock_entry/', views.stock_entries_view, name='stock_entries_view'),
    path('stock_entry/add/', views.add_stock_entry, name='add_stock_entry'),
    path('stock_entry/edit/<stock_entry_id>', views.edit_stock_entry, name='edit_stock_entry'),
    path('stock_entry/delete/<stock_entry_id>', views.delete_stock_entry, name='delete_stock_entry'),
    path('stock_entry/withdraw/<stock_entry_id>', views.withdraw_stock_entry, name='withdraw_stock_entry'),
    path('stock_withdraw/all/', views.withdrawals_view, name='withdrawals_view'),
    # Reports 
    path('reports/inventory/', views.inventory_report_view, name='inventory_report_view'),
    path('reports/supplier/', views.supplier_report_view, name='supplier_report_view'),
] 