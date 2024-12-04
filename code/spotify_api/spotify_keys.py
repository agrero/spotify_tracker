import os
import requests
from dotenv import load_dotenv
# how to request keys and refresh keys

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
grant_type = 'client_credentials'
spotify_url = 'https://accounts.spotify.com'

def get_newkey():
    """Send a request using the stored environment key and secret to get an access key
    
    tokens are returned as jsons with three attributes:
    access_token : the individual api access token
    token_type : the type of token being given
    expires_in : an integer representing 1 hour in seconds (or however long the token lives for)

    returns requests object"""
    post_request = requests.post(
        url=f'{spotify_url}/api/token',
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
    )

    return post_request

# returns dictionary of 
# # access token 
# # token type
# # expires in 3600 (int of seconds)