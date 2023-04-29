from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import csv
from django.contrib.auth.decorators import login_required
from .decorators import *
from recommender_system_django_app.models import *
from .decorators import *
from .forms import *
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import coo_matrix
import pandas as pd
import numpy as np
import sqlite3

# Create your views here.
def homepage(request):
    spiderManComic = MarvelComics.objects.filter(characterName = "Spider-Man")
    spiderManComicImage = IssueImageNames.objects.filter(comicID__in = spiderManComic)[:3]
    print(spiderManComicImage)
    context = {"spider_man_comic" : spiderManComicImage}
    return render(request, "recommender_system_django_app/parent_page.html", context)
    


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

@login_required(login_url='/login')
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

    # with open("ratings.csv", "r", encoding = "utf8") as csvfile:
    #     dataReader = csv.DictReader(csvfile)
    #     for row in dataReader:
    #         ComicRatings.objects.create(
    #             userRatings = row["User Ratings"],
    #             comicID = MarvelComics.objects.get(id = int(row["comicID"])),
    #             userID = User.objects.get(id = int(row["userID"])),
    #         )
            
    logout(request)
    return redirect(login_function)

def register_function(request):
    registrationFormNewUser = NewUserForm()

    if request.method == "POST":
        registrationFormNewUser = NewUserForm(request.POST)
        
        if registrationFormNewUser.is_valid():

            registrationFormNewUser.save(commit=False)
            group = Group.objects.get(name='Regular User')
            user = registrationFormNewUser.save()
            user.groups.add(group)
            return redirect(login_function)
        else:
            print("Hello")
            errorMessage = "Error! Invalid credentials"
            return render(request, 'recommender_system_django_app/registration_page.html', {'registrationForm': registrationFormNewUser, 'errorMessage' : errorMessage})
    return render(request, 'recommender_system_django_app/registration_page.html', {'registrationForm': registrationFormNewUser})

@login_required(login_url='/login')
def recommender_system_function(request):
    conn = sqlite3.connect("db.sqlite3", isolation_level=None)
    comics = pd.read_sql_query("SELECT * from recommender_system_django_app_marvelcomics", conn)
    comicRatings = pd.read_sql_query("SELECT * from recommender_system_django_app_comicratings", conn)

    #print(comics.head(30))

    comicRatings["comicID"] = comicRatings["comicID_id"].astype(str)
    comicRatings["userID"] = comicRatings["userID_id"].astype(str)
    comicRatings["User_Ratings"] = pd.to_numeric(comicRatings["userRatings"])

    comicRatings["user_index"] = comicRatings["userID"].astype("category").cat.codes
    comicRatings["comic_index"] = comicRatings["comicID"].astype("category").cat.codes

    ratings_matrix = coo_matrix((comicRatings["User_Ratings"], (comicRatings["user_index"], comicRatings["comic_index"])))
    ratings_mat = ratings_matrix.tocsr()
    #print(ratings_mat)

    similarity = cosine_similarity(ratings_mat[0,:], ratings_mat).flatten()
    indices = np.argpartition(similarity, -3)[-3:]  
    #print(indices)

    similar_users = comicRatings[comicRatings["user_index"].isin(indices)].copy()
    currentUser = request.user 
    similar_users = similar_users[similar_users["userID"]!= str(currentUser.id)] 
    print(similar_users)

    comicRecommendations = similar_users.groupby("comicID").User_Ratings.agg(['count', 'mean'])
    #print(comicRecommendations)

    comicRatings["comicID"] = comicRatings["comicID"].astype(str)

    comicRecommendations = comicRecommendations.merge(comicRatings, how="inner", on="comicID")
    #print(comicRecommendations)

    comicRecommendations["adjusted_count"] = comicRecommendations["count"] * (comicRecommendations["count"] / 9)

    comicRecommendations["score"] = comicRecommendations["mean"] * comicRecommendations["adjusted_count"]
    currentUser = request.user
    print(currentUser.id)
    myComics = comicRatings[comicRatings['userID'] == str(currentUser.id)]

    print(myComics)

    #print(comicRatings["userID_id"])

    comicRecommendations = comicRecommendations[~comicRecommendations["comicID"].isin(myComics["comicID"])]
    #print(comicRecommendations)

    comicRecommendations = comicRecommendations[~comicRecommendations["comicID"].isin(myComics["comicID"])]
    #print(comicRecommendations)

    comicRecommendations = comicRecommendations[comicRecommendations["mean"] >= 4]

    top_recs = comicRecommendations.sort_values("mean", ascending=False)
    print(len(top_recs))

    topRecommendations = top_recs["comicID"].unique()
    print(len(topRecommendations))

    df1 = pd.DataFrame(topRecommendations)
    #print(top_recs.columns)

    top_recommendations = df1.values.tolist()

    comicDetails = []

    #print(top_recommendations)

    for comic in top_recommendations:
        comicDetails.append(MarvelComics.objects.get(id = int(comic[0])))

    conn.close()
    context = {"recommended_comics": comicDetails}
    return render(request, "recommender_system_django_app/recommendations_page.html", context)

def comics_list_function(request):
    issue_covers = IssueImageNames.objects.all()
    context = {"comics_list":issue_covers}
    return render(request, "recommender_system_django_app/comics_list_page.html", context)

def individual_comic_function(request, comicID):
    individualComic = IssueImageNames.objects.get(id = comicID)
    print(individualComic)
    context = {"individual_comic" : individualComic}
    return render(request, "recommender_system_django_app/individual_comic_page.html", context)

@login_required(login_url='/login')
@allowed_users(allowed_roles='Admin')
def all_comics_function(request):
    comics = MarvelComics.objects.all()
    print(comics)
    context = {"comics_list" : comics}
    return render(request, "recommender_system_django_app/admin_view.html", context)

@login_required(login_url='/login')
@allowed_users(allowed_roles='Admin')
def update_comic_function(request, comicID):
    comicDetails = MarvelComics.objects.get(id = comicID)
    print(comicDetails)
    context = {"comic details" : comicDetails}
    updateForm = UpdateComicsForm(request.POST or None, instance = comicDetails)
    if updateForm.is_valid():
        updateForm.save()
        return redirect(all_comics_function)
    context = {"updated_form": updateForm}
    return render(request, "recommender_system_django_app/update_comic_page.html", context)\

@login_required(login_url='/login')
@allowed_users(allowed_roles='Admin')
def delete_comic_function(request, comicID):
    comicDetails = MarvelComics.objects.get(id = comicID)
    print(comicDetails)
    comicDetails.delete()
    return redirect(all_comics_function)