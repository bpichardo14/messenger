import requests
import os

CLIENT_ID = '4d7fed3f38454c82abe7000ed50f7a13'
CLIENT_SECRET = 'da72dddc08124f93acce69857bbc36ed'

AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()

access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token)} #This tells the server(?) that we are authorized to access information?

BASE_URL = 'https://api.spotify.com/v1/'
# track_id = input('Enter track id: ')
r = requests.get(BASE_URL + 'me/player/currently-playing/', headers=headers)

print(r.json())