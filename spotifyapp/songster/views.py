from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from requests import Response
from rest_framework import status

from .forms import AddSongForm, RegisterUserForm
from .models import List, Song

@login_required(login_url='/login')
def index(request):
    context = {
        'list' : List.objects
    }
    return render(request,'homescreen.html', context)

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('songster:')
    else:
        form = RegisterUserForm()
    context = {
        'form': form
    }
    return render(request, 'registration/registration.html', context)

@receiver(user_logged_in)
def save_session_key(sender, request, user, **kwargs):
    request.session['user_session_key'] = request.session.session_key

def get_user_profile_page(request):
    userid = request.query_params.get("id", None)
    username = User.objects.filter(id=userid).first().username
    userlists = List.objects.filter(userid=id)
    context = {
        'lists': userlists,
        'user': username,
        'is_your_page': userid == request.user.id
    }
    return render(request,'profilepage.hmtl', context)

def get_list(request):
    listid = request.query_params.get("id", None)
    userid = List.objects.filter(userid=userid).first().user.pk
    list_name = List.objects.filter(id=listid).first().name
    songlist = Song.objects.filter(listid=listid)
    context = {
        'songs' : songlist,
        'list_name' : list_name,
        'listid' : listid ,
        'is_current_user_list' : userid == request.user.id
    }
    return render(request, 'listpage.html', context)

def add_song(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
        artists = request.POST.get('artists', None)
        year = request.POST.get('year', None)
        spotify_uri = request.POST.get('spotify_uri', None)
        listid = request.POST.get('listid', None)
        number = request.POST.get('number', None)
    else:
        return Response({"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)
    artists_array = artists.split(', ')
    main_artist = artists_array[0]
    featured_artists = ' '.join(artists_array[1:])
    form = AddSongForm({'name': name,
                        'artists': main_artist,
                        'featuredartists:': featured_artists,
                        'year': year,
                        'spotify_uri': spotify_uri,
                        'listowner': listid,
                        'listnumber': number})
    if not form.is_valid():
      return Response({"error": "invalid form"}, status=status.HTTP_400_BAD_REQUEST)  
    form.save()
    return(render, f'getlist?id={listid}')

def swap_songs(request):
    if request.method == "POST":
        source_number = request.POST.get('source_number', None)
        destination_number = request.POST.get("destination_number", None)
        listid = request.POST.get("listid", None)
    else:
       return Response({"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)
    if source_number > 50 or destination_number > 50: 
       return Response({"error": "max number of songs in lists is 50"}, status=status.HTTP_400_BAD_REQUEST)
    if source_number == destination_number:
       return Response({"error": "cannot swap a song with itself"}, status=status.HTTP_400_BAD_REQUEST)
    source_item = Song.objects.filter(listnumber=source_number, listid=listid).first()
    destination_item = Song.objects.filter(listnumber=destination_number, listid=listid).first()
    if source_item == None or destination_item == None:
        return Response({"error": "numbers to swap do not exist"}, status=status.HTTP_400_BAD_REQUEST)
    source_item.listnumber = destination_number
    destination_number.listnumber = source_number
    source_item.save()
    destination_item.save()
    return Response({'state': 'songs successfully swapped'}, status.HTTP_200_OK)

def remove_list(request):
    if request.method == "POST":
        id = request.POST.get("id", None)
    else:
        return Response({"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)
    song_list = List.objects.get(id=id)
    if not song_list:
        return Response({'state': 'invalid list id'}, status.HTTP_400_BAD_REQUEST)
    song_list.delete()
    return Response({'state': 'sucessfully removed list'}, status.HTTP_200_OK)

def remove_song(request):
    if request.method == "POST":
        id = request.POST.get("id", None)
        listid = request.POST.get("listid", None)
    else:
        return Response({"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)
    song = List.objects.get(id=id, listid=listid)
    if not song:
        return Response({'state': 'song not found'}, status.HTTP_400_BAD_REQUEST)
    song.delete()
    return Response({'state': 'sucessfully removed list'}, status.HTTP_200_OK)



    



    

