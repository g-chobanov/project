from django.db import models

from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class List(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    spotify_uri = models.CharField(max_length=256)
    artist = models.CharField(max_length=128)
    featured_artists = models.CharField(max_length=256, blank=True)
    year = models.IntegerField(validators=[MaxValueValidator(9999)])
    list_number = models.IntegerField()
    img_url = models.CharField(max_length=256)
    writeup = models.CharField(max_length=256, blank=True)
    list_owner = models.ForeignKey(List, on_delete=models.CASCADE)
