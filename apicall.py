from flask import redirect
import os
import spotipy
import spotipy.util as util

CLIENT_ID = '4d7fed3f38454c82abe7000ed50f7a13'
CLIENT_SECRET = '9748fcc8cf064b7eb259f2adf4f43abe'

username = "pichardobrayan"
scope = "user-read-currently-playing"
redirect_uri = 'http://localhost:5000/callback/'

token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

sp = spotipy.Spotify(auth=token)
currentsong = sp.currently_playing()

song_name = currentsong['item']['name']
song_artist = currentsong['item']['artists'][0]['name']
print("Now playing {} by {}".format(song_name, song_artist))