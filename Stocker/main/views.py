from django.shortcuts import render
from django.http import HttpRequest, HttpResponse 

def home_view(request: HttpRequest):
	return render(request, "main/index.html")

def dashboard_view(request: HttpRequest):
	if request.user.is_authenticated:
		print(request.user)
	return render(request, "main/dashboard.html")
