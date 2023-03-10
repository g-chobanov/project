from django.urls import path

from .views import *

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_api_callback),
    path('is-authenticated', IsAuthenticated.as_view()),
    path('search', SearchSong.as_view()),
    path('create_playlist', CreateNewPlaylistFromList.as_view())
]