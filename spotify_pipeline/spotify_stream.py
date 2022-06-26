import logging
from logging import config

import requests
import yaml
import os
from dotenv import load_dotenv
from datetime import datetime as dt
from datetime import timedelta
from utils.authorisation import AuthoriseUser
from selenium import webdriver
import time


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

    auth_user = AuthoriseUser()
    auth_user_data = auth_user.authorise()
    print(auth_user_data)

    # encoded_creds = os.getenv('CLIENT_CRED_ENCODED')
    #
    #
    # post_data = {
    #     'grant_type':'authorization_code',
    #     'code':f'{auth_user_data}',
    #     'redirect_uri':f'{redirect_uri}'
    # }
    #
    # print(encoded_creds)
    # post_headers = {
    #     'Authorization':f'Basic {encoded_creds}'
    # }
    #
    # auth_url = os.getenv('AUTH_URL')
    # set_up_token = GetAccessToken()
    # access_token = set_up_token.get_access_token(auth_url, post_data, post_headers)


    # today = dt.now()
    # yesterday = today-timedelta(days=1)
    # unix_yesterday = int((yesterday.timestamp())*1000)


