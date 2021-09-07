from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lxml

# getting year of the playlist you want to create
year = input('Which year do you want to travel to? \
Type the date in this format YYYY-MM-DD: ')
year_iso = year.split('-')[0]

CLIENT_ID = input('What is your spotify client id?: ')
CLIENT_SECRET = input('What is your client-secret?: ')

# Fetching the html of billboards100
url = f'https://www.billboard.com/charts/hot-100/{year}'
response = requests.get(url=url)

# Using beautiful spoon to scrape the html with lxml parser
soup = BeautifulSoup(response.text, 'lxml')

# Find all instances of the class that matches the name of the song
names = soup.find_all(class_='chart-element__information__song text--truncate color--primary',
                      name='span')

songs = [name.getText() for name in names]
song_uris = []

# Using spotipy and their OAuth class to streamline authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='http://example.com',
        show_dialog=True,
        cache_path="token.txt",
    ))

id = sp.current_user()['id']

# looping through songs scraped and finding the url for them
for song in songs:
    return_song = sp.search(q=f"track:{song} year:{year_iso}", type="track")
    try:
        add_song = return_song['tracks']['items'][0]['uri']
        song_uris.append(add_song)
    except:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating the playlist
playlist = sp.user_playlist_create(user=id,
                                   name=f'Top 100 of {year_iso}',
                                   public=False,
                                   description='Just a playlist of top 100 songs in the US on my\
                        birth Date')

# adding all the urls into the playlist we created
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
