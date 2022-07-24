import logging
import os
import time
from logging import config
import yaml
from dotenv import load_dotenv
import requests
from utils.time_stamp import TimeStamp
from utils.transfrorm import TransformTracksData
from database.connector import DatabaseConnection
from database.Load import CreateEngine, ValidateData
from utils.authorisation import AuthoriseUser, GetAccessToken
from selenium.common.exceptions import NoSuchElementException


load_dotenv()


class GetData:
    def __init__(self, headers, data):
        self.endpoint = ''
        self.headers = headers
        self.data = data

class GetRecentlyPlayedTracks(GetData):
    def __init__(self, headers):
        super().__init__(headers, data=None)


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
        response = requests.get(self.endpoint, headers=self.headers, data=None)
        return response.json()


if __name__ =='__main__':
    with open('../utils/my_logger.YAML') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.info('testing logger')

    my_authorisation = AuthoriseUser()
    encoded_creds = my_authorisation.client_creds_encoded
    authorisation_code = my_authorisation.get_auth()
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
        "Authorization": "Bearer {access_token}".format(access_token=access_token)
    }

    get_tracks_data = GetRecentlyPlayedTracks(get_headers)
    tstamp_url = get_tracks_data.unix_timestamp_endpoint(t_stamp)
    get_tracks_data.endpoint = tstamp_url
    my_tracks_data = get_tracks_data.get_data()

    tracks_transform = TransformTracksData()
    tracks_transform.tracks_from_json(my_tracks_data)
    tracks_transform.tracks_dict()
    data_df = tracks_transform.tracks_dict_to_df()

    validate = ValidateData(data_df)

    a = validate.df_empty()
    b = validate.is_null_vals()

    create_engine = CreateEngine()
    engine = create_engine.engine_connection()
    db = os.getenv("DB_NAME")
    with DatabaseConnection(db) as db_conn:
        query = '''
        CREATE TABLE IF NOT EXISTS songs (
                id SERIAL PRIMARY KEY,
                track_name VARCHAR(55) NOT NULL,
                artist_name VARCHAR(55) NOT NULL,
                time_stamp VARCHAR (55) NOT NULL
                )'''
        db_conn.execute(query)
    if a is False or b is False:
        with DatabaseConnection(db) as db_conn:
            data_df.to_sql('songs', engine, index=False, if_exists='append')
    print('execution finished')










