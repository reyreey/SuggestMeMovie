from django.conf import settings
from django.db import models
from PIL import Image
import requests


class NameBasics(models.Model):
    nconst = models.CharField(max_length=200, primary_key=True)
    primaryName = models.CharField(max_length=200)
    birthYear = models.IntegerField()
    deathYear = models.IntegerField()
    primaryProfession = models.TextField()
    knownForTitles = models.TextField()


class TitleBasics(models.Model):
    tconst = models.CharField(max_length=200, primary_key=True)
    titleType = models.CharField(max_length=200)
    primaryTitle = models.CharField(max_length=200)
    originalTitle = models.CharField(max_length=200)
    isAdult = models.BooleanField()
    startYear = models.IntegerField()
    runtimeMinutes = models.IntegerField()
    genres = models.TextField()


class TitleAkas(models.Model):
    id = models.AutoField(primary_key=True)
    titleId = models.ForeignKey(TitleBasics, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    title = models.CharField(max_length=200)
    region = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    types = models.CharField(max_length=200)
    attributes = models.TextField()
    isOriginalTitle = models.BooleanField()


class TitleCrew(models.Model):
    tconst = models.ForeignKey(TitleBasics, on_delete=models.CASCADE,primary_key=True)
    directors = models.TextField()
    writers = models.TextField()


class TitleEpisode(models.Model):
    tconst = models.ForeignKey(TitleBasics, on_delete=models.CASCADE,primary_key=True)
    parentTconst = models.CharField(max_length=200)
    seasonNumber = models.IntegerField()
    episodeNumber = models.IntegerField()


class TitleRatings(models.Model):
    tconst = models.ForeignKey(TitleBasics, on_delete=models.CASCADE,primary_key=True)
    averageRating = models.IntegerField()
    numVotes = models.IntegerField()


class Poster(models.Model):
    tconst = models.ForeignKey(TitleBasics, on_delete=models.CASCADE,primary_key=True)
    url = models.URLField()

    def showPoster(self):
        response = requests.get(f'{settings.OMDB_URL}?i={self.tconst}&apikey={settings.OMDB_API_KEY}')
        data = response.json()
        print(data)

        url = data['Poster']
        im = Image.open(requests.get(url, stream=True).raw)
        Image._show(im)
