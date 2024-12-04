import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv

import os

import json

from datetime import datetime, timedelta

import math

import pandas as pd

from code.classes.Song import Song


load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
def get_history():
    # SCOPES
    # user-library-read
    # user-read-recently-played

    # THIS GETS THE USER HISTORY
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            redirect_uri=os.environ.get('CLIENT_REDIRECT'),
            scope='user-read-recently-played',
        ))
    
    return sp.current_user_recently_played()

def extract_songs(data) -> list[Song]:
    """extracts songs based in a json like format"""
    songs = []
    for song in data['items']:
        # make the time component usable
        played_at = song['played_at'].strip('Z').split('T')

        # split time and make datetime 
        time = datetime.strptime(
            ':'.join([str(math.floor(float(i))) 
            for i in played_at[1].split(':')]), '%H:%M:%S')
        # convert to time delta
        time = timedelta(
            hours=time.hour, 
            minutes=time.minute, 
            seconds=time.second
        )

        # format date into datetime and add time component back
        date = datetime.strptime(played_at[0], '%Y-%m-%d')
        time += date

        # create pydantic song model and append to songs
        songs.append(Song(
            song_name=song['track']['name'],
            duration_ms=song['track']['duration_ms'],
            played_at=time,
            popularity=song['track']['popularity']
        ))
   
    return songs

def calculate_skips(data) -> pd.DataFrame:
    """Calculate skips from a list of song objects
    
    data: json like as derove from extract_songs
    
    currently if you pause it for long enough, regardless of
    whether or not you skip it again
    """
    # create dataframe
    data = pd.DataFrame([d.model_dump() for d in data])

    # calculate skips
    data = data.sort_values(by='played_at')
    data['duration_ms'] =  pd.to_timedelta(data.duration_ms, unit='ms')
    data['play_length'] = data['played_at'].shift(-1) - data['played_at']

    data['skipped'] = data['play_length'] < data['duration_ms']

    return data

def main():
    with open('data.json', 'r') as f:
        data = json.load(f)

    data = extract_songs(data)

    data = calculate_skips(data)

    return data



if __name__ == '__main__':
    # use threading to allow this to upload data and 
    # allow inputs at the same time
    data = main()

    print(data)