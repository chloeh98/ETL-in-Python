import logging
import os
import time
from logging import config
import yaml
from dotenv import load_dotenv
from utils.authorisation import AuthoriseUser, GetAccessToken
import webbrowser
import urllib.parse


load_dotenv()

def get_tracks():
    

if __name__ =='__main__':
    with open('../utils/my_logger.YAML') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.info('testing logger')

    my_authorisation = AuthoriseUser()
    encoded_creds = my_authorisation.client_creds_encoded
    print(encoded_creds)
    endpoint = my_authorisation.get_auth_endpoint()
    print('copy the url you are redirected to.')
    webbrowser.open(endpoint)

    resp = input('redirected url: ')
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

    access_token = GetAccessToken()
    access_token.get_access_token(post_data, post_headers)

