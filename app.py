
from flask import Flask, url_for, session, request, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# App config
app = Flask(__name__)

app.secret_key = 'asdasdasdas'
app.config['SESSION_COOKIE_NAME'] = 'sebas cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks')
def getTracks():
    try:
     token_info = get_token()
    except:
        print("user not logged in")
        redirect("/")

    sp = spotipy.Spotify(auth= token_info["access_token"])
    all_songs =[]
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iter * 50)["items"]
        iter += 1
        all_songs += items
        if (len(items)< 50):
            break
    return str(len(all_songs))

def get_token():

    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info
def create_spotify_oauth():
    return SpotifyOAuth(
            client_id="97ef969d95a34b2482648289bc3ed65a",
            client_secret="0da07c4487d042768b81aa2b19c75b1d",
            redirect_uri=url_for('redirectPage', _external=True),
            scope="user-library-read")

