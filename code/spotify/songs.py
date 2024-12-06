import spotipy
from spotipy.oauth2 import SpotifyOAuth

from datetime import datetime, timedelta

import math

import pandas as pd

from code.classes.Song import Song


def get_history(client_id:str, client_secret:str, client_redirect:str):
    # SCOPES
    # user-library-read
    # user-read-recently-played

    # THIS GETS THE USER HISTORY
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=client_redirect,
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

def convert_songlist_to_dataframe(songlist:list[Song]) -> pd.DataFrame:
    """converts a list of song objects to a pandas dataframe"""
    return pd.DataFrame([song.model_dump() for song in songlist])


def calculate_play_length(data:pd.DataFrame) -> pd.DataFrame:
    """Calculate skips from a list of song objects
    
    data: json like as derove from extract_songs
    
    currently if you pause it for long enough, regardless of
    whether or not you skip it again
    """

    # calculate skips
    data = data.sort_values(by='played_at')
    data['duration_ms'] =  pd.to_timedelta(data.duration_ms, unit='ms')
    data['play_length'] = data['played_at'].shift(-1) - data['played_at']

    return data

def convert_dt_to_seconds(data:pd.DataFrame, columns:list[str]) -> pd.DataFrame:
    """
    from a list of column names 
    convert datetime objects to seconds
    
    data: a pandas dataframe \\
    columns: a list of column names represented as strings \
    
    returns: original dataframe with specified columns as 
    total seconds"""
    
    for column in columns:
        data[column] = data[column].dt.total_seconds()

    return data

####### These could probably be merged
def label_skips(data:pd.DataFrame, skip_threshold:float=-10.0) -> pd.DataFrame:
    """
    Label skips by thresholding the pandas dataframe
    
    returns a dataframe with skips labeled as a boolean
    """
    data['skip'] = data['play_length'] - data['duration_ms']
    data['skip'] = data['skip'] < skip_threshold

    return data

def label_pauses(data:pd.DataFrame, pause_threshold:float=10.0) -> pd.DataFrame:
    """
    Label pauses by thresholding the pandas dataframe

    returns a dataframe with pauses labeled as a boolean
    """
    data['pauses'] = data['play_length'] - data['duration_ms']
    data['pauses'] = data['pauses'] > pause_threshold

    return data
#############################################

def label_plays(data:pd.DataFrame) -> pd.DataFrame:
    # data['plays'] = pd.concat([data['skip'], data['pauses']]).any()
    data['play'] = False
    data.loc[((data['skip'] + data['pauses']) == 0), 'play'] = True

    return data

def calculate_skip_percent(data:pd.DataFrame) -> pd.DataFrame:
    """"""
    data['skip_percent'] = 100 - (data[data['skip']]['play_length'] /
                            data[data['skip']]['duration_ms'] * 100)   
    return data.fillna(0.0)