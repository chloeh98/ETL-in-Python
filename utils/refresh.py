import os

import requests
from spotify_pipeline.spotify_stream import refresh_token

class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.b64_creds = os.getenv('CLIENT_CRED_ENCODED')

    def refresh(self):
        response = requests.post(os.getenv('AUTH_URL'), data={'grant_type':'refresh_token', 'refresh_token':f'{refresh_token}'}, headers={'Authorization':f'Basic {self.b64_creds}'})
        new_access_token = response['access_token']
        return new_access_token