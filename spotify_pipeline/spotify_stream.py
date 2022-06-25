import logging
from logging import config

import requests
import yaml
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from datetime import timedelta
from utils.authorisation import AuthoriseUser, GetAccessToken, Credentials, redirect_uri
from utils.connector import DatabaseConnection


load_dotenv()


class GetTracks:
    def __init__(self, access_token, endpoint, headers):
        self.access_token = access_token
        self.endpoint = endpoint
        self.headers = headers


    def get_tracks(self):
        try:
            response = requests.get(self.endpoint, self.headers)
        except Exception:
            logging.exception('unable to get tracks')
        else:
            print(self.headers)
            tracks_played_data = response.json()
            print(tracks_played_data)
            return tracks_played_data


if __name__ =='__main__':
    with open('../utils/my_logger.YAML') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.info('testing logger')

    creds = Credentials()
    encoded_creds = creds.encode_credentials_b64()

    auth_user = AuthoriseUser()
    auth_user_data = auth_user.authorise()

    post_data = {
        'grant_type':'authorization_code',
        'code':f'{auth_user_data}',
        'redirect_uri':f'{redirect_uri}'
    }

    post_headers = {
        'Authorization':f'Basic {encoded_creds}'
    }

    auth_url = os.getenv('AUTH_URL')
    set_up_token = GetAccessToken()
    access_token = set_up_token.get_access_token(auth_url, post_data, post_headers)



    # get_headers = {
    #     'Accept':'application/json',
    #     'Content-Type':'application/json',
    #     'Authorization':f'Bearer {token}'
    # }
    #
    # today = dt.now()
    # yesterday = today-timedelta(days=1)
    # unix_yesterday = int((yesterday.timestamp())*1000)


