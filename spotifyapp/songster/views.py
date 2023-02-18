import json
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from .forms import AddSongForm, RegisterUserForm
from .models import List, Song

@login_required(login_url='/login')
def index(request):
    context = {
        'lists' : List.objects.all(),
        'userid' : request.user.id
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
    userid = request.GET.get("id", None)
    if userid is None: 
        Response({"error" : "user not found"}, status=status.HTTP_400_BAD_REQUEST)
    userid = int(userid)
    username = User.objects.filter(id=userid).first().username
    userlists = List.objects.filter(user_id=userid)
    context = {
        'lists': userlists,
        'username': username,
        'is_your_page': userid == request.user.id
    }
    return render(request,'profilepage.html', context)

def get_list(request):
    listid = request.GET.get("id", None)
    userid = List.objects.filter(id=listid).first().user.pk
    list = List.objects.filter(id=listid).first()
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        list.name = new_name
        list.save()    
    songlist = Song.objects.filter(list_owner_id=listid).order_by('-list_number')
    context = {
        'songs' : songlist,
        'list_name' : list.name,
        'listid' : listid ,
        'reached_max': len(songlist) >= 50,
        'is_current_user_list' : userid == request.user.id ,
    }
    return render(request, 'listpage.html', context)

def create_new_list(request):
    user = User.objects.get(id=request.user.id)
    new_list = List(name="New List", user=user)
    new_list.save()
    return redirect(f'/list?id={new_list.id}')

def add_song(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        body_post_json_data = json.loads(body)
        name = body_post_json_data.get('name', None)
        artists = body_post_json_data.get('artists', None)
        year = body_post_json_data.get('year', None)
        spotify_uri = body_post_json_data.get('spotify_uri', None)
        listid = body_post_json_data.get('listid', None)
        writeup = body_post_json_data.get('writeup', None)
        img_url = body_post_json_data.get('img_url', None)
    else:
        return JsonResponse({"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)
    artists_array = artists.split(', ')
    main_artist = artists_array[0]
    featured_artists = ' '.join(artists_array[1:])
    form = AddSongForm({'name': name,
                        'artist': main_artist,
                        'featured_artists:': featured_artists,
                        'year': int(year),
                        'spotify_uri': spotify_uri,
                        'list_owner': listid,
                        'list_number': len(Song.objects.filter(list_owner_id=listid)) + 1,
                        'writeup': writeup,
                        'img_url': img_url
                        })
    if not form.is_valid():
      return JsonResponse({"error": "invalid form"}, status=status.HTTP_400_BAD_REQUEST)  
    form.save()
    return JsonResponse({ "link": f'list?id={listid}'}, status=status.HTTP_200_OK)

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
    return Response({'state': 'successfully removed list'}, status.HTTP_200_OK)

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
    return Response({'state': 'successfully removed list'}, status.HTTP_200_OK)



    



    

