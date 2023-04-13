import os

os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:5000/callback'

from flask import Flask, render_template, request, redirect, url_for, session
from spotify_playlist import create_top_songs_playlist, sp_oauth

app = Flask(__name__)
app.secret_key = 'de14262590575e6e9db54028fbc450e7'

@app.route('/')
def index():
    auth_url = sp_oauth.get_authorize_url()
    return render_template('index.html', auth_url=auth_url)

@app.route('/callback/', methods=['GET', 'POST'])
def callback():
    print("Callback function called")  # Keep this line
    code = request.args.get('code')
    if code is None:
        return redirect(url_for('index'))
    token_info = sp_oauth.get_access_token(code)
    session['access_token'] = token_info['access_token']
    return redirect(url_for('create_playlist'))

@app.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    if 'access_token' not in session:
        return redirect(url_for('index'))

    access_token = session['access_token']

    # Implement payment processing here

    playlist_name = create_top_songs_playlist(access_token)
    return render_template('success.html', playlist_name=playlist_name)

@app.route('/success')
def success():
    playlist_name = session.get('playlist_name')
    if not playlist_name:
        return redirect(url_for('index'))
    return render_template('success.html', playlist_name=playlist_name)

if __name__ == '__main__':
    app.run(debug=True)