"""
This file is to showcase code written as experimentation to demonstrate how to perform different actions
"""
from contextlib import contextmanager
import logging
from utils.connector import db_connector
import psycopg2

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