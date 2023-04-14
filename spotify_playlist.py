import os
import spotipy

def create_top_songs_playlist(user_id, sp):
    top_tracks = sp.current_user_top_tracks(limit=5, time_range='long_term')
    track_ids = [track['id'] for track in top_tracks['items']]

    recommendations = sp.recommendations(seed_tracks=track_ids, limit=50, market='US')

    playlist_name = "Prueba 1.2"
    new_playlist = sp.user_playlist_create(user_id, playlist_name)

    playlist_id = new_playlist['id']
    sp.user_playlist_add_tracks(user_id, playlist_id, [track['id'] for track in recommendations['tracks']])

    return playlist_name