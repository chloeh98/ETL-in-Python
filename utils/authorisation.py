import os
import logging
import requests
from utils.custom_Exceptions import ResponseError
from dotenv import load_dotenv

load_dotenv()

class AuthoriseUser:
    def __init__(self):
        self.endpoint = ''
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.client_creds_encoded = os.getenv('CLIENT_CRED_ENCODED')
        self.url_encoded_redirect_uri = os.getenv('REDIRECT_URI_ENCODED')
        self.scopes = os.getenv('SCOPES')
        self.authorise_endpoint = ''


    def get_auth_endpoint(self):
        self.authorise_endpoint=f'https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.url_encoded_redirect_uri}&scope={self.scopes}'
        return self.authorise_endpoint

class GetAccessToken:
    def __init__(self):
        self.access_token = ''
        self.expiry_time = ''
        self.refresh_token = ''

    def get_access_token(self, post_data, post_headers):
        auth_url = os.getenv('AUTH_URL')
        logging.info('posting credentials to get access token...')
        auth_response = requests.post(auth_url, data=post_data, headers=post_headers)
        s_code = auth_response.status_code
        if s_code != 200:
            logging.exception(f'unable to get token, response code: {s_code}')
            raise ResponseError(s_code)
        else:
            logging.info('post method successful')
            response_data = auth_response.json()
            self.access_token = response_data['access_token']
            print('\nAccess Token: ', self.access_token + '\n')
            self.refresh_token = response_data['refresh_token']
            print('\nRefresh Token: ', self.refresh_token + '\n')
            logging.info('access token and refresh token saved')
            print("\nSave the access and refresh token!")
            return auth_response.json()