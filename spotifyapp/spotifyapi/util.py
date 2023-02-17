from requests import Response, get, post, put
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import *

BASE_URL = 'https://api.spotify.com/v1'

def get_users_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else: 
        return None

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_users_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.token_type = token_type
        tokens.expires_in = expires_in 
        tokens.refresh_token = refresh_token
        tokens.save(update_fields=['access_token', 'token_type', 'expires_in', 'refresh_token'])
    else: 
        tokens = SpotifyToken(user=session_id, 
                              access_token=access_token, 
                              token_type=token_type,
                              refresh_token=refresh_token,
                              expires_in=expires_in)
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
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(session_id, 
                                access_token,
                                token_type,
                                expires_in)
    
def spotify_request(session_id, method_url, method, body = None, params = None):
    if method not in ['GET', 'POST', 'PUT']:
        return Response()
    tokens = get_users_tokens(session_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {tokens.access_token}"
    }
    print(params)
    response = ''
    if method == 'POST':
       response = post(f'{BASE_URL}/{method_url}', params=params, data=body, headers=headers)
    elif method == 'PUT':
       response = put(f'{BASE_URL}/{method_url}', params=params, data=body, headers=headers)
    elif method == 'GET':
       response = get(f'{BASE_URL}/{method_url}', params=params, data=body, headers=headers)

    try:
        return response.json()
    except:
        return {"Error" : "Request failed"}
    

    