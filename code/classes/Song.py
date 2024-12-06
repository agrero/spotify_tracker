from pydantic import BaseModel
import datetime

class Song(BaseModel):

    song_name : str
    popularity : int
    duration_ms : int 

    played_at : datetime.datetime
    
    # add artist unpacking
    # # artists : list[str] | None

class Songplay(Song):
    
    # floats
    play_length : float
    skip_percent : float
    
    # bools
    skip : bool
    pause : bool
    play : bool
    

    

class SongList(BaseModel):
    
    songs : list[Song] | None

