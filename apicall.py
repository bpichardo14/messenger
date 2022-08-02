from flask import redirect
import os
import spotipy
import spotipy.util as util

CLIENT_ID = ''
CLIENT_SECRET = ''

username = "pichardobrayan"
scope = "user-read-currently-playing"
redirect_uri = 'http://localhost:5000/callback/'

token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

sp = spotipy.Spotify(auth=token)
currentsong = sp.currently_playing()

song_name = currentsong['item']['name']
song_artist = currentsong['item']['artists'][0]['name']
print("Now playing {} by {}".format(song_name, song_artist))