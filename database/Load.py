import os
from dotenv import load_dotenv
import sqlalchemy
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