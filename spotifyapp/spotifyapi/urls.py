from django.urls import path

from .views import AuthURL, spotify_api_callback, IsAuthenticated

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_api_callback),
    path('is-authenticated', IsAuthenticated.as_view())
]