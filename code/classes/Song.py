from pydantic import BaseModel
import datetime
class Song(BaseModel):

    song_name : str
    popularity : int
    duration_ms : int 

    played_at : datetime.datetime
    
    # get reading to work then add artist unpacking
    # # artists : list[str] | None
    # # album_name