import os
import requests
from datetime import datetime as dt
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs
import time
from utils.custom_Exceptions import CannotAuthoriseUser, AccessTokenNotAuthorised





class AuthoriseUser:
    def __init__(self):
        self.endpoint = ''
        self.client_id = os.getenv('CLIENT_ID')
        self.redirect_uri = os.getenv('REDIRECT_URI_ENCODED')
        self.scope = os.getenv('SCOPE')


    def authorise(self):
        self.endpoint=f'https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&scope={self.scope}'
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(self.endpoint)
        username = driver.find_element(By.ID, 'login-username')
        username.send_keys(os.getenv('SPOTIFY_USERNAME'))
        time.sleep(2)
        password = driver.find_element(By.ID, 'login-password')
        password.send_keys(os.getenv('SPOTIFY_PASSWORD'))
        time.sleep(2)
        login_Button = driver.find_element(By.ID, 'login-button')
        if not login_Button:
            logging.info('User unable to log in.')
            raise CannotAuthoriseUser
        login_Button.click()
        time.sleep(2)
        parsed_url = driver.current_url
        code = parse_qs(urlparse(parsed_url).query)['code'][0]
        return code



class GetAccessToken:
    def __init__(self):
        self.access_token = ''
        self.expiry_time = ''
        self.token_time = ''

    def get_access_token(self, auth_url, post_data, post_headers):
        logging.info('posting credentials to get access token...')
        auth_response = requests.post(auth_url, data=post_data, headers=post_headers)
        s_code = auth_response.status_code
        if s_code != 200:
            logging.exception(f'unable to get token, response code: {s_code}')
            raise AccessTokenNotAuthorised(s_code)
        else:
            logging.info('post method successful...')
        self.token_time = dt.now()
        response_data = auth_response.json()
        print(response_data)
        self.access_token = response_data['access_token']
        self.expiry_time = response_data['expires_in']
        logging.info('access token saved...')
        return self.access_token
