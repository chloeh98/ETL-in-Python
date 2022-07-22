"""
This file is to showcase code written as experimentation to demonstrate how to perform different actions
"""
import os
from contextlib import contextmanager
import logging
from database import db_connector
import psycopg2
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs
from utils.custom_exceptions import AccessTokenNotAuthorised
import time
@contextmanager
def database_context_manager(db_name):
    """
    Alternative context manager for the database connection. Uses a generator to yield the cursor
     and exception handling to ensure the database connection is always closed.
    :param db_name:
    :return:
    """
    conn = db_connector(db_name)
    cur = conn.cursor()
    try:
        logging.info('Getting cursor...')
        yield cur
    except psycopg2.DatabaseError as error:
        conn.rollback()
        logging.error(error)
    else:
        conn.commit()
    finally:
        logging.info('Closing connection to database...')
        conn.close()


""" Tried to get the below code to work, managed to get authorisation code and access token but when the access
token is used in the get request, always get 401 saying no token provided. The correct scope was used when
requesting the authorisation code so unsure of what the issue is.
"""

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
        time.sleep(2)
        username = driver.find_element(By.ID, 'login-username')
        username.send_keys(os.getenv('SPOTIFY_USERNAME'))
        password = driver.find_element(By.ID, 'login-password')
        password.send_keys(os.getenv('SPOTIFY_PASSWORD'))
        login_button = driver.find_element(By.ID, 'login-button')
        login_button.click()
        time.sleep(2)
        agree_button = driver.find_element(By.XPATH,  '//button[@data-testid="auth-accept"]')
        agree_button.click()
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

    def get_access_token(self, auth_url, post_data, post_headers):
        logging.info('posting credentials to get access token...')
        auth_response = requests.post(auth_url, data=post_data, headers=post_headers)
        s_code = auth_response.status_code
        if s_code != 200:
            logging.exception(f'unable to get token, response code: {s_code}')
            raise AccessTokenNotAuthorised(s_code)
        else:
            logging.info('post method successful...')
        response_data = auth_response.json()
        self.access_token = response_data['access_token']
        self.expiry_time = response_data['expires_in']
        self.refresh_token = response_data['refresh_token']
        logging.info('access token saved...')


"""
The class below was used to try and automate the process of getting the access token. Web automation
was done using Selenium. This was successful and an access token was obtained. However when this was passed
into the headers in the get request using the appropriate endpoint, the value returned was always a None type
with an error giving a status code of 401 saying 'no token provided'. The process of doing the same steps manually 
gave an access token that when used in a get request would return a status code 200 and return the expected json
object. Is there a reason the web automation prevents the access token from being authenticated?
"""
class AuthoriseToken:

    def __init__(self, scopes: list[str], endpoint_type: str):
        self.endpoint_type = endpoint_type
        self.scopes = scopes

    @staticmethod
    def initialise_driver():
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        return driver

    def authorise_access_token(self):
        driver = self.initialise_driver()
        driver.get(rf'https://developer.spotify.com/console/{self.endpoint_type}/')
        time.sleep(100)
        cookies_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        cookies_button.click()
        time.sleep(2)
        get_token_button = driver.find_element(By.XPATH, '//button[@data-target="#oauth-modal"]')
        get_token_button.click()
        time.sleep(2)
        for scope in self.scopes:
            button = driver.find_element(By.XPATH, f'//*[@id="scope-{scope}"]')
            button.send_keys(webdriver.common.keys.Keys.SPACE)
            time.sleep(1)
        authorise_button = driver.find_element(By.ID, 'oauthRequestToken')
        authorise_button.click()
        try:
            username = driver.find_element(By.ID, 'login-username')
        except NoSuchElementException as e:
            logging.error(e)
        else:
            username.send_keys(os.getenv('SPOTIFY_USERNAME'))
            password = driver.find_element(By.ID, 'login-password')
            password.send_keys(os.getenv('SPOTIFY_PASSWORD'))
            login_button = driver.find_element(By.ID, 'login-button')
            login_button.click()
        finally:
            time.sleep(2)
            access_token = driver.find_element(By.XPATH, '//*[@id="oauth-input"]').get_attribute('value')
            time.sleep(1)
            print(access_token)
            return access_token

    """
    this function was written to base 64 encode the client id and credentials as required for the
    post request to get the access token.
    """
    def encode_client_creds(self):
        self.client_creds = f'{self.client_id}:{self.client_secret}'
        bytes_client_creds = self.client_creds.encode('ascii')
        self.client_creds_encoded = base64.urlsafe_b64encode(bytes_client_creds)
        return self.client_creds


"""
This method checks the time stamps from the rows to see if they are within the past day
"""
# def check_timestamps(self):
    #     yesterday_date_stamp = datetime.now().date() - timedelta(days=1)
    #     time_stamps_list = self.df['time_stamp'].values.tolist()
    #     for song_tstamps in time_stamps_list:
    #         song_date_stamp = datetime.strptime(song_tstamps, '%Y/%m/%d')
    #         if song_date_stamp != yesterday_date_stamp:
    #             logging.info('At least one song was not played yesterday')
    #             raise SongNotPlayedYesterday
    #     return True