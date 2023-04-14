# spotify_playlist.py
import spotipy

def create_top_songs_playlist(user_id, sp):
    # Your logic to fetch top songs or tracks for the authenticated user

    # Example playlist name
    playlist_name = "My Top Songs"

    # Create a new playlist for the authenticated user
    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description='A playlist of top songs.')

    # Add tracks to the new playlist (replace `tracks` with your list of track IDs)
    sp.user_playlist_add_tracks(user_id, new_playlist['id'], tracks)

    return playlist_name