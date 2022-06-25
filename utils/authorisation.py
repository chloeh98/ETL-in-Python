import base64
import os
import requests
from datetime import datetime as dt
from datetime import timedelta
import logging

redirect_uri = os.getenv('REDIRECT_URI_ENCODED')
cli_id = os.getenv('CLIENT_ID')
cli_secret = os.getenv('CLIENT_SECRET')
red_uri = os.getenv('REDIRECT_URI_ENCODED')
scope = os.getenv('SCOPE')

class Credentials:
    def __init__(self):
        self.client_id = cli_id
        self.client_secret = cli_secret

    def encode_credentials_b64(self):
        client_credentials = f'{self.client_id}:{self.client_secret}'
        client_credentials_b64 = base64.b64encode(client_credentials.encode())
        return client_credentials_b64


class AuthoriseUser:
    def __init__(self):
        self.endpoint = 'https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri={}&scope={}'
        self.client_id = cli_id
        self.redirect_uri = red_uri
        self.scope = scope


    def authorise(self):
        self.endpoint=f'https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&scope={self.scope}'
        authorise_user_code = requests.get(self.endpoint)
        return authorise_user_code

class GetAccessToken:
    def __init__(self):
        self.access_token = ''
        self.expiry_time = ''
        self.token_time = ''

    def get_access_token(self, auth_url, post_data, post_headers):
        logging.info('posting credentials to get access token...')
        auth_response = requests.post(auth_url, data=post_data, headers=post_headers)
        logging.info('post method successful...')
        self.token_time = dt.now()
        response_data = auth_response.json()
        print(response_data)
        self.access_token = response_data['access_token']
        self.expiry_time = response_data['expires_in']
        logging.info('access token saved...')
        return self.access_token

    def is_valid(self):
        current_time = dt.now()
        expires = self.token_time + timedelta(seconds=self.expiry_time)
        expired = expires < current_time
        return expired