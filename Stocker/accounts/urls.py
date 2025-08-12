from django.urls import path 
from . import views  

app_name = "accounts"

urlpatterns = [ 
    path('signup/', views.sign_up, name='sign_up'),
    path('signin/', views.sign_in, name='sign_in'),
    path('logout/', views.log_out, name='log_out'),
    path("pending/", views.pending_users, name="pending_users"),
    path("approve/<int:user_id>/", views.approve_user, name="approve_user"),

] 