from django.shortcuts import render, redirect
from .credentials import *
from rest_framework.views import APIView
from requests import Request, post
from rest_framework.response import Response
from rest_framework import status
from .util import is_spotify_authenticated, update_or_create_user_tokens
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

    print(expires_in)
    
    session_key = request.session.session_key
    if not request.session.exists(session_key):
        request.session.create(session_key, access_token, token_type, expires_in, refresh_token)

    update_or_create_user_tokens(session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('songster:')