import os
import logging
import spotipy
import uuid
from spotipy.oauth2 import SpotifyOAuth
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, session
import pickle
from spotify_playlist import create_top_songs_playlist

app = Flask(__name__)
app.secret_key = 'de14262590575e6e9db54028fbc450e7'

CLIENT_ID = 'fba9c64e3fd7465699d57c02c746fe88'
CLIENT_SECRET = '6b6601dfbaa54706b64f89fa82f55130'
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:5000/callback/")

@app.route("/")
def index():
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f".cache-{str(uuid.uuid4())}")
    sp_oauth = spotipy.SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read playlist-modify-public",
        show_dialog=True,
        cache_path=cache_path
    )
    session['sp_oauth'] = pickle.dumps(sp_oauth)
    auth_url = sp_oauth.get_authorize_url()
    return render_template("index.html", auth_url=auth_url)

@app.route('/callback/', methods=['GET', 'POST'])
def callback():
    print("Callback function called")  # Keep this line
    code = request.args.get('code')
    if code is None:
        return redirect(url_for('index'))
    
    sp_oauth = pickle.loads(session['sp_oauth'])
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']
    session['access_token'] = token_info['access_token']

    # Store the user's ID in the session
    sp = spotipy.Spotify(auth=access_token)
    user_id = sp.current_user()['id']

    return redirect(url_for('create_playlist', user_id=user_id))

@app.route('/create_playlist/<user_id>', methods=['GET', 'POST'])
def create_playlist(user_id):
    if 'access_token' not in session:
        return redirect(url_for('index'))

    access_token = session['access_token']

    sp = spotipy.Spotify(auth=access_token)

    # Implement payment processing here

    playlist_name = create_top_songs_playlist(user_id, sp)
    return render_template('success.html', playlist_name=playlist_name)

@app.route('/success')
def success():
    playlist_name = session.get('playlist_name')
    if not playlist_name:
        return redirect(url_for('index'))
    return render_template('success.html', playlist_name=playlist_name)

if __name__ == '__main__':
    app.run(debug=True)