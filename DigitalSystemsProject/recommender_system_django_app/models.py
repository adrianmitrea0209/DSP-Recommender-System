from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.
class MarvelComics(models.Model):
    comicName = models.CharField(max_length=255)
    issueTitle = models.CharField(max_length=255)
    dateOfPublication = models.CharField(max_length=255)
    issueDescription = models.TextField()
    writer = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    characterName = models.CharField(max_length=255)
    characterAlignment = models.CharField(max_length=255)
    characterGender = models.CharField(max_length=255)
    characterRace = models.CharField(max_length=255) 

class ComicRatings(models.Model):
    userRatingOptions = ((1,1), (2,2), (3,3), (4,4), (5,5))
    userRatings = models.IntegerField(choices = userRatingOptions )
    userID = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    comicID = models.ForeignKey(MarvelComics, null=True, blank = True, on_delete=models.CASCADE)

class IssueImageNames(models.Model):
    comicID = models.ForeignKey(MarvelComics, null=True, blank=True, on_delete=models.CASCADE)
    issueImageName = models.ImageField('issueImages/Images/', null=True, blank=True)
