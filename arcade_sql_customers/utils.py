import os
import logging
import sqlite3

# Configure the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_connection(database_url: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(database_url)
        logger.info("Database connection established.")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise e
