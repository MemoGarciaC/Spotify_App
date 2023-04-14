import spotipy

def create_top_songs_playlist(user_id, sp):
    top_tracks = sp.current_user_top_tracks(limit=20, time_range='medium_term')

    # Extract track IDs from the top tracks
    track_ids = [track['id'] for track in top_tracks['items']]

    # Fetch recommendations based on the user's top tracks
    recommendations = sp.recommendations(seed_tracks=track_ids[:5], limit=20)

    # Extract track IDs from the recommendations
    recommended_track_ids = [track['id'] for track in recommendations['tracks']]

    # Example playlist name
    playlist_name = "My Top Songs Recommendations"

    # Create a new playlist for the authenticated user
    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description='A playlist of recommended songs based on your top tracks.')

    # Add tracks to the new playlist
    sp.playlist_add_items(new_playlist['id'], recommended_track_ids)

    return playlist_name