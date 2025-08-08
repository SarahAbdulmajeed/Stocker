from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout

def sign_up (request: HttpRequest):
    if request.method == "POST":
        try: 
            new_user = User.objects.create_user(username=request.POST["username"], email=request.POST["email"], password=request.POST["password"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            new_user.save()
            messages.success(request,"Account created successfully!")
            return redirect("accounts:sign_in")
        except Exception as e:
            print(e)
            messages.error(request, "An error occurred while creating your account. Please try again.")
    return render(request, "accounts/signup.html")

def sign_in (request: HttpRequest):
    if request.method == "POST":
        try:
            user = authenticate(request, username = request.POST["username"], password = request.POST["password"])
            if user:
                login(request, user)
                messages.success(request,"Welcome back, " + user.first_name + "!")
                return redirect('main:dashboard_view')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        except Exception as e:
            print(e)
    return render(request, "accounts/signin.html")


def log_out (request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("main:home_view")