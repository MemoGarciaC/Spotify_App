import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = 'fba9c64e3fd7465699d57c02c746fe88'
CLIENT_SECRET = '6b6601dfbaa54706b64f89fa82f55130'
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:5000/callback/")

sp_oauth = spotipy.SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read playlist-modify-public",
    show_dialog=True
)

def create_top_songs_playlist(access_token):
    sp = spotipy.Spotify(auth=access_token)

    top_tracks = sp.current_user_top_tracks(limit=5, time_range='long_term')
    track_ids = [track['id'] for track in top_tracks['items']]

    recommendations = sp.recommendations(seed_tracks=track_ids, limit=10)

    playlist_name = "Test Playlist"
    new_playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name)

    playlist_id = new_playlist['id']
    sp.user_playlist_add_tracks(sp.current_user()['id'], playlist_id, [track['id'] for track in recommendations['tracks']])

    return playlist_name