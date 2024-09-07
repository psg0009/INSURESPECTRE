# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def solution(request):
    return render(request, 'solution.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('index')
            else:
                # Check if the username exists
                if not User.objects.filter(username=form.cleaned_data.get('username')).exists():
                    messages.error(request, 'User does not exist. Please sign up first.')
                    return render(request, 'login.html', {'form': form, 'show_signup_link': True})
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('index')

def who(request):
    return render(request, 'who.html')

def what(request):
    return render(request, 'what.html')

def goal(request):
    return render(request, 'goal.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                form.save()
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Signup successful')
                    return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def team(request):
    return render(request, 'team.html')

def contact(request):
    return render(request, 'contact.html')