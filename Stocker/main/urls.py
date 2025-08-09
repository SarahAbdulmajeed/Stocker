from django.urls import path 
from . import views  

app_name = "main"

urlpatterns = [ 
    path('', views.home_view, name='home_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('products/', views.all_products_view, name='all_products_view'),
    path('categories/', views.categories_view, name='categories_view'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<category_id>', views.edit_category, name='edit_category'),
    path('categories/delete/<category_id>', views.delete_category, name='delete_category'),
] 