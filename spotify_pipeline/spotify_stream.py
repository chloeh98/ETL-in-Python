import logging
import os
import time
from logging import config
import yaml
from dotenv import load_dotenv
from utils.authorisation import AuthoriseUser, GetAccessToken
import webbrowser
import urllib.parse
import requests
from utils.time_stamp import TimeStamp


load_dotenv()


class GetData:
    def __init__(self, headers, data):
        self.endpoint = ''
        self.headers = headers
        self.data = data


    @staticmethod
    def unix_timestamp_endpoint(unix_timestamp):
        t_stamp_url = f'https://api.spotify.com/v1/me/player/recently-played?after={unix_timestamp}'
        return t_stamp_url

    @property
    def get_endpoint(self):
        return self.endpoint

    @get_endpoint.setter
    def get_endpoint(self, t_stamp_url):
        self.endpoint = t_stamp_url
        print(self.endpoint)

    def get_data(self):
        response = requests.get(self.endpoint, self.headers, self.data)
        return response.json()

class SaveData:
    def __init__(self):
        self.tracks_dictionary = {}
        self.song_names = []
        self.artists = []
        self.track_played_at = []

    def tracks_from_json(self, json_data):
        tracks = json_data["items"]
        for track in tracks:
            self.song_names.append(track["track"]["name"])
            self.artists.append(track["track"]["album"]["artists"][0]["name"])
            self.track_played_at.append(track["played_at"])
            self.tracks_dictionary = {
                'track_name':  self.song_names,
                'artist_name': self.artists,
                'played_at': self.track_played_at
            }
        return self.tracks_dictionary



if __name__ =='__main__':
    with open('../utils/my_logger.YAML') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.info('testing logger')

    my_authorisation = AuthoriseUser()
    encoded_creds = my_authorisation.client_creds_encoded
    print(encoded_creds)
    endpoint = my_authorisation.get_auth_endpoint()
    print('copy the url you are redirected to.')
    webbrowser.open(endpoint)

    resp = input('redirected url: ')
    authorisation_code = urllib.parse.parse_qs(urllib.parse.urlparse(resp).query)['code'][0]
    time.sleep(2)

    post_headers = {
        "Authorization": f"Basic {encoded_creds}",
        "Content_Type": "application/x-www-form-urlencoded"
    }

    redirect_uri = os.getenv("REDIRECT_URI")
    post_data = {
        "grant_type": "authorization_code",
        "code": f"{authorisation_code}",
        "redirect_uri": f"{redirect_uri}"
    }

    my_access_token = GetAccessToken()
    access_token = my_access_token.get_access_token(post_data, post_headers)
    timestamp = TimeStamp()
    t_stamp = timestamp.unix_timestamp()


    get_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    get_tracks_data = GetData(get_headers, data=None)
    tstamp_url = get_tracks_data.unix_timestamp_endpoint(t_stamp)
    get_tracks_data.endpoint = tstamp_url
    my_tracks_data = get_tracks_data.get_data()









