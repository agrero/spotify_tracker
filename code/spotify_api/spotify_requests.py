import requests

base_url = 'https://api.spotify.com.'


# get history 
def get_history():
    req_path = '/me/player/recently-played'
    get = requests.get(
        url=f'{base_url}{req_path}',
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=''
    )