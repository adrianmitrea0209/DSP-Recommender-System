from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from recommender_system_django_app.models import *

# Registration form new users
class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

class UpdateComicsForm(forms.ModelForm):
    class Meta:
        model = MarvelComics
        fields = ['comicName', 'issueTitle', 'dateOfPublication' , 'issueDescription' , 'writer', 'price', 'characterName', 'characterAlignment', 'characterGender', 'characterRace']