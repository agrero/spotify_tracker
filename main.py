from dotenv import load_dotenv

import os

# i should really rename this file lol
import code.spotify.songs as sk

def main():

    load_dotenv()

    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    client_redirect = os.environ.get("CLIENT_REDIRECT")

    # we can cache queries as jsons
    # with open('data.json', 'r') as f:
    #     data = json.load(f)

    data = sk.get_history(client_id, client_secret, client_redirect)

    data = sk.extract_songs(data)

    data = sk.convert_songlist_to_dataframe(data)

    data = sk.calculate_play_length(data)

    data = sk.convert_dt_to_seconds(data, ['play_length', 'duration_ms'])

    data = sk.label_skips(data)

    data = sk.label_pauses(data)

    data = sk.label_plays(data)

    data = sk.calculate_skip_percent(data)

    return data



if __name__ == '__main__':
    # use threading to allow this to upload data and 
    # allow inputs at the same time
    data = main()
    print(data)

    # just for checking
    data.to_csv('data.csv')