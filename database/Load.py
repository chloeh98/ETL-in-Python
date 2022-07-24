import os
from dotenv import load_dotenv
import sqlalchemy
import logging
from utils.custom_exceptions import DataHasNullValues, SongsNotPlayedYesterday
from sqlalchemy.orm import sessionmaker

load_dotenv()

class CreateEngine:
    def __init__(self):
        self.engine = None
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.db_name = os.getenv('DB_NAME')


    def engine_connection(self):
        connection_string = f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}/{self.db_name}'
        engine = sqlalchemy.create_engine(connection_string)
        return engine


class ValidateData:
    def __init__(self, df):
        self.df = df

    def df_empty(self):
        empty = self.df.empty
        if empty:
            logging.info('No data to load to database')
            raise SongsNotPlayedYesterday
        return empty

    def is_null_vals(self):
        null_values = self.df.isnull().values.any()
        if null_values:
            logging.info('Data contains null values')
            raise DataHasNullValues
        return null_values