from django.shortcuts import render, redirect
from .credentials import *
from rest_framework.views import APIView
from requests import Request, post
from rest_framework.response import Response
from rest_framework import status
from .util import is_spotify_authenticated, spotify_request, update_or_create_user_tokens
# Create your views here.

class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'playlist-modify-private playlist-modify-public'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)
    
class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
    
def spotify_api_callback(request, format=None):
    code = request.GET.get('code')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    
    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('songster:')

class SearchSong(APIView):
    def get(self, request):
        if not request.session.exists(request.session.session_key):
             request.session.create()

        session_id = request.session.get('user_session_key', None)
        q = request.query_params.get("query", None)
        spotify_endpoint = "search"
        spotify_response = spotify_request(session_id, spotify_endpoint, "GET", params={'q': q, 'type' : 'track'})
        tracks = spotify_response["tracks"]["items"]
        tracks_template_data = []
        for track in tracks:
            needed_info = {
                'artists' : [artist['name'] for artist in track['artists']],
                'name': track['name'],
                'year': track['album']['release_date'].split('-')[0],
                'track_cover': track['album']['images'][1],
                'preview_url': track['preview_url']
            }
            tracks_template_data.append(needed_info)
        return Response({'status': tracks_template_data}, status=status.HTTP_200_OK)

