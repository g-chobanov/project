from requests import post
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import *

def get_users_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else: 
        return None

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refersh_token):
    tokens = get_users_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.token_type = token_type
        tokens.expires_in = expires_in 
        tokens.refresh_token = refersh_token
        tokens.save(update_fields=['access_token', 'token_type', 'expires_in', 'refersh_token'])
    else: 
        tokens = SpotifyToken(user=session_id, 
                              access_token=access_token, 
                              token_type=token_type,
                              refersh_token=refersh_token)
        tokens.save()

def is_spotify_authenticated(session_id):
    tokens = get_users_tokens(session_id)

    if tokens: 
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_token(tokens)
    return False

def refresh_token(session_id):
    refresh_token = get_users_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get(refresh_token)

    update_or_create_user_tokens(session_id, 
                                access_token,
                                token_type,
                                expires_in)