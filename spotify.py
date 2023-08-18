from bs4 import BeautifulSoup
import requests

URL = "https://www.billboard.com/charts/hot-100/"
songnames = []
time = input("Which year do you want to travel to? Type it in the format YYYY-MM-DD ")
requiredlink = URL+time+'/'
webpage = requests.get(requiredlink)
webpage_text = webpage.text
soup = BeautifulSoup(webpage_text,"html.parser")
tittle = soup.find(name = "h3")
songnames.append(tittle.find(name="a").text.strip())
title = soup.find_all(name="h3",class_ = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
for i in title:
    q = i.text
    songnames.append(q.strip())

with open("songnames.txt","w") as f:
    for i in range(len(songnames)):
        f.write(f"{songnames[i]} \n")

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="2b1b10918f7a46fb89b79c8095888c7f",
        client_secret="bd5e5ad4e1cd4f7da625959d2a325ea1",
        show_dialog=True,
        cache_path="token.txt",
        #Use your spotify username here
        username="Username",
    )
)
user_id = sp.current_user()["id"]

l_uri = []
with open('songnames.txt','r') as fs:
    while True:
        str_song = fs.readline()
        if not str_song:
            break
        q = f'track:{str_song[:-1]} year:1997'
        result = sp.search(q, type='track', limit=1)
        if result and len(result["tracks"]["items"]) == 1:
            l_uri.append(result['tracks']['items'][0]['uri'])

print(l_uri)
playlist = sp.user_playlist_create(user=user_id, name=f"{time} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=l_uri)
