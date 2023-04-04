from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from recommender_system_django_app.models import *
from .decorators import *
from .forms import *

# Create your views here.
def homepage(request):
    return render(request, 'recommender_system_django_app/parent_page.html')

def login_function(request):

    if request.method == "POST":
        usernameOrEmail = request.POST.get('username')
        password = request.POST.get('password')

        randomUser = authenticate(request, username = usernameOrEmail, password = password)

        if randomUser is not None:
            login(request, randomUser)
            return redirect(homepage)
        else:
            errorMessage = "Error! Invalid Credentials!"
            return render(request, 'recommender_system_django_app/login_page.html', {'errorMessage': errorMessage})
    
    return render(request, 'recommender_system_django_app/login_page.html')

def logout_function(request):
    logout(request)
    return redirect(login_function)

def register_function(request):
    registrationFormNewUser = NewUserForm()

    if request.method == "POST":
        registrationFormNewUser = NewUserForm(request.POST)
        
        if registrationFormNewUser.is_valid():
            registrationFormNewUser.save()
            return redirect(login_function)
        else:
            errorMessage = "Error! Invalid credentials"
            return render(request, 'recommender_system_django_app/registration_page.html', {'registrationForm': registrationFormNewUser, 'errorMessage' : errorMessage})
    return render(request, 'recommender_system_django_app/registration_page.html', {'registrationForm': registrationFormNewUser})