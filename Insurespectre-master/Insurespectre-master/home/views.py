# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse

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

@csrf_exempt
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        full_message = f"Message from {name} ({email}):\n\n{message}"
        
        # Send email to the site owner
        send_mail(
            subject="Contact Form Message",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['support@insurespectre.com'],
        )
        
        # Send thank you email to the user
        thank_you_message = f"Dear {name},\n\nThank you for contacting Insurespectre. We have received your message and will get back to you shortly.\n\nBest regards,\nInsurespectre Team"
        send_mail(
            subject="Thank You for Contacting",
            message=thank_you_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        
        return JsonResponse({"message": "Message sent successfully!"})
    return render(request, 'contact.html')