from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import re

def signup(request):
    if request.method == "POST":
        name = request.POST.get('username')
        emailId = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not (name and emailId and password and confirm_password):
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Check if user already exists
        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        if User.objects.filter(email=emailId).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'signup.html')

        # ✅ Correct way to create a user (Django handles password hashing)
        user = User.objects.create_user(username=name, email=emailId, password=password)
        user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')
def login_view(request):
    if request.method == "POST":
        emailId = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # ✅ Fetch user using email
            user = User.objects.get(email=emailId)
            username = user.username  # Get the username associated with the email

            # ✅ Authenticate using username and password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")  # ✅ Success message
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password. Please try again.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'login.html')
