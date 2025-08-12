from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

def sign_up(request: HttpRequest):
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password"],
                first_name=request.POST.get("first_name", ""),
                last_name=request.POST.get("last_name", "")
            )
            new_user.is_active = False
            new_user.is_staff = False
            new_user.save()
            messages.success(request, "Account created. Wait for admin approval.")
            return redirect("accounts:sign_in")
        except Exception as e:
            print(e)
            messages.error(request, "An error occurred while creating your account. Please try again.")
    return render(request, "accounts/signup.html")

def sign_in(request: HttpRequest):
    if request.method == "POST":
        try:
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user:
                if not user.is_active:
                    messages.error(request, "Your account is pending approval.")
                else:
                    login(request, user)
                    messages.success(request, "Welcome back, " + (user.first_name or user.username) + "!")
                    return redirect('main:dashboard_view')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        except Exception as e:
            print(e)
    return render(request, "accounts/signin.html")

def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("main:home_view")

@login_required
@permission_required('auth.change_user', raise_exception=True)
def pending_users(request: HttpRequest):
    users = User.objects.filter(is_active=False).order_by('-date_joined')
    return render(request, "accounts/pending.html", {"users": users})

@login_required
@permission_required('auth.change_user', raise_exception=True)
def approve_user(request: HttpRequest, user_id: int):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        role = request.POST.get("role", "employee")
        user.is_active = True
        if role == "admin":
            user.is_staff = True
            group, _ = Group.objects.get_or_create(name="Admin")
        else:
            user.is_staff = False
            group, _ = Group.objects.get_or_create(name="Employee")
        user.save()
        user.groups.clear()
        user.groups.add(group)
        messages.success(request, "User approved.")
        return redirect("accounts:pending_users")
    return render(request, "accounts/approve.html", {"user": user})
