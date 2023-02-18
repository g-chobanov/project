from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Song

class RegisterUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class AddSongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ('list_owner', 
                  'name', 
                  'spotify_uri',
                  'artist',
                  'featured_artists',
                  'list_number',
                  'year')