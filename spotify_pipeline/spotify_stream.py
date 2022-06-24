import logging
from logging import config
import yaml
from utils.connector import db_connector
import os
from dotenv import load_dotenv
import requests
from utils.encode_b64 import Credentials
from datetime import datetime as dt
from datetime import timedelta


load_dotenv()


class DatabaseConnection:
    """
    Used as a context manager for a database connection. __enter__ and __exit__ are magic methods that 'set-up'
    and 'tear down' the the database connection.
    """

    def __init__(self, db_name: str):
        self._conn = db_connector(db_name)

    def __enter__(self):
        logging.info('Calling the db connection enter method...')
        return self._conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info('Calling the db connection exit method...')
        self._conn.commit()
        self._conn.close()

class GetAccessToken:
    def __init__(self):
        self.access_token = ''
        self.expiry_time = ''
        self.token_time = ''

    def get_access_token(self):
        logger.info('posting credentials to get access token...')
        auth_response = requests.post(auth_url, data=post_data, headers=post_headers)
        logger.info('post method successful...')
        self.token_time = dt.now()
        response_data = auth_response.json()
        print(response_data)
        self.access_token = response_data['access_token']
        self.expiry_time = response_data['expires_in']
        logging.info('access token saved...')
        return self.access_token

    def is_valid(self):
        current_time = dt.now()
        expires = self.token_time + dt.timedelta(seconds=self.expiry_time)
        expired = expires < current_time
        return expired

class GetTracks:
    def __init__(self, access_token, endpoint):
        self.access_token = access_token
        self.endpoint = endpoint

    def get_tracks(self):


if __name__ =='__main__':
    with open('../utils/my_logger.YAML') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.info('testing logger')

    my_creds = Credentials()
    encoded_creds = my_creds.encode_credentials_b64()
    auth_url = os.getenv('AUTH_URL')
    post_data = {'grant_type': 'client_credentials'}
    post_headers = {'Authorization': f'Basic {encoded_creds.decode()}'}

    generate_token = GetAccessToken()
    token = generate_token.get_access_token()

    get_headers = {
        'Accept':'application/json',
        'Content-Type':'application/json',
        'Authorization':f'Bearer {token}'
    }

    today = dt.now()
    yesterday = today-dt.timedelta(days=1)
    unix_yesterday = int((yesterday.timestamp())*1000)









    

