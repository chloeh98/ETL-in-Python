import os
import psycopg2
from dotenv import load_dotenv
import logging

load_dotenv()


def db_connector(db_name: str):
        return psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=db_name,
            user=os.getenv('DB_USER'),
            port=os.getenv('DB_PORT'),
            password=os.getenv('DB_PASSWORD'))


class DatabaseConnection:
    """
    Used as a context manager for a database connection. __enter__ and __exit__ are magic methods that 'set-up'
    and 'tear down' the the database connection.
    """

    def __init__(self, db_name: str):
        self._conn = db_connector(db_name)

    def __enter__(self):
        logging.info('Calling the db connection enter method...')
        return self._conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info('Calling the db connection exit method...')
        if exc_tb is None:
            self._conn.commit()
        else:
            self._conn.rollback()
        self._conn.close()