import base64
import os

class Credentials:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

    def encode_credentials_b64(self):
        client_credentials = f'{self.client_id}:{self.client_secret}'
        client_credentials_b64 = base64.b64encode(client_credentials.encode())
        return client_credentials_b64