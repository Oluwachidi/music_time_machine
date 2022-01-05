import requests
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import argparse


URL = "https://www.billboard.com/charts/hot-100/"
Client_ID = "cacbcf1824474646b190016121611d0f"
Client_Secret = "07c8b11e60274a1f97a1d185147c0895"
redirect_url = "https://example.com"
scope = "playlist-modify-private"


date = input('What year would you like to trave to? YYY-MM-DD \n')
response = requests.get(URL + date).text


# Instantiate BeautifulSoup to scrape billboard site
soup = BeautifulSoup(response, "html.parser")
all_songs = soup.find_all("h3", class_="a-no-trucate")
song_names = [song.string.strip('\n') for song in all_songs]
print(song_names)


# Implement authorization code
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID, client_secret=Client_Secret, redirect_uri=redirect_url, scope=scope,
                  cache_path="token.txt", username="Oluwachidi", show_dialog=True, requests_timeout=3))
user_id = sp.current_user()['id']


# Search for each song in song_names on spotify to obtain its url
song_url = []
year = date.split('-')[0]
for song in song_names:
    result = sp.search(q= f"track:{song} year:{year}", type="track", limit=1)
    try:
        url = result['tracks']["items"][0]['external_urls']['spotify']
        song_url.append(url)
    except IndexError:
        print(f"{song} does not exist in Spotify. Skipped")

# Through the song_url, create a new playlist on spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_url)
