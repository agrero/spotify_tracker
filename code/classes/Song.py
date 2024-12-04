from pydantic import BaseModel
import datetime

class Song(BaseModel):

    song_name : str
    popularity : int
    duration_ms : int 

    played_at : datetime.datetime
    
    # add artist unpacking
    # # artists : list[str] | None
    
class SongList(BaseModel):
    
    songs : list[Song] | None

