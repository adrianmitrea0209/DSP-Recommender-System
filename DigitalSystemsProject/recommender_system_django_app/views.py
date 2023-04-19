from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import csv
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
    # with open("FinalComicsDataset.csv", "r", encoding = "utf8") as csvfile:
    #     dataReader = csv.DictReader(csvfile)
    #     for row in dataReader:
    #         MarvelComics.objects.create(
    #             comicName = row["Comic_Name"], 
    #             issueTitle = row["Issue_Title"], 
    #             dateOfPublication = row["Date_Of_Publication"],
    #             issueDescription = row["Issue_Description"], 
    #             writer = row["Writer"], 
    #             price = row["Price"], 
    #             characterName = row["Character_Name"], 
    #             characterAlignment = row["Character_Alignment"], 
    #             characterGender = row["Character_Gender"], 
    #             characterRace = row["Character_Race"]
    #             )

    with open("ratings.csv", "r", encoding = "utf8") as csvfile:
        dataReader = csv.DictReader(csvfile)
        for row in dataReader:
            ComicRatings.objects.create(
                userRatings = row["User Ratings"],
                comicID = MarvelComics.objects.get(id = int(row["comicID"])),
                userID = User.objects.get(id = int(row["userID"])),
            )
            
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
            print("Hello")
            errorMessage = "Error! Invalid credentials"
            return render(request, 'recommender_system_django_app/registration_page.html', {'registrationForm': registrationFormNewUser, 'errorMessage' : errorMessage})
    return render(request, 'recommender_system_django_app/registration_page.html', {'registrationForm': registrationFormNewUser})

