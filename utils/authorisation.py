import os
import logging
import requests
from utils.custom_exceptions import ResponseError
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

class AuthoriseUser:
    def __init__(self):
        self.endpoint = ''
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.client_creds_encoded = os.getenv('CLIENT_CRED_ENCODED')
        self.redirect_uri = os.getenv('REDIRECT_URI_ENCODED')
        self.scopes = os.getenv('SCOPES')
        self.authorise_endpoint = ''


    def get_auth(self):
        self.endpoint = f'https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&scope={self.scopes}'
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(self.endpoint)
        time.sleep(2)
        username = driver.find_element(By.ID, 'login-username')
        username.send_keys(os.getenv('SPOTIFY_USERNAME'))
        password = driver.find_element(By.ID, 'login-password')
        password.send_keys(os.getenv('SPOTIFY_PASSWORD'))
        login_button = driver.find_element(By.ID, 'login-button')
        login_button.click()
        try:
            agree_button = driver.find_element(By.XPATH, '//button[@data-testid="auth-accept"]')
            agree_button.click()
            time.sleep(2)
        except NoSuchElementException as e:
            logging.error(e)
            logging.info('User already authorised, continue data extraction')
        finally:
            time.sleep(2)
            parsed_url = driver.current_url
            code = parse_qs(urlparse(parsed_url).query)['code'][0]
            time.sleep(2)
            return code

class GetAccessToken:
    def __init__(self):
        self.access_token = ''
        self.expiry_time = ''
        self.refresh_token = ''

    def get_access_token(self, post_data, post_headers):
        auth_url = 'https://accounts.spotify.com/api/token'
        logging.info('posting credentials to get access token...')
        auth_response = requests.post(auth_url, data=post_data, headers=post_headers)
        s_code = auth_response.status_code
        if s_code != 200:
            logging.exception(f'unable to get token, response code: {s_code}')
            raise ResponseError(s_code)
        else:
            logging.info('post method successful')
            response_data = auth_response.json()
            print("\nSave the access and refresh token!")
            self.access_token = response_data['access_token']
            print('\nAccess Token: ', self.access_token + '\n')
            self.refresh_token = response_data['refresh_token']
            print('\nRefresh Token: ', self.refresh_token + '\n')
            logging.info('access token and refresh token saved')
            return self.access_token