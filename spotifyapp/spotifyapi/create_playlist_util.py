import json
from songster.models import List, Song
from spotifyapi.util import spotify_request

def create_playlist(session_id, list_id, user_id):
    list_name = List.objects.filter(id=list_id).first().name 
    endpoint = f'users/{user_id}/playlists'
    body = {
        'name' : list_name,
        'description' : "This playlist was created by Songster"
    }
    body_json = json.dumps(body).encode('utf-8')

    return spotify_request(session_id, endpoint, "POST", body=body_json)

def put_songs_in_playlist(session_id, list_id, playlist_id):
    songlist = Song.objects.filter(list_owner_id=list_id)
    uris = [song.spotify_uri for song in songlist]
    endpoint = f'playlists/{playlist_id}/tracks'
    body = {
        'uris': uris,
    }
    body_json = json.dumps(body).encode('utf-8')
    return spotify_request(session_id, endpoint, "POST", body=body_json)


