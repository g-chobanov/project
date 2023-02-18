from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'songster'

urlpatterns = [
    path('', views.index, name=''),
    path('login', auth_views.LoginView.as_view()),
    path('logout', auth_views.LogoutView.as_view()),
    path('register', views.register),
    path('user', views.get_user_profile_page),
    path('add_song', views.add_song),
    path('list', views.get_list),
    path('new_list', views.create_new_list),
    path('profile_page', views.get_user_profile_page),
    path('swap_songs', views.swap_songs),
    path('remove_list', views.remove_list),
    path('remove_song', views.remove_song)
]