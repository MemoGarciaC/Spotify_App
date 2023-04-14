import os
import spotipy
import pickle  # Replace json import with pickle
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, redirect, url_for, session
from spotify_playlist import create_top_songs_playlist

app = Flask(__name__)
app.secret_key = 'de14262590575e6e9db54028fbc450e7'

CLIENT_ID = 'fba9c64e3fd7465699d57c02c746fe88'
CLIENT_SECRET = '6b6601dfbaa54706b64f89fa82f55130'
REDIRECT_URI = os.environ.get("REDIRECT_URI", "https://new-spotify-app.herokuapp.com/callback")

@app.route("/")
def index():
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read playlist-modify-public",
        show_dialog=True,
    )
    session['sp_oauth'] = pickle.dumps(sp_oauth)  # Serialize the sp_oauth object using pickle
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
    session['access_token'] = token_info['access_token']

    # Create the sp object here
    sp = spotipy.Spotify(auth=session['access_token'])

    # Store the user's ID in the session
    user_id = sp.current_user()['id']

    return redirect(url_for('create_playlist', user_id=user_id))

@app.route('/create_playlist/<user_id>', methods=['GET', 'POST'])
def create_playlist(user_id):
    if 'access_token' not in session:
        return redirect(url_for('index'))

    access_token = session['access_token']
    sp = spotipy.Spotify(auth=access_token)  # Create the sp object here

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