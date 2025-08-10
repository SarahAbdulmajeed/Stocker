from django.urls import path 
from . import views  

app_name = "main"

urlpatterns = [ 
    path('', views.home_view, name='home_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    # Product
    path('products/', views.products_view, name='products_view'),
    path('products/add/', views.add_product, name='add_product'),
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
    path('suppliers/edit/<supplier_id>', views.edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<supplier_id>', views.delete_supplier, name='delete_supplier'),
   
] 