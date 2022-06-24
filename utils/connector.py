import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def db_connector(db_name):
        return psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=db_name,
            user=os.getenv('DB_USER'),
            port=os.getenv('DB_PORT'),
            password=os.getenv('DB_PASSWORD'))
