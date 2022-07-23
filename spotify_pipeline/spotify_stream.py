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
from database.Load import CreateEngine
from utils.authorisation import AuthoriseUser, GetAccessToken
import urllib.parse
import webbrowser
from utils.custom_exceptions import DataHasNullValues, SongNotPlayedYesterday
from datetime import datetime, timedelta

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


class ValidateData:
    def __init__(self, df):
        self.df = df

    def df_empty(self):
        if self.df.empty:
            logging.info('No data to load to database')
            return True

    def is_null_vals(self):
        null_values = self.df.isnull().values.any()
        if null_values:
            logging.info('Data contains null values')
            raise DataHasNullValues
        return null_values

    def check_timestamps(self):
        yesterday_date_stamp = datetime.now().date() - timedelta(days=1)
        time_stamps_list = self.df['time_stamp'].values.tolist()
        for song_tstamps in time_stamps_list:
            song_date_stamp = datetime.strptime(song_tstamps, '%Y/%m/%d')
            if song_date_stamp != yesterday_date_stamp:
                logging.info('At least one song was not played yesterday')
                raise SongNotPlayedYesterday
        return True




if __name__ =='__main__':
    with open('../utils/my_logger.YAML') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.info('testing logger')

    my_authorisation = AuthoriseUser()
    encoded_creds = my_authorisation.client_creds_encoded
    endpoint = my_authorisation.get_auth_endpoint()
    print('Copy the url you are redirected to.')
    webbrowser.open(endpoint)

    resp = input('Redirected url: ')
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
        "Authorization": "Bearer {access_token}".format(access_token=access_token)
    }

    get_tracks_data = GetRecentlyPlayedTracks(get_headers)
    tstamp_url = get_tracks_data.unix_timestamp_endpoint(t_stamp)
    get_tracks_data.endpoint = tstamp_url
    my_tracks_data = get_tracks_data.get_data()

    tracks_transform = TransformTracksData()
    tracks_transform.tracks_from_json(my_tracks_data)
    data_df = tracks_transform.tracks_dict_to_df()

    validate = ValidateData(data_df)
    a = validate.df_empty()
    b = validate.is_null_vals()
    if a is False or b is False:
        db = os.getenv('DB_NAME')
        create_engine = CreateEngine()
        engine = create_engine.engine_connection()
        with DatabaseConnection(db) as db_conn:
            query = '''CREATE TABLE IF NOT EXISTS Songs (
        id SERIAL,
        song_name VARCHAR(55) NOT NULL,
        artist_name VARCHAR(55) NOT NULL,
        time_stamp VARCHAR (55) PRIMARY KEY NOT NULL
        )'''
            db_conn.execute(query)

        with DatabaseConnection(db) as db_conn:
            data_df.to_sql('music', engine, index=False, if_exists='append')
    print('execution finished')










