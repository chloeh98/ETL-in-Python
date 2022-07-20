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
from utils.transfrorm import TransformTracksData
from database.connector import DatabaseConnection
from database.Load import CreateEngine
from utils.custom_exceptions import DataHasNullValues, SongNotPlayedYesterday
from datetime import datetime, timedelta

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
        response = requests.get(self.endpoint, self.headers)
        print(response)
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

    # my_authorisation = AuthoriseUser()
    # encoded_creds = my_authorisation.client_creds_encoded
    # print(encoded_creds)
    # endpoint = my_authorisation.get_auth_endpoint()
    # print('Copy the url you are redirected to.')
    # webbrowser.open(endpoint)
    #
    # resp = input('Redirected url: ')
    # authorisation_code = urllib.parse.parse_qs(urllib.parse.urlparse(resp).query)['code'][0]
    # time.sleep(2)
    #
    # post_headers = {
    #     "Authorization": f"Basic {encoded_creds}",
    #     "Content_Type": "application/x-www-form-urlencoded"
    # }
    #
    # redirect_uri = os.getenv("REDIRECT_URI")
    # post_data = {
    #     "grant_type": "authorization_code",
    #     "code": f"{authorisation_code}",
    #     "redirect_uri": f"{redirect_uri}"
    # }
    #
    # my_access_token = GetAccessToken()
    # access_token = my_access_token.get_access_token(post_data, post_headers)
    access_token = "BQD4nQVOWWpm2RGXYWmIaLagtSh-DN18ydjcxA44wfWutgOoOB6L28VZFnDAr_lMjqWgV8KjCIl1xprik-azzCncZSH-UcxpoZQET92FB4NKQUgTL0Rm_bj_XsejMvMqZWM9P15sB110_Gt-kLuyWYzo6LP4No92KyK0upSTUGD-txDdFanv"
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
    print(get_tracks_data.headers)
    print(my_tracks_data)

    # tracks_transform = TransformTracksData()
    # tracks_transform.tracks_from_json(my_tracks_data)
    # data_df = tracks_transform.tracks_dict_to_df()

    # db = os.getenv('DB_NAME')
    # create_engine = CreateEngine()
    # engine = create_engine.engine_connection()
    # with DatabaseConnection(db) as db_conn:
    #     query = '''CREATE TABLE IF NOT EXISTS Songs (
	# id BIGINT AUTO_INCREMENT PRIMARY KEY,
    # song_name VARCHAR(55) NOT NULL,
    # artist_name VARCHAR(55) NOT NULL,
    # time_stamp VARCHAR (55) PRIMARY KEY NOT NULL
    # )'''
    #     db_conn.execute(query)
    #
    # with DatabaseConnection(db) as db_conn:
    #     data_df.to_sql('music', engine, index=False, if_exists='append')










